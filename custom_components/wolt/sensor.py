"""Sensor entities for Wolt integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator, WoltVenueConfig
from .const import (
    ATTR_DELIVERY_FEE,
    ATTR_MINIMUM_ORDER,
    CONF_DELIVERY_METHOD,
    CONF_HUB_ID,
    CONF_HUB_NAME,
    CONF_SLUG,
    CONF_VENUES,
    DEFAULT_DELIVERY_METHOD,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wolt sensors based on a config entry."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    venues = entry.data.get(CONF_VENUES, [])
    hub_id = entry.data.get(CONF_HUB_ID, entry.entry_id)
    hub_name = entry.data.get(CONF_HUB_NAME, "Wolt Hub")

    entities = []

    for venue in venues:
        slug = venue.get(CONF_SLUG)
        delivery_method = venue.get(CONF_DELIVERY_METHOD, DEFAULT_DELIVERY_METHOD)

        if not slug:
            continue

        venue_config = WoltVenueConfig(slug=slug, delivery_method=delivery_method)
        coordinator = WoltDataUpdateCoordinator(hass, entry, venue_config)
        entry_data["coordinators"][slug] = coordinator

        await coordinator.async_config_entry_first_refresh()

        venue_entities = [
            WoltStatusTextSensor(coordinator, hub_id, hub_name),
            WoltDeliveryTimeSensor(coordinator, hub_id, hub_name),
            WoltDeliveryFeeSensor(coordinator, hub_id, hub_name),
            WoltMinimumOrderSensor(coordinator, hub_id, hub_name),
        ]
        entities.extend(venue_entities)

    async_add_entities(entities)


class WoltStatusTextSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Wolt venue status text."""

    _attr_name: Final = "Status"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
    ) -> None:
        """Initialize the status text sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.venue_config.slug)},
            "name": f"Wolt {coordinator.venue_config.slug.title()}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
        }

    @property
    def native_value(self) -> str | None:
        """Return the status text."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.status_text


class WoltDeliveryTimeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for estimated delivery time."""

    _attr_name: Final = "Delivery Time"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
    ) -> None:
        """Initialize the delivery time sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_delivery_time"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.venue_config.slug)},
            "name": f"Wolt {coordinator.venue_config.slug.title()}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
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

    _attr_name: Final = "Delivery Fee"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
    ) -> None:
        """Initialize the delivery fee sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_delivery_fee"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.venue_config.slug)},
            "name": f"Wolt {coordinator.venue_config.slug.title()}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
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


class WoltMinimumOrderSensor(CoordinatorEntity, SensorEntity):
    """Sensor for minimum order amount."""

    _attr_name: Final = "Minimum Order"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
    ) -> None:
        """Initialize the minimum order sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_minimum_order"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.venue_config.slug)},
            "name": f"Wolt {coordinator.venue_config.slug.title()}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
        }

    @property
    def native_value(self) -> str | None:
        """Return the minimum order amount."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.minimum_order_amount_formatted

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        if self.coordinator.data is None:
            return {}
        return {
            ATTR_MINIMUM_ORDER: self.coordinator.data.minimum_order_amount,
        }

    @property
    def icon(self) -> str:
        """Return the icon."""
        return "mdi:cart"
