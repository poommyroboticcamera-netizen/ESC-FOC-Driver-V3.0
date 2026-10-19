# ผลตรวจ DRV8302_B02 วันที่ 19 ตุลาคม 2026

บอร์ดต่อผ่าน COM7 และ ST-Link; ผู้ใช้ยืนยันว่าถอดมอเตอร์แล้ว ไม่มีคำสั่งสั่งหมุนหรือ Motor Detection ในการตรวจรอบนี้

## สิ่งที่แก้และตรวจยืนยัน

- ค่าที่อ่านจากบอร์ดก่อนแก้: motor_type=0 (BLDC), motor current +5/-2 A, absolute fault 10 A, slow abs current=false
- สำรอง configuration ไว้ใน mcconf_before_foc.bin แล้วเปลี่ยน motor_type เป็น 2 (FOC) ผ่าน protocol ของ VESC โดยไม่แก้ค่า current limits
- เฟิร์มแวร์คาลิเบรต current/voltage offsets ใหม่เมื่อเปลี่ยนโหมด
- หลัง reboot อ่านกลับได้ FOC และ absolute fault 10 A; fault ปัจจุบันเป็น FAULT_CODE_NONE
- ตรวจ 492 ครั้งใน 25 วินาที: fault=0 ทุกครั้ง, bus voltage 24.0-24.1 V, reported average motor current=0 A
- ประวัติหลัง boot ยังมี DRV และ UNDER_VOLTAGE ระหว่างเริ่มระบบ ยังไม่ยืนยันว่าเป็น transient ของ ADC/driver initialization หรือไฟเลี้ยงจริง

## สิ่งที่ยังไม่ผ่าน

ข้อมูล current sampling จาก firmware ระหว่างถอดมอเตอร์ 2,755 ตัวอย่าง:

| ช่อง | ต่ำสุด (A ตามสเกล firmware) | สูงสุด | RMS |
|---|---:|---:|---:|
| I1 | -11.44 | 15.15 | 4.05 |
| I2 | -13.38 | 15.79 | 3.98 |

นี่คือค่าที่ ADC และ firmware ตีความ ไม่ใช่การวัดกระแสจริงด้วยเครื่องมืออิสระ
ค่า reported current=0 A ในสถานะ FOC idle ไม่ได้พิสูจน์ว่าสัญญาณดิบปกติ

ทดสอบ DC_CAL ภายในชั่วคราวโดยยืนยันว่ามอเตอร์ถอดอยู่:
- input ปกติ: standard deviation ประมาณ 16.2 / 19.3 ADC counts
- DC_CAL ภายใน: standard deviation ประมาณ 28.9 / 28.7 counts
- การทดสอบนี้ยังไม่แยก DRV output, REF/ground, MCU VDDA หรือ ADC acquisition ออกจากกัน ต้องวัดด้วย scope
- คืน DC_CAL เป็น LOW แล้ว และ reboot คืนค่า peripheral ทั้งหมด; ตรวจ ODR=0xEFFF, ADC1 SMPR2=0x09001001, ADC2 SMPR2=0x09048008
- การลองเขียน sample time ขณะ ADC ทำงานถูกเครื่องมือปฏิเสธ จึงไม่มีผลเปรียบเทียบ sample time ที่ใช้สรุปได้ และไม่ได้เก็บการแก้นี้ใน firmware

ค่า 12.0 A ใน log BLDC เดิมไม่ใช่หลักฐานของพีกจริง 12.0 A: mcpwm.c จำกัดค่าที่รายงานไว้ที่ 1.2 x absolute limit (10 A) ก่อน fault handler อ่านค่า

## ขั้นตรวจทางกายภาพถัดไป

ยังถอดมอเตอร์และห้ามกด Detection ระหว่างวัด
ใช้ scope probe x10, ground spring/สายกราวด์สั้น ต่อ ground ที่ GND logic เท่านั้น
วัด SO1/BR_SO1 (U20 pin25 หรือ PB1), SO2/BR_SO2 (pin26 หรือ PB0) และ REF (pin24)
เริ่ม DC coupling ยืนยันระดับประมาณ 1.65 / 1.65 / 3.3 V จากนั้น AC coupling 20 mV/div, 10 us/div และ bandwidth limit 20 MHz
วัดซ้ำที่ 1 ms/div เพื่อดู ripple ช้า เก็บ waveform SO1 คู่กับ REF แล้ว SO2 คู่กับ REF
ถ้า SO1/SO2 และ REF กระเพื่อมสัมพันธ์กัน ให้ตรวจ rail/reference/ground; ถ้า REF นิ่งแต่ SO แกว่ง ให้ตรวจ DRV analog supply/output path และหาก SO ที่ DRV นิ่งแต่ PB0/PB1 แกว่ง ให้ตรวจ trace/ADC supply/connection

ยังไม่ทดสอบมอเตอร์และยังไม่ยืนยันว่าปัญหา Detection ถูกแก้ครบ
