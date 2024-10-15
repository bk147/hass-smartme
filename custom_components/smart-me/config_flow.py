import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth

from .const import DOMAIN

class SmartmeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
  
    async def async_step_user(self, userdata):
        if userdata is not None:
            websession = async_get_clientsession(self.hass)
            username = userdata['username']
            password = userdata['password']
            try:
                async with websession.get(url="https://api.smart-me.com/Devices", auth=BasicAuth(username, password)) as response:
                    response.raise_for_status()
                    print(response.json())
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
