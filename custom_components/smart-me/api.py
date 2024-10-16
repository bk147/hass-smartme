from dataclasses import dataclass
from enum import StrEnum
import logging
from random import choice, randrange

_LOGGER = logging.getLogger(__name__)


class DeviceType(StrEnum):
    """Device types."""

    TEMP_SENSOR = "temp_sensor"
    DOOR_SENSOR = "door_sensor"
    OTHER = "other"


@dataclass
class Device:
    """API device."""

    device_id: int
    device_unique_id: str
    device_type: DeviceType
    name: str
    state: int | bool


class API:
    """Class for example API."""

    def __init__(self, deviceid: str, username: str, password: str) -> None:
        """Initialise."""
        self.deviceid = deviceid
        self.username = username
        self.password = password
        self.connected: bool = False

    @property
    def controller_name(self) -> str:
        """Return the name of the controller."""
        return self.deviceid

    def connect(self) -> bool:
        """Connect to api."""
        if self.username != "test":
            self.connected = True
            return True
        raise APIAuthError("Error connecting to api. Invalid username or password.")

    def disconnect(self) -> bool:
        """Disconnect from api."""
        self.connected = False
        return True


class APIAuthError(Exception):
    """Exception class for auth error."""


class APIConnectionError(Exception):
    """Exception class for connection error."""
