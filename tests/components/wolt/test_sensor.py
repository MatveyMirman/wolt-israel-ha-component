"""Tests for the Wolt sensor entities."""

from unittest.mock import MagicMock

import pytest

from custom_components.wolt.sensor import (
    WoltStatusTextSensor,
    WoltDeliveryTimeSensor,
    WoltDeliveryFeeSensor,
    WoltMinimumOrderSensor,
)


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


class TestWoltStatusTextSensor:
    """Tests for WoltStatusTextSensor."""

    def test_native_value_with_data(self, mock_coordinator):
        """Test native_value returns status text when data is available."""
        sensor = WoltStatusTextSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value == "Open for delivery"

    def test_native_value_no_data(self, mock_coordinator_no_data):
        """Test native_value returns None when no data."""
        sensor = WoltStatusTextSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value is None

    def test_unique_id(self, mock_coordinator):
        """Test unique_id is correctly set."""
        sensor = WoltStatusTextSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_unique_id == "wolt_gdb_status"

    def test_device_info(self, mock_coordinator):
        """Test device_info is correctly set."""
        sensor = WoltStatusTextSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_device_info["identifiers"] == {("wolt", "gdb_homedelivery")}
        assert sensor._attr_device_info["name"] == "Gdb - Delivery"
        assert sensor._attr_device_info["manufacturer"] == "Wolt"
        assert sensor._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert sensor._attr_device_info["suggested_area"] == "Test Home"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        sensor = WoltStatusTextSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_name == "Status"

    def test_device_name_includes_method_label(self, mock_coordinator_takeaway):
        """Test device name includes method label."""
        sensor = WoltStatusTextSensor(mock_coordinator_takeaway, "test_hub_id", "Test Home", "Takeaway")
        assert sensor._attr_device_info["name"] == "Gdb - Takeaway"


class TestWoltDeliveryTimeSensor:
    """Tests for WoltDeliveryTimeSensor."""

    def test_native_value_with_data(self, mock_coordinator):
        """Test native_value returns delivery time when data is available."""
        sensor = WoltDeliveryTimeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value == "25-35 min"

    def test_native_value_no_data(self, mock_coordinator_no_data):
        """Test native_value returns None when no data."""
        sensor = WoltDeliveryTimeSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value is None

    def test_icon(self, mock_coordinator):
        """Test icon returns correct value."""
        sensor = WoltDeliveryTimeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.icon == "mdi:clock-outline"

    def test_unique_id(self, mock_coordinator):
        """Test unique_id is correctly set."""
        sensor = WoltDeliveryTimeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_unique_id == "wolt_gdb_delivery_time"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        sensor = WoltDeliveryTimeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_name == "Delivery Time"


class TestWoltDeliveryFeeSensor:
    """Tests for WoltDeliveryFeeSensor."""

    def test_native_value_with_data(self, mock_coordinator):
        """Test native_value returns formatted fee when data is available."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value == "₪14.00"

    def test_native_value_no_data(self, mock_coordinator_no_data):
        """Test native_value returns None when no data."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value is None

    def test_extra_state_attributes_with_data(self, mock_coordinator):
        """Test extra_state_attributes returns fee in agorot."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        attrs = sensor.extra_state_attributes
        assert attrs["delivery_fee"] == 1400

    def test_extra_state_attributes_no_data(self, mock_coordinator_no_data):
        """Test extra_state_attributes returns empty dict when no data."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.extra_state_attributes == {}

    def test_icon(self, mock_coordinator):
        """Test icon returns correct value."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.icon == "mdi:currency-usd"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        sensor = WoltDeliveryFeeSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_name == "Delivery Fee"


class TestWoltMinimumOrderSensor:
    """Tests for WoltMinimumOrderSensor."""

    def test_native_value_with_data(self, mock_coordinator):
        """Test native_value returns minimum order when data is available."""
        sensor = WoltMinimumOrderSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value == "₪49.00"

    def test_native_value_no_data(self, mock_coordinator_no_data):
        """Test native_value returns None when no data."""
        sensor = WoltMinimumOrderSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.native_value is None

    def test_extra_state_attributes_with_data(self, mock_coordinator):
        """Test extra_state_attributes returns minimum order in agorot."""
        sensor = WoltMinimumOrderSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        attrs = sensor.extra_state_attributes
        assert attrs["order_minimum"] == 4900

    def test_extra_state_attributes_no_data(self, mock_coordinator_no_data):
        """Test extra_state_attributes returns empty dict when no data."""
        sensor = WoltMinimumOrderSensor(mock_coordinator_no_data, "test_hub_id", "Test Home", "Delivery")
        assert sensor.extra_state_attributes == {}

    def test_icon(self, mock_coordinator):
        """Test icon returns correct value."""
        sensor = WoltMinimumOrderSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor.icon == "mdi:cart"

    def test_attr_name(self, mock_coordinator):
        """Test attr_name is set to display type name."""
        sensor = WoltMinimumOrderSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_name == "Order Minimum"

    def test_unique_id_has_minimum_order_suffix(self, mock_coordinator):
        """Test unique_id includes _minimum_order suffix."""
        sensor = WoltMinimumOrderSensor(mock_coordinator, "test_hub_id", "Test Home", "Delivery")
        assert sensor._attr_unique_id == "wolt_gdb_minimum_order"
