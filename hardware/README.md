# ESC FOC Driver V3.0 — Hardware

![Board](../docs/assets/esc-foc-v3-board.png)

- [Schematic PDF](schematic/SCH_SchematicV01_2_2026-10-19.pdf)
- [Mechanical files](mechanical/)
- [Hardware configuration header](../output/firmware/DRV8302_B02/hw_drv8302_b02.h)

## Pin mapping จาก B02 profile

| Function | STM32F405 pin |
|:--|:--|
| PWM H1 / H2 / H3 | PA10 / PA9 / PA8 |
| PWM L1 / L2 / L3 | PB15 / PB14 / PB13 |
| Current SO1 / SO2 | PB1 / PB0 |
| Phase sense 1 / 2 / 3 | PA2 / PA1 / PA0 |
| EN_GATE / DC_CAL / nFAULT | PC10 / PB12 / PC12 (active low) |
| Bus voltage / FET temp / motor temp | PC2 / PA3 / PC0 |
| Hall 1 / 2 / 3 | PB6 / PB7 / PC11 |
| SWDIO / SWCLK | PA13 / PA14 |

SWD test points: TP1 VCC (3.3 V reference), TP2 RESET, TP3 DIO, TP4 CLK, TP5 GND ตามคู่มือ B02

## เคสและชิ้นส่วน

![Enclosure](../docs/assets/esc-foc-v3-enclosure.png)

เก็บไฟล์ทุกชิ้นที่มีในโฟลเดอร์ 3D ต้นทางร่วมกันเพื่อรักษาการอ้างอิง assembly เท่าที่มี ยังไม่ได้เปิด rebuild ด้วย SolidWorks จึงไม่รับรองว่า references ภายนอกครบหรือชิ้นงานพร้อมผลิต

ผลตรวจทางไฟฟ้าและข้อจำกัดล่าสุดดูที่ [README หลัก](../README.md#สถานะการทดสอบล่าสุด)
