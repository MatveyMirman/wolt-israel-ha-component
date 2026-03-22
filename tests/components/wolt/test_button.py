"""Tests for the Wolt button entities."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.wolt.button import WoltOrderButton


@pytest.fixture
def mock_coordinator(mock_wolt_venue_data):
    """Return a mock coordinator with venue config."""
    coordinator = MagicMock()
    coordinator.data = mock_wolt_venue_data
    coordinator.venue_config.slug = "gdb"
    coordinator.venue_config.delivery_method = "homedelivery"
    coordinator.order_url = "https://wolt.com/en/isr/tel-aviv/restaurant/gdb"
    return coordinator


class TestWoltOrderButton:
    """Tests for WoltOrderButton."""

    def test_unique_id(self, mock_coordinator):
        """Test unique_id is correctly set."""
        button = WoltOrderButton(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert button._attr_unique_id == "wolt_gdb_order"

    def test_device_info(self, mock_coordinator):
        """Test device_info is correctly set."""
        button = WoltOrderButton(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert button._attr_device_info["identifiers"] == {("wolt", "gdb_homedelivery")}
        assert button._attr_device_info["name"] == "Gdb - Delivery"
        assert button._attr_device_info["manufacturer"] == "Wolt"
        assert button._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert button._attr_device_info["suggested_area"] == "Test Home"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        button = WoltOrderButton(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert button._attr_name == "Order"

    async def test_async_press_opens_url(self, mock_coordinator):
        """Test async_press opens the correct URL."""
        button = WoltOrderButton(mock_coordinator, "test_hub_id", "Test Home", "Delivery")

        mock_hass = MagicMock()
        mock_hass.services.async_call = AsyncMock()
        button.hass = mock_hass

        await button.async_press()

        mock_hass.services.async_call.assert_called_once_with(
            "notify",
            "persistent_notification",
            {
                "title": "Open Wolt Order",
                "message": "[Click here to order from Wolt](https://wolt.com/en/isr/tel-aviv/restaurant/gdb)",
                "data": {"click_action": {"action": "url", "url": "https://wolt.com/en/isr/tel-aviv/restaurant/gdb"}},
            },
        )
