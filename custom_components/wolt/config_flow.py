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
            elif location_type == "custom":
                custom_lat = user_input.get(CONF_LATITUDE)
                custom_lon = user_input.get(CONF_LONGITUDE)
                if custom_lat is None or custom_lon is None:
                    errors["base"] = "no_location"
                else:
                    hub_id = str(uuid.uuid4())
                    return self.async_create_entry(
                        title=f"Wolt Hub - {hub_name}",
                        data={
                            CONF_HUB_ID: hub_id,
                            CONF_HUB_NAME: hub_name,
                            CONF_ZONE: "Custom Location",
                            CONF_LATITUDE: float(custom_lat),
                            CONF_LONGITUDE: float(custom_lon),
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
            default_location = f"area_{zones[0]['id']}" if zones else "custom"

        for zone in zones:
            location_options[f"area_{zone['id']}"] = f"Zone: {zone['name']}"

        location_options["custom"] = "Enter Custom Coordinates"

        schema_dict = {
            vol.Required(CONF_HUB_NAME, default=user_input.get(CONF_HUB_NAME, DEFAULT_HUB_NAME)): str,
            vol.Required("location_type", default=user_input.get("location_type", default_location)): vol.In(location_options),
        }

        if user_input.get("location_type") == "custom":
            schema_dict[vol.Required(CONF_LATITUDE, default=user_input.get(CONF_LATITUDE))] = vol.Coerce(float)
            schema_dict[vol.Required(CONF_LONGITUDE, default=user_input.get(CONF_LONGITUDE))] = vol.Coerce(float)

        return vol.Schema(schema_dict)

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
        self._entry_id = config_entry.entry_id

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlow:
        """Manage the options - show menu."""
        if user_input is not None:
            return await self.async_step_venues()

        options_schema = vol.Schema({
            vol.Optional("manage_venues", default=False): bool,
            vol.Optional(CONF_POLLING_INTERVAL, default=self._config_entry.options.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={
                "polling_help": "Polling interval in seconds (60-3600, default: 300)",
            },
            last_step=False,
        )

    async def async_step_venues(self, user_input: dict | None = None) -> ConfigFlow:
        """Manage venues - add or remove."""
        errors: dict[str, str] = {}
        entry = self.hass.config_entries.async_get_entry(self._entry_id)

        if user_input is not None:
            venues = []

            slugs = user_input.get(CONF_SLUG, [])
            if isinstance(slugs, str):
                slugs = [slugs]

            delivery_methods = user_input.get(CONF_DELIVERY_METHOD, [])
            if isinstance(delivery_methods, str):
                delivery_methods = [delivery_methods]

            for i, slug in enumerate(slugs):
                slug = slug.lower().strip() if slug else ""
                method = delivery_methods[i] if i < len(delivery_methods) else DEFAULT_DELIVERY_METHOD
                if slug:
                    venues.append({
                        CONF_SLUG: slug,
                        CONF_DELIVERY_METHOD: method,
                    })

            if entry:
                new_data = {**entry.data, CONF_VENUES: venues}
                self.hass.config_entries.async_update_entry(entry, data=new_data)

            options = {CONF_POLLING_INTERVAL: user_input.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)}
            return self.async_create_entry(title="", data=options)

        current_venues = entry.data.get(CONF_VENUES, []) if entry else []

        venue_count = len(current_venues)
        if venue_count == 0:
            venue_count = 1

        slugs = []
        methods = []
        for i in range(venue_count):
            slugs.append(current_venues[i].get(CONF_SLUG, "") if i < len(current_venues) else "")
            methods.append(current_venues[i].get(CONF_DELIVERY_METHOD, DEFAULT_DELIVERY_METHOD) if i < len(current_venues) else DEFAULT_DELIVERY_METHOD)

        venue_schema = vol.Schema({
            vol.Optional(CONF_SLUG, default=slugs): [str],
            vol.Optional(CONF_DELIVERY_METHOD, default=methods): [vol.In({m[0]: m[1] for m in DELIVERY_METHODS})],
            vol.Optional(CONF_POLLING_INTERVAL, default=self._config_entry.options.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
        })

        return self.async_show_form(
            step_id="venues",
            data_schema=venue_schema,
            errors=errors,
            description_placeholders={
                "slug_help": "The venue slug from the Wolt URL (e.g., 'gdb' from wolt.com/isr/tel-aviv/venue/gdb)",
            },
        )
