"""Button entities for Wolt integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import WoltDataUpdateCoordinator
from .const import CONF_SLUG, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wolt buttons based on a config entry."""
    coordinator: WoltDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    slug = entry.data[CONF_SLUG]

    async_add_entities([WoltOrderButton(coordinator, slug)])


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
