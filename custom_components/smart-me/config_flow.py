import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth

from .const import DOMAIN

class SmartmeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._session = async_get_clientsession(self.hass)
        self._username: None = None
        self._password: None = None
        self._deviceid:  None = None
        self._discovered_devices: dict[str, str] = {}
  
    async def async_step_user(self, formdata):
        if formdata is not None:
            self._username = formdata['username']
            self._password = formdata['password']
            try:
                async with self._session.get(url="https://api.smart-me.com/Devices", auth=BasicAuth(self._username, self._password)) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    for device in response_data:
                         self._discovered_devices[device.Id] = device.Name
            except ClientResponseError as exc:
                return self.async_abort(reason="authentication")
            except ClientError as exc:
                return self.async_abort(reason="connenction")

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
              vol.Required("username"): str,
              vol.Required("password"): str
            })
        )
  
    async def async_step_device(self, formdata):
        if formdata is not None:
            return self.async_abort(reason="unknown")

        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema(
                {vol.Required("deviceid"): vol.In(self._discovered_devices)}
            ),
        )
