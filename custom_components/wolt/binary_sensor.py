"""Binary sensor entities for Wolt integration."""

from __future__ import annotations

from typing import Final

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator, WoltVenueConfig
from .const import (
    ATTR_NEXT_CLOSE,
    ATTR_NEXT_OPEN,
    ATTR_VENUE_ID,
    CONF_DELIVERY_METHOD,
    CONF_HUB_ID,
    CONF_HUB_NAME,
    CONF_SLUG,
    CONF_VENUES,
    DEFAULT_DELIVERY_METHOD,
    DOMAIN,
    METHOD_LABELS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wolt binary sensors based on a config entry."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    venues = entry.data.get(CONF_VENUES, [])
    hub_id = entry.data.get(CONF_HUB_ID, entry.entry_id)
    hub_name = entry.data.get(CONF_HUB_NAME, "Wolt Hub")

    entities = []

    for venue in venues:
        slug = venue.get(CONF_SLUG)
        delivery_method = (
            venue.get(CONF_DELIVERY_METHOD, DEFAULT_DELIVERY_METHOD)
            or DEFAULT_DELIVERY_METHOD
        )
        method_label = METHOD_LABELS[delivery_method]
        coordinator_key = f"{slug}_{delivery_method}"

        if not slug:
            continue

        venue_config = WoltVenueConfig(slug=slug, delivery_method=delivery_method)
        coordinator = WoltDataUpdateCoordinator(hass, entry, venue_config)
        entry_data["coordinators"][coordinator_key] = coordinator

        await coordinator.async_config_entry_first_refresh()

        entities.append(
            WoltAvailabilitySensor(coordinator, hub_id, hub_name, method_label)
        )

    async_add_entities(entities)


class WoltAvailabilitySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for Wolt venue availability."""

    _attr_name: Final = "Available"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
        method_label: str,
    ) -> None:
        """Initialize the availability sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_availability"
        self._attr_device_info = {
            "identifiers": {
                (
                    DOMAIN,
                    f"{coordinator.venue_config.slug}_{coordinator.venue_config.delivery_method}",
                )
            },
            "name": f"{coordinator.venue_config.slug.title()} - {method_label}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
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
