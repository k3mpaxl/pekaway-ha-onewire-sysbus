"""DataUpdateCoordinator for the 1-Wire SysBus integration."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta

from pi1wire import InvalidCRCException, UnsupportResponseException

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .onewirehub import OneWireHub

_LOGGER = logging.getLogger(__name__)


@dataclass
class OneWireData:
    """Runtime data for a 1-Wire config entry."""

    hub: OneWireHub
    coordinator: OneWireCoordinator


type OneWireConfigEntry = ConfigEntry[OneWireData]


class OneWireCoordinator(DataUpdateCoordinator[dict[str, float | None]]):
    """Poll all known 1-Wire sensors on an interval."""

    config_entry: OneWireConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: OneWireConfigEntry,
        hub: OneWireHub,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN}-{entry.entry_id}",
            update_interval=timedelta(seconds=30),
        )
        self.hub = hub

    async def _async_update_data(self) -> dict[str, float | None]:
        """Read all sensors once per cycle."""
        if self.hub.devices is None:
            raise UpdateFailed("Hub has no devices discovered yet")
        try:
            readings = await self.hass.async_add_executor_job(self._read_all)
        except OSError as err:
            raise UpdateFailed(f"SysBus read error: {err}") from err
        return readings

    def _read_all(self) -> dict[str, float | None]:
        """Blocking read of all registered 1-Wire sensors."""
        values: dict[str, float | None] = {}
        assert self.hub.devices is not None
        for device in self.hub.devices:
            device_id = device.device_info["identifiers"]
            # device_id is a set with one (DOMAIN, id) tuple
            key = next(iter(device_id))[1]
            try:
                values[key] = round(device.interface.get_temperature(), 1)
            except (
                FileNotFoundError,
                InvalidCRCException,
                UnsupportResponseException,
            ) as err:
                _LOGGER.debug(
                    "Read failed for %s: %s", key, err
                )
                values[key] = None
        return values
