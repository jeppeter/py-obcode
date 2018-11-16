#! /usr/bin/env python

import sys
import os
import disttools

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from pyparser import *


def make_string_slash_ok(s):
    sarr = re.split('\n', s)
    rets = ''
    for l in sarr:
        l = l.rstrip('\r\n')
        cexpr = None
        if len(l) > 0 and l[-1] == '\\':
            cexpr = get_random_name(20)
            cont = True
            while cont:
                cont = False
                matchl = re.sub(cexpr, '', l)
                if matchl != l:
                    cont = True
                    cexpr = get_random_name(20)
            l = re.sub('\\$', cexpr, l)
        l = re.sub(r'\\', r'\\\\', l)
        if cexpr is not None:
            l = re.sub(cexpr, r'\\', l)
        rets += '%s\n'%(l)
    return rets

def get_import_file(fname):
    rets = ''
    started = False
    with open(fname,'r+b') as f:
        for l in f:
            if sys.version[0] == '3':
                l = l.decode('utf8')                
            l = l.rstrip('\r\n')
            if not started:
                if l.startswith('##extractcode_start'):
                    started = True
            else:
                if l.startswith('##extractcode_end'):
                    started = False
                else:
                    rets += l
                    rets += '\n'
    return rets

def make_filters_out(ims,files):
    cont = True
    jdx = 0
    idx = 0
    while cont:
        cont = False
        idx = 0
        while idx < len(ims) and not cont:
            jdx = 0
            while jdx < len(files) and not cont:
                if ims[idx].frommodule == files[jdx]:
                    cont = True
                    logging.info('del [%d] jdx [%d] [%s]'%(idx,jdx,ims[idx]))
                    del ims[idx]
                    logging.info('%s'%(ims))
                    break
                jdx += 1                
            idx += 1
    return ims

def fromat_ext_import_files(origfile,files):
    curbase = re.sub('\.py$','',os.path.basename(origfile))
    allims = []
    for f in files:
        allims.extend(get_import_names(f))

    curims= get_import_names(origfile)
    curims = packed_import(curims)
    curims = make_filters_out(curims, files)
    logging.info('curims %s'%(curims))
    allims = packed_import(allims)
    allims = make_filters_out(allims, files)
    logging.info('allims %s'%(allims))
    cont = True
    seccont = True
    while cont:
        cont = False
        idx = 0
        while idx < len(allims) :
            jdx = 0
            while jdx < len(curims) :
                if allims[idx].frommodule == curims[jdx].frommodule and \
                    allims[idx].module == curims[jdx].module:
                    cont = True
                    #logging.info('del [%d] %s'%(idx,allims[idx]))
                    del allims[idx]
                    break
                jdx += 1
            if cont:
                break
            idx += 1
    rets = ''
    for m in allims:
        rets += '%s\n'%(format_import(m))
    return rets
