#! /usr/bin/env python
import sys
import json
import logging
import re
import os
import sys


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from fmthdl import *
##importdebugend


##extractcode_start
def read_file(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    rets = ''
    for l in fin:
        s = l
        if 'b' in fin.mode:
            if sys.version[0] == '3':
                s = l.decode('utf-8')
        rets += s

    if fin != sys.stdin:
        fin.close()
    fin = None
    return rets

def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'w+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 

def append_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'a+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 


def get_file_lines(sfile=None):
    rets = read_file(sfile)
    retsarr = []
    sarr = re.split('\n', rets)
    for c in sarr:
        c = c.rstrip('\r\n')
        retsarr.append(c)
    return retsarr


def count_tabs(l):
    tabs = 0
    idx =0
    curspace = 0
    while idx < len(l):
        c = l[idx]
        if c == ' ':
            curspace += 1
            if curspace == 4:
                tabs += 1
                curspace = 0
        elif c == '\t':
            tabs += 1
        else:
            break
        idx += 1
    return tabs

def make_dir_safe(ddir):
    try:
        os.makedirs(ddir)
    except Exception as e:
        if os.path.isdir(ddir):
            return
        raise e
    return

def raw_copy(sfile,dfile):
    make_dir_safe(os.path.dirname(dfile))
    #logging.info('[%s] => [%s]'%(sfile,dfile))
    shutil.copy2(sfile, dfile)
    return

def get_file_filter(sdir,suffixes=['.py']):
    filters = []
    absdir = os.path.abspath(sdir)
    for root, dirs, files in os.walk(absdir):
        if root == absdir:
            for f in files:
                for s in suffixes:
                    if f.endswith(s):                        
                        filters.append(re.sub('%s$'%(s),'',f))
    return filters
##extractcode_end
