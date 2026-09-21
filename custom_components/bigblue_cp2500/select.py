from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

OPTIONS = ["400 W", "800 W", "1200 W"]
OPTION_TO_WATTS = {
    "400 W": 400,
    "800 W": 800,
    "1200 W": 1200,
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BigBlueAcChargingPowerSelect(coordinator, entry)])


class BigBlueAcChargingPowerSelect(CoordinatorEntity, SelectEntity):
    _attr_has_entity_name = True
    _attr_name = "AC Charging Power Limit"
    _attr_icon = "mdi:transmission-tower-import"
    _attr_options = OPTIONS

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.data['address']}_ac_charging_power_limit"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": "BigBlue CP2500",
            "manufacturer": "BigBlue",
            "model": "CP2500",
        }

    @property
    def current_option(self):
        watts = self.coordinator.ac_charging_power
        return f"{watts} W" if watts in (400, 800, 1200) else None

    async def async_select_option(self, option: str) -> None:
        watts = OPTION_TO_WATTS[option]
        await self.coordinator.async_set_ac_charging_power(watts)
        self.async_write_ha_state()
