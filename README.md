# BigBlue CP2500 BLE for Home Assistant

Experimental local Bluetooth integration for the BigBlue CP2500 portable power station.

## Features
- State of Charge (SOC)
- State of Health (SOH)
- Battery voltage/current/power
- Surplus and total capacity
- Battery temperature
- AC input temperature
- AC output temperature
- DC temperature
- 16 cell voltages
- Minimum/maximum cell voltage and cell delta

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

## Version 0.3.1
- Renamed the two previously auxiliary temperature sensors to AC Input Temperature and AC Output Temperature.
- Added DC Temperature.
- Temperature mappings were matched against values shown on the CP2500 display.

This integration is reverse engineered and experimental.
