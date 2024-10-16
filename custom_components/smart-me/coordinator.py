from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_FRIENDLY_NAME,
    CONF_USERNAME,
    CONF_PASSWORD,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import API, APIAuthError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class SmartmeAPIData:
    """Class to hold api data."""

    ActivePower: float
    ActivePowerL1: float
    ActivePowerL2: float
    ActivePowerL3: float

    Voltage: float
    VoltageL1: float
    VoltageL2: float
    VoltageL3: float

    CounterReading: int
    CounterReadingImport: int
    CounterReadingExport: int


class SmartmeCoordinator(DataUpdateCoordinator):
    """My coordinator."""

    data: SmartmeAPIData

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""

        # Set variables from values entered in config flow setup
        self.deviceid = config_entry.data[CONF_DEVICE_ID]
        self.devicename = config_entry.data[CONF_FRIENDLY_NAME]
        self.username = config_entry.data[CONF_USERNAME]
        self.password = config_entry.data[CONF_PASSWORD]

        # Initialise DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            # Method to call on every update interval.
            update_method=self.async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=10),
        )

        # Initialise your api here
        self.api = API(hass, deviceid=self.deviceid, username=self.username, password=self.password)

    async def async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            devicedata = await self.api.pullDeviceData()
            return SmartmeAPIData(
                ActivePower=devicedata['ActivePower'],
                ActivePowerL1=devicedata['ActivePowerL1'],
                ActivePowerL2=devicedata['ActivePowerL2'],
                ActivePowerL3=devicedata['ActivePowerL3'],
                Voltage=devicedata['Voltage'],
                VoltageL1=devicedata['VoltageL1'],
                VoltageL2=devicedata['VoltageL2'],
                VoltageL3=devicedata['VoltageL3'],
                CounterReading=devicedata['CounterReading'],
                CounterReadingImport=devicedata['CounterReadingImport'],
                CounterReadingExport=devicedata['CounterReadingExport']
            )
        except APIAuthError as err:
            _LOGGER.error(err)
            raise UpdateFailed(err) from err
        except Exception as err:
            # This will show entities as unavailable by raising UpdateFailed exception
            raise UpdateFailed(f"Error communicating with API: {err}") from err
