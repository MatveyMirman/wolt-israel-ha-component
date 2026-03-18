"""Constants for the Wolt integration."""

from typing import Final

DOMAIN: Final = "wolt"

API_BASE_URL: Final = "https://consumer-api.wolt.com"
API_DYNAMIC_ENDPOINT: Final = "/order-xp/web/v1/venue/slug/{slug}/dynamic/"
API_PURCHASE_ENDPOINT: Final = "/order-xp/web/v1/pages/venue/pricing-estimates"

DEFAULT_COUNTRY: Final = "isr"
DEFAULT_CITY: Final = "tel-aviv"
DEFAULT_DELIVERY_METHOD: Final = "homedelivery"
DEFAULT_POLLING_INTERVAL: Final = 300

CONF_SLUG: Final = "slug"
CONF_CITY: Final = "city"
CONF_COUNTRY: Final = "country"
CONF_LATITUDE: Final = "latitude"
CONF_LONGITUDE: Final = "longitude"
CONF_DELIVERY_METHOD: Final = "delivery_method"
CONF_POLLING_INTERVAL: Final = "polling_interval"

DELIVERY_METHODS: Final = [
    ("homedelivery", "Home Delivery"),
    ("takeaway", "Takeaway"),
    ("eatin", "Eat In"),
]

HEADERS: Final = {
    "app-language": "en",
    "platform": "Web",
    "Origin": "https://wolt.com",
    "User-Agent": "Mozilla/5.0 (compatible; HomeAssistant)",
}

UPDATE_ERROR: Final = "Failed to update Wolt venue data"

ATTR_AVAILABILITY: Final = "availability"
ATTR_STATUS_TEXT: Final = "status_text"
ATTR_DELIVERY_TIME: Final = "delivery_time"
ATTR_DELIVERY_FEE: Final = "delivery_fee"
ATTR_DELIVERY_FEE_FORMATTED: Final = "delivery_fee_formatted"
ATTR_VENUE_ID: Final = "venue_id"
ATTR_NEXT_OPEN: Final = "next_open"
ATTR_NEXT_CLOSE: Final = "next_close"
ATTR_ORDER_URL: Final = "order_url"
