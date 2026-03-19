"""Config flow for Wolt integration."""

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
)
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_CITY,
    CONF_COUNTRY,
    CONF_DELIVERY_METHOD,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_POLLING_INTERVAL,
    CONF_SLUG,
    DEFAULT_CITY,
    DEFAULT_COUNTRY,
    DEFAULT_DELIVERY_METHOD,
    DEFAULT_POLLING_INTERVAL,
    DELIVERY_METHODS,
    DOMAIN,
)


USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SLUG): str,
        vol.Optional(CONF_CITY, default=DEFAULT_CITY): str,
        vol.Optional(CONF_COUNTRY, default=DEFAULT_COUNTRY): str,
        vol.Optional(CONF_DELIVERY_METHOD, default=DEFAULT_DELIVERY_METHOD): vol.In(
            [method[0] for method in DELIVERY_METHODS]
        ),
    }
)


class WoltConfigFlow(ConfigFlow):
    """Handle a config flow for Wolt."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            slug = user_input[CONF_SLUG].lower().strip()
            existing_entries = self._async_current_entries()
            for entry in existing_entries:
                if entry.data[CONF_SLUG] == slug:
                    errors[CONF_SLUG] = "already_configured"
                    break

            if not errors:
                lat, lon = self._get_home_location()
                if lat is None or lon is None:
                    errors["base"] = "no_location"

            if not errors:
                user_input[CONF_SLUG] = slug
                return self.async_create_entry(
                    title=f"Wolt - {slug.title()}",
                    data={**user_input, CONF_LATITUDE: lat, CONF_LONGITUDE: lon},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
            description_placeholders={
                "slug_help": "The venue slug from the Wolt URL (e.g., 'gdb' from wolt.com/isr/tel-aviv/venue/gdb)",
                "city_default": DEFAULT_CITY,
            },
        )

    def _get_home_location(self) -> tuple:
        """Get home location from Home Assistant config."""
        if self.hass.config.location is not None:
            return (self.hass.config.location.latitude, self.hass.config.location.longitude)
        return (None, None)

    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow."""
        return WoltOptionsFlow(config_entry)


class WoltOptionsFlow(OptionsFlow):
    """Handle options for Wolt integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        super().__init__()
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_POLLING_INTERVAL,
                    default=self.config_entry.options.get(
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
