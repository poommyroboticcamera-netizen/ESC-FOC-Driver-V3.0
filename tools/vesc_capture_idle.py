from vesc_diag import Link,OUT
import struct,time,json,statistics
l=Link();rows=[]
try:
    for batch in range(3):
        l.send(bytes([19,1])+struct.pack('>H',1000)+bytes([10,0]))
        until=time.monotonic()+6; block=[]
        while len(block)<1000 and time.monotonic()<until:
            p=l.recv(.3)
            if p and p[0]==19:
                v=struct.unpack_from('>8f',p,1)
                block.append({'i1':v[0],'i2':v[1],'switching_hz':v[7]})
        print('Captured',batch,len(block),flush=True);rows+=block
    result={'samples':len(rows),'motor_connected':False,'motor_command_sent':False}
    for name in ['i1','i2']:
        values=[r[name] for r in rows]
        result[name]={'min':min(values),'max':max(values),'mean':statistics.mean(values),'rms':(statistics.mean(v*v for v in values))**.5}
    result['fault']=l.term('fault')
    (OUT/'idle_current_capture.json').write_text(json.dumps(result,indent=2))
    (OUT/'idle_current_samples.json').write_text(json.dumps(rows))
    print(json.dumps(result,indent=2))
finally:l.s.close()
