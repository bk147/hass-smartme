from __future__ import annotations

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

class Hub:
    def __init__(self, hass: HomeAssistant, address: str) -> None:
        """Init dummy hub."""
        self.address = address


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up device from a config entry."""
    return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
