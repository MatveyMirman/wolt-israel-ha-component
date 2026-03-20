"""Tests for the Wolt API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import aiohttp

from custom_components.wolt.api import WoltApiClient, WoltVenueData
from custom_components.wolt.const import API_BASE_URL, API_DYNAMIC_ENDPOINT


class TestWoltApiClient:
    """Tests for WoltApiClient."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock aiohttp session."""
        session = AsyncMock(spec=aiohttp.ClientSession)
        return session

    @pytest.fixture
    def api_client(self, mock_session):
        """Create an API client instance."""
        return WoltApiClient(mock_session)

    async def test_async_get_venue_dynamic_success(
        self, api_client, mock_session, mock_wolt_venue_data
    ):
        """Test successful venue data fetch."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "venue": {
                    "online": True,
                    "order_minimum": {
                        "formatted": "₪49.00",
                        "amount": 4900
                    },
                    "delivery_open_status": {
                        "value": "Open for delivery",
                        "next_open": "2024-01-15T10:00:00",
                        "next_close": "2024-01-15T22:00:00",
                    },
                    "delivery_configs": [
                        {
                            "method": "homedelivery",
                            "estimate": {"label": "25-35 min"},
                        }
                    ],
                    "header": {
                        "delivery_method_statuses": [
                            {
                                "delivery_method": "UNAVAILABLE",
                                "metadata": [
                                    {
                                        "type": "LINK_WITH_ICON",
                                        "link": "DELIVERY_FEE",
                                        "value": "₪14.00",
                                    }
                                ],
                            }
                        ]
                    },
                    "id": "venue_123",
                },
                "venue_raw": {},
            }
        )
        mock_session.get.return_value.__aenter__.return_value = mock_response

        result = await api_client.async_get_venue_dynamic(
            slug="gdb",
            lat=32.0853,
            lon=34.7818,
            delivery_method="homedelivery",
        )

        assert result is not None
        assert result.online is True
        assert result.status_text == "Open for delivery"
        assert result.delivery_time == "25-35 min"
        assert result.delivery_fee == 1400
        assert result.delivery_fee_formatted == "₪14.00"
        assert result.minimum_order_amount == 4900
        assert result.minimum_order_amount_formatted == "₪49.00"
        assert result.venue_id == "venue_123"

    async def test_async_get_venue_dynamic_api_error(
        self, api_client, mock_session
    ):
        """Test venue data fetch with API error."""
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_session.get.return_value.__aenter__.return_value = mock_response

        result = await api_client.async_get_venue_dynamic(
            slug="gdb",
            lat=32.0853,
            lon=34.7818,
            delivery_method="homedelivery",
        )

        assert result is None

    async def test_async_get_venue_dynamic_client_error(
        self, api_client, mock_session
    ):
        """Test venue data fetch with client error."""
        mock_session.get.side_effect = aiohttp.ClientError("Connection error")

        result = await api_client.async_get_venue_dynamic(
            slug="gdb",
            lat=32.0853,
            lon=34.7818,
            delivery_method="homedelivery",
        )

        assert result is None

    async def test_parse_fee_valid(self, api_client):
        """Test parsing valid delivery fee."""
        result = api_client._parse_fee("₪14.00")
        assert result == 1400

    async def test_parse_fee_with_comma(self, api_client):
        """Test parsing delivery fee with comma."""
        result = api_client._parse_fee("₪14,990.00")
        assert result == 1499000

    async def test_parse_fee_none(self, api_client):
        """Test parsing None delivery fee."""
        result = api_client._parse_fee(None)
        assert result is None

    async def test_parse_fee_invalid(self, api_client):
        """Test parsing invalid delivery fee."""
        result = api_client._parse_fee("invalid")
        assert result is None

    async def test_get_delivery_method(self, api_client):
        """Test getting delivery method."""
        result = api_client._get_delivery_method()
        assert result == "homedelivery"


class TestWoltVenueData:
    """Tests for WoltVenueData dataclass."""

    def test_venue_data_creation(self, mock_wolt_venue_data):
        """Test creating WoltVenueData instance."""
        assert mock_wolt_venue_data.online is True
        assert mock_wolt_venue_data.status_text == "Open for delivery"
        assert mock_wolt_venue_data.delivery_time == "25-35 min"
        assert mock_wolt_venue_data.delivery_fee == 1400
        assert mock_wolt_venue_data.delivery_fee_formatted == "₪14.00"
        assert mock_wolt_venue_data.minimum_order_amount == 4900
        assert mock_wolt_venue_data.minimum_order_amount_formatted == "₪49.00"
        assert mock_wolt_venue_data.venue_id == "venue_123"

    def test_venue_data_unavailable(self, mock_wolt_venue_data_unavailable):
        """Test creating WoltVenueData for unavailable venue."""
        assert mock_wolt_venue_data_unavailable.online is False
        assert mock_wolt_venue_data_unavailable.status_text == "Closed"
        assert mock_wolt_venue_data_unavailable.delivery_time is None
        assert mock_wolt_venue_data_unavailable.delivery_fee is None
        assert mock_wolt_venue_data_unavailable.minimum_order_amount == 3900
        assert mock_wolt_venue_data_unavailable.minimum_order_amount_formatted == "₪39.00"
