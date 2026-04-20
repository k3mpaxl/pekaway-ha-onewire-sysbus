"""Diagnostics for the 1-Wire SysBus integration."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from .coordinator import OneWireConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: OneWireConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = entry.runtime_data
    hub = data.hub
    coordinator = data.coordinator

    return {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "update_interval_seconds": (
                coordinator.update_interval.total_seconds()
                if coordinator.update_interval
                else None
            ),
            "data": coordinator.data or {},
        },
        "devices": (
            [
                {
                    "identifiers": [list(t) for t in d.device_info["identifiers"]],
                    "manufacturer": d.device_info.get("manufacturer"),
                    "model": d.device_info.get("model"),
                    "name": d.device_info.get("name"),
                }
                for d in hub.devices
            ]
            if hub.devices
            else []
        ),
    }
