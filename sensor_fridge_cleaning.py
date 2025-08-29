import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTime

from .const import DOMAIN
from .coordinator import VitesyCoordinator
from .maintenance_base import FridgeMaintenanceSensor
_LOGGER = logging.getLogger(__name__)

from datetime import datetime

class FridgeCleaningSensor(FridgeMaintenanceSensor):

    @property
    def device_class(self) -> str:
        """Return device class."""
        # https://developers.home-assistant.io/docs/core/entity/sensor/#available-device-classes
        return SensorDeviceClass.DURATION

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"DaysUntilFridgeCleanRequired{self.device_id}-{self.maintenance_data_id}"

    @property
    def native_unit_of_measurement(self) -> str | None:
        return UnitOfTime.DAYS

    @property
    def native_value(self) -> int | float:
        """Return the state of the entity."""
        # Using native value and native unit of measurement, allows you to change units
        # in Lovelace and HA will automatically calculate the correct value.
        sensorDateString = self.maintenance_data.get('due_date', None)
        if sensorDateString is None:
            return -1
        sensorDateTime = datetime.strptime(sensorDateString, "%Y-%m-%dT%H:%M:%S.%fZ")
        delta = sensorDateTime - datetime.now()
        return max(0, delta.days)

    @property
    def state_class(self) -> str | None:
        """Return state class."""
        # https://developers.home-assistant.io/docs/core/entity/sensor/#available-state-classes
        return SensorStateClass.MEASUREMENT
    