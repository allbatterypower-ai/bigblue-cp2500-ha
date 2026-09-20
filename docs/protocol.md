# BLE-протокол BigBlue CP2500

Цей документ фіксує лише поля, які вже використовуються інтеграцією або мають сильне експериментальне підтвердження.

## Канал обміну

| Параметр | Значення |
|---|---|
| Telemetry write characteristic | FFE9 |
| Telemetry notify characteristic | FFE4 |
| Main frame | 236 bytes |
| Main header | `10 01 00 01 00 fa 15 06` |
| Secondary notification | 32 bytes, призначення ще досліджується |

Telemetry request:

`10 01 00 01 00 00 15 05 00 00 00 00 00 00 00 00 00 00`

## Підтверджені / використовувані поля

Offsets рахуються від нульового байта 236-байтового main frame.

| Offset | Тип | Масштаб | Поле | Статус |
|---:|---|---:|---|---|
| 28 | u16 LE | /10 | AC Input Voltage | підтверджено |
| 40 | u16 LE | /100 | AC Input Frequency | підтверджено |
| 44 | u16 LE | /10 | AC Input Current | підтверджено |
| 50 | u16 LE | ×1 | AC Input Power | підтверджено |
| 56 | s16 LE | ×1 °C | AC Input Temperature | використовується |
| 58 | s16 LE | ×1 °C | Battery Temperature | підтверджено |
| 60 | s16 LE | ×1 °C | AC Output Temperature | використовується |
| 74 | u16 LE | /10 | DC Output Voltage | підтверджено |
| 76 | u16 LE | /10 | DC Output Current | підтверджено |
| 78 | u16 LE | ×1 | DC Output Power | підтверджено |
| 84..115 | 16 × u16 LE | /1000 | Cell 1..16 Voltage | підтверджено |
| 134 | s16 LE | /100 | Battery Current | підтверджено |
| 136 | u16 LE | /100 | Battery Voltage | підтверджено |
| 138 | u16 LE | /100 | Surplus Capacity | підтверджено |
| 142 | u16 LE | /100 | Total Capacity | підтверджено |
| 144 | u16 LE | ×1 | Cell Count | підтверджено |
| 146 | u8 | ×1 | SOH | підтверджено |
| 147 | u8 | ×1 | SOC | підтверджено |
| 210 | s16 LE | ×1 °C | DC Temperature | сильний кандидат / використовується |

## Похідні значення

- Battery Power = Battery Voltage × Battery Current
- Cell Min = min(Cell 1..16)
- Cell Max = max(Cell 1..16)
- Cell Delta = Cell Max − Cell Min

## Ще не завершено

Потребують додаткових контрольних тестів:
- AC Output Power
- AC Output Voltage
- AC Output Current
- AC Output Frequency
- DC Input Power
- DC Input Voltage
- DC Input Current
- To Full
- To Empty
- призначення 32-байтового secondary notification
