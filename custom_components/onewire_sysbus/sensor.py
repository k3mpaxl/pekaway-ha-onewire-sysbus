"""1-Wire SysBus temperature sensors."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import OneWireConfigEntry, OneWireCoordinator

_LOGGER = logging.getLogger(__name__)

# Pure reads — parallel updates safe.
PARALLEL_UPDATES = 0

TEMPERATURE_DESCRIPTION = SensorEntityDescription(
    key="temperature",
    translation_key="temperature",
    device_class=SensorDeviceClass.TEMPERATURE,
    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    state_class=SensorStateClass.MEASUREMENT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OneWireConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up 1-Wire sensors from a config entry."""
    data = entry.runtime_data
    coordinator = data.coordinator
    hub = data.hub

    entities: list[OneWireSensor] = []
    if hub.devices:
        for device in hub.devices:
            device_id = next(iter(device.device_info["identifiers"]))[1]
            entities.append(
                OneWireSensor(
                    coordinator=coordinator,
                    device_id=device_id,
                    device_info=device.device_info,
                )
            )
    async_add_entities(entities)


class OneWireSensor(CoordinatorEntity[OneWireCoordinator], SensorEntity):
    """1-Wire temperature sensor driven by the coordinator."""

    _attr_has_entity_name = True
    entity_description = TEMPERATURE_DESCRIPTION

    def __init__(
        self,
        coordinator: OneWireCoordinator,
        device_id: str,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_temperature"
        self._attr_device_info = device_info

    @property
    def available(self) -> bool:
        """Sensor available when coordinator has a reading for this device."""
        if not super().available or self.coordinator.data is None:
            return False
        return self.coordinator.data.get(self._device_id) is not None

    @property
    def native_value(self) -> float | None:
        """Return the current temperature reading."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._device_id)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return extra state attributes."""
        return {
            "device_file": f"/sys/bus/w1/devices/{self._device_id}/w1_slave",
        }
