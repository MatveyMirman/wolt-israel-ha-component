# Wolt Venue Status for Home Assistant

A Home Assistant custom integration to track restaurant availability on Wolt.

## Features

- **Availability Status** - Real-time open/closed status for your favorite restaurants
- **Delivery Time** - Estimated delivery time from the restaurant
- **Delivery Fee** - Current delivery cost
- **Quick Order** - Button to open Wolt app/website directly
- **Multiple Venues** - Track multiple restaurants independently
- **Auto Location** - Uses your Home Assistant home location for accurate pricing

## Supported Countries

Currently optimized for **Israel** (country code: `isr`) with Tel Aviv as the default city.

## Installation

### Manual Installation

1. Copy the `custom_components/wolt` folder to your Home Assistant's `config/custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration**
4. Search for "Wolt" and click to configure

### HACS Installation (Future)

> HACS support coming soon.

## Configuration

### Initial Setup

1. Click **Configure** on the Wolt integration
2. Enter the venue slug from Wolt URL
   - Example: For `wolt.com/isr/tel-aviv/venue/gdb`, the slug is `gdb`
3. Optionally adjust city and delivery method
4. Coordinates are automatically set from your Home Assistant home location

### Options

- **Polling Interval** - How often to check venue status (60-3600 seconds, default: 300)

## Entities

Each configured venue creates the following entities:

| Entity | Type | Description |
|--------|------|-------------|
| `wolt_{slug}_availability` | Binary Sensor | `on` if venue is accepting orders |
| `wolt_{slug}_status` | Sensor | Status text (e.g., "Open until 24:00") |
| `wolt_{slug}_delivery_time` | Sensor | Estimated delivery time |
| `wolt_{slug}_delivery_fee` | Sensor | Delivery fee amount |
| `wolt_{slug}_order` | Button | Opens Wolt order page |

## Attributes

### Availability Sensor
- `venue_id` - Wolt venue identifier
- `next_open` - Next opening time (ISO 8601)
- `next_close` - Next closing time (ISO 8601)

### Delivery Fee Sensor
- `delivery_fee` - Fee in agorot (cents)

## Example Automation

```yaml
automation:
  - alias: "Notify when favorite restaurant opens"
    trigger:
      platform: state
      entity_id: binary_sensor.wolt_gdb_availability
      from: "off"
      to: "on"
    action:
      service: notify.persistent_notification
      data:
        title: "GDB is Open!"
        message: "Your favorite burger place is now accepting orders."
```

```yaml
automation:
  - alias: "Quick order button"
    trigger:
      platform: state
      entity_id: binary_sensor.wolt_gdb_availability
      state: "on"
    action:
      service: button.press
      target:
        entity_id: button.wolt_gdb_order
```

## Supported Delivery Methods

- `homedelivery` - Delivery to your address
- `takeaway` - Pick up from restaurant
- `eatin` - Dine in (not fully supported)

## Requirements

- Home Assistant 2024.1 or higher
- Internet connection (cloud polling)
- Home location configured in Home Assistant

## Technical Details

- **API**: Wolt Consumer API (undocumented, used with permission)
- **Polling**: Configurable interval (default 5 minutes)
- **Location**: Uses Home Assistant's configured home coordinates

## Troubleshooting

### "No home location configured" error
Make sure to set your home location in Home Assistant:
**Settings → System → General → Set home location**

### Venue shows as unavailable
- Check if the restaurant is actually open on Wolt
- Verify the venue slug is correct
- Try adjusting the delivery method in options

### Wrong delivery fee
The delivery fee depends on your location. Make sure your Home Assistant home location is set correctly.

## Contributing

Issues and pull requests welcome on [GitHub](https://github.com/your-repo/wolt-isr-ha).

## Disclaimer

This integration is not officially affiliated with Wolt. It uses Wolt's public consumer API. Use responsibly.
