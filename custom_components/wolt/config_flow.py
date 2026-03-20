"""Config flow for Wolt integration."""

import uuid

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)

from .const import (
    CONF_DELIVERY_METHOD,
    CONF_HUB_ID,
    CONF_HUB_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_POLLING_INTERVAL,
    CONF_SLUG,
    CONF_VENUES,
    CONF_ZONE,
    DEFAULT_DELIVERY_METHOD,
    DEFAULT_HUB_NAME,
    DEFAULT_POLLING_INTERVAL,
    DELIVERY_METHODS,
    DOMAIN,
)


class WoltConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wolt."""

    VERSION = 2
    MINOR_VERSION = 0

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlow:
        """Handle the initial step - configure hub."""
        errors: dict[str, str] = {}
        zones = self._get_zones()
        home_lat, home_lon = self._get_home_location()

        if user_input is not None:
            hub_name = user_input.get(CONF_HUB_NAME, DEFAULT_HUB_NAME)
            location_type = user_input.get("location_type", "home")

            if location_type == "home":
                if home_lat is None or home_lon is None:
                    errors["base"] = "no_location"
                else:
                    hub_id = str(uuid.uuid4())
                    return self.async_create_entry(
                        title=f"Wolt Hub - {hub_name}",
                        data={
                            CONF_HUB_ID: hub_id,
                            CONF_HUB_NAME: hub_name,
                            CONF_ZONE: "Home Assistant Home",
                            CONF_LATITUDE: home_lat,
                            CONF_LONGITUDE: home_lon,
                            CONF_VENUES: [],
                        },
                    )
            else:
                for zone in zones:
                    if zone["id"] == location_type:
                        hub_id = str(uuid.uuid4())
                        return self.async_create_entry(
                            title=f"Wolt Hub - {hub_name}",
                            data={
                                CONF_HUB_ID: hub_id,
                                CONF_HUB_NAME: hub_name,
                                CONF_ZONE: zone["name"],
                                CONF_LATITUDE: zone["latitude"],
                                CONF_LONGITUDE: zone["longitude"],
                                CONF_VENUES: [],
                            },
                        )

        if home_lat is None and not zones:
            return self.async_abort(reason="no_location")

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(user_input or {}, zones, home_lat),
            errors=errors,
            description_placeholders={
                "hub_name_help": "A friendly name for this hub (e.g., 'Home', 'Office')",
            },
        )

    def _get_schema(self, user_input: dict, zones: list, home_lat: float | None) -> vol.Schema:
        """Build the schema based on available options."""
        location_options = {}
        default_location = "home"

        if home_lat is not None:
            location_options["home"] = "Use Home Assistant Home Location"
        else:
            default_location = f"area_{zones[0]['id']}" if zones else "home"

        for zone in zones:
            location_options[f"area_{zone['id']}"] = f"Zone: {zone['name']}"

        return vol.Schema({
            vol.Required(CONF_HUB_NAME, default=user_input.get(CONF_HUB_NAME, DEFAULT_HUB_NAME)): str,
            vol.Required("location_type", default=user_input.get("location_type", default_location)): vol.In(location_options),
        })

    def _get_home_location(self) -> tuple:
        """Get home location from Home Assistant config."""
        config_dict = self.hass.config.as_dict()
        if (
            config_dict.get("latitude") is not None
            and config_dict.get("longitude") is not None
        ):
            return (config_dict["latitude"], config_dict["longitude"])
        return (None, None)

    def _get_zones(self) -> list[dict]:
        """Get zones from Home Assistant."""
        zones = []
        try:
            area_registry = self.hass.data.get("area_registry")
            if area_registry:
                for area_id, area in area_registry.areas.items():
                    if hasattr(area, "latitude") and area.latitude is not None:
                        zones.append({
                            "id": area_id,
                            "name": area.name,
                            "latitude": area.latitude,
                            "longitude": area.longitude,
                        })
        except Exception:
            pass
        return zones

    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow."""
        return WoltOptionsFlow(config_entry)


class WoltOptionsFlow(OptionsFlow):
    """Handle options for Wolt integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlow:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_POLLING_INTERVAL,
                    default=self._config_entry.options.get(
                        CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={
                "polling_help": "Polling interval in seconds (60-3600, default: 300)",
            },
        )
