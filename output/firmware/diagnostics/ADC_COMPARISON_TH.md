# ผลเปรียบเทียบการอ่าน ADC - 19 ตุลาคม 2026

สถานะ: ยังไม่ผ่านการยืนยันพร้อมใช้งานกับมอเตอร์
ไม่มีการเพิ่ม current limit หรือสั่ง Motor Detection ในการทดสอบนี้ ผู้ใช้ยืนยันถอดมอเตอร์ในช่วงตรวจ

| การตั้งค่า | ตัวอย่างที่ได้รับ | SD I1/I2 ตามสเกล A | ช่วงพีก I1/I2 ตามสเกล A |
|---|---:|---|---|
| เดิม 42 MHz | 1829 | 3.85 / 3.91 | -12.89 ถึง +13.05 / -14.99 ถึง +13.54 |
| R2: 21 MHz, sample เดิม | 2000 | 1.59 / 1.69 | -11.12 ถึง +11.93 / -13.05 ถึง +10.15 |
| R4: 21 MHz, rank 2 sample 56 cycles ทั้ง 3 ADC | 1891 | 1.46 / 1.50 | -11.44 ถึง +12.41 / -13.54 ถึง +12.57 |
| R5: 10.5 MHz, sample เดิม | 1816 | 1.14 / 1.23 | -19.02 ถึง +10.64 / -20.95 ถึง +10.32 |
| R6: 21 MHz, currents first, half-DMA interrupt | 1938 | 1.54 / 1.51 | -11.77 ถึง +10.64 / -14.18 ถึง +14.51 |
| R2 ปิด prefetch ตาม ST ES0182 | 1919 | 1.69 / 1.58 | -8.70 ถึง +13.22 / -10.48 ถึง +13.86 |

ค่าข้างต้นคำนวณจาก ADC current samples และสเกล 3.3 V / 4095 / (gain 10 x shunt 0.0005 ohm)
ไม่ใช่กระแสที่วัดด้วย current probe และกลุ่มข้อมูลอาจเก็บไม่ครบ 2000 ตัวอย่างเพราะ USB sampling packet บางส่วนไม่มาถึงในเวลารอ

ทุกการตั้งค่าที่ยืนยันสัญญาณได้ยังพบพีกที่เกิน current fault 10 A จึงไม่ถือว่าแก้ปัญหาสำเร็จ
ค่า fault ปัจจุบันในสถานะ FOC idle เป็น NONE ไม่ได้ยืนยันว่าสัญญาณกระแสดิบใช้ควบคุมมอเตอร์ได้
ประวัติหลัง boot ยังมี DRV และ UNDER_VOLTAGE ในช่วงเริ่มต้น

R3 ถูกคัดออก: เพิ่ม sample time เฉพาะ ADC current แต่ไม่ได้ปรับ ADC3 rank เดียวกัน ทำให้ลำดับข้อมูลผิดและค่าแรงดันผิด
R4 แก้การจับเวลาของ rank ให้ตรงกันแล้ว แต่ยังไม่แก้พีกได้

ได้คืน R2 และ verify ผ่านก่อนทดลอง independent ADC diagnostic
โปรแกรม independent ADC diagnostic เป็นโปรแกรมชั่วคราว 704 bytes เขียน sector 0 เท่านั้น เก็บ config sectors 1/2 และ bootloader ไว้
โปรแกรมนี้ไม่มี PWM ให้ gate driver และไม่มีคำสั่งมอเตอร์ แต่เข้าสู่ WFI หลังเก็บข้อมูล ทำให้ debugger ไม่สามารถเชื่อมต่อกลับในสภาพการต่อปัจจุบัน
ต้องกด RESET / เชื่อม NRST เพื่อกลับเข้าดีบักและคืน R2 ก่อนใช้งาน VESC Tool ต่อ
ยังไม่มีข้อมูลจาก independent ADC diagnostic ที่อ่านออกมาได้ ห้ามถือว่าการทดสอบนี้ผ่าน

อัปเดตหลัง recovery: ผู้ใช้กด RESET แล้วจับ CPU ด้วย HOTPLUG และ halt ได้สำเร็จ
เขียน R2 กลับพร้อม verify ผ่าน และรีเซ็ตเรียบร้อย อ่านทาง USB ได้ชื่อ DRV8302_B02_R2,
motor type FOC และ FAULT_CODE_NONE โปรแกรมวินิจฉัยชั่วคราวถูกแทนที่แล้ว
ผลยืนยันการคืนระบบอยู่ใน recovery_verified.json ปัญหาพีก ADC ยังไม่ถือว่าแก้สำเร็จ

## Independent ADC test ที่อ่านผลได้สำเร็จในรอบถัดมา

แก้โปรแกรมชั่วคราวให้เปิด debug low-power access และรอด้วย NOP แทน WFI แล้วทดสอบซ้ำ
ตรวจ header ได้ magic 0xADC04052, profile count 3 และ completion 0x600DC0DE
ใช้ HSI 16 MHz / ADC1 อิสระ 8 MHz ไม่มี DMA ไม่มี USB และไม่มี PWM
แต่ละ profile มี 512 samples ต่อช่อง SO1/PB1, SO2/PB0 และ VREFINT ภายใน MCU

| Profile | SO1 min/max/SD counts | SO2 min/max/SD counts | VREFINT min/max/SD counts |
|---|---|---|---|
| acquisition 15 cycles | 1991 / 2176 / 12.88 | 1997 / 2118 / 9.99 | 1407 / 1552 / 13.12 |
| acquisition 480 cycles | 1991 / 2112 / 11.03 | 2003 / 2118 / 11.04 | 1455 / 1552 / 11.92 |
| 480 cycles + DC_CAL | 1919 / 2112 / 11.47 | 1983 / 2176 / 12.59 | 1407 / 1552 / 13.73 |

ผลยังแกว่งแม้ไม่มีระบบควบคุม VESC และแม้ช่อง VREFINT ภายใน MCU จึงต้องตรวจ ADC / VDDA / VSSA / decoupling หรือข้อจำกัดภายใน MCU เพิ่ม
ไม่ใช่หลักฐานว่าตัวชิปเสียแน่นอน และไม่ใช่หลักฐานว่าค่า current จริงเท่ากับที่ ADC ตีความ
ผู้ใช้รายงานว่าจุด SO1 ที่ DRV และ MCU ดูนิ่งบนสโคป แต่ยังไม่มี waveform ที่นำมาเทียบช่วงเวลาเดียวกับ ADC capture

หลังอ่านข้อมูลได้ คืน R2 และ read-back verify ผ่านอีกครั้ง ตรวจ USB ได้ DRV8302_B02_R2 และ FAULT_CODE_NONE
DBGMCU_IDCODE = 0x101F6413 ซึ่ง revision 0x101F อยู่ในตาราง ST ES0182 Rev 19
ค่าคาลิเบรต VREFINT/temperature จาก factory area: 0x05DC, 0x039C, 0x04AC
ไฟล์ข้อมูล: adc_independent_samples.bin และ adc_independent_report.json

แหล่งอ้างอิง:
- ST ES0182 Rev 19, section 2.2.15: internal noise impacting ADC accuracy และ workaround ปิด prefetch เปิด instruction/data cache
  https://www.st.com/resource/en/errata_sheet/dm00037591-stm32f405-407xx-and-stm32f415-417xx-device-limitations-stmicroelectronics.pdf
- ซอร์สต้นฉบับ VESC 6.00 ใน mcpwm_foc.c ระบุ ADC 42 MHz สูงกว่าขีดจำกัด 36 MHz
