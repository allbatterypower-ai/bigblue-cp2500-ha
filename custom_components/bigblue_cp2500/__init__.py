from __future__ import annotations

import asyncio
import logging

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, FFE4_UUID, FFE9_UUID, TELEMETRY_REQUEST, POLL_INTERVAL

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "button"]
_MAIN_HEADER = bytes.fromhex("10 01 00 01 00 fa 15 06")
_MAIN_FRAME_LENGTH = 236


def _u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little", signed=False)


def _s16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little", signed=True)


def parse_telemetry(data: bytes) -> dict:
    if len(data) < _MAIN_FRAME_LENGTH:
        raise ValueError(f"Telemetry frame too short: {len(data)} bytes")

    if data[:8] != _MAIN_HEADER:
        raise ValueError(f"Unexpected telemetry header: {data[:8].hex(' ')}")

    cells_mv = [_u16(data, 84 + i * 2) for i in range(16)]

    battery_voltage = _u16(data, 136) / 100.0
    battery_current = _s16(data, 134) / 100.0
    surplus_capacity = _u16(data, 138) / 100.0
    total_capacity = _u16(data, 142) / 100.0
    cell_count = _u16(data, 144)

    soh = data[146]
    soc = data[147]

    # Temperature fields mapped against the station display.
    ac_input_temperature = _s16(data, 56)
    battery_temperature = _s16(data, 58)
    ac_output_temperature = _s16(data, 60)
    dc_temperature = _s16(data, 210)

    result = {
        "soc": soc,
        "soh": soh,
        "battery_voltage": round(battery_voltage, 2),
        "battery_current": round(battery_current, 2),
        "battery_power": round(battery_voltage * battery_current, 1),
        "surplus_capacity": round(surplus_capacity, 2),
        "total_capacity": round(total_capacity, 2),
        "cell_count": cell_count,
        "battery_temperature": battery_temperature,
        "aux_temperature_1": ac_input_temperature,
        "aux_temperature_2": ac_output_temperature,
        "dc_temperature": dc_temperature,
        "cell_min": round(min(cells_mv) / 1000.0, 3),
        "cell_max": round(max(cells_mv) / 1000.0, 3),
        "cell_delta": round((max(cells_mv) - min(cells_mv)) / 1000.0, 3),
    }

    for i, mv in enumerate(cells_mv, start=1):
        result[f"cell_{i}"] = round(mv / 1000.0, 3)

    return result


class BigBlueCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, address: str):
        super().__init__(hass, _LOGGER, name=f"BigBlue CP2500 {address}")
        self.address = address
        self._client: BleakClient | None = None
        self._task: asyncio.Task | None = None
        self._stopping = False
        self.data = {}
        self.last_raw_main_frame: bytes | None = None
        self.last_raw_notifications: list[bytes] = []

    async def async_start(self) -> None:
        self._stopping = False
        self._task = asyncio.create_task(self._run())

    async def async_stop(self) -> None:
        self._stopping = True
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        if self._client and self._client.is_connected:
            try:
                await self._client.disconnect()
            except Exception:
                pass
        self._client = None

    async def _run(self) -> None:
        while not self._stopping:
            try:
                ble_device = bluetooth.async_ble_device_from_address(
                    self.hass, self.address, connectable=True
                )

                if ble_device is None:
                    _LOGGER.warning(
                        "BigBlue %s has not been discovered by Home Assistant Bluetooth yet; retrying",
                        self.address,
                    )
                    await asyncio.sleep(10)
                    continue

                self._client = await establish_connection(
                    BleakClient,
                    ble_device,
                    self.address,
                    max_attempts=3,
                )

                chunks: list[bytes] = []

                def notification_callback(_sender, payload: bytearray) -> None:
                    chunks.append(bytes(payload))

                await self._client.start_notify(FFE4_UUID, notification_callback)

                while self._client.is_connected and not self._stopping:
                    chunks.clear()
                    await self._client.write_gatt_char(
                        FFE9_UUID,
                        TELEMETRY_REQUEST,
                        response=False,
                    )

                    main_frame = None
                    for _ in range(30):
                        await asyncio.sleep(0.1)

                        # BLE stacks may deliver the 236-byte response in one
                        # notification or split it across several notifications.
                        combined = b"".join(chunks)
                        start = combined.find(_MAIN_HEADER)
                        if (
                            start >= 0
                            and len(combined) >= start + _MAIN_FRAME_LENGTH
                        ):
                            main_frame = combined[
                                start:start + _MAIN_FRAME_LENGTH
                            ]
                            break

                    self.last_raw_notifications = list(chunks)

                    if main_frame is None:
                        _LOGGER.warning(
                            "BigBlue %s returned no complete main telemetry frame after request "
                            "(notifications=%s, total_bytes=%d)",
                            self.address,
                            [len(chunk) for chunk in chunks],
                            sum(len(chunk) for chunk in chunks),
                        )
                    else:
                        self.last_raw_main_frame = main_frame
                        self.async_set_updated_data(parse_telemetry(main_frame))

                    await asyncio.sleep(POLL_INTERVAL)

            except asyncio.CancelledError:
                raise
            except Exception as err:
                _LOGGER.warning("BigBlue %s BLE loop error: %s", self.address, err)
                self.async_set_update_error(err)
                if self._client and self._client.is_connected:
                    try:
                        await self._client.disconnect()
                    except Exception:
                        pass
                self._client = None
                await asyncio.sleep(10)


    async def async_dump_raw_to_log(self) -> None:
        """Write the latest raw BLE telemetry to the Home Assistant log."""
        if self.last_raw_main_frame is None:
            _LOGGER.warning(
                "BIGBLUE RAW DUMP %s: no complete main frame is available yet; "
                "notification_lengths=%s",
                self.address,
                [len(chunk) for chunk in self.last_raw_notifications],
            )
            if self.last_raw_notifications:
                _LOGGER.warning(
                    "BIGBLUE RAW NOTIFICATIONS %s: %s",
                    self.address,
                    " | ".join(
                        chunk.hex(" ") for chunk in self.last_raw_notifications
                    ),
                )
            return

        _LOGGER.warning(
            "BIGBLUE RAW MAIN FRAME %s (%d bytes): %s",
            self.address,
            len(self.last_raw_main_frame),
            self.last_raw_main_frame.hex(" "),
        )

        _LOGGER.warning(
            "BIGBLUE PARSED DATA %s: %s",
            self.address,
            self.data,
        )

        if self.last_raw_notifications:
            _LOGGER.warning(
                "BIGBLUE RAW NOTIFICATION LENGTHS %s: %s",
                self.address,
                [len(chunk) for chunk in self.last_raw_notifications],
            )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = BigBlueCoordinator(hass, entry.data["address"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await coordinator.async_start()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_stop()
    return unload_ok
