"""Tests for the Wolt binary sensor entities."""

from unittest.mock import MagicMock

import pytest

from custom_components.wolt.binary_sensor import WoltAvailabilitySensor


@pytest.fixture
def mock_coordinator(mock_wolt_venue_data):
    """Return a mock coordinator with venue config."""
    coordinator = MagicMock()
    coordinator.data = mock_wolt_venue_data
    coordinator.venue_config.slug = "gdb"
    coordinator.venue_config.delivery_method = "homedelivery"
    return coordinator


@pytest.fixture
def mock_coordinator_takeaway(mock_wolt_venue_data):
    """Return a mock coordinator for takeaway."""
    coordinator = MagicMock()
    coordinator.data = mock_wolt_venue_data
    coordinator.venue_config.slug = "gdb"
    coordinator.venue_config.delivery_method = "takeaway"
    return coordinator


@pytest.fixture
def mock_coordinator_no_data():
    """Return a mock coordinator with no data."""
    coordinator = MagicMock()
    coordinator.data = None
    coordinator.venue_config.slug = "gdb"
    coordinator.venue_config.delivery_method = "homedelivery"
    return coordinator


class TestWoltAvailabilitySensor:
    """Tests for WoltAvailabilitySensor."""

    def test_is_on_when_online(self, mock_coordinator):
        """Test is_on returns True when venue is online."""
        sensor = WoltAvailabilitySensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.is_on is True

    def test_is_on_when_offline(self, mock_wolt_venue_data_unavailable):
        """Test is_on returns False when venue is offline."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data_unavailable
        coordinator.venue_config.slug = "gdb"
        coordinator.venue_config.delivery_method = "homedelivery"
        sensor = WoltAvailabilitySensor(coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.is_on is False

    def test_is_on_no_data(self, mock_coordinator_no_data):
        """Test is_on returns None when no data."""
        sensor = WoltAvailabilitySensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.is_on is None

    def test_extra_state_attributes_with_data(self, mock_coordinator):
        """Test extra_state_attributes returns venue info."""
        sensor = WoltAvailabilitySensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        attrs = sensor.extra_state_attributes

        assert attrs["venue_id"] == "venue_123"
        assert attrs["next_open"] == "2024-01-15T10:00:00"
        assert attrs["next_close"] == "2024-01-15T22:00:00"

    def test_extra_state_attributes_no_data(self, mock_coordinator_no_data):
        """Test extra_state_attributes returns empty dict when no data."""
        sensor = WoltAvailabilitySensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.extra_state_attributes == {}

    def test_unique_id(self, mock_coordinator):
        """Test unique_id is correctly set."""
        sensor = WoltAvailabilitySensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_unique_id == "wolt_gdb_availability"

    def test_device_info(self, mock_coordinator):
        """Test device_info is correctly set."""
        sensor = WoltAvailabilitySensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_device_info["identifiers"] == {("wolt", "gdb_homedelivery")}
        assert sensor._attr_device_info["name"] == "Gdb - Delivery"
        assert sensor._attr_device_info["manufacturer"] == "Wolt"
        assert sensor._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert sensor._attr_device_info["suggested_area"] == "Test Home"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        sensor = WoltAvailabilitySensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_name == "Available"

    def test_device_name_includes_method_label(self, mock_coordinator_takeaway):
        """Test device name includes method label."""
        sensor = WoltAvailabilitySensor(mock_coordinator_takeaway, "test_hub_id", "Test Home", "Takeaway")
        assert sensor._attr_device_info["name"] == "Gdb - Takeaway"
