#! /usr/bin/env python

import sys
import os


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from fmthdl import *
##importdebugend


##extractcode_start
class MixedString(object):
    def __get_bytes(self,size):
        rb = []
        for i in range(size):
            rb.append(random.randint(0,255))
        return rb

    def __get_func(self,sbyte):
        return format_bytes_set_function(sbyte,self.__cfg.prefix, \
                random.randint(self.__cfg.namemin,self.__cfg.namemax), \
                random.randint(len(sbyte),len(sbyte)*2), \
                0,self.__cfg.debug,self.__line)

    def __init__(self,sbyte,cfg,line=None):
        self.__sbyte = sbyte
        self.__iswide = False
        self.__cfg = cfg
        self.__line = line
        if len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
            self.__iswide = True
        self.__abyte = self.__get_bytes(len(sbyte))
        self.__bbyte = self.__get_bytes(len(sbyte))
        self.__afuncstr ,self.__afuncname = self.__get_func(self.__abyte)
        self.__bfuncstr , self.__bfuncname = self.__get_func(self.__bbyte)
        self.__sfuncstr , self.__sfuncname = format_bytes_xor_function(sbyte, \
                self.__abyte, self.__afuncname, \
                self.__bbyte, self.__bfuncname, \
                self.__cfg.prefix, \
                random.randint(self.__cfg.namemin,self.__cfg.namemax), \
                random.randint(len(sbyte),len(sbyte)*2), \
                0,self.__cfg.debug, self.__line)
        #logging.info('afunc [%s] bfunc [%s] name [%s] hash [%s]'%(self.__afuncname, \
        #    self.__bfuncname, self.__sfuncname, self.__get_hash(self.__sbyte)))
        return

    def __get_hash(self,sbyte):
        return get_bytes_hash(sbyte)

    def __getattr__(self,keyname):
        if keyname == 'sbyte':
            return self.__sbyte
        elif keyname == 'iswide':
            return self.__iswide
        elif keyname == 'afunc':
            return self.__afuncstr
        elif keyname == 'bfunc':
            return self.__bfuncstr
        elif keyname == 'func':
            return self.__sfuncstr
        elif keyname == 'funcname':
            return self.__sfuncname
        elif keyname == 'hash':
            return self.__get_hash(self.__sbyte)
        else:
            if keyname in self.__dict__.keys():
                return self.__dict__[keyname]
            else:
                raise Exception('not support [%s]'%(keyname))

    def hash_number(self,sbyte):
        return self.__get_hash(sbyte)

    def equal_byte(self,sbyte):
        if len(sbyte) != len(self.__sbyte):
            return False
        for i in range(len(sbyte)):
            if sbyte[i] != self.__sbyte[i]:
                return False
        return True

class MixedStrVariable(object):
    def __init__(self,dc):
        self.__dict = dict()
        self.__dc = dc
        return

    def add_bytes(self,sbyte,cfg):        
        # to check whether the name in the handle
        for k in self.__dict.keys():
            s = self.__dict[k]
            if s.equal_byte(sbyte):
                return k, None
        # now we do not have this ,so we should 
        # find out
        s = MixedString(sbyte, cfg)
        hn = '%s'%(s.hash)
        if hn not in self.__dc.keys():
            raise Exception('can not find [%s] for insert'%(sbyte))
        for k in self.__dc[hn]:
            if k.equal_byte(sbyte):
                name = get_random_name(random.randint(cfg.namemin,cfg.namemax))
                self.__dict[name] = k
                return name, k.funcname
        raise Exception('can not found %s bytes'%(sbyte))   

if sys.platform == 'win32':
    GL_INIT_ATTR={
        'prefix' : 'prefix',
        'namemin' : 5,
        'namemax' : 20,
        'funcmin' : 3,
        'funcmax' : 30,
        'xorsize' : 16,
        'maxround': 32,
        'debug' : 0,
        'noline' : 0,
        'unicodewidth' : 16,
        'widechartype' : 'wchar_t'
    }
else:
    GL_INIT_ATTR={
        'prefix' : 'prefix',
        'namemin' : 5,
        'namemax' : 20,
        'funcmin' : 3,
        'funcmax' : 30,
        'xorsize' : 16,
        'maxround': 32,
        'debug' : 0,
        'noline' : 0,
        'unicodewidth' : 32,
        'widechartype' : 'wchar_t'
    }

GL_DEFAULT_ATTR=GL_INIT_ATTR

