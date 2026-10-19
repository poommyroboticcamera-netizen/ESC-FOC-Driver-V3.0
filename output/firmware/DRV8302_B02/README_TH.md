# DRV8302 B02 - ชุดเฟิร์มแวร์สำหรับแฟลชครั้งแรก

จัดเตรียมวันที่ 19 ตุลาคม 2026 สำหรับ schematic SCH_SchematicV01_2_2026-10-19.pdf
ชื่อบอร์ดในเอกสาร: vesc4_12B02 ใช้ STM32F405RGT6, คริสตัล 8 MHz

สถานะ: คอมไพล์และตรวจไฟล์ผ่าน ยังไม่ได้แฟลชหรือทดสอบบนบอร์ดจริง
ใช้ VESC firmware 6.00 ไม่ได้อ้างว่าเป็นรุ่นล่าสุด ตรึง source commit
4b822f0f944918957c55391ca0672925153f3fde และปรับ hardware header เฉพาะบอร์ด

## เลือกไฟล์

- `drv8302_b02_factory.hex`: ใช้กับ STM32CubeProgrammer / ST-Link สำหรับบอร์ดใหม่ มีทั้ง firmware และ generic VESC bootloader พร้อมตำแหน่งเขียนในไฟล์
- `drv8302_b02.bin`: firmware อย่างเดียว เริ่มที่ 0x08000000 ไม่ใช่ 0x0800C000 และไม่ใช่ไฟล์ factory รวม bootloader
- `drv8302_b02.hex`: firmware อย่างเดียว พร้อม address
- `drv8302_b02.elf`: ใช้ debug มี symbol
- `bootloader_generic.bin`: bootloader จาก upstream เขียนที่ 0x080E0000 ถ้าต้องการแยกเขียน; generic ไม่ขับขา LED ของบอร์ดรุ่นอื่น
- `firmware_source.zip`: source VESC ทั้งชุดพร้อม hardware header และ build script ที่ใช้
- `bootloader_source.zip`: source bootloader ตรง commit ที่ระบุใน bootloader_commit.txt
- `SHA256SUMS.txt`, `validation.json`, `build.log`: หลักฐานตรวจไฟล์และการคอมไพล์

## ค่าที่ปรับตามวงจร

| รายการ | ค่า / ขา |
|---|---|
| Shunt R14, R15 | 0.0005 ohm (0.5 mΩ) |
| DRV8302 GAIN | 10 V/V, GAIN ต่อ GND |
| วัดแรงดัน bus / phase | 39 kohm / 2.2 kohm |
| NTC MOSFET R30 / R31 | 10 kohm, B3450 ด้านบน / 10 kohm ลง GND |
| กระแส 1 / 2 | BR_SO1 -> PB1 ADC9 / BR_SO2 -> PB0 ADC8 |
| Phase sense 1 / 2 / 3 | PA2 / PA1 / PA0 |
| PWM H1 / H2 / H3 | PA10 / PA9 / PA8 |
| PWM L1 / L2 / L3 | PB15 / PB14 / PB13 |
| EN_GATE / DC_CAL / nFAULT | PC10 / PB12 / PC12 active low |
| Bus voltage / FET temp / motor temp | PC2 / PA3 / PC0 |
| Hall 1 / 2 / 3 | PB6 / PB7 / PC11 |
| CAN RX / TX | PB8 / PB9 |
| USB DM / DP | PA11 / PA12 |
| LED เขียว / แดง | PC4 / PC5 |

ตรวจจาก schematic ทั้ง 5 หน้า ยังไม่ได้ตรวจ continuity บน PCB จริง
วงจร dead time และ overcurrent ของ DRV8302 ตั้งด้วยขาฮาร์ดแวร์ เฟิร์มแวร์ไม่สามารถแก้ค่าตัวต้านทานหรือการต่อขาเหล่านี้ได้

## ค่าเริ่มต้นสำหรับ commissioning

ค่าเหล่านี้เป็นค่าเริ่มต้นใน firmware ไม่ใช่พิกัดกระแสหรือแรงดันที่รับรองของบอร์ด

- Motor current: +5 A / -2 A; battery current: +2 A / -0.5 A
- Absolute current fault: 10 A; voltage window: 10-30 V
- Battery cut start/end: 11/10 V เป็นค่า bench test ต้องปรับตามแบตเตอรี่จริงก่อนใช้งานกับแบตเตอรี่
- ERPM: +/-10000; duty สูงสุด 20%; output power +50/-10 W
- FET temperature เริ่มลดกระแสที่ 60 °C / ตัดที่ 75 °C
- APP_NONE: ปิดแอป PPM/ADC/UART อัตโนมัติ; USB และ CAN ยังรับคำสั่งได้
- Command timeout 1000 ms, timeout brake current 0 A
- ใช้ FOC เดิมของ VESC; พารามิเตอร์ R/L/flux ของมอเตอร์ยังเป็นค่า default ต้องตรวจวัดก่อนหมุน

การอัปโหลด firmware บนบอร์ดที่เคยใช้แล้วอาจเก็บค่า motor/app เดิมไว้ ทำให้ค่าเริ่มต้นไม่ถูกนำมาใช้
ขั้นตอน first install ด้านล่างล้าง flash ทั้งหมด รวมค่าที่เคยบันทึกไว้ จึงใช้สำหรับบอร์ดใหม่หรือบอร์ดที่ต้องการเริ่มตั้งค่าใหม่เท่านั้น
VESC Tool wizard หรือการเขียน configuration สามารถเปลี่ยน limits เหล่านี้ได้ ตรวจค่าซ้ำหลังทุกครั้งที่ใช้ wizard

