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
    CONF_LATITUDE,
    CONF_LONGITUDE,
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

    @pytest.mark.asyncio
    async def test_full_flow(self):
        """Test complete user flow."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.location = MagicMock()
        flow.hass.config.location.latitude = 32.0853
        flow.hass.config.location.longitude = 34.7818
        flow._async_current_entries = MagicMock(return_value=[])

        user_input = {
            CONF_SLUG: "gdb",
            CONF_CITY: DEFAULT_CITY,
            CONF_COUNTRY: DEFAULT_COUNTRY,
            CONF_DELIVERY_METHOD: DEFAULT_DELIVERY_METHOD,
        }

        result = await flow.async_step_user(user_input)

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == "Wolt - Gdb"
        assert result["data"][CONF_SLUG] == "gdb"
        assert result["data"][CONF_CITY] == DEFAULT_CITY
        assert result["data"][CONF_COUNTRY] == DEFAULT_COUNTRY
        assert result["data"][CONF_DELIVERY_METHOD] == DEFAULT_DELIVERY_METHOD
        assert CONF_LATITUDE in result["data"]
        assert CONF_LONGITUDE in result["data"]


class TestWoltOptionsFlow:
    """Tests for WoltOptionsFlow."""

    @pytest.fixture
    def mock_config_entry(self):
        """Create a mock config entry."""
        entry = MagicMock()
        entry.options = {}
        return entry

    @pytest.fixture
    def options_flow(self, mock_config_entry):
        """Create options flow with mocked internals."""
        flow = WoltOptionsFlow.__new__(WoltOptionsFlow)
        flow.hass = MagicMock()
        flow._config_entry = mock_config_entry
        return flow

    def test_options_flow_init(self, mock_config_entry):
        """Test options flow initialization via WoltConfigFlow."""
        config_flow = WoltConfigFlow()
        options_flow = config_flow.async_get_options_flow(mock_config_entry)
        assert options_flow is not None
        assert isinstance(options_flow, WoltOptionsFlow)

    @pytest.mark.asyncio
    async def test_options_flow_show_form(self, options_flow):
        """Test options flow shows form."""
        result = await options_flow.async_step_init()

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "init"
        assert CONF_POLLING_INTERVAL in result["data_schema"].schema

    @pytest.mark.asyncio
    async def test_options_flow_update(self, options_flow):
        """Test options flow updates successfully."""
        user_input = {CONF_POLLING_INTERVAL: 600}

        result = await options_flow.async_step_init(user_input)

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["data"][CONF_POLLING_INTERVAL] == 600

    @pytest.mark.asyncio
    async def test_options_flow_default_polling_interval(self, options_flow):
        """Test options flow uses default polling interval via vol.Optional."""
        result = await options_flow.async_step_init()
        data_schema = result["data_schema"]

        test_result = data_schema({})
        assert test_result[CONF_POLLING_INTERVAL] == DEFAULT_POLLING_INTERVAL
