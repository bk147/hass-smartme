"""The Detailed Hello World Push integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

class Hub:
    def __init__(self, deviceid: str, username: str, password: str) -> None:
        self.deviceid = deviceid
        self.username = username
        self.password = password

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    deviceid = entry.unique_id
    assert deviceid is not None
    username = entry.data["username"]
    password = entry.data["password"]
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Hub(deviceid, username, password)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