class COBAttr(object):
    def __trans_number(self,vstr):
        retv = vstr
        if self.__float_expr.match(vstr):
            retv = float(vstr)
        elif self.__dec_expr.match(vstr):
            retv = int(vstr)
        return retv

    def __prepare_attr(self,attrs=None):
        v = attrs
        if attrs is not None and isinstance(attrs, str):
            sarr = re.split(',', attrs)
            v = dict()
            for c in sarr:
                varr = re.split('=', c)
                if len(varr) > 1:
                    v[varr[0]] = self.__trans_number(varr[1])
                else:
                    v[varr[0]] = None
        elif attrs is not None and not isinstance(attrs, dict):
            raise Exception('attrs [%s] not valid type'%(attrs))
        if v is not None:
            for k in v.keys():
                if k not in self.__obj.keys():
                    self.__obj[k] = v[k]
        return

    def __check_value(self):
        if self.namemin > self.namemax:
            raise Exception('namemin [%d] > namemax [%d]'%(self.namemin,self.namemax))
        if self.xorsize <= 0:
            raise Exception('xorsize [%s] < 0'%(self.xorsize))

        if self.maxround <= 0:
            raise Exception('maxround [%d] < 0'%(self.maxround))

        if len(self.prefix) == 0:
            raise Exception('prefix [] empty')
        #logging.info('funcmin [%s] funcmax [%s]'%(self.funcmin,self.funcmax))
        if self.funcmin > self.funcmax or self.funcmin < 0 or self.funcmax <= 0:
            raise Exception('funcmin [%d] or funcmax [%d] not valid'%(self.funcmin, self.funcmax))
        return

    def format_values(self):
        global GL_INIT_ATTR
        s = ''
        for k in GL_INIT_ATTR.keys():
            if len(s) > 0:
                s += ','
            s += '%s=%s'%(k,GL_INIT_ATTR[k])
        return s


    def __init__(self,attrs=None,news=None):
        global GL_DEFAULT_ATTR
        self.__obj = dict()
        self.__dec_expr = re.compile('^[-+]?[0-9]+$')
        self.__float_expr = re.compile('^[-+]?[0-9]\.[0-9]+$')
        self.__prepare_attr(attrs)
        self.__prepare_attr(news)
        self.__prepare_attr(GL_DEFAULT_ATTR)
        self.__check_value()
        return

    def __getattr__(self,k):
        if k in self.__obj.keys():
            return self.__obj[k]
        return None


class CompoundAttr(COBAttr):
    def __inc_prefix(self):
        self.__basic_inc += 1
        s = '%s_%d'%(self.__basic_prefix,self.__basic_inc)
        #logging.info('prefix [%s]'%(s))
        return s

    def __init__(self,attrs=None):
        self.__basiccfg = COBAttr(attrs,None)
        self.__filecfg = None
        self.__basic_prefix = '%s'%(self.__basiccfg.prefix)
        self.__basic_inc = 0
        d = dict()
        d['prefix'] = self.__inc_prefix()
        self.__basiccfg = COBAttr(attrs,d)
        return

    def __getattr__(self,k):
        return self.__basiccfg.__getattr__(k)

    def load_file(self,f):
        retval = False
        try:
            s = read_file(f)
            # now to pass 
            d = json.loads(s)
            self.__filecfg = Utf8Encode(d).get_val()
            self.__filecfg = d
            retval = True
        except:
            pass
        return retval

    def get_file_config(self,name):
        retval = None
        #logging.info('id <%s>'%(self))
        if self.__filecfg is not None and \
            name in self.__filecfg.keys():
            retval = COBAttr(self.__filecfg[name],None)
        elif isinstance(name,str):
            retval = COBAttr(name,None)
        else:
            retval = COBAttr(None,None)
        return retval

    def load_new_prefix(self):
        self.__inc_prefix()
        d = dict()
        d['prefix'] = '%s_%d'%(self.__basic_prefix,self.__basic_inc)
        s = self.__basiccfg.format_values()
        self.__basiccfg = COBAttr(s,d)
        return self

    def get_count(self):
        return self.__basic_inc

def format_object_string(odict,tabs):
    s = json.dumps(odict,indent=4)
    #logging.info('s\n%s'%(s))
    sarr = re.split('\n', s)
    idx = 1
    rets = ''
    while idx < (len(sarr) - 1):
        curs = sarr[idx]
        curs = curs.rstrip('\r\n')
        if idx == (len(sarr) - 2):
            rets += format_tabs(tabs)
            rets += '%s'%(curs)
        else:
            rets += format_line('%s'%(curs), tabs)
        idx += 1    
    return rets


def set_default_cob_attr(args):
    global GL_DEFAULT_ATTR
    global GL_INIT_ATTR
    for k in GL_INIT_ATTR.keys():
        nk = 'cob_%s'%(k)
        v = args.__getattr__(nk)
        GL_DEFAULT_ATTR[k] = v
    return


def format_cob_config(tabs):
    global GL_INIT_ATTR
    return format_object_string(GL_INIT_ATTR, tabs)

##extractcode_end