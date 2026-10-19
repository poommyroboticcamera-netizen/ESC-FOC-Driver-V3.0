import os, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent.parent/'tmp/vesc-firmware-review'
env=os.environ.copy()
env['OS']='Linux'
env['PATH']='C:/Program Files/Git/usr/bin;C:/Users/poomc/.platformio/packages/toolchain-gccarmnoneeabi@1.70201.0/bin;'+env['PATH']
for part in ['obj','lst','.dep']:
    (root/'build/drv8302_b02'/part).mkdir(parents=True,exist_ok=True)
(root/'build_identity_b02.h').write_text('''#define HW_SOURCE "hwconf/other/vesc4/hw_410.c"
#define HW_HEADER "hwconf/other/vesc4/hw_drv8302_b02.h"
#define GIT_BRANCH_NAME "6.00-b02"
#define GIT_COMMIT_HASH "4b822f0f944918957c55391ca0672925153f3fde+b02"
#define ARM_GCC_VERSION "7.2.1"
''')
args=['make','-B','-f','make/fw.mk','-j8','USE_COPT=-Werror','PROJECT=drv8302_b02','BUILDDIR=build/drv8302_b02','TCHAIN_PREFIX=arm-none-eabi-',
      'build_args=-include build_identity_b02.h',
      'SHELL=C:/Program Files/Git/usr/bin/sh.exe']
with open(root/'build_b02.log','w') as log:
    r=subprocess.run(args,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
print('Build exit:',r.returncode)
print((root/'build_b02.log').read_text(errors='replace')[-6000:])
raise SystemExit(r.returncode)
