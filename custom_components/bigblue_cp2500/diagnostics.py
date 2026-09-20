from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    return {
        "integration_version": "0.3.5",
        "parsed_data": coordinator.data,
        "raw_main_frame_hex": (
            coordinator.last_raw_main_frame.hex(" ")
            if coordinator.last_raw_main_frame
            else None
        ),
        "raw_notification_lengths": [
            len(chunk) for chunk in coordinator.last_raw_notifications
        ],
        "raw_notifications_hex": [
            chunk.hex(" ") for chunk in coordinator.last_raw_notifications
        ],
    }
