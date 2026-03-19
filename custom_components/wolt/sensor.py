"""Sensor entities for Wolt integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator
from .const import (
    ATTR_DELIVERY_FEE,
    CONF_SLUG,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wolt sensors based on a config entry."""
    coordinator: WoltDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    slug = entry.data[CONF_SLUG]

    entities = [
        WoltStatusTextSensor(coordinator, slug),
        WoltDeliveryTimeSensor(coordinator, slug),
        WoltDeliveryFeeSensor(coordinator, slug),
    ]

    async_add_entities(entities)


class WoltStatusTextSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Wolt venue status text."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "status_text"
    _attr_native_unit_of_measurement: Final = None

    def __init__(self, coordinator: WoltDataUpdateCoordinator, slug: str) -> None:
        """Initialize the status text sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{slug}_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, slug)},
            "name": f"Wolt {slug.title()}",
            "manufacturer": "Wolt",
        }

    @property
    def native_value(self) -> str | None:
        """Return the status text."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.status_text


class WoltDeliveryTimeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for estimated delivery time."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "delivery_time"

    def __init__(self, coordinator: WoltDataUpdateCoordinator, slug: str) -> None:
        """Initialize the delivery time sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{slug}_delivery_time"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, slug)},
            "name": f"Wolt {slug.title()}",
            "manufacturer": "Wolt",
        }

    @property
    def native_value(self) -> str | None:
        """Return the estimated delivery time."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.delivery_time

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:clock-outline"


class WoltDeliveryFeeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for delivery fee."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "delivery_fee"

    def __init__(self, coordinator: WoltDataUpdateCoordinator, slug: str) -> None:
        """Initialize the delivery fee sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{slug}_delivery_fee"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, slug)},
            "name": f"Wolt {slug.title()}",
            "manufacturer": "Wolt",
        }

    @property
    def native_value(self) -> str | None:
        """Return the formatted delivery fee."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.delivery_fee_formatted

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        if self.coordinator.data is None:
            return {}
        return {
            ATTR_DELIVERY_FEE: self.coordinator.data.delivery_fee,
        }

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:currency-usd"
