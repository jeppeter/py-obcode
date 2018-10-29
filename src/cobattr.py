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
        'unicodewidth' : 16
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
        'unicodewidth' : 32
    }

GL_DEFAULT_ATTR={}

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
        logging.info('funcmin [%s] funcmax [%s]'%(self.funcmin,self.funcmax))
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
        logging.info('prefix [%s]'%(s))
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
        logging.info('id <%s>'%(self))
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
##extractcode_end