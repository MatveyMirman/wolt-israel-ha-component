"""Binary sensor entities for Wolt integration."""

from __future__ import annotations

from typing import Final

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator
from .const import (
    ATTR_NEXT_CLOSE,
    ATTR_NEXT_OPEN,
    ATTR_VENUE_ID,
    CONF_SLUG,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wolt binary sensors based on a config entry."""
    coordinator: WoltDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    slug = entry.data[CONF_SLUG]

    async_add_entities([WoltAvailabilitySensor(coordinator, slug)])


class WoltAvailabilitySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for Wolt venue availability."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "availability"

    def __init__(self, coordinator: WoltDataUpdateCoordinator, slug: str) -> None:
        """Initialize the availability sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{slug}_availability"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, slug)},
            "name": f"Wolt {slug.title()}",
            "manufacturer": "Wolt",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if venue is online/open."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.online

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        if self.coordinator.data is None:
            return {}
        return {
            ATTR_VENUE_ID: self.coordinator.data.venue_id,
            ATTR_NEXT_OPEN: self.coordinator.data.next_open,
            ATTR_NEXT_CLOSE: self.coordinator.data.next_close,
        }
