from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class SmartmeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
  
    async def async_step_user(self, info):
        if info is not None:
            return self.async_abort(reason="test")
            pass  # TODO: process info

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
              vol.Required("username"): str,
              vol.Required("password"): str,
              vol.Required("deviceid"): str
            })
        )