## แฟลชผ่าน ST-Link และ STM32CubeProgrammer

1. ถอดมอเตอร์และสายรับคำสั่งภายนอกก่อนแฟลช เตรียมแหล่งจ่าย bench แบบจำกัดกระแส
2. ต่อ ST-Link: SWDIO -> TP3 DIO (PA13), SWCLK -> TP4 CLK (PA14), GND -> TP5, NRST -> TP2 RESET และ VTref -> TP1 VCC (3.3 V)
3. VTref ใช้วัดแรงดันอ้างอิงตามรุ่น ST-Link ห้ามนำ 5 V เข้าขา VCC/MCU และอย่าขนานแหล่งจ่าย 3.3 V โดยไม่ตรวจการต่อ
4. BOOT0 อยู่ GND ตามวงจร ใช้ SWD ได้ เปิดไฟเลี้ยง logic และตรวจ 3.3 V ก่อนเชื่อมต่อ
5. ใน STM32CubeProgrammer เลือก ST-LINK / SWD / Under Reset / Hardware reset / 1000 kHz และ Connect ตรวจว่าเป็น STM32F405, flash 1 MB
6. สำหรับ first install เลือก Full chip erase (ข้อมูลเดิมทั้งหมดจะหาย)
7. เปิด `drv8302_b02_factory.hex` เลือก Verify programming แล้ว Download จากนั้น Reset ไฟล์ HEX มี address อยู่แล้ว ไม่ต้องกรอก offset
8. หรือเรียก `powershell -ExecutionPolicy Bypass -File .\flash_first_install.ps1` จากโฟลเดอร์นี้ สคริปต์ทำ erase, program, verify และ reset ตามลำดับ ไม่ได้ถูกรันระหว่างเตรียมแพ็กเกจ

## ตรวจหลังแฟลชก่อนต่อมอเตอร์

1. ใช้ bench supply 12 V จำกัดกระแสเริ่มต้นประมาณ 0.2-0.5 A (เพิ่มเฉพาะเมื่อยืนยันว่าไม่มี short และภาคจ่ายไฟปกติ) อย่าจ่ายกำลังให้มอเตอร์ด้วย USB อย่างเดียว
2. เชื่อม USB กับ VESC Tool ที่รองรับ firmware 6.00 ตรวจชื่อ HW `DRV8302_B02` และ firmware 6.00
3. อ่าน motor/app configuration ยืนยันค่า commissioning ตรงรายการด้านบน และ APP_NONE
4. เทียบ bus voltage กับมัลติมิเตอร์ กระแสเมื่อไม่มีมอเตอร์ต้องใกล้ศูนย์ อุณหภูมิ FET ต้องใกล้อุณหภูมิห้องและเพิ่มเมื่ออุ่นเซนเซอร์
5. ตรวจ fault history หากมี DRV/undervoltage/overcurrent ให้หาสาเหตุก่อนเริ่ม motor detection
6. เมื่อจะต่อมอเตอร์: ปิดไฟก่อน ยึดมอเตอร์ให้นิ่งและให้เพลาหมุนอิสระ ตรวจ gate PWM/dead time ด้วยออสซิลโลสโคปและ current offset ก่อนใช้ FOC detection
7. เริ่มการตรวจวัดมอเตอร์ด้วยกระแสต่ำที่เหมาะกับมอเตอร์และแหล่งจ่าย ตรวจ limits ซ้ำก่อนสั่งหมุน การมีไฟล์พร้อมแฟลชไม่ได้ยืนยันความพร้อมขับกำลังของ PCB
8. Bench supply ทั่วไปอาจรับพลังงานคืนไม่ได้ ค่า battery regen -0.5 A ไม่ใช่การรับประกันว่าจะไม่มี bus overvoltage หลีกเลี่ยงการทดสอบเบรกจนเตรียมแหล่งรับพลังงานคืนแล้ว

## Source และการสร้างซ้ำ

Upstream firmware: https://github.com/vedderb/bldc/tree/4b822f0f944918957c55391ca0672925153f3fde
Bootloader: https://github.com/vedderb/bldc-bootloader (commit ใน bootloader_commit.txt)
DRV8302: https://www.ti.com/lit/ds/symlink/drv8302.pdf

ใช้ GNU Arm GCC 7.2.1 จาก PlatformIO toolchain 1.70201.0, GNU Make, Python 3 และ Git for Windows shell
แตก firmware_source.zip ลงโฟลเดอร์ source แล้วรัน `python build_b02.py` (ปรับ path toolchain/shell ในสคริปต์ให้ตรงเครื่อง)
แก้เฉพาะ header `hwconf/other/vesc4/hw_drv8302_b02.h`; ใช้ hardware source `hw_410.c` เดิม
Source VESC และการแก้ไขใช้ GPL-3.0-or-later ตามหัวไฟล์เดิม; ไลบรารีที่รวมอยู่คงเงื่อนไข license ของแต่ละไฟล์
ไม่มีการแก้ส่วนควบคุมมอเตอร์หลัก ไม่มีผลการทดสอบจริงแนบมา
