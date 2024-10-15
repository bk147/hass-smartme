from homeassistant.components.sensor import (
    SensorDeviceClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import hub

from . import HubConfigEntry
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    hub = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([ExampleSensor(hub)])

class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    should_poll = False
    
    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hub) -> None:
        """Initialize a sensor."""
        self._deviceid = hub.deviceid
        self._username = hub.username
        self._password = hub.password
        self._callbacks = set()
        self._value = 25

        self.hub = hub
        self.name = "Test Name"
        self.firmware_version = f"0.0.{random.randint(1, 9)}"
        self.model = "Test Model"

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._deviceid)}}
        
    # The value of this sensor.
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value
    
    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._roller.online and self._roller.hub.online

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._callbacks.add(callback)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

