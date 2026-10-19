from vesc_diag import Link,OUT
import subprocess,re,struct,time,json,statistics
CLI='C:/Program Files/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.exe'
def run(args):
    r=subprocess.run([CLI,'-c','port=SWD','mode=HOTPLUG','freq=1000','sn=37FF71064E573436C8061743']+args,capture_output=True,text=True,errors='replace')
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    return r.stdout
def read(addr):
    s=run(['-r32',hex(addr),'4']);m=re.search(hex(addr)+r'\s*:\s*([0-9a-fA-F]+)',s,re.I)
    assert m,s;return int(m[1],16)
def capture(l):
    # Collect only a small buffer so no prior capture remains in the USB queue.
    l.buf.clear();l.s.reset_input_buffer()
    l.send(bytes([19,1])+struct.pack('>H',400)+bytes([20,1]))
    rows=[];until=time.monotonic()+5
    while len(rows)<400 and time.monotonic()<until:
        p=l.recv(.2)
        if p and p[0]==19:rows.append(struct.unpack_from('>8f',p,1)[:2])
    assert len(rows)>100,len(rows)
    return {'samples':len(rows),'channels':[{'min_counts':min(v),'max_counts':max(v),'mean_counts':statistics.mean(v),'stdev_counts':statistics.pstdev(v)} for v in zip(*rows)]}
saved={a:read(a) for a in [0x40012010,0x40012110]};l=Link();report={}
try:
    assert l.request(14)[7]==2
    report['15cycles']=capture(l)
    for a,v in saved.items():run(['-w32',hex(a),hex((v&~0x3f000000)|0x1b000000)])
    report['56cycles']=capture(l)
finally:
    for a,v in saved.items():run(['-w32',hex(a),hex(v)]);assert read(a)==v
    l.s.close()
(OUT/'adc_acquisition_comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
