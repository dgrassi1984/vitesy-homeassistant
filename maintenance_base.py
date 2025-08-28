import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from .coordinator import VitesyCoordinator

_LOGGER = logging.getLogger(__name__)

class FridgeMaintenanceSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a maintenance_data."""

    def __init__(self, coordinator: VitesyCoordinator, device: dict, name: str, maintenance_data: dict) -> None:
        """Initialise maintenance_data."""
        super().__init__(coordinator)
        self.device = device
        self.maintenance_data = maintenance_data
        
        self.device_id = device.get('id')
        self.maintenance_data_id = name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update maintenance_data with latest data from coordinator."""
        # This method is called by your DataUpdateCoordinator when a successful update runs.
        self.device = self.coordinator.get_device_by_id(self.device_id)
        self.maintenance_data = self.coordinator.get_maintenance_data_by_id(self.device_id, self.maintenance_data_id)
        self.async_write_ha_state()

    @property
    def device_class(self) -> str:
        raise NotImplementedError("Device class not implemented")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Identifiers are what group entities into the same device.
        # If your device is created elsewhere, you can just specify the indentifiers parameter.
        # If your device connects via another device, add via_device parameter with the indentifiers of that device.
        return DeviceInfo(
            name=f"Shelfy{self.device_id}",
            manufacturer="Vitesy",
            model="Shelfy",
            sw_version=self.device.get('firmware_version'),
            identifiers={
                (
                    DOMAIN,
                    self.device_id
                )
            },
        )

    @property
    def name(self) -> str:
        raise NotImplementedError("Device class not implemented")

    @property
    def native_unit_of_measurement(self) -> str | None:
        raise NotImplementedError("Device class not implemented")

    @property
    def native_value(self) -> int | float:
        raise NotImplementedError("Native value not implemented")
    @property
    def state_class(self) -> str | None:
        raise NotImplementedError("State class not implemented")

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-{self.device_id}-{self.maintenance_data_id}"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["extra_info"] = self.maintenance_data
        return attrs