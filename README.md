# BigBlue CP2500 BLE для Home Assistant

Експериментальна локальна Bluetooth-інтеграція для портативної зарядної станції **BigBlue CP2500**.

> Інтеграція створена методом reverse engineering. Частина полів уже підтверджена тестами на реальному пристрої, інші будуть додаватися поступово після перевірки.

## Українська

### Можливості

- State of Charge (SOC)
- State of Health (SOH)
- Напруга, струм і потужність акумулятора
- Залишкова та повна ємність
- Температура акумулятора
- AC Input: потужність, напруга, струм, частота, температура
- DC Output: потужність, напруга, струм
- AC Output Temperature
- DC Temperature
- Напруги 16 комірок
- Мінімальна/максимальна напруга комірок та delta
- Завантажувана діагностика з останнім raw BLE frame
- Кнопка **Dump Raw BLE to Log**
- Кнопка **Upload BLE Snapshot to GitHub** для приватного журналу вимірювань
- Керування **AC Charging Power Limit**: 400 W / 800 W / 1200 W

### Встановлення через HACS

1. Додайте цей репозиторій у HACS як **Custom Repository**.
2. Категорія: **Integration**.
3. Завантажте інтеграцію.
4. Перезапустіть Home Assistant.
5. Відкрийте **Налаштування → Пристрої та служби → Додати інтеграцію**.
6. Знайдіть **BigBlue CP2500 BLE**.
7. Введіть Bluetooth MAC-адресу станції.

### GitHub-журнал BLE snapshot

У параметрах інтеграції можна вказати приватний GitHub-репозиторій та fine-grained token з правом **Contents: Read and write** тільки для цього репозиторію.

Після натискання **Upload BLE Snapshot to GitHub** інтеграція створює окремий JSON-файл із:
- часом;
- розібраними значеннями;
- повним 236-байтовим BLE frame;
- отриманими notification chunks.

### Документація

- [Історія змін / Changelog](CHANGELOG.md)
- [Карта BLE-протоколу](docs/protocol.md)
- [Нотатки reverse engineering](docs/reverse-engineering.md)

---

## English

Experimental local Bluetooth integration for the **BigBlue CP2500** portable power station.

### Features

- State of Charge (SOC)
- State of Health (SOH)
- Battery voltage/current/power
- Surplus and total capacity
- Battery temperature
- AC Input power, voltage, current, frequency and temperature
- DC Output power, voltage and current
- AC Output temperature
- DC temperature
- 16 cell voltages
- Minimum/maximum cell voltage and cell delta
- Downloadable diagnostics with the latest raw BLE telemetry frame
- One-tap **Dump Raw BLE to Log** button
- **Upload BLE Snapshot to GitHub** button for private telemetry logging
- **AC Charging Power Limit** control: 400 W / 800 W / 1200 W

### Installation with HACS

1. Add this repository to HACS as a **Custom Repository**.
2. Category: **Integration**.
3. Download/install the integration.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Search for **BigBlue CP2500 BLE**.
7. Enter the Bluetooth MAC address of the power station.

### Documentation

- [Changelog / Історія змін](CHANGELOG.md)
- [BLE protocol map](docs/protocol.md)
- [Reverse engineering notes](docs/reverse-engineering.md)

## Tested device

- BigBlue CP2500
- Telemetry request via FFE9
- Notifications via FFE4
- Main telemetry frame: 236 bytes
- Secondary notification observed: 32 bytes

Current integration version: **0.3.17**
