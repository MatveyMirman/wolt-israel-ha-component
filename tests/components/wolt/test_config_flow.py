"""Tests for the Wolt config flow."""

from unittest.mock import MagicMock, patch, PropertyMock

import pytest
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.config_entries import OptionsFlow

from custom_components.wolt.config_flow import WoltConfigFlow, WoltOptionsFlow
from custom_components.wolt.const import (
    CONF_CITY,
    CONF_COUNTRY,
    CONF_DELIVERY_METHOD,
    CONF_POLLING_INTERVAL,
    CONF_SLUG,
    DEFAULT_CITY,
    DEFAULT_COUNTRY,
    DEFAULT_DELIVERY_METHOD,
    DEFAULT_POLLING_INTERVAL,
    DOMAIN,
)


class TestWoltConfigFlow:
    """Tests for WoltConfigFlow."""

    @pytest.mark.asyncio
    async def test_user_step_shows_form(self):
        """Test user step shows form."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = MagicMock()
        flow.hass.config.location.latitude = 32.0853
        flow.hass.config.location.longitude = 34.7818

        result = await flow.async_step_user()

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert CONF_SLUG in result["data_schema"].schema
        assert CONF_CITY in result["data_schema"].schema
        assert CONF_COUNTRY in result["data_schema"].schema
        assert CONF_DELIVERY_METHOD in result["data_schema"].schema

    @pytest.mark.asyncio
    async def test_user_step_slug_normalized(self):
        """Test that slug is normalized to lowercase."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = MagicMock()
        flow.hass.config.location.latitude = 32.0853
        flow.hass.config.location.longitude = 34.7818
        flow._async_current_entries = MagicMock(return_value=[])

        result = await flow.async_step_user({CONF_SLUG: "  GDB  "})

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["data"][CONF_SLUG] == "gdb"

    @pytest.mark.asyncio
    async def test_user_step_already_configured(self):
        """Test already configured error."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = MagicMock()
        flow.hass.config.location.latitude = 32.0853
        flow.hass.config.location.longitude = 34.7818

        existing_entry = MagicMock()
        existing_entry.data = {CONF_SLUG: "gdb"}
        flow._async_current_entries = MagicMock(return_value=[existing_entry])

        result = await flow.async_step_user({CONF_SLUG: "gdb"})

        assert result["errors"] == {CONF_SLUG: "already_configured"}

    @pytest.mark.asyncio
    async def test_user_step_no_location(self):
        """Test no location error."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = None
        flow._async_current_entries = MagicMock(return_value=[])

        result = await flow.async_step_user({CONF_SLUG: "gdb"})

        assert result["errors"] == {"base": "no_location"}

    def test_get_home_location(self):
        """Test getting home location."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = MagicMock()
        flow.hass.config.location.latitude = 32.0853
        flow.hass.config.location.longitude = 34.7818

        lat, lon = flow._get_home_location()
        assert lat == 32.0853
        assert lon == 34.7818

    def test_get_home_location_not_set(self):
        """Test getting home location when not set."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = None

        lat, lon = flow._get_home_location()
        assert lat is None
        assert lon is None


class TestWoltOptionsFlow:
    """Tests for WoltOptionsFlow.

    Note: WoltOptionsFlow requires config_entry to be set, but in newer HA versions
    config_entry is a property with no setter. These tests verify the config flow
    class structure and options flow detection.
    """

    def test_options_flow_has_get_options_flow(self):
        """Test that WoltConfigFlow has async_get_options_flow method."""
        flow = WoltConfigFlow()
        assert hasattr(flow, 'async_get_options_flow')
        assert callable(flow.async_get_options_flow)
