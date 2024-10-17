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
        SensorActivePower(coordinator, DeviceInfo(
            #only generate device once!
            name=coordinator.devicename,
            manufacturer="smart-me AG",
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="ActivePower"),
        SensorActivePower(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="ActivePowerL1", visible=False),
        SensorActivePower(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="ActivePowerL2", visible=False),
        SensorActivePower(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="ActivePowerL3", visible=False),
        
        SensorVoltage(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="Voltage"),
        SensorVoltage(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="VoltageL1", visible=False),
        SensorVoltage(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="VoltageL2", visible=False),
        SensorVoltage(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="VoltageL3", visible=False),
        
        SensorCounterReading(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="CounterReading"),
        SensorCounterReading(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="CounterReadingImport", visible=False),
        SensorCounterReading(coordinator, DeviceInfo(
            identifiers={(DOMAIN, coordinator.deviceid)}
        ), key="CounterReadingExport", visible=False),
    ]

    # Create the sensors.
    async_add_entities(sensors)

class SensorActivePower(CoordinatorEntity):
    
    _attr_should_poll = False
    
    _attr_has_entity_name = True
    _attr_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    
    def __init__(self, coordinator: SmartmeCoordinator, deviceinfo: DeviceInfo, key: str, visible: bool = True) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = key
        self.unique_id = f"{coordinator.deviceid}-{key}"
        self.entity_registry_enabled_default = visible

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
    
    @property
    def state(self):
        return round(self.coordinator.data.device_data[self.translation_key] * 1000, 0)
    
    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["state_class"] = SensorStateClass.MEASUREMENT
        return attrs

class SensorVoltage(CoordinatorEntity):
    
    _attr_should_poll = False
    
    _attr_has_entity_name = True
    _attr_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    
    def __init__(self, coordinator: SmartmeCoordinator, deviceinfo: DeviceInfo, key: str, visible: bool = True) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = key
        self.unique_id = f"{coordinator.deviceid}-{key}"
        self.entity_registry_enabled_default = visible

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
    
    @property
    def state(self):
        return round(self.coordinator.data.device_data[self.translation_key], 1)
    
    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["state_class"] = SensorStateClass.MEASUREMENT
        return attrs

class SensorCounterReading(CoordinatorEntity):
    
    _attr_should_poll = False
    
    _attr_has_entity_name = True
    _attr_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    
    def __init__(self, coordinator: SmartmeCoordinator, deviceinfo: DeviceInfo, key: str, visible: bool = True) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = key
        self.unique_id = f"{coordinator.deviceid}-{key}"
        self.entity_registry_enabled_default = visible

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
    
    @property
    def state(self):
        return self.coordinator.data.device_data[self.translation_key]
    
    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["state_class"] = SensorStateClass.TOTAL_INCREASING
        return attrs
