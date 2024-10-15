"""Platform for sensor integration."""
from __future__ import annotations

from .const import DOMAIN

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

async def async_setup_entry(hass, config_entry, async_add_entities):
    sensor = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([SmartmeSensor(sensor)])


class SmartmeSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT


    def __init__(self, sensor) -> None:
        """Initialize an bluetooth light."""
        self._deviceid = sensor.deviceid
        self._username = sensor.username
        self._password = sensor.password
    
    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 23
