# Firmware source และการ build

## Source snapshots

- `../output/firmware/DRV8302_B02/firmware_source.zip`: ชุด source และ build script ของ B02 ต้นรอบ
- `source/vesc-6.00-b02-diagnostic-source.zip`: snapshot ของ working source หลังทดลอง ADC รวม custom header R2–R6, hardware source ที่เพิ่ม, build identity และการแก้ `motor/mcpwm.c` / `motor/mcpwm_foc.c`
- `../output/firmware/DRV8302_B02/bootloader_source.zip`: source bootloader พร้อม license เดิม

Upstream VESC commit: `4b822f0f944918957c55391ca0672925153f3fde` (6.00)

## เตรียม build บน Windows

1. แตก diagnostic source archive ให้ได้โฟลเดอร์ `tmp/vesc-firmware-review` ที่ root ของ repository
2. ติดตั้ง GNU Arm GCC 7.2.1 (PlatformIO toolchain 1.70201.0), GNU Make, Python 3 และ Git for Windows shell
3. ปรับ path toolchain และ shell ใน `tools/build_b02.py` ให้ตรงเครื่อง
4. เรียก `python tools/build_b02_r2.py` จาก root เพื่อสร้าง R2 หรือเลือก build script ของ revision ที่ต้องการ
5. ตรวจ build log และ identity ของไฟล์ที่ได้ก่อนนำไปใช้

Build scripts เก็บมาจากรอบพัฒนา ใช้ toolchain paths เฉพาะ Windows และยังไม่ได้ build ซ้ำในขั้นตอนจัด repository นี้ Binary ที่แนบเป็นผลเดิมจากรอบพัฒนา; ไม่ได้อ้างว่าทุก experimental revision ผ่านการใช้งานจริง

R2 ใช้ ADC prescaler /4 (21 MHz) ส่วน profiles อื่นเป็นการทดลองเปรียบเทียบ อ่าน [ADC report](../output/firmware/diagnostics/ADC_COMPARISON_TH.md) ก่อนเลือก โดยเฉพาะ R3 ที่ถูกคัดออก

Diagnostic source snapshot เก็บสถานะ source ล่าสุดร่วมกัน ไม่ใช่ snapshot แยกตรงเวลาของ binary ทุก revision ส่วน original B02 source เก็บแยกในแพ็กเกจต้นรอบ
