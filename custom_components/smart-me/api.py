from dataclasses import dataclass
from enum import StrEnum
import logging
from random import choice, randrange

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class API:
    """Class for example API."""

    def __init__(self, hass: HomeAssistant, deviceid: str, username: str, password: str) -> None:
        """Initialise."""
        self.deviceid = deviceid
        self.username = username
        self.password = password
        self._session = async_get_clientsession(hass)
        self.connected: bool = False

    async def pullDeviceData(self):
        """get device data from api."""
        try:
            async with self._session.get(url=f"https://api.smart-me.com/Devices/{self.deviceid}", auth=BasicAuth(self.username, self.password)) as response:
                response.raise_for_status()
                response_data = await response.json()
                self.connected = true
                return response_data
        except ClientResponseError as exc:
            raise APIAuthError("Error connecting to api. Invalid username or password.")
        except ClientError as exc:
            raise APIConnectionError("Error connecting to api.")


class APIAuthError(Exception):
    """Exception class for auth error."""


class APIConnectionError(Exception):
    """Exception class for connection error."""
