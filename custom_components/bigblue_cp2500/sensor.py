from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


@dataclass(frozen=True)
class SensorDef:
    key: str
    name: str
    unit: str | None = None
    device_class: SensorDeviceClass | None = None
    precision: int | None = None


SENSORS = [
    SensorDef("soc", "State of Charge", PERCENTAGE, SensorDeviceClass.BATTERY, 0),
    SensorDef("soh", "State of Health", PERCENTAGE, None, 0),
    SensorDef("battery_voltage", "Battery Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, 2),
    SensorDef("battery_current", "Battery Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, 2),
    SensorDef("battery_power", "Battery Power", UnitOfPower.WATT, SensorDeviceClass.POWER, 1),
    SensorDef("surplus_capacity", "Surplus Capacity", "Ah", None, 2),
    SensorDef("total_capacity", "Total Capacity", "Ah", None, 2),
    SensorDef("battery_temperature", "Battery Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 1),
    SensorDef("aux_temperature_1", "AC Input Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 1),
    SensorDef("aux_temperature_2", "AC Output Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 1),
    SensorDef("dc_temperature", "DC Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 1),
    SensorDef("cell_min", "Minimum Cell Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, 3),
    SensorDef("cell_max", "Maximum Cell Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, 3),
    SensorDef("cell_delta", "Cell Delta", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, 3),
]

SENSORS += [
    SensorDef(f"cell_{i}", f"Cell {i} Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, 3)
    for i in range(1, 17)
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [BigBlueSensor(coordinator, entry, description) for description in SENSORS]
    )


class BigBlueSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, description: SensorDef):
        super().__init__(coordinator)
        self.description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{entry.data['address']}_{description.key}"
        self._attr_native_unit_of_measurement = description.unit
        self._attr_device_class = description.device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = description.precision
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": "BigBlue CP2500",
            "manufacturer": "BigBlue",
            "model": "CP2500",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get(self.description.key)

    @property
    def available(self):
        return (
            self.coordinator.last_update_success
            and self.description.key in self.coordinator.data
        )
