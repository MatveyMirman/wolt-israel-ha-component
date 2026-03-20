"""Tests for the Wolt binary sensor entities."""

from unittest.mock import MagicMock

import pytest

from custom_components.wolt.binary_sensor import WoltAvailabilitySensor


class TestWoltAvailabilitySensor:
    """Tests for WoltAvailabilitySensor."""

    def test_is_on_when_online(self, mock_wolt_venue_data):
        """Test is_on returns True when venue is online."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.is_on is True

    def test_is_on_when_offline(self, mock_wolt_venue_data_unavailable):
        """Test is_on returns False when venue is offline."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data_unavailable
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.is_on is False

    def test_is_on_no_data(self):
        """Test is_on returns None when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.is_on is None

    def test_extra_state_attributes_with_data(self, mock_wolt_venue_data):
        """Test extra_state_attributes returns venue info."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        attrs = sensor.extra_state_attributes

        assert attrs["venue_id"] == "venue_123"
        assert attrs["next_open"] == "2024-01-15T10:00:00"
        assert attrs["next_close"] == "2024-01-15T22:00:00"

    def test_extra_state_attributes_no_data(self):
        """Test extra_state_attributes returns empty dict when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.extra_state_attributes == {}

    def test_unique_id(self, mock_wolt_venue_data):
        """Test unique_id is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_unique_id == "wolt_gdb_availability"

    def test_device_info(self, mock_wolt_venue_data):
        """Test device_info is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_device_info["identifiers"] == {("wolt", "gdb")}
        assert sensor._attr_device_info["name"] == "Wolt Gdb"
        assert sensor._attr_device_info["manufacturer"] == "Wolt"
        assert sensor._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert sensor._attr_device_info["suggested_area"] == "Test Home"

    def test_translation_key(self, mock_wolt_venue_data):
        """Test translation_key is set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_translation_key == "availability"
