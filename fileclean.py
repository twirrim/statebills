#!/usr/bin/env python

from shutil import move
import re

def sedish(filename,fromstr,tostr):
    tempname = "%s.tmp" % filename
    with open(tempname, "w") as out:
        for line in open(filename):
            if line.strip():
                out.write(re.sub(fromstr,tostr,line))
    move(tempname,filename)

def cleanup(filename):
    sedish(filename,"\r\n","\n")
    sedish(filename,"<br>","\n")
    sedish(filename,r' <A HREF=\"(.*)\">.*</A>',r',"\1"')
    sedish(filename,r'(AM|PM)\s*\d*',r'\1"')
    sedish(filename,r'^\s*(\w)',r'"\1')
    sedish(filename,r'^<.*',r'')
    sedish(filename,"","")
