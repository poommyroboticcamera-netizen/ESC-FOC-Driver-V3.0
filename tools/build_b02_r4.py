from pathlib import Path
p=Path(__file__).resolve().parent/'build_b02.py'
s=p.read_text()
s=s.replace('hw_drv8302_b02.h','hw_drv8302_b02_r4.h')
s=s.replace('build_identity_b02.h','build_identity_b02_r4.h')
s=s.replace('drv8302_b02\'', 'drv8302_b02_r4\'')
s=s.replace('build/drv8302_b02/', 'build/drv8302_b02_r4/')
s=s.replace('build_b02.log','build_b02_r4.log')
s=s.replace('6.00-b02','6.00-b02-r4').replace('+b02"','+b02-r4"')
exec(compile(s,str(p),'exec'))
