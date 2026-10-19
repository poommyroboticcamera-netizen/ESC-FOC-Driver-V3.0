# Development tools

Build scripts และ diagnostic scripts ที่เก็บจากการ bring-up วันที่ 19 ตุลาคม 2026

- `build_b02*.py`: build B02 และ experimental revisions ดู [ขั้นตอน build](../firmware/README.md)
- `vesc_*.py`: capture, configuration และการตรวจผ่าน VESC protocol
- `adc_diag.c`, `adc_diag.ld`: independent ADC diagnostic ชั่วคราวที่ใช้ในการสอบสวน

สคริปต์ diagnostic บางตัวเขียน configuration หรือทำงานกับพอร์ตอุปกรณ์โดยตรง และใช้ path/COM port เฉพาะเครื่องเดิม ต้องอ่าน source และปรับก่อนรัน ไม่ใช่ชุดทดสอบอัตโนมัติสำหรับผู้ใช้ทั่วไป ไม่มีการรันสคริปต์เหล่านี้หรือเชื่อมต่อบอร์ดระหว่างจัด repository
