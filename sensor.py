"""Interfaces with the Integration 101 Template api sensors."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from .sensor_temperature import FridgeTemperatureSensor
from .sensor_battery import FridgeBatterySensor
from .sensor_door import FridgeDoorSensor
from .sensor_filter import FridgeFilterSensor
from .sensor_fridge_cleaning import FridgeCleaningSensor
from .const import DOMAIN
from .coordinator import VitesyCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Sensors."""
    # This gets the data update coordinator from hass.data as specified in your __init__.py
    coordinator: VitesyCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ].coordinator

    # Enumerate all the sensors in your data value from your DataUpdateCoordinator and add an instance of your sensor class
    # to a list for each one.
    # This maybe different in your specific case, depending on how your data is structured
    sensors = []
    for device in coordinator.data.devices:
        _LOGGER.debug(f"Checking device: {device.get('id')}")
        for sensor in device.get('sensors', []):
            _LOGGER.debug(f"Checking sensor: {sensor.get('id')}")
            if sensor.get('id') == "TMP01-SY":
                sensors.append(FridgeTemperatureSensor(coordinator, device, sensor))
            elif sensor.get('id') == "battery":
                sensors.append(FridgeBatterySensor(coordinator, device, sensor))
            elif sensor.get('id') == "DOT-SY":
                sensors.append(FridgeDoorSensor(coordinator, device, sensor))

        
        maintenance_data = device.get('maintenance', {})
        sensors.append(FridgeFilterSensor(coordinator, device, "filter", maintenance_data.get('filter')))
        sensors.append(FridgeCleaningSensor(coordinator, device, "fridge", maintenance_data.get('fridge')))
        

    # Create the sensors.
    async_add_entities(sensors)


