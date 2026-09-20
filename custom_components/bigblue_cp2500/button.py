from __future__ import annotations

import logging

from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            BigBlueRawDumpButton(coordinator, entry),
            BigBlueGitHubUploadButton(coordinator, entry),
        ]
    )


class BigBlueBaseButton(CoordinatorEntity, ButtonEntity):
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


class BigBlueRawDumpButton(BigBlueBaseButton):
    _attr_name = "Dump Raw BLE to Log"
    _attr_icon = "mdi:bug"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.data['address']}_dump_raw_ble"

    async def async_press(self) -> None:
        await self.coordinator.async_dump_raw_to_log()


class BigBlueGitHubUploadButton(BigBlueBaseButton):
    _attr_name = "Upload BLE Snapshot to GitHub"
    _attr_icon = "mdi:github"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.data['address']}_upload_ble_github"

    async def async_press(self) -> None:
        try:
            url = await self.coordinator.async_upload_snapshot_to_github()
        except Exception as err:
            _LOGGER.error("BigBlue GitHub snapshot upload failed: %s", err)
            persistent_notification.async_create(
                self.hass,
                f"BigBlue snapshot upload failed: {err}",
                title="BigBlue CP2500",
                notification_id="bigblue_cp2500_github_upload",
            )
            return

        persistent_notification.async_create(
            self.hass,
            f"BigBlue BLE snapshot uploaded successfully.\n\n{url}",
            title="BigBlue CP2500",
            notification_id="bigblue_cp2500_github_upload",
        )
