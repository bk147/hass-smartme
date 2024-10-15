import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth

from .const import DOMAIN

class SmartmeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._username: None = None
        self._password: None = None
        self._discovered_devices: dict[str, str] = {}
        self._data: dict[str, Any] = {}
  
    async def async_step_user(self, formdata):
        if formdata is not None:
            websession = async_get_clientsession(self.hass)
            self._username = formdata['username']
            self._password = formdata['password']
            try:
                async with websession.get(url="https://api.smart-me.com/Devices", auth=BasicAuth(self._username, self._password)) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    for device in response_data:
                        device_id = device['Id']
                        device_name = device['Name']
                        self._discovered_devices[device_id] = device_name
                    return await self.async_step_device(None)
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
            deviceid = formdata['deviceid']
            await self.async_set_unique_id(deviceid, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            self._data['devicename'] = self._discovered_devices[deviceid];
            self._data['username'] = self._username
            self._data['password'] = self._password
            return self.async_create_entry(title=self._discovered_devices[deviceid], data=self._data)

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")
        
        return self.async_show_form(
            step_id="device", data_schema=vol.Schema(
                {vol.Required("deviceid"): vol.In(self._discovered_devices)}
            ),
        )
