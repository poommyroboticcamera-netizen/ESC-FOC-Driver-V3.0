from vesc_diag import Link,OUT
import subprocess,struct,time,json,statistics,re
CLI='C:/Program Files/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.exe'
def gpio(high):
    r=subprocess.run([CLI,'-c','port=SWD','mode=HOTPLUG','freq=1000','sn=37FF71064E573436C8061743','-w32','0x40020418','0x1000' if high else '0x10000000'],capture_output=True,text=True,errors='replace')
    # BSRR is write-only: CubeProgrammer's automatic read-back cannot verify it.
    # Verify the resulting pin state via the readable ODR register instead.
    check=subprocess.run([CLI,'-c','port=SWD','mode=HOTPLUG','freq=1000','sn=37FF71064E573436C8061743','-r32','0x40020414','4'],capture_output=True,text=True,errors='replace')
    m=re.search(r'0x40020414\s*:\s*([0-9A-Fa-f]+)',check.stdout)
    if not m or bool(int(m[1],16)&0x1000)!=high:raise RuntimeError('DC_CAL state not verified')
def capture(l):
    l.buf.clear();l.s.reset_input_buffer()
    l.send(bytes([19,1])+struct.pack('>H',1000)+bytes([10,1]))
    rows=[];until=time.monotonic()+10
    while len(rows)<1000 and time.monotonic()<until:
        p=l.recv(.2)
        if p and p[0]==19:rows.append(struct.unpack_from('>8f',p,1)[:2])
    if not rows:raise RuntimeError('No ADC samples')
    return {'samples':len(rows),'channels':[{'min_counts':min(v),'max_counts':max(v),'mean_counts':statistics.mean(v),'stdev_counts':statistics.pstdev(v)} for v in zip(*rows)]}
l=Link();report={}
try:
    assert l.request(14)[7]==2
    report['normal_shunt_inputs']=capture(l)
    gpio(True);time.sleep(.1)
    report['internal_dc_cal_inputs']=capture(l)
finally:
    gpio(False);l.s.close()
(OUT/'dc_cal_isolation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
