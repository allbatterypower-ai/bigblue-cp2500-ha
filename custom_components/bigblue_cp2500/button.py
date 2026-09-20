from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BigBlueRawDumpButton(coordinator, entry)])


class BigBlueRawDumpButton(CoordinatorEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "Dump Raw BLE to Log"
    _attr_icon = "mdi:bug"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['address']}_dump_raw_ble"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": "BigBlue CP2500",
            "manufacturer": "BigBlue",
            "model": "CP2500",
        }

    async def async_press(self) -> None:
        await self.coordinator.async_dump_raw_to_log()
