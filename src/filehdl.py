#! /usr/bin/env python
import sys
import json
import logging
import re

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

def format_comment_line(l):
    s = ''
    idx = 0
    while idx < len(l):
        if l[idx] == '*':
            s += '\\*'
        elif l[idx] == '/':
            s += '\\/'
        else:
            s += l[idx]
        idx += 1
    return s

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
##extractcode_end
