# Історія змін / Changelog

## v0.3.22

### Українська
- Повернуто погоджений горизонтальний логотип **BigBlue CP2500 BLE** для logo-слотів Home Assistant.
- Кругла синя іконка `icon.png` / `icon@2x.png` залишена без змін для списку інтеграцій.
- Для `logo.png` та `dark_logo.png` використано перевірені файли з v0.3.11.

### English
- Restored the approved horizontal **BigBlue CP2500 BLE** logo for Home Assistant logo slots.
- The circular blue `icon.png` / `icon@2x.png` remains unchanged for the integrations list.
- Reused the validated `logo.png` and `dark_logo.png` assets from v0.3.11.

## v0.3.21

### Українська
- Виправлено обрізання логотипа на сторінці інтеграції Home Assistant.
- Видалено окремі `logo.png` та `dark_logo.png`.
- Home Assistant тепер використовує квадратний `icon.png` як fallback для logo, що є рекомендованим варіантом, коли бренд використовує той самий знак для icon і logo.

### English
- Fixed the cropped logo on the Home Assistant integration details page.
- Removed separate `logo.png` and `dark_logo.png`.
- Home Assistant now falls back to the square `icon.png` for the logo, which is the recommended setup when the same artwork is used for both.

## v0.3.20

### Українська
- Виправлено branding на сторінці інтеграції Home Assistant.
- У списку інтеграцій кругла іконка вже відображалась правильно, але сторінка самої інтеграції використовувала окремі старі `logo.png` / `dark_logo.png`, через що логотип виглядав обрізаним.
- `logo.png` та `dark_logo.png` тепер використовують той самий погоджений круглий синій знак BigBlue.

### English
- Fixed branding on the Home Assistant integration details page.
- The integrations list already showed the circular icon correctly, but the details page still used the older separate `logo.png` / `dark_logo.png`, which appeared cropped.
- `logo.png` and `dark_logo.png` now use the same approved circular blue BigBlue mark.

## v0.3.19

### Українська
- Додано вбудоване **автоматичне GitHub BLE logging** без окремої автоматизації Home Assistant.
- У параметрах інтеграції доступні інтервали: **Off / 5 / 10 / 15 / 30 / 60 хв**.
- Додано поріг **Minimum SOC** для автологування, за замовчуванням 95%.
- Додано опцію логувати тільки коли присутня напруга на **AC Input**.
- Автоматичні snapshot позначаються `"snapshot_source": "auto"`; ручні — `"manual"`.
- При помилці GitHub інтеграція не спамить повторними запитами кожні 15 секунд.

### English
- Added built-in **automatic GitHub BLE logging** without requiring a Home Assistant automation.
- Available intervals: **Off / 5 / 10 / 15 / 30 / 60 minutes**.
- Added a configurable **Minimum SOC** threshold, default 95%.
- Added an option to log only while **AC Input** is connected.
- Automatic snapshots are tagged `"snapshot_source": "auto"`; manual snapshots as `"manual"`.
- GitHub errors are rate-limited so a failed upload does not retry every telemetry poll.

## v0.3.18

### Українська
- Додано керування **AC Output** та **DC Output** як switch entities у Home Assistant.
- Протокол отримано безпосередньо з APK BigBlue Energy: `ACS = 16 09`, `DCS = 16 07`, payload `00 00 00 01` = ON, `00 00 00 00` = OFF.
- Команди використовують той самий двочастинний FFE9 transport, що й уже перевірений AC Charging Power Limit.
- Додано очікування ACK `16 0A` для AC та `16 08` для DC.
- Виправлено branding icon: тепер `icon.png` має 256×256, `icon@2x.png` — 512×512; використано погоджений круглий синій варіант.

### English
- Added **AC Output** and **DC Output** switch entities in Home Assistant.
- Protocol was recovered directly from the BigBlue Energy APK: `ACS = 16 09`, `DCS = 16 07`, payload `00 00 00 01` = ON, `00 00 00 00` = OFF.
- Commands use the same two-part FFE9 transport as the now-validated AC Charging Power Limit.
- Added ACK handling for `16 0A` (AC) and `16 08` (DC).
- Fixed branding icon sizes: `icon.png` is now 256×256 and `icon@2x.png` is 512×512, using the approved circular blue icon.

