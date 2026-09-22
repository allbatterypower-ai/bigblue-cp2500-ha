from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS

from .const import (
    AUTO_LOG_INTERVAL_OPTIONS,
    DEFAULT_ADDRESS,
    DEFAULT_AUTO_LOG_INTERVAL,
    DEFAULT_AUTO_LOG_MIN_SOC,
    DEFAULT_AUTO_LOG_ONLY_AC_CONNECTED,
    DOMAIN,
)

DEFAULT_GITHUB_REPO = "allbatterypower-ai/bigblue-cp2500-logs"


class BigBlueConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            address = user_input[CONF_ADDRESS].upper()
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"BigBlue CP2500 {address}",
                data={"address": address},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_ADDRESS, default=DEFAULT_ADDRESS): str}
            ),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return BigBlueOptionsFlow()


class BigBlueOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "github_repo",
                        default=self.config_entry.options.get(
                            "github_repo", DEFAULT_GITHUB_REPO
                        ),
                    ): str,
                    vol.Optional(
                        "github_token",
                        default=self.config_entry.options.get(
                            "github_token", ""
                        ),
                    ): str,
                    vol.Optional(
                        "auto_log_interval",
                        default=self.config_entry.options.get(
                            "auto_log_interval", DEFAULT_AUTO_LOG_INTERVAL
                        ),
                    ): vol.In(AUTO_LOG_INTERVAL_OPTIONS),
                    vol.Optional(
                        "auto_log_min_soc",
                        default=self.config_entry.options.get(
                            "auto_log_min_soc", DEFAULT_AUTO_LOG_MIN_SOC
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                    vol.Optional(
                        "auto_log_only_ac_connected",
                        default=self.config_entry.options.get(
                            "auto_log_only_ac_connected",
                            DEFAULT_AUTO_LOG_ONLY_AC_CONNECTED,
                        ),
                    ): bool,
                }
            ),
        )
