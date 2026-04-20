"""Config flow for the 1-Wire SysBus integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant

from .const import CONF_MOUNT_DIR, DEFAULT_SYSBUS_MOUNT_DIR, DOMAIN
from .onewirehub import InvalidPath, OneWireHub

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MOUNT_DIR, default=DEFAULT_SYSBUS_MOUNT_DIR): str,
    }
)


async def _validate_mount_dir(hass: HomeAssistant, mount_dir: str) -> None:
    """Validate that the configured path is a valid 1-Wire SysBus mount."""
    hub = OneWireHub(hass)
    await hub.check_mount_dir(mount_dir)


class OneWireConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 1-Wire SysBus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_MOUNT_DIR])
            self._abort_if_unique_id_configured()

            try:
                await _validate_mount_dir(self.hass, user_input[CONF_MOUNT_DIR])
            except InvalidPath:
                errors["base"] = "invalid_path"
            except Exception:
                _LOGGER.exception("Unexpected error validating mount dir")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_MOUNT_DIR], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Allow reconfiguring the mount directory."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_MOUNT_DIR])
            self._abort_if_unique_id_mismatch(reason="mount_dir_mismatch")

            try:
                await _validate_mount_dir(self.hass, user_input[CONF_MOUNT_DIR])
            except InvalidPath:
                errors["base"] = "invalid_path"
            except Exception:
                _LOGGER.exception("Unexpected error validating mount dir")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    entry, data_updates=user_input
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MOUNT_DIR,
                        default=entry.data.get(CONF_MOUNT_DIR, DEFAULT_SYSBUS_MOUNT_DIR),
                    ): str,
                }
            ),
            errors=errors,
        )