## v0.3.17

### Українська
- Виправлено протокол зміни **AC Charging Power Limit** після повторного аналізу HCI snoop.
- Офіційний застосунок надсилає команду не одним записом, а **двома послідовними Write Without Response** у FFE9.
- Другий 2-байтовий фрагмент містить саме значення потужності у big-endian: `01 90` = 400 W, `03 20` = 800 W, `04 B0` = 1200 W.
- ACK `16 32` очікується лише після відправлення обох фрагментів.

### English
- Fixed the **AC Charging Power Limit** protocol after re-checking the HCI snoop capture.
- The official app sends the command as **two consecutive Write Without Response** operations to FFE9, not one write.
- The second 2-byte fragment contains the actual power value in big-endian: `01 90` = 400 W, `03 20` = 800 W, `04 B0` = 1200 W.
- ACK `16 32` is awaited only after both fragments are sent.

## v0.3.16

### Українська
- Оновлено іконку інтеграції на погоджений круглий синій варіант без внутрішньої білої крапки.
- Візуально іконка краще читається у малому розмірі на сторінці пристрою Home Assistant.

### English
- Updated the integration icon to the approved blue circular variant without the inner white dot.
- The icon is more legible at small sizes on the Home Assistant device page.

## v0.3.15

### Українська
- Виправлено критичну синтаксичну помилку в `__init__.py`, через яку інтеграція не завантажувалась після v0.3.14.
- Помилка була спричинена буквальними символами `\\n` у рядку ініціалізації BLE lock/ACK event.
- Логіка ACK для AC Charging Power та виправлена іконка залишені без змін.

### English
- Fixed a critical syntax error in `__init__.py` that prevented the integration from loading after v0.3.14.
- The issue was caused by literal `\\n` characters in the BLE lock/ACK event initialization line.
- AC Charging Power ACK logic and the corrected icon are unchanged.

## v0.3.14

### Українська
- Замінено неправильний `icon.png` на справжню квадратну іконку з APK BigBlue Energy.
- Та сама перевірена іконка використовується для `icon.png` та `icon@2x.png`, щоб Home Assistant більше не показував тонку синю смугу замість ярлика.

### English
- Replaced the incorrect `icon.png` with the real square icon extracted from the BigBlue Energy APK.
- The verified square icon is used for both `icon.png` and `icon@2x.png` so Home Assistant no longer renders a thin blue line instead of the integration icon.

## v0.3.13

### Українська
- Виправлено можливу колізію між polling телеметрії та BLE-командами керування.
- Тепер увесь цикл telemetry request/response захищено одним BLE transaction lock.
- Після зміни AC Charging Power інтеграція очікує реальне підтвердження `16 32` від CP2500; без ACK значення не вважається зміненим.

### English
- Fixed a possible collision between telemetry polling and BLE control writes.
- The complete telemetry request/response transaction is now protected by one BLE lock.
- AC Charging Power changes now wait for the real `16 32` acknowledgement from the CP2500; without ACK, the value is not accepted as changed.

## v0.3.12

### Українська
- Додано керування **AC Charging Power Limit** через Home Assistant.
- Доступні значення: **400 W**, **800 W**, **1200 W**.
- BLE-команди підтверджено HCI snoop-записом офіційного застосунку BigBlue Energy.
- Команди записуються у FFE9 через те саме BLE-з'єднання, яке використовує телеметрія.
- Додано блокування BLE write, щоб телеметрія та керування не писали одночасно.

### English
- Added **AC Charging Power Limit** control in Home Assistant.
- Available values: **400 W**, **800 W**, **1200 W**.
- BLE write commands were confirmed from an HCI snoop capture of the official BigBlue Energy app.
- Commands are written to FFE9 using the same BLE connection as telemetry.
- Added BLE write locking so telemetry and control writes do not collide.

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
