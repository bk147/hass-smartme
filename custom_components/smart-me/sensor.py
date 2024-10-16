"""Interfaces with the Integration 101 Template api sensors."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Device, DeviceType
from .const import DOMAIN
from .coordinator import SmartmeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Sensors."""
    # This gets the data update coordinator from hass.data as specified in your __init__.py
    coordinator: SmartmeCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ].coordinator

    # Enumerate all the sensors in your data value from your DataUpdateCoordinator and add an instance of your sensor class
    # to a list for each one.
    # This maybe different in your specific case, depending on how your data is structured
    sensors = [
        SmartmeDeviceSensor(coordinator),
        SmartmeSensor1(coordinator),
    ]

    # Create the sensors.
    async_add_entities(sensors)

class SmartmeDeviceSensor(CoordinatorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: SmartmeCoordinator) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._deviceid = f"device-{coordinator.deviceid}"
        self._devicename = f"Device {coordinator.devicename}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        # This method is called by your DataUpdateCoordinator when a successful update runs.
        self.async_write_ha_state()

    @property
    def device_class(self) -> str:
        """Return device class."""
        # https://developers.home-assistant.io/docs/core/entity/sensor/#available-device-classes
        return SensorDeviceClass.TEMPERATURE

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Identifiers are what group entities into the same device.
        # If your device is created elsewhere, you can just specify the indentifiers parameter.
        # If your device connects via another device, add via_device parameter with the indentifiers of that device.
        return DeviceInfo(
            name=self._devicename,
            manufacturer="smart-me AG",
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.data.controller_name,
                )
            },
        )

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Test Device Sensor"
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return 30

    @property
    def unit_of_measurement(self) -> str | None:
        """Return unit of temperature."""
        return UnitOfTemperature.CELSIUS

    @property
    def state_class(self) -> str | None:
        """Return state class."""
        # https://developers.home-assistant.io/docs/core/entity/sensor/#available-state-classes
        return SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-{self._deviceid}-1"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["extra_info"] = "Extra Info 1"
        return attrs

class SmartmeSensor1(CoordinatorEntity):
    """Implementation of a sensor."""

    name = "Test Sensor 1"
    unit_of_measurement = UnitOfTemperature.CELSIUS
    state_class = SensorStateClass.MEASUREMENT
    device_class = SensorDeviceClass.TEMPERATURE
    
    def __init__(self, coordinator: SmartmeCoordinator) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._deviceid = f"device-{coordinator.deviceid}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        # This method is called by your DataUpdateCoordinator when a successful update runs.
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Identifiers are what group entities into the same device.
        # If your device is created elsewhere, you can just specify the indentifiers parameter.
        # If your device connects via another device, add via_device parameter with the indentifiers of that device.
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.data.controller_name,
                )
            },
        )
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return 30

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-{self._deviceid}-2"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["extra_info"] = "Extra Info 2"
        return attrs
