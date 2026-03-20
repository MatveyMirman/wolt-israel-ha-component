"""Tests for the Wolt config flow."""

from unittest.mock import MagicMock, patch, PropertyMock

import pytest
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.config_entries import OptionsFlow

from custom_components.wolt.config_flow import WoltConfigFlow, WoltOptionsFlow
from custom_components.wolt.const import (
    CONF_HUB_ID,
    CONF_HUB_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_POLLING_INTERVAL,
    CONF_SLUG,
    CONF_VENUES,
    CONF_ZONE,
    DEFAULT_HUB_NAME,
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
        flow.hass.config.as_dict.return_value = {
            "latitude": 32.0853,
            "longitude": 34.7818,
        }

        result = await flow.async_step_user()

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert CONF_HUB_NAME in result["data_schema"].schema
        assert "location_type" in result["data_schema"].schema

    @pytest.mark.asyncio
    async def test_user_step_creates_entry(self):
        """Test that user step creates entry with hub config."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.as_dict.return_value = {
            "latitude": 32.0853,
            "longitude": 34.7818,
        }

        user_input = {
            CONF_HUB_NAME: "My Home",
            "location_type": "home",
        }

        result = await flow.async_step_user(user_input)

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == "Wolt Hub - My Home"
        assert CONF_HUB_ID in result["data"]
        assert result["data"][CONF_HUB_NAME] == "My Home"
        assert result["data"][CONF_ZONE] == "Home Assistant Home"
        assert result["data"][CONF_LATITUDE] == 32.0853
        assert result["data"][CONF_LONGITUDE] == 34.7818
        assert result["data"][CONF_VENUES] == []

    @pytest.mark.asyncio
    async def test_user_step_no_location_aborts(self):
        """Test that user step aborts when no location is available."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.as_dict.return_value = {
            "latitude": None,
            "longitude": None,
        }

        result = await flow.async_step_user()

        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "no_location"

    @pytest.mark.asyncio
    async def test_user_step_no_location_error(self):
        """Test no location error when home not set and zones available."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.as_dict.return_value = {
            "latitude": None,
            "longitude": None,
        }

        user_input = {
            CONF_HUB_NAME: "Test",
            "location_type": "home",
        }

        result = await flow.async_step_user(user_input)

        assert result["errors"] == {"base": "no_location"}

    def test_get_home_location(self):
        """Test getting home location."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.as_dict.return_value = {
            "latitude": 32.0853,
            "longitude": 34.7818,
        }

        lat, lon = flow._get_home_location()
        assert lat == 32.0853
        assert lon == 34.7818

    def test_get_home_location_not_set(self):
        """Test getting home location when not set."""
        flow = WoltConfigFlow()
        flow.hass = MagicMock()
        flow.hass.config.as_dict.return_value = {
            "latitude": None,
            "longitude": None,
        }

        lat, lon = flow._get_home_location()
        assert lat is None
        assert lon is None


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
