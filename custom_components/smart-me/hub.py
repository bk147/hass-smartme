"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import random

from homeassistant.core import HomeAssistant


class Hub:
    manufacturer = "Smartme Hub"

    def __init__(self, hass: HomeAssistant, deviceid: str, username: str, password: str) -> None:
        """Init dummy hub."""
        self._hass = hass
        self._deviceid = deviceid
        self._username = username
        self._password= password
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._deviceid

    async def test_connection(self) -> bool:
        """TODO"""
        return True
