# BigBlue CP2500 BLE for Home Assistant

Experimental local Bluetooth integration for the BigBlue CP2500 portable power station.

## Features
- State of Charge (SOC)
- State of Health (SOH)
- Battery voltage/current/power
- Surplus and total capacity
- Battery temperature
- AC input power, voltage, current, frequency and temperature
- DC output power, voltage and current
- AC output temperature
- DC temperature
- 16 cell voltages
- Minimum/maximum cell voltage and cell delta
- Downloadable diagnostics with the latest raw BLE telemetry frame
- One-tap raw BLE dump button for the Home Assistant log
- Upload BLE snapshot directly to a private GitHub repository

## Installation with HACS
1. Add this repository to HACS as a Custom Repository.
2. Category: Integration.
3. Download/install the integration from HACS.
4. Restart Home Assistant.
5. Go to Settings -> Devices & services -> Add integration.
6. Search for **BigBlue CP2500 BLE**.
7. Enter the Bluetooth MAC address of the power station.

## Tested device
- BigBlue CP2500
- BLE telemetry request via FFE9
- Notifications via FFE4

## Version 0.3.7
- Added confirmed DC Output Power, Voltage and Current sensors.
- DC output mapping was validated against a live 40 W / 24 V / 1.6 A test and a prior 0 W state.

## Version 0.3.6
- Added confirmed AC Input Power, Voltage, Current and Frequency sensors.
- AC input field mappings were validated against two charging levels (~400 W and ~800 W).
- Updated uploaded snapshot and diagnostics version markers.

## Version 0.3.5
- Fixed the Home Assistant 2026.x options flow crash (500 Internal Server Error).
- Updated the diagnostics version marker.

## Version 0.3.4
- Added **Upload BLE Snapshot to GitHub** button.
- GitHub repository and fine-grained token are configured in the integration options.
- Each button press uploads one timestamped JSON snapshot to the private log repository.
- The token is not written to diagnostics or logs.

## Version 0.3.3
- Added a **Dump Raw BLE to Log** button entity.
- Pressing the button writes the latest 236-byte BLE frame and parsed values to the Home Assistant log.
- This makes reverse engineering new fields possible directly from the phone without downloading diagnostics.

## Version 0.3.2
- Reassembles telemetry when a 236-byte BLE response is split across multiple notifications.
- Adds Home Assistant diagnostics containing the latest raw BLE frame and notification chunks.
- Improves warning details when a complete telemetry frame is not received.

## Version 0.3.1
- Renamed the two previously auxiliary temperature sensors to AC Input Temperature and AC Output Temperature.
- Added DC Temperature.
- Temperature mappings were matched against values shown on the CP2500 display.

This integration is reverse engineered and experimental.
