from __future__ import annotations

import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth
from homeassistant.const import Platform

from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]

class Hub:
    def __init__(self, hass: HomeAssistant, deviceid: str, username: str, password: str) -> None:
        """Init dummy hub."""
        self._deviceid = deviceid
        self._username = username
        self._password = password


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up device from a config entry."""
    deviceid = entry.unique_id
    username = entry.data.get("username")
    password = entry.data.get("password")
    assert deviceid is not None
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Hub(hass, deviceid=deviceid, username=username, password=password)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
