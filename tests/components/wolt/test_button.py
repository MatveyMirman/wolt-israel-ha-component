"""Tests for the Wolt button entities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wolt.button import WoltOrderButton


class TestWoltOrderButton:
    """Tests for WoltOrderButton."""

    def test_unique_id(self, mock_wolt_venue_data):
        """Test unique_id is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data

        button = WoltOrderButton(coordinator, "gdb")
        assert button._attr_unique_id == "wolt_gdb_order"

    def test_device_info(self, mock_wolt_venue_data):
        """Test device_info is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data

        button = WoltOrderButton(coordinator, "gdb")
        assert button._attr_device_info["identifiers"] == {("wolt", "gdb")}
        assert button._attr_device_info["name"] == "Wolt Gdb"
        assert button._attr_device_info["manufacturer"] == "Wolt"

    def test_translation_key(self, mock_wolt_venue_data):
        """Test translation_key is set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data

        button = WoltOrderButton(coordinator, "gdb")
        assert button._attr_translation_key == "order"

    async def test_async_press_opens_url(self, mock_wolt_venue_data):
        """Test async_press opens the correct URL."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.order_url = "https://wolt.com/isr/tel-aviv/venue/gdb"

        button = WoltOrderButton(coordinator, "gdb")
        
        mock_hass = MagicMock()
        async def mock_executor(*args, **kwargs):
            pass
        mock_hass.async_add_executor_job = mock_executor
        button.hass = mock_hass

        with patch("webbrowser.open"):
            await button.async_press()
