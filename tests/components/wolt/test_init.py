"""Tests for the Wolt integration __init__ module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wolt import PLATFORMS
from custom_components.wolt import async_setup_entry, async_unload_entry
from custom_components.wolt.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SLUG,
    DOMAIN,
)


def test_platforms_constant():
    """Test that PLATFORMS contains expected platforms."""
    assert "sensor" in PLATFORMS
    assert "binary_sensor" in PLATFORMS
    assert "button" in PLATFORMS


def test_platforms_list():
    """Test that PLATFORMS is a list with 3 items."""
    assert len(PLATFORMS) == 3


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        CONF_SLUG: "test-venue",
        CONF_LATITUDE: 32.0853,
        CONF_LONGITUDE: 34.7818,
    }
    entry.options = {}
    return entry


@pytest.mark.asyncio
async def test_async_setup_entry_success(mock_config_entry):
    """Test successful setup of config entry."""
    mock_hass = MagicMock()
    mock_hass.data = {}
    mock_hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    mock_config_entry.async_on_unload = MagicMock()

    with patch(
        "custom_components.wolt.WoltDataUpdateCoordinator"
    ) as mock_coordinator_class:
        mock_coordinator = MagicMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()
        mock_coordinator_class.return_value = mock_coordinator

        result = await async_setup_entry(mock_hass, mock_config_entry)

        assert result is True
        mock_coordinator.async_config_entry_first_refresh.assert_called_once()
        mock_hass.config_entries.async_forward_entry_setups.assert_called_once()
        assert DOMAIN in mock_hass.data
        assert mock_config_entry.entry_id in mock_hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_async_setup_entry_no_location(mock_config_entry):
    """Test setup fails when no location is available."""
    mock_config_entry.data = {CONF_SLUG: "test-venue"}
    mock_hass = MagicMock()
    mock_hass.config.as_dict.return_value = {
        "latitude": None,
        "longitude": None,
    }

    result = await async_setup_entry(mock_hass, mock_config_entry)

    assert result is False


@pytest.mark.asyncio
async def test_async_setup_entry_adds_coordinates(mock_config_entry):
    """Test setup adds coordinates from home location."""
    mock_config_entry.data = {CONF_SLUG: "test-venue"}
    mock_hass = MagicMock()
    mock_hass.data = {}
    mock_hass.config.as_dict.return_value = {
        "latitude": 32.0853,
        "longitude": 34.7818,
    }
    mock_hass.config_entries.async_update_entry = MagicMock()
    mock_hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    mock_config_entry.async_on_unload = MagicMock()

    with patch(
        "custom_components.wolt.WoltDataUpdateCoordinator"
    ) as mock_coordinator_class:
        mock_coordinator = MagicMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()
        mock_coordinator_class.return_value = mock_coordinator

        result = await async_setup_entry(mock_hass, mock_config_entry)

        assert result is True
        mock_hass.config_entries.async_update_entry.assert_called_once()
        update_call = mock_hass.config_entries.async_update_entry.call_args
        assert CONF_LATITUDE in update_call[1]["data"]
        assert CONF_LONGITUDE in update_call[1]["data"]


@pytest.mark.asyncio
async def test_async_unload_entry(mock_config_entry):
    """Test successful unloading of config entry."""
    mock_hass = MagicMock()
    mock_hass.data = {DOMAIN: {mock_config_entry.entry_id: MagicMock()}}
    mock_hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

    result = await async_unload_entry(mock_hass, mock_config_entry)

    assert result is True
    mock_hass.config_entries.async_unload_platforms.assert_called_once()
    assert mock_config_entry.entry_id not in mock_hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_async_unload_entry_failure(mock_config_entry):
    """Test unloading fails when platforms fail to unload."""
    mock_hass = MagicMock()
    mock_hass.data = {DOMAIN: {mock_config_entry.entry_id: MagicMock()}}
    mock_hass.config_entries.async_unload_platforms = AsyncMock(return_value=False)

    result = await async_unload_entry(mock_hass, mock_config_entry)

    assert result is False
    assert mock_config_entry.entry_id in mock_hass.data[DOMAIN]
