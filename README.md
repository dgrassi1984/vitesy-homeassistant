# Vitesy Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This integration allows you to integrate your Vitesy air purifiers with Home Assistant.

## Features

- Monitor your Vitesy device's air quality sensors
- Track device status and operation modes
- View battery levels and filter status
- Control device settings

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Add"
7. Search for "Vitesy" in HACS
8. Click "Install"
9. Restart Home Assistant

### Manual Installation

1. Copy the `vitesy` folder from this repository to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click the "+ Add Integration" button
3. Search for "Vitesy"
4. Enter your Vitesy API key
5. Click "Submit"

## Supported Devices

- List your supported Vitesy devices here

## Available Entities

### Sensors
- Air Quality
- Temperature
- Humidity
- Battery Level
- Filter Status

### Controls
- Power On/Off
- Operation Mode
- Fan Speed

## API Key

To obtain your Vitesy API key:
1. Log in to your Vitesy account
2. Navigate to your profile settings
3. Find the API section
4. Generate or copy your API key

## Troubleshooting

If you encounter any issues:
1. Check your API key is correct
2. Ensure your device is online and connected to the internet
3. Check the Home Assistant logs for any error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This integration is not officially supported by Vitesy. Use at your own risk. 