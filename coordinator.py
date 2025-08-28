"""Integration 101 Template integration using DataUpdateCoordinator."""

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
)
from homeassistant.core import DOMAIN, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from vitesy.client import VitesyClient

from datetime import datetime

_LOGGER = logging.getLogger(__name__)


@dataclass
class VitesyAPIData:
    """Class to hold api data."""

    devices: list


class VitesyCoordinator(DataUpdateCoordinator):

    data: VitesyAPIData

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""

        # Set variables from values entered in config flow setup
        self.api_key = config_entry.data[CONF_API_KEY]
        self.api_connected = False

        # Initialise DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            # Method to call on every update interval.
            update_method=self.async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            # Using config option here but you can just use a value.
            update_interval=timedelta(seconds=60),
        )

        # Initialise your api here
        if self.api_key:
            self.api = VitesyClient(api_key=self.api_key)
            self.api_connected = True

    async def async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.debug("vitesy async_update_data has been called")
        try:
            devices = await self.hass.async_add_executor_job(self.api.get_devices)
            _LOGGER.debug(f"Devices: {devices}")
            sensors = []
            for device in devices:

                # Get sensors from the last 1 hour in iso format
                data_in = await self.hass.async_add_executor_job(
                    self.api.query_measurements, device["id"], None, None, None, True
                )
                for sensor_data in data_in[0]["sensors_data"]:
                    sensors.append(sensor_data)  # noqa: PERF402

                for status_data in data_in[0]["status_data"]:
                    sensors.append(status_data)  # noqa: PERF402
                
                _LOGGER.debug(f"Sensors: {sensors}")
                device["sensors"] = sensors
        except Exception as err:
            # This will show entities as unavailable by raising UpdateFailed exception
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        # What is returned here is stored in self.data by the DataUpdateCoordinator
        return VitesyAPIData(devices)

    def get_device_by_id(self, device_id: str):
        """Return device by device id."""
        # Called by the binary sensors and sensors to get their updated data from self.data
        try:
            return [
                device for device in self.data.devices if device.get('id') == device_id
            ][0]
        except IndexError:
            return None
        
    def get_sensor_by_id(self, device_id: str, sensor_id: str):
        """Return sensor by sensor id."""
        device = self.get_device_by_id(device_id)
        if device:
            return [
                sensor for sensor in device.get('sensors', []) if sensor.get('id') == sensor_id
            ][0]
        return None
        
    def get_maintenance_data_by_id(self, device_id: str, sensor_id: str):
        """Return maintenance_data by maintenance_data id."""
        device = self.get_device_by_id(device_id)
        maintenance_data = device.get('maintenance', {})
        if device and maintenance_data:
            return  maintenance_data.get('filter')
        return None
