from vesc_diag import Link,OUT,fields
import struct,time,json,statistics,sys
label=sys.argv[1]; l=Link();rows=[]
try:
    fw=l.request(0);conf=l.request(14);(OUT/(label+'_mcconf.bin')).write_bytes(conf)
    assert conf[7]==2,'FOC required'
    f=fields(conf)
    result={'hardware':fw[3:].split(b'\0')[0].decode(),'mode':'FOC','abs_limit_A':struct.unpack_from('>f',conf,1+f['l_abs_current_max'][0])[0]}
    result['fault_before']=l.term('fault')
    for batch in range(5):
        l.send(bytes([19,1])+struct.pack('>H',400)+bytes([1,1]))
        block=[]; until=time.monotonic()+4
        while len(block)<400 and time.monotonic()<until:
            p=l.recv(.2)
            if p and p[0]==19:block.append(struct.unpack_from('>8f',p,1))
        rows+=block
        # Flush already-completed capture packets, never a motor command.
        while l.recv(.1):pass
    factor=3.3/4095/.005
    result['samples']=len(rows)
    assert len(rows)>=1500,len(rows)
    for i in [0,1]:
        v=[r[i]*factor for r in rows]
        result['i'+str(i+1)]={'min_A_equivalent':min(v),'max_A_equivalent':max(v),'mean_A_equivalent':statistics.mean(v),'stdev_A_equivalent':statistics.pstdev(v)}
    result['fault_after']=l.term('fault')
    result['fault_history']=l.term('faults')
    (OUT/(label+'_samples.json')).write_text(json.dumps(rows))
    (OUT/(label+'_report.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
finally:l.s.close()
