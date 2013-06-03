#!/usr/bin/env python
# cpu graph (needs gnu/linux, grep, top, tail)
# 2009 mennonite
# public domain
import os
import time
while True:
    f = os.system("top -n 2 | grep -i cpu\(s\) | tail -1 > /tmp/cpugr")
    f = open("/tmp/cpugr")
    ff = f.readlines()
    f.close()
    f = os.system("rm /tmp/cpugr")
    f = "".join(ff)
    ff = f.split("\x1b[") # clean up some of the ansi codes
    f = "".join(ff)
    f = f[:f.find("us")] # left of "us"
    f = f[:f.find(".")] # left of "."
    f = f[f.rfind(" "):] # right of bsearch " "
    f = int(float(int(f)) * 4 / 5) # 80 / 100... 100% = 80 columns
    ff = f
    if f < 0: f = 0
    if f > 79: f = 79 
    print "]" * f
    time.sleep(1)
