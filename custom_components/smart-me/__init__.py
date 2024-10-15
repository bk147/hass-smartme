"""The Detailed Hello World Push integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS = [Platform.SENSOR]

class Hub:
    def __init__(self, deviceid: str, username: str, password: str) -> None:
        self.deviceid = deviceid
        self.username = username
        self.password= password

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Hub(hass, entry.unique_id, entry.data["username"], entry.data["password"])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
