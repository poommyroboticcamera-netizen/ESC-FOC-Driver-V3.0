from vesc_diag import Link,OUT,fields
import time,json
l=Link()
try:
    before=l.request(14)
    (OUT/'mcconf_before_foc.bin').write_bytes(before)
    at,n=fields(before)['motor_type']; assert at==6 and n==1
    assert before[1+at]==0, 'Expected BLDC mode'
    after=bytearray(before); after[0]=13; after[1+at]=2
    l.send(bytes(after)); ack=l.recv(3)
    assert ack and ack[0]==13, f'No config ack: {ack}'
    time.sleep(2)
    actual=l.request(14); (OUT/'mcconf_after_foc.bin').write_bytes(actual)
    print('Mode readback:',actual[1+at]); assert actual[1+at]==2
    changes=[i for i,(a,b) in enumerate(zip(before,actual)) if a!=b]
    print('Changed configuration bytes:',changes)
    for cmd in ['fault','faults','hw_status']:
        result=l.term(cmd);print(cmd+':\n'+result);(OUT/(cmd+'_after_foc.txt')).write_text(result)
finally:l.s.close()
