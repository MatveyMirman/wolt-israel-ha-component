"""Button entities for Wolt integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator, WoltVenueConfig
from .const import (
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
    """Set up Wolt buttons based on a config entry."""
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

        entities.append(WoltOrderButton(coordinator, hub_id, hub_name))

    async_add_entities(entities)


class WoltOrderButton(CoordinatorEntity, ButtonEntity):
    """Button to open Wolt for ordering."""

    _attr_has_entity_name: Final = True
    _attr_translation_key: Final = "order"

    def __init__(
        self,
        coordinator: WoltDataUpdateCoordinator,
        hub_id: str,
        hub_name: str,
    ) -> None:
        """Initialize the order button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"wolt_{coordinator.venue_config.slug}_order"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.venue_config.slug)},
            "name": f"Wolt {coordinator.venue_config.slug.title()}",
            "manufacturer": "Wolt",
            "via_device": (DOMAIN, hub_id),
            "suggested_area": hub_name,
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        url = self.coordinator.order_url
        _LOGGER.debug("Opening Wolt order page: %s", url)
        await self.hass.services.async_call(
            "notify",
            "persistent_notification",
            {
                "title": "Open Wolt Order",
                "message": f'[Click here to order from Wolt]({url})',
                "data": {"click_action": {"action": "url", "url": url}},
            },
        )
