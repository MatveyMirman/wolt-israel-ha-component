# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2026-03-22

### Added
- **Delivery Method Support**: Add support for both Home Delivery and Takeaway
  - Device names now include delivery method (e.g., "Marlen - Delivery", "Marlen - Takeaway")
  - Device identifiers use slug+method to prevent collisions when same venue is added multiple times
  - Takeaway venues only show: Status, Order Minimum, Available, Order
  - Delivery venues show all: Status, Delivery Time, Delivery Fee, Order Minimum, Available, Order
- **Dev Container**: Add `.devcontainer/` with Docker-based Home Assistant for local testing
- **Makefile**: Add convenience targets for `make ha-start`, `make ha-restart`, `make ha-logs`, `make ha-test`, `make ha-lint`

### Fixed
- **Entity Naming**: Remove "Wolt" prefix from device names (now just "Marlen" not "Wolt Marlen")
- **Entity Naming**: Remove venue name from entity names (now just "Status" not "Marlen Status")
- **Translation Files**: Delete conflicting `translations/en.json` and `translations/he.json` that were overriding `strings.json`
- **Delivery Fee Parsing**: Fix to check correct delivery method instead of always checking "UNAVAILABLE"
- **Order Minimum**: Rename from "Minimum Order" to "Order Minimum" to match API field name
- **Unused Imports**: Remove `CONF_DELIVERY_METHOD`, `CONF_SLUG`, `CONF_VENUES` from `__init__.py`
- **Linting**: Fix whitespace and formatting issues in multiple files

### Changed
- Hub entry titles no longer include "Wolt Hub -" prefix (now just "My Home" not "Wolt Hub - My Home")

### Tests
- Add 65 tests covering all entity classes, API parsing, config flow
- Add tests for delivery method filtering and device naming
- Add tests for integer `order_minimum` parsing (live API format)
- Update all entity tests to use new `method_label` parameter

## [0.2.4] - 2026-03-21

### Fixed
- Remove rating sensor (not available in API response)
- Fix minimum order parsing for integer format from live API
- Fix Wolt order URL format to include venue slug

## [0.2.3] - 2026-03-20

### Fixed
- Simplify options flow schema to avoid voluptuous serialization errors

## [0.2.2] - 2026-03-19

### Changed
- Bump version

## [0.2.1] - 2026-03-19

### Fixed
- Resolve failing tests for config flow changes