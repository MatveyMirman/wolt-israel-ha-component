"""Wolt integration for Home Assistant."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import WoltApiClient, WoltVenueData
from .const import (
    CONF_CITY,
    CONF_COUNTRY,
    CONF_DELIVERY_METHOD,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_POLLING_INTERVAL,
    CONF_SLUG,
    DEFAULT_POLLING_INTERVAL,
    DOMAIN,
)

PLATFORMS: Final = ["sensor", "binary_sensor", "button"]

_LOGGER = logging.getLogger(__name__)


class WoltDataUpdateCoordinator(DataUpdateCoordinator[WoltVenueData | None]):
    """Class to manage fetching Wolt data."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self._slug = entry.data[CONF_SLUG]
        self._city = entry.data[CONF_CITY]
        self._country = entry.data[CONF_COUNTRY]
        self._delivery_method = entry.data[CONF_DELIVERY_METHOD]

        polling_interval = entry.options.get(
            CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"Wolt {self._slug}",
            update_interval=timedelta(seconds=polling_interval),
        )

        session = async_get_clientsession(hass)
        self.api = WoltApiClient(session)

    async def _async_update_data(self) -> WoltVenueData | None:
        """Fetch data from Wolt API."""
        lat = self.entry.data.get(CONF_LATITUDE)
        lon = self.entry.data.get(CONF_LONGITUDE)

        if lat is None or lon is None:
            _LOGGER.warning("No coordinates configured for Wolt integration")
            return None

        return await self.api.async_get_venue_dynamic(
            slug=self._slug,
            lat=lat,
            lon=lon,
            delivery_method=self._delivery_method,
        )

    @property
    def order_url(self) -> str:
        """Generate the Wolt order URL."""
        return f"https://wolt.com/{self._country}/{self._city}/venue/{self._slug}"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wolt integration from a config entry."""

    if CONF_LATITUDE not in entry.data or CONF_LONGITUDE not in entry.data:
        config_dict = hass.config.as_dict()
        lat = config_dict.get("latitude")
        lon = config_dict.get("longitude")

        if lat is None or lon is None:
            _LOGGER.error("No home location configured in Home Assistant")
            return False

        new_data = {**entry.data, CONF_LATITUDE: lat, CONF_LONGITUDE: lon}
        hass.config_entries.async_update_entry(entry, data=new_data)

    coordinator = WoltDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle a config entry being reloaded."""
    await hass.config_entries.async_reload(entry.entry_id)
