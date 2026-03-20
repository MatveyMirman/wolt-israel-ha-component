"""Pytest fixtures for Wolt integration tests."""

import asyncio
from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from custom_components.wolt.api import WoltVenueData
from custom_components.wolt.const import (
    CONF_DELIVERY_METHOD,
    CONF_HUB_ID,
    CONF_HUB_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SLUG,
    CONF_VENUES,
    CONF_ZONE,
    DOMAIN,
)


@pytest.fixture
def mock_wolt_venue_data() -> WoltVenueData:
    """Return mock Wolt venue data."""
    return WoltVenueData(
        online=True,
        status_text="Open for delivery",
        delivery_time="25-35 min",
        delivery_fee=1400,
        delivery_fee_formatted="₪14.00",
        venue_id="venue_123",
        next_open="2024-01-15T10:00:00",
        next_close="2024-01-15T22:00:00",
        rating=4.5,
        minimum_order_amount=4900,
        minimum_order_amount_formatted="₪49.00",
        raw_data={},
    )


@pytest.fixture
def mock_wolt_venue_data_unavailable() -> WoltVenueData:
    """Return mock Wolt venue data for unavailable venue."""
    return WoltVenueData(
        online=False,
        status_text="Closed",
        delivery_time=None,
        delivery_fee=None,
        delivery_fee_formatted=None,
        venue_id="venue_123",
        next_open="2024-01-16T10:00:00",
        next_close=None,
        rating=4.2,
        minimum_order_amount=3900,
        minimum_order_amount_formatted="₪39.00",
        raw_data={},
    )


@pytest.fixture
def mock_api_client():
    """Return a mock API client."""
    from unittest.mock import AsyncMock
    return AsyncMock()


@pytest.fixture
def mock_config_entry():
    """Return a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        CONF_HUB_ID: "test_hub_id",
        CONF_HUB_NAME: "Test Home",
        CONF_ZONE: "Home Assistant Home",
        CONF_LATITUDE: 32.0853,
        CONF_LONGITUDE: 34.7818,
        CONF_VENUES: [
            {
                CONF_SLUG: "gdb",
                CONF_DELIVERY_METHOD: "homedelivery",
            }
        ],
    }
    entry.options = {}
    return entry


@pytest.fixture
def mock_hass_location():
    """Return a mock home location."""
    location = MagicMock()
    location.latitude = 32.0853
    location.longitude = 34.7818
    return location


@pytest.fixture
def hass(hass_fixture, mock_hass_location):
    """Return a HomeAssistant instance."""
    hass_fixture.config.location = mock_hass_location
    hass_fixture.data[DOMAIN] = {}
    return hass_fixture


@pytest.fixture
def mock_setup_entry():
    """Return a mock setup_entry function."""
    from unittest.mock import AsyncMock
    return AsyncMock(return_value=True)


@pytest.fixture
def hass_with_location(hass, mock_hass_location):
    """Return a HomeAssistant instance with configured location."""
    hass.config.location = mock_hass_location
    return hass
