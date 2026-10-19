import serial,time,struct,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent.parent/'output/firmware/diagnostics'
OUT.mkdir(parents=True,exist_ok=True)
def crc(data):
    c=0
    for b in data:
        c ^= b<<8
        for _ in range(8): c=((c<<1)^0x1021 if c&0x8000 else c<<1)&65535
    return c
class Link:
    def __init__(self): self.s=serial.Serial('COM7',115200,timeout=.1); self.buf=bytearray()
    def send(self,p):
        h=bytes([2,len(p)]) if len(p)<256 else bytes([3,len(p)>>8,len(p)&255])
        self.s.write(h+p+crc(p).to_bytes(2,'big')+b'\x03')
    def recv(self,timeout=1):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            self.buf.extend(self.s.read(self.s.in_waiting or 1))
            while self.buf:
                if self.buf[0] not in (2,3): self.buf.pop(0); continue
                h=2 if self.buf[0]==2 else 3
                if len(self.buf)<h: break
                n=int.from_bytes(self.buf[1:h],'big')
                if len(self.buf)<h+n+3: break
                raw=bytes(self.buf[:h+n+3]); del self.buf[:h+n+3]
                p=raw[h:h+n]
                if raw[-1]==3 and crc(p)==int.from_bytes(raw[-3:-1],'big'): return p
        return None
    def request(self,cmd):
        self.send(bytes([cmd]))
        until=time.monotonic()+3
        while time.monotonic()<until:
            p=self.recv(.5)
            if p and p[0]==cmd:return p
        raise RuntimeError('No response '+str(cmd))
    def term(self,t):
        self.send(bytes([20])+t.encode())
        result=[]; until=time.monotonic()+1.5
        while time.monotonic()<until:
            p=self.recv(.2)
            if p and p[0]==21:result.append(p[1:].decode(errors='replace'))
        return '\n'.join(result)
def fields(config):
    src=(Path(__file__).resolve().parent/'vesc-firmware-review/confgenerator.c').read_text()
    src=src.split('int32_t confgenerator_serialize_mcconf',1)[1].split('return ind;',1)[0]
    at=4; result={}
    for line in src.splitlines():
        m=re.search(r'buffer\[ind\+\+\] = (?:\(uint8_t\))?conf->([\w\[\]]+)',line)
        if m: result[m[1]]=(at,1); at+=1; continue
        m=re.search(r'buffer_append_(\w+)\(buffer, conf->([\w\[\]]+)',line)
        if m:
            size=2 if '16' in m[1] else 4
            result[m[2]]=(at,size); at+=size
    return result
if __name__=='__main__':
    l=Link()
    try:
        fw=l.request(0); print('FW:',fw[:35])
        conf=l.request(14); (OUT/'mcconf_before.bin').write_bytes(conf)
        offsets=fields(conf); summary={}
        for name in ['motor_type','l_current_max','l_current_min','l_abs_current_max','l_slow_abs_current','foc_offsets_current[0]','foc_offsets_current[1]','foc_offsets_current[2]']:
            at,n=offsets[name]; raw=conf[1+at:1+at+n]
            summary[name]=raw[0] if n==1 else struct.unpack('>f',raw)[0]
        print(json.dumps(summary,indent=2))
        for cmd in ['fault','faults','uptime']:
            result=l.term(cmd); print(cmd+':\n'+result); (OUT/(cmd+'_before.txt')).write_text(result)
        (OUT/'config_before.json').write_text(json.dumps(summary,indent=2))
    finally:l.s.close()
