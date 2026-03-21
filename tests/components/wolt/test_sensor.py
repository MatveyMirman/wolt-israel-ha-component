"""Tests for the Wolt sensor entities."""

from unittest.mock import MagicMock

import pytest

from custom_components.wolt.sensor import (
    WoltStatusTextSensor,
    WoltDeliveryTimeSensor,
    WoltDeliveryFeeSensor,
    WoltMinimumOrderSensor,
)


class TestWoltStatusTextSensor:
    """Tests for WoltStatusTextSensor."""

    def test_native_value_with_data(self, mock_wolt_venue_data):
        """Test native_value returns status text when data is available."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value == "Open for delivery"

    def test_native_value_no_data(self):
        """Test native_value returns None when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value is None

    def test_unique_id(self, mock_wolt_venue_data):
        """Test unique_id is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_unique_id == "wolt_gdb_status"

    def test_device_info(self, mock_wolt_venue_data):
        """Test device_info is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_device_info["identifiers"] == {("wolt", "gdb")}
        assert sensor._attr_device_info["name"] == "Wolt Gdb"
        assert sensor._attr_device_info["manufacturer"] == "Wolt"
        assert sensor._attr_device_info["via_device"] == ("wolt", "test_hub_id")
        assert sensor._attr_device_info["suggested_area"] == "Test Home"

    def test_attr_name(self, mock_wolt_venue_data):
        """Test attr_name is set to display type name."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_name == "Status"

    def test_device_name_uses_slug_title(self):
        """Test device name title-cases the slug."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "marlen"

        sensor = WoltStatusTextSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_device_info["name"] == "Wolt Marlen"


class TestWoltDeliveryTimeSensor:
    """Tests for WoltDeliveryTimeSensor."""

    def test_native_value_with_data(self, mock_wolt_venue_data):
        """Test native_value returns delivery time when data is available."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryTimeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value == "25-35 min"

    def test_native_value_no_data(self):
        """Test native_value returns None when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryTimeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value is None

    def test_icon(self, mock_wolt_venue_data):
        """Test icon returns correct value."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryTimeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.icon == "mdi:clock-outline"

    def test_unique_id(self, mock_wolt_venue_data):
        """Test unique_id is correctly set."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryTimeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_unique_id == "wolt_gdb_delivery_time"

    def test_attr_name(self, mock_wolt_venue_data):
        """Test attr_name is set to display type name."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryTimeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_name == "Delivery Time"


class TestWoltDeliveryFeeSensor:
    """Tests for WoltDeliveryFeeSensor."""

    def test_native_value_with_data(self, mock_wolt_venue_data):
        """Test native_value returns formatted fee when data is available."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value == "₪14.00"

    def test_native_value_no_data(self):
        """Test native_value returns None when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value is None

    def test_extra_state_attributes_with_data(self, mock_wolt_venue_data):
        """Test extra_state_attributes returns fee in agorot."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        attrs = sensor.extra_state_attributes
        assert attrs["delivery_fee"] == 1400

    def test_extra_state_attributes_no_data(self):
        """Test extra_state_attributes returns empty dict when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.extra_state_attributes == {}

    def test_icon(self, mock_wolt_venue_data):
        """Test icon returns correct value."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.icon == "mdi:currency-usd"

    def test_attr_name(self, mock_wolt_venue_data):
        """Test attr_name is set to display type name."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltDeliveryFeeSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_name == "Delivery Fee"


class TestWoltMinimumOrderSensor:
    """Tests for WoltMinimumOrderSensor."""

    def test_native_value_with_data(self, mock_wolt_venue_data):
        """Test native_value returns minimum order when data is available."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value == "₪49.00"

    def test_native_value_no_data(self):
        """Test native_value returns None when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.native_value is None

    def test_extra_state_attributes_with_data(self, mock_wolt_venue_data):
        """Test extra_state_attributes returns minimum order in agorot."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        attrs = sensor.extra_state_attributes
        assert attrs["minimum_order"] == 4900

    def test_extra_state_attributes_no_data(self):
        """Test extra_state_attributes returns empty dict when no data."""
        coordinator = MagicMock()
        coordinator.data = None
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.extra_state_attributes == {}

    def test_icon(self, mock_wolt_venue_data):
        """Test icon returns correct value."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor.icon == "mdi:cart"

    def test_attr_name(self, mock_wolt_venue_data):
        """Test attr_name is set to display type name."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_name == "Minimum Order"

    def test_unique_id_has_minimum_order_suffix(self, mock_wolt_venue_data):
        """Test unique_id includes _minimum_order suffix."""
        coordinator = MagicMock()
        coordinator.data = mock_wolt_venue_data
        coordinator.venue_config.slug = "gdb"

        sensor = WoltMinimumOrderSensor(coordinator, "test_hub_id", "Test Home")
        assert sensor._attr_unique_id == "wolt_gdb_minimum_order"
