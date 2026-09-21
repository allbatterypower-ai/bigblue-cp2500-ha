# Історія змін / Changelog

## v0.3.11

### Українська
- Перероблено логотип інтеграції під горизонтальний слот Home Assistant.
- Додано окремі світлий і темний варіанти логотипа з прозорим фоном.
- Прибрано старі `logo@2x.png` / `dark_logo@2x.png`, щоб Home Assistant не підхоплював попередні квадратні файли.
- Оновлено маркер версії в GitHub BLE snapshot та README.

### English
- Reworked the integration logo for Home Assistant's horizontal branding slot.
- Added separate light and dark transparent logo variants.
- Removed the old `logo@2x.png` / `dark_logo@2x.png` files so Home Assistant does not select the previous square assets.
- Updated the GitHub BLE snapshot version marker and README.

## v0.3.10

### Українська
- Виправлено відображення branding у Home Assistant: замість невдалого широкого logo використовується перевірена квадратна офіційна іконка BigBlue.
- Оновлено `logo.png`, `logo@2x.png`, `dark_logo.png` та `dark_logo@2x.png`.

### English
- Fixed Home Assistant branding display: replaced the broken wide logo with the verified square official BigBlue app icon.
- Updated `logo.png`, `logo@2x.png`, `dark_logo.png`, and `dark_logo@2x.png`.

## v0.3.9

### Українська
- Додано повний логотип BigBlue для сторінки інтеграції Home Assistant.
- Додано окремий `dark_logo.png` для темної теми.

### English
- Added the full BigBlue logo for the Home Assistant integration page.
- Added a separate `dark_logo.png` for dark mode.

## v0.3.8

### Українська
- Додано офіційну іконку BigBlue для сторінки користувацької інтеграції в Home Assistant.
- Додано локальні brand assets: `brand/icon.png` (256×256) та `brand/icon@2x.png` (512×512).

### English
- Added the official BigBlue icon for the custom integration page in Home Assistant.
- Added local brand assets: `brand/icon.png` (256×256) and `brand/icon@2x.png` (512×512).

## v0.3.7

### Українська
- Додано підтверджені сенсори **DC Output Power**, **DC Output Voltage**, **DC Output Current**.
- Мапінг DC Output перевірено при реальному навантаженні приблизно **40 W / 24 V / 1.6 A** та у стані 0 W.

### English
- Added confirmed **DC Output Power**, **DC Output Voltage**, and **DC Output Current** sensors.
- DC Output mapping validated against a live approximately **40 W / 24 V / 1.6 A** test and a previous 0 W state.

## v0.3.6

### Українська
- Додано **AC Input Power**, **AC Input Voltage**, **AC Input Current**, **AC Input Frequency**.
- Мапінг перевірено при двох рівнях заряджання: приблизно **400 W** та **800 W**.
- Оновлено version marker у diagnostics та GitHub snapshot.

### English
- Added **AC Input Power**, **AC Input Voltage**, **AC Input Current**, and **AC Input Frequency**.
- Field mappings validated at approximately **400 W** and **800 W** charging levels.
- Updated diagnostics and uploaded snapshot version markers.

## v0.3.5

### Українська
- Виправлено помилку **500 Internal Server Error** у Options Flow на Home Assistant 2026.x.
- Оновлено version marker у diagnostics.

### English
- Fixed the Home Assistant 2026.x Options Flow crash (**500 Internal Server Error**).
- Updated the diagnostics version marker.

## v0.3.4

### Українська
- Додано кнопку **Upload BLE Snapshot to GitHub**.
- GitHub repository та fine-grained token налаштовуються в Options інтеграції.
- Кожне натискання створює окремий timestamped JSON snapshot.
- Token не записується в diagnostics або log.

### English
- Added **Upload BLE Snapshot to GitHub**.
- GitHub repository and fine-grained token are configured in integration options.
- Each button press uploads one timestamped JSON snapshot.
- The token is not written to diagnostics or logs.

## v0.3.3

### Українська
- Додано кнопку **Dump Raw BLE to Log**.
- Кнопка виводить останній 236-байтовий BLE frame та parsed values у журнал Home Assistant.

### English
- Added **Dump Raw BLE to Log**.
- The button writes the latest 236-byte BLE frame and parsed values to the Home Assistant log.

## v0.3.2

### Українська
- Додано складання BLE frame з кількох notification chunks.
- Додано diagnostics із raw BLE frame.
- Покращено повідомлення про помилки при неповному telemetry frame.

### English
- Added reassembly when a 236-byte BLE response is split across multiple notifications.
- Added diagnostics containing the latest raw BLE frame.
- Improved warnings when a complete telemetry frame is not received.

## v0.3.1

### Українська
- Перейменовано auxiliary temperature sensors на **AC Input Temperature** та **AC Output Temperature**.
- Додано **DC Temperature**.
- Мапінг температур зіставлено з показами дисплея CP2500.

### English
- Renamed auxiliary temperature sensors to **AC Input Temperature** and **AC Output Temperature**.
- Added **DC Temperature**.
- Temperature mappings were matched against values shown on the CP2500 display.
