from __future__ import annotations

import asyncio
import base64
import json
import logging

from bleak import BleakClient
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import DOMAIN, FFE4_UUID, FFE9_UUID, TELEMETRY_REQUEST, POLL_INTERVAL

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "button", "select"]
_MAIN_HEADER = bytes.fromhex("10 01 00 01 00 fa 15 06")
_MAIN_FRAME_LENGTH = 236

# Confirmed from the official BigBlue Energy app HCI capture.
_AC_CHARGING_POWER_COMMANDS = {
    400: bytes.fromhex("10 01 00 01 00 04 16 31 00 00 00 00 00 00 00 00 00 91 00 00"),
    800: bytes.fromhex("10 01 00 01 00 04 16 31 00 00 00 00 00 00 00 00 00 23 00 00"),
    1200: bytes.fromhex("10 01 00 01 00 04 16 31 00 00 00 00 00 00 00 00 00 b4 00 00"),
}


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

    ac_input_voltage = _u16(data, 28) / 10.0
    ac_input_frequency = _u16(data, 40) / 100.0
    ac_input_current = _u16(data, 44) / 10.0
    ac_input_power = _u16(data, 50)

    dc_output_voltage = _u16(data, 74) / 10.0
    dc_output_current = _u16(data, 76) / 10.0
    dc_output_power = _u16(data, 78)

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
        "ac_input_power": ac_input_power,
        "ac_input_voltage": round(ac_input_voltage, 1),
        "ac_input_current": round(ac_input_current, 1),
        "ac_input_frequency": round(ac_input_frequency, 2),
        "dc_output_power": dc_output_power,
        "dc_output_voltage": round(dc_output_voltage, 1),
        "dc_output_current": round(dc_output_current, 1),
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
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        address = entry.data["address"]
        super().__init__(hass, _LOGGER, name=f"BigBlue CP2500 {address}")
        self.entry = entry
        self.address = address
        self._client: BleakClient | None = None
        self._task: asyncio.Task | None = None
        self._stopping = False
        self._ble_write_lock = asyncio.Lock()
        self._control_ack_event = asyncio.Event()
        self.data = {}
        self.last_raw_main_frame: bytes | None = None
        self.last_raw_notifications: list[bytes] = []
        self.ac_charging_power: int | None = None

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

    async def async_set_ac_charging_power(self, watts: int) -> None:
        """Set the AC charging power limit using the command captured from the official app."""
        command = _AC_CHARGING_POWER_COMMANDS.get(watts)
        if command is None:
            raise ValueError(f"Unsupported AC charging power: {watts} W")

        client = self._client
        if client is None or not client.is_connected:
            raise RuntimeError("BigBlue CP2500 is not connected over Bluetooth")

        async with self._ble_write_lock:
            self._control_ack_event.clear()
            await client.write_gatt_char(
                FFE9_UUID,
                command,
                response=False,
            )
            try:
                await asyncio.wait_for(self._control_ack_event.wait(), timeout=2.0)
            except TimeoutError as err:
                raise RuntimeError(
                    f"BigBlue CP2500 did not acknowledge AC charging power {watts} W"
                ) from err

        self.ac_charging_power = watts
        self.async_update_listeners()
        _LOGGER.info(
            "BigBlue %s AC charging power set to %d W and acknowledged",
            self.address,
            watts,
        )

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
                    packet = bytes(payload)
                    chunks.append(packet)
                    if (
                        len(packet) >= 8
                        and packet[:6] == bytes.fromhex("10 01 00 01 00 04")
                        and packet[6:8] == bytes.fromhex("16 32")
                    ):
                        self._control_ack_event.set()

                await self._client.start_notify(FFE4_UUID, notification_callback)

                while self._client.is_connected and not self._stopping:
                    main_frame = None
                    async with self._ble_write_lock:
                        chunks.clear()
                        await self._client.write_gatt_char(
                            FFE9_UUID,
                            TELEMETRY_REQUEST,
                            response=False,
                        )

                        for _ in range(30):
                            await asyncio.sleep(0.1)

                            combined = b"".join(chunks)
                            start = combined.find(_MAIN_HEADER)
                            if start >= 0 and len(combined) >= start + _MAIN_FRAME_LENGTH:
                                main_frame = combined[start:start + _MAIN_FRAME_LENGTH]
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
                    " | ".join(chunk.hex(" ") for chunk in self.last_raw_notifications),
                )
            return

        _LOGGER.warning(
            "BIGBLUE RAW MAIN FRAME %s (%d bytes): %s",
            self.address,
            len(self.last_raw_main_frame),
            self.last_raw_main_frame.hex(" "),
        )
        _LOGGER.warning("BIGBLUE PARSED DATA %s: %s", self.address, self.data)

        if self.last_raw_notifications:
            _LOGGER.warning(
                "BIGBLUE RAW NOTIFICATION LENGTHS %s: %s",
                self.address,
                [len(chunk) for chunk in self.last_raw_notifications],
            )

    async def async_upload_snapshot_to_github(self) -> str:
        """Upload the latest BLE snapshot to a configured private GitHub repo."""
        github_token = self.entry.options.get("github_token")
        github_repo = self.entry.options.get(
            "github_repo", "allbatterypower-ai/bigblue-cp2500-logs"
        )

        if not github_token:
            raise RuntimeError(
                "GitHub upload is not configured. Open the integration options "
                "and add a fine-grained GitHub token."
            )

        if self.last_raw_main_frame is None:
            raise RuntimeError(
                "No complete BLE telemetry frame is available yet. "
                "Wait for live sensor data and try again."
            )

        now = dt_util.now()
        timestamp = now.isoformat()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3] + ".json"
        path = now.strftime("logs/%Y/%m/%d/") + filename

        payload = {
            "timestamp": timestamp,
            "integration_version": "0.3.15",
            "device": {
                "name": "BigBlue CP2500",
                "address": self.address,
            },
            "parsed_data": self.data,
            "raw_main_frame_hex": self.last_raw_main_frame.hex(" "),
            "raw_notification_lengths": [
                len(chunk) for chunk in self.last_raw_notifications
            ],
            "raw_notifications_hex": [
                chunk.hex(" ") for chunk in self.last_raw_notifications
            ],
        }

        encoded = base64.b64encode(
            json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("ascii")

        url = f"https://api.github.com/repos/{github_repo}/contents/{path}"
        session = async_get_clientsession(self.hass)
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        body = {
            "message": f"Add BigBlue BLE snapshot {timestamp}",
            "content": encoded,
        }

        async with session.put(url, headers=headers, json=body) as response:
            response_text = await response.text()
            if response.status not in (200, 201):
                raise RuntimeError(
                    f"GitHub upload failed with HTTP {response.status}: "
                    f"{response_text[:300]}"
                )
            response_json = json.loads(response_text)

        html_url = response_json.get("content", {}).get("html_url")
        if not html_url:
            html_url = f"https://github.com/{github_repo}/blob/main/{path}"

        _LOGGER.warning(
            "BIGBLUE SNAPSHOT UPLOADED %s: %s",
            self.address,
            html_url,
        )
        return html_url


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = BigBlueCoordinator(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await coordinator.async_start()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_stop()
    return unload_ok
