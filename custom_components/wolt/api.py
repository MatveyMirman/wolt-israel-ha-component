"""API client for Wolt venue data."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import aiohttp

from .const import (
    API_BASE_URL,
    API_DYNAMIC_ENDPOINT,
    HEADERS,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class WoltVenueData:
    """Data class for Wolt venue information."""

    online: bool
    status_text: str | None
    delivery_time: str | None
    delivery_fee: int | None
    delivery_fee_formatted: str | None
    venue_id: str | None
    next_open: str | None
    next_close: str | None
    rating: float | None
    minimum_order_amount: int | None
    minimum_order_amount_formatted: str | None
    raw_data: dict[str, Any] | None


class WoltApiClient:
    """Client for interacting with Wolt API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def async_get_venue_dynamic(
        self,
        slug: str,
        lat: float,
        lon: float,
        delivery_method: str,
    ) -> WoltVenueData | None:
        """Fetch venue dynamic data from Wolt API.

        Args:
            slug: The venue slug (e.g., 'gdb')
            lat: Latitude for location-specific data
            lon: Longitude for location-specific data
            delivery_method: Delivery method preference

        Returns:
            WoltVenueData object or None if request fails
        """
        url = f"{API_BASE_URL}{API_DYNAMIC_ENDPOINT.format(slug=slug)}"
        params = {
            "lat": lat,
            "lon": lon,
            "selected_delivery_method": delivery_method,
        }

        try:
            async with self._session.get(
                url, headers=HEADERS, params=params, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_venue_data(data)
                _LOGGER.warning(
                    "Wolt API returned status %s for venue %s", response.status, slug
                )
                return None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching Wolt venue data: %s", err)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error fetching Wolt venue data: %s", err)
            return None

    def _parse_venue_data(self, data: dict[str, Any]) -> WoltVenueData:
        """Parse API response into WoltVenueData.

        Args:
            data: Raw API response dictionary

        Returns:
            Parsed WoltVenueData object
        """
        venue = data.get("venue", {})

        online = venue.get("online", False)

        delivery_open_status = venue.get("delivery_open_status", {})
        status_text = delivery_open_status.get("value")
        next_open = delivery_open_status.get("next_open")
        next_close = delivery_open_status.get("next_close")

        delivery_configs = venue.get("delivery_configs", [])
        delivery_time = None
        for config in delivery_configs:
            if config.get("method") == self._get_delivery_method():
                estimate = config.get("estimate", {})
                delivery_time = estimate.get("label")
                break

        delivery_fee = None
        delivery_fee_formatted = None
        minimum_order_amount = None
        minimum_order_amount_formatted = None
        header = venue.get("header", {})
        method_statuses = header.get("delivery_method_statuses", [])
        for method_status in method_statuses:
            if method_status.get("delivery_method") == "UNAVAILABLE":
                metadata = method_status.get("metadata", [])
                for item in metadata:
                    if item.get("type") == "LINK_WITH_ICON":
                        link = item.get("link")
                        if link == "DELIVERY_FEE":
                            delivery_fee_formatted = item.get("value")
                            delivery_fee = self._parse_fee(delivery_fee_formatted)
                        elif link == "MINIMUM_ORDER":
                            minimum_order_amount_formatted = item.get("value")
                            minimum_order_amount = self._parse_fee(minimum_order_amount_formatted)

        rating = self._parse_rating(venue)

        return WoltVenueData(
            online=online,
            status_text=status_text,
            delivery_time=delivery_time,
            delivery_fee=delivery_fee,
            delivery_fee_formatted=delivery_fee_formatted,
            venue_id=venue.get("id"),
            next_open=next_open,
            next_close=next_close,
            rating=rating,
            minimum_order_amount=minimum_order_amount,
            minimum_order_amount_formatted=minimum_order_amount_formatted,
            raw_data=data,
        )

    def _parse_rating(self, venue: dict[str, Any]) -> float | None:
        """Parse rating from venue data.

        Args:
            venue: Venue dictionary

        Returns:
            Rating as float or None if not available
        """
        raw_rating = venue.get("rating")
        if raw_rating is not None:
            try:
                return float(raw_rating)
            except (ValueError, TypeError):
                return None
        return None

    def _get_delivery_method(self) -> str:
        """Get the configured delivery method."""
        return "homedelivery"

    def _parse_fee(self, formatted: str | None) -> int | None:
        """Parse delivery fee from formatted string.

        Args:
            formatted: Formatted fee string like '₪14.00'

        Returns:
            Fee in agorot (cents) or None if parsing fails
        """
        if not formatted:
            return None
        try:
            cleaned = formatted.replace("₪", "").replace(",", "").strip()
            amount = float(cleaned) * 100
            return int(amount)
        except (ValueError, AttributeError):
            return None
