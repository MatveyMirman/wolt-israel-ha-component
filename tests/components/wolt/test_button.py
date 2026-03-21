"""Tests for the Wolt button entities."""

from unittest.mock import AsyncMock, MagicMock

from custom_components.wolt.button import WoltOrderButton


class TestWoltOrderButton:
    """Tests for WoltOrderButton."""

    def test_unique_id(self, mock_wolt_venue_data):
        """Test unique_id is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        button = WoltOrderButton(coordinator, "test_hub_id", "Test Home")
        assert button._attr_unique_id == "wolt_gdb_order"

    def test_device_info(self, mock_wolt_venue_data):
        """Test device_info is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        button = WoltOrderButton(coordinator, "test_hub_id", "Test Home")
        assert button._attr_device_info["identifiers"] == {("wolt", "gdb")}
        assert button._attr_device_info["name"] == "Wolt Gdb"
        assert button._attr_device_info["manufacturer"] == "Wolt"
        assert button._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert button._attr_device_info["suggested_area"] == "Test Home"

    def test_attr_name(self, mock_wolt_venue_data):
        """Test attr_name is set to display type name."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        button = WoltOrderButton(coordinator, "test_hub_id", "Test Home")
        assert button._attr_name == "Order"

    async def test_async_press_opens_url(self, mock_wolt_venue_data):
        """Test async_press opens the correct URL."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"
        coordinator.order_url = "https://wolt.com/en/isr/tel-aviv/restaurant/gdb"

        button = WoltOrderButton(coordinator, "test_hub_id", "Test Home")

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
