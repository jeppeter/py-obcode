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
        logging.info('afunc [%s] bfunc [%s] name [%s] hash [%s]'%(self.__afuncname, \
            self.__bfuncname, self.__sfuncname, self.__get_hash(self.__sbyte)))
        return

    def __get_hash(self,sbyte):
        cval = 0
        for s in sbyte:
            cval += s
            # 113 is the prime number
            cval *= 113
            # 104729 is the prime number
            cval = cval % 104729
        return cval

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
##extractcode_end