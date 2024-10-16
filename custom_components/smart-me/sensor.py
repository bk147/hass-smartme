"""Interfaces with the Integration 101 Template api sensors."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfElectricPotential, UnitOfEnergy
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        SensorActivePower(coordinator),
        SensorVoltage(coordinator),
        SensorCounterReading(coordinator),
    ]

    # Create the sensors.
    async_add_entities(sensors)

class SensorActivePower(CoordinatorEntity):
    
    name = "ActivePower"
    unit_of_measurement = UnitOfPower.WATT
    state_class = SensorStateClass.MEASUREMENT
    device_class = SensorDeviceClass.POWER
    
    def __init__(self, coordinator: SmartmeCoordinator) -> None:
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            """ generate new device """
            name=self.coordinator.devicename,
            manufacturer="smart-me AG",
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.deviceid,
                )
            },
        )
    
    @property
    def state(self):
        return round(self.coordinator.data.ActivePower * 1000, 0)

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}-{self.coordinator.deviceid}-{self.name}"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["ActivePowerL1"] = round(self.coordinator.data.ActivePowerL1 * 1000, 0)
        attrs["ActivePowerL2"] = round(self.coordinator.data.ActivePowerL2 * 1000, 0)
        attrs["ActivePowerL3"] = round(self.coordinator.data.ActivePowerL3 * 1000, 0)
        return attrs

class SensorVoltage(CoordinatorEntity):
    
    name = "Voltage"
    unit_of_measurement = UnitOfElectricPotential.VOLT
    state_class = SensorStateClass.MEASUREMENT
    device_class = SensorDeviceClass.VOLTAGE
    
    def __init__(self, coordinator: SmartmeCoordinator) -> None:
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.deviceid,
                )
            },
        )
    
    @property
    def state(self):
        return round(self.coordinator.data.Voltage, 1)

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}-{self.coordinator.deviceid}-{self.name}"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["VoltageL1"] = round(self.coordinator.data.VoltageL1, 1)
        attrs["VoltageL2"] = round(self.coordinator.data.VoltageL2, 1)
        attrs["VoltageL3"] = round(self.coordinator.data.VoltageL3, 1)
        return attrs

class SensorCounterReading(CoordinatorEntity):
    
    name = "CounterReading"
    unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    state_class = SensorStateClass.TOTAL_INCREASING
    device_class = SensorDeviceClass.ENERGY
    
    def __init__(self, coordinator: SmartmeCoordinator) -> None:
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.deviceid,
                )
            },
        )
    
    @property
    def state(self):
        return self.coordinator.data.CounterReading

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}-{self.coordinator.deviceid}-{self.name}"

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        # Add any additional attributes you want on your sensor.
        attrs = {}
        attrs["CounterReadingImport"] = self.coordinator.data.CounterReadingImport
        attrs["CounterReadingExport"] = self.coordinator.data.CounterReadingExport
        return attrs
