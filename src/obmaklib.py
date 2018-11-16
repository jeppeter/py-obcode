#! /usr/bin/env python

import sys
import os
import shutil

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
##importdebugend


##extractcode_start
GL_MAKOB_FILE_VAR='MAKOB_FILE'

def get_makeob_file(fname,makeobfile,args):
    retf = ''
    cdict = dict()
    if os.path.exists(makeobfile):
        s = read_file(makeobfile)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
    if fname in fdict.keys():
        retf = fdict[fname]
    else:
        valid = False
        while not valid :
            valid = True
            retf = os.path.join(os.path.dirname(fname),get_random_name(random.randint(args.makob_namemin,args.makob_namemax)))
            fc, extf = os.path.splitext(fname)
            retf += extf
            for k in fdict.keys():
                if fdict[k] == retf:
                    valid = False
        # now to write back
        fdict[fname] = retf
        cdict['files'] = fdict
        write_file(json.dumps(cdict, indent=4), makeobfile)
    # if exists fname and not exists retf just copy
    if os.path.exists(fname) and not os.path.exists(retf):
        shutil.copy2(fname, retf)
    return retf

def makob_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    makeobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makeobfile = os.environ[GL_MAKOB_FILE_VAR]
    rets = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        retf = get_makeob_file(c,makeobfile,args)
        if len(rets) > 0:
            rets += ' '
        rets += retf
    sys.stdout.write('%s\n'%(rets))
    sys.exit(0)
    return

def obtrans_file_inner(fname,args):
    cdict = dict()
    if os.path.exists(fname):
        s = read_file(fname)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    if 'files' in cdict.keys():
        fdict = cdict['files']
        sortkeys = sorted(fdict.keys())
        idx = 0
        while idx < len(sortkeys):
            ok = sortkeys[idx]
            ov = fdict[ok]
            k = re.sub(args.obtrans_srcdir, args.obtrans_dstdir, ok)
            v = re.sub(args.obtrans_srcdir, args.obtrans_dstdir, ov)
            k = os.path.abspath(k)
            v = os.path.abspath(v)
            fdict[k] = v
            del fdict[ok]
            idx += 1
        # now rewrite back to files
        cdict['files'] = fdict
        write_file(json.dumps(cdict,indent=4), fname)
    return

def obtrans_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        obtrans_file_inner(c, args)
    sys.exit(0)
    return

def get_unmakob_file(fname,makeobfile,args):
    retf = fname
    cdict = dict()
    if os.path.exists(makeobfile):
        s = read_file(makeobfile)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
    if fname in fdict.values():
        for k in fdict.keys():
            if fdict[k] == fname:
                retf = k
                break
    if args.unmakob_short:
        retf = os.path.basename(retf)
    return retf


def unmakob_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    makeobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makeobfile = os.environ[GL_MAKOB_FILE_VAR]
    s = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        rets = get_unmakob_file(c,makeobfile,args)
        if len(s) > 0:
            s += ' '
        s += rets
    sys.stdout.write('%s\n'%(s))
    sys.exit(0)
    return

def get_ob_list(fname,args,parser):
    rets = ''
    cdict = dict()
    with open(fname) as fin:
        try:
            cdict = json.load(fin)
        except:
            cdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
        for k in fdict.keys():
            rets += '%s\n'%(fdict[k])
    return rets

def oblist_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    if len(args.subnargs) == 0:
        makobfile = os.path.join(os.getcwd(),'makob.json')
        if GL_MAKOB_FILE_VAR in os.environ.keys():
            makobfile = os.environ[GL_MAKOB_FILE_VAR]
        rets = get_ob_list(makobfile, args, parser)
        sys.stdout.write('%s'%(rets))
    else:
        for c in args.subnargs:
            rets = get_ob_list(c, args, parser)
            sys.stdout.write('%s'%(rets))
    sys.exit(0)
    return

def obuntrans_inner(fname,makobfile,args):
    rets= ''
    ins = read_file(fname)
    sarr = re.split('\n', ins)
    cdict = dict()
    with open(makobfile) as fin:
        try:
            cdict = json.load(fin)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']

    for l in sarr:
        l = l.rstrip('\r\n')
        for k in fdict.keys():
            v = fdict[k]
            ck = os.path.basename(k)
            cv = os.path.basename(v)
            logging.info('ck [%s] cv [%s]'%(ck,cv))
            l = re.sub(cv, ck, l)
            s1 = re.split('\.', ck)
            ok = s1[0]
            s2 = re.split('\.', cv)
            ov = s2[0]
            l = re.sub(ov, ok, l)
        rets += '%s\n'%(l)

    return rets

def obuntrans_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('need at least one put file')

    fname = args.subnargs[0]
    outfile = None
    if len(args.subnargs) > 1:
        outfile = args.subnargs[1]
    makobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makobfile = os.environ[GL_MAKOB_FILE_VAR]
    rets = obuntrans_inner(fname, makobfile, args)
    write_file(rets,outfile)
    sys.exit(0)
    return


def basename_handler(args,parser):
    set_logging_level(args)
    s = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        rets = os.path.basename(c)
        if len(s) > 0:
            s += ' '
        s += rets
    sys.stdout.write('%s\n'%(s))
    sys.exit(0)
    return
##extractcode_end