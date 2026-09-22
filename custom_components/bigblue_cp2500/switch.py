from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            BigBlueAcOutputSwitch(coordinator, entry),
            BigBlueDcOutputSwitch(coordinator, entry),
        ]
    )


class BigBlueBaseSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": "BigBlue CP2500",
            "manufacturer": "BigBlue",
            "model": "CP2500",
        }


class BigBlueAcOutputSwitch(BigBlueBaseSwitch):
    _attr_name = "AC Output"
    _attr_icon = "mdi:power-socket-eu"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.data['address']}_ac_output"

    @property
    def is_on(self):
        return self.coordinator.ac_output_enabled

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_ac_output(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_ac_output(False)


class BigBlueDcOutputSwitch(BigBlueBaseSwitch):
    _attr_name = "DC Output"
    _attr_icon = "mdi:current-dc"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.data['address']}_dc_output"

    @property
    def is_on(self):
        return self.coordinator.dc_output_enabled

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_dc_output(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_dc_output(False)
