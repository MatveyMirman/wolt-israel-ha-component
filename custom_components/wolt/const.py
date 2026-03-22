"""Constants for the Wolt integration."""

from typing import Final

DOMAIN: Final = "wolt"
DOMAIN_VERSION: Final = 2

API_BASE_URL: Final = "https://consumer-api.wolt.com"
API_DYNAMIC_ENDPOINT: Final = "/order-xp/web/v1/venue/slug/{slug}/dynamic/"
API_PURCHASE_ENDPOINT: Final = "/order-xp/web/v1/pages/venue/pricing-estimates"

DEFAULT_COUNTRY: Final = "isr"
DEFAULT_CITY: Final = "tel-aviv"
DEFAULT_DELIVERY_METHOD: Final = "homedelivery"
DEFAULT_POLLING_INTERVAL: Final = 300
DEFAULT_HUB_NAME: Final = "My Home"

CONF_HUB_NAME: Final = "hub_name"
CONF_HUB_ID: Final = "hub_id"
CONF_ZONE: Final = "zone"
CONF_ADDRESS: Final = "address"
CONF_SLUGS: Final = "slugs"
CONF_SLUG: Final = "slug"
CONF_CITY: Final = "city"
CONF_COUNTRY: Final = "country"
CONF_LATITUDE: Final = "latitude"
CONF_LONGITUDE: Final = "longitude"
CONF_DELIVERY_METHOD: Final = "delivery_method"
CONF_POLLING_INTERVAL: Final = "polling_interval"
CONF_VENUES: Final = "venues"

VENUE_CONFIG_SCHEMA = {
    CONF_SLUG: str,
    CONF_DELIVERY_METHOD: str,
}

DELIVERY_METHODS: Final = [
    ("homedelivery", "Home Delivery"),
    ("takeaway", "Takeaway"),
]

METHOD_LABELS: Final = {
    "homedelivery": "Delivery",
    "takeaway": "Takeaway",
}

HEADERS: Final = {
    "app-language": "en",
    "platform": "web",
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
ATTR_ORDER_MINIMUM: Final = "order_minimum"
ATTR_ORDER_MINIMUM_FORMATTED: Final = "order_minimum_formatted"
