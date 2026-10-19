from vesc_diag import Link,OUT,fields
import time,struct,json
l=Link()
try:
    conf=l.request(14); (OUT/'mcconf_verified_foc.bin').write_bytes(conf)
    assert conf[7]==2
    original=(OUT/'mcconf_before_foc.bin').read_bytes()
    f=fields(conf)
    changes=[]
    for name,(at,n) in f.items():
        if original[1+at:1+at+n]!=conf[1+at:1+at+n]:changes.append(name)
    print('Changed fields:',changes)
    for key in ['l_current_max','l_current_min','l_in_current_max','l_in_current_min','l_abs_current_max','l_slow_abs_current']:
        at,n=f[key];assert original[1+at:1+at+n]==conf[1+at:1+at+n],key
    print(l.term('hw_status'))
    l.send(bytes([29])); print('Reboot requested; no motor command sent')
finally:l.s.close()
time.sleep(8)
l=Link(); samples=[]
try:
    conf=l.request(14);assert conf[7]==2
    (OUT/'mcconf_after_reboot.bin').write_bytes(conf)
    until=time.monotonic()+25
    while time.monotonic()<until:
        p=l.request(4)
        samples.append({'current':struct.unpack_from('>i',p,5)[0]/100,'input_current':struct.unpack_from('>i',p,9)[0]/100,'voltage':struct.unpack_from('>h',p,27)[0]/10,'fault':p[53],'temp_fet':struct.unpack_from('>h',p,1)[0]/10,'duty':struct.unpack_from('>h',p,21)[0]/1000})
        time.sleep(.05)
    report={'mode':'FOC','limits_unchanged':True,'changed_fields':changes,'reboot_persisted':True,'samples':len(samples),'fault_codes':sorted(set(s['fault'] for s in samples)),'voltage_min':min(s['voltage'] for s in samples),'voltage_max':max(s['voltage'] for s in samples),'current_abs_max':max(abs(s['current']) for s in samples),'duty_abs_max':max(abs(s['duty']) for s in samples)}
    (OUT/'idle_verification.json').write_text(json.dumps(report,indent=2))
    (OUT/'idle_samples.json').write_text(json.dumps(samples))
    print(json.dumps(report,indent=2))
    for cmd in ['fault','faults','hw_status']:
        res=l.term(cmd); print(cmd+':\n'+res);(OUT/(cmd+'_verified.txt')).write_text(res)
finally:l.s.close()
