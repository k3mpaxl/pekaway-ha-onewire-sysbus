"""The 1-Wire SysBus integration."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import PLATFORMS
from .coordinator import OneWireConfigEntry, OneWireCoordinator, OneWireData
from .onewirehub import InvalidPath, OneWireHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: OneWireConfigEntry) -> bool:
    """Set up a 1-Wire hub for a config entry."""
    hub = OneWireHub(hass)
    try:
        await hub.initialize(entry)
    except InvalidPath as err:
        raise ConfigEntryNotReady(f"1-Wire mount dir invalid: {err}") from err

    coordinator = OneWireCoordinator(hass, entry, hub)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = OneWireData(hub=hub, coordinator=coordinator)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: OneWireConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: OneWireConfigEntry) -> None:
    """Reload entry after options/config change."""
    await hass.config_entries.async_reload(entry.entry_id)
