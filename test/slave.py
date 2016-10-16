#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


import subprocess
import shlex
import time

cmd = 'dzen2 -fn Terminus -bg #333333 -fg #ffffff -x 0 -y 0 -w 1920 -h 24'
args = shlex.split(cmd)
p = subprocess.Popen(args, stdin=subprocess.PIPE)

msg = 'hello world\n'
bmsg = bytes(msg,'UTF-8')
if False:
    p.communicate(input=bmsg)
else:
    p.stdin.write(bmsg)
    p.stdin.flush()
    # p.wait()
    time.sleep(3)
    p.terminate()
