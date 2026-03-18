"""Sensor entities for Wolt integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator
from .const import (
    ATTR_AVAILABILITY,
    ATTR_DELIVERY_FEE,
    ATTR_DELIVERY_FEE_FORMATTED,
    ATTR_DELIVERY_TIME,
    ATTR_NEXT_CLOSE,
    ATTR_NEXT_OPEN,
    ATTR_ORDER_URL,
    ATTR_STATUS_TEXT,
    ATTR_VENUE_ID,
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
        WoltAvailabilitySensor(coordinator, slug),
        WoltStatusTextSensor(coordinator, slug),
        WoltDeliveryTimeSensor(coordinator, slug),
        WoltDeliveryFeeSensor(coordinator, slug),
        WoltOrderButton(coordinator, slug),
    ]

    async_add_entities(entities)


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


class WoltOrderButton(CoordinatorEntity, ButtonEntity):
    """Button to open Wolt for ordering."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "order"

    def __init__(self, coordinator: WoltDataUpdateCoordinator, slug: str) -> None:
        """Initialize the order button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{slug}_order"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, slug)},
            "name": f"Wolt {slug.title()}",
            "manufacturer": "Wolt",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        import webbrowser

        url = self.coordinator.order_url
        _LOGGER.debug("Opening Wolt order page: %s", url)
        await self.hass.async_add_executor_job(webbrowser.open, url)
