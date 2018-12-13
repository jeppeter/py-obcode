#! /usr/bin/env python

import re
import logging
import sys
import os
import random


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from cobattr import *
##importdebugend



##extractcode_start
class COBFileBase(object):
    def __init__(self,sfile,dfile,cfg=None):
        self.__define_expr = []
        self.srcfile = sfile
        self.dstfile = dfile
        self.__append_define_expr('^\s*\#\s*define\s+')
        self.__append_define_expr('^\s*\#\s*undef\s+')
        self.__append_define_expr('^\s*\#\s*if\s+')
        self.__append_define_expr('^\s*\#\s*ifdef\s+')
        self.__append_define_expr('^\s*\#\s*ifndef\s+')
        self.__append_define_expr('^\s*\#\s*endif\s+')
        self.__append_define_expr('^\s*\#\s*else\s+')
        self.__append_define_expr('^\s*\#\s*elif\s+')
        if cfg is not None:
            self.base_cfg = cfg
        else:
            self.base_cfg = COBAttr()
        if sfile is not None:
            self.in_lines = get_file_lines(sfile)
        else:
            self.in_lines = []
        self.cur_line = 0
        return

    def __append_define_expr(self,exprstr):
        expr = re.compile(exprstr)
        self.__define_expr.append(expr)
        return

    def get_filter_expr_not_defined(self,l,expr1):
        m = expr1.findall(l)
        if m is not None and len(m) > 0:
            filtered = False
            for expr in self.__define_expr:
                m = expr.findall(l)
                if m is not None and len(m) > 0:
                    logging.info('[match] %s'%(m[0]))
                    filtered = True
                    break
            if not filtered:
                return True
        return False


    def get_variables(self,l,expr1):
        variables = expr1.findall(l)
        # we do this on the increment
        logging.info('[%d][%s] variables[%d]'%(self.cur_line,l, len(variables)))
        assert(len(variables) == 1)
        assert(len(variables[0]) > 1)
        cfgattr = self.base_cfg
        logging.info('v [%s]'%(variables[0][1]))
        sbyte = string_to_ints(variables[0][1])
        params, lbyte = parse_param(sbyte)
        before = l.replace(variables[0][0],'',1)
        return cfgattr,params,before,ints_to_string(lbyte)


    def get_spec_config_variables(self,l,expr1):
        leftvars = []
        cfgattr = None
        variables = expr1.findall(l)
        assert(len(variables) == 1)
        assert(len(variables[0]) > 1)
        sbyte = string_to_ints(variables[0][1])
        params,lbyte = parse_param(sbyte)
        if len(params) < 1:
            raise Exception('at [%d] line [%s] not valid for specific'%(self.cur_line,l))
        after = ints_to_string(lbyte)
        cfgstr,lbyte = parse_raw_string(string_to_ints(params[0]))
        cfgstr = ints_to_string(cfgstr)
        logging.info('cfgstr [%s]'%(cfgstr))
        cfgattr = self.base_cfg.get_file_config(cfgstr)
        retparams = []
        if len(params) > 1:
            retparams = params[1:]
        before = l.replace(variables[0][0],'',1)
        return cfgattr,retparams, before,after

    def __format_one_variable_handle(self,varname,ptrvar,obaddrvar,szvar,pcvar,tabs):
        cbytes = get_random_bytes(8)
        ccidx = []
        for i in range(8):
            ccidx.append(i)
        curbytes = []
        curidx = []
        rets=''
        rets += format_line('', tabs)
        rets += format_debug_line('to handle %s variable'%(varname),tabs,3)
        rets += format_debug_line('format %s xors'%(format_bytes_c(cbytes)), tabs, 3)
        rets += format_line('%s = (void*)&%s;'%(ptrvar,varname), tabs)
        rets += format_line('%s = (OB_ADDR)%s;'%(obaddrvar,ptrvar), tabs)        
        rets += format_line('%s = sizeof(%s);'%(szvar,obaddrvar), tabs)
        rets += format_line('%s = (unsigned char*)%s;'%(pcvar,obaddrvar), tabs)

        rets += format_line('', tabs)
        rets += format_debug_line('encoding', tabs, 3)
        while len(cbytes) > 0:
            idx = random.randint(0,len(cbytes) - 1)
            curidx.append(ccidx[idx])
            del ccidx[idx]
            curbytes.append(cbytes[idx])
            del cbytes[idx]
            rets += format_line('if (%d < %s){'%(curidx[-1],szvar), tabs) 
            rets += format_line('%s[%d] ^= 0x%x;'%(pcvar,curidx[-1],curbytes[-1]), tabs + 1)
            rets += format_line('}', tabs)

        rets += format_line('', tabs)
        rets += format_debug_line('decoding', tabs, 3)
        cbytes.extend(curbytes)
        curbytes = []
        ccidx.extend(curidx)
        curidx = []
        while len(cbytes) > 0:
            idx = random.randint(0,len(cbytes) - 1)
            curidx.append(ccidx[idx])
            del ccidx[idx]
            curbytes.append(cbytes[idx])
            del cbytes[idx]
            rets += format_line('if (%d < %s){'%(curidx[-1],szvar), tabs) 
            rets += format_line('%s[%d] ^= 0x%x;'%(pcvar,curidx[-1],curbytes[-1]), tabs + 1)
            rets += format_line('}', tabs)

        # now to give the value
        rets += format_line('%s = *((OB_TYPEOF(%s)*)%s);'%(varname,varname,pcvar), tabs)

        return rets

    def expand_code(self,l,params,cfg,before,after):
        rets = ''
        obaddrvar = get_random_name(random.randint(cfg.namemin,cfg.namemax))
        ptrvar = get_random_name(random.randint(cfg.namemin,cfg.namemax))
        pcvar = get_random_name(random.randint(cfg.namemin,cfg.namemax))
        szvar = get_random_name(random.randint(cfg.namemin,cfg.namemax))
        tabs = count_tabs(l)
        rets += format_line('do{', tabs)
        rets += format_line('void* %s;'%(ptrvar),tabs + 1)
        rets += format_line('OB_ADDR %s;'%(obaddrvar), tabs + 1)
        rets += format_line('unsigned char* %s;'%(pcvar), tabs + 1)
        rets += format_line('unsigned int %s;'%(szvar), tabs + 1)
        idx = 0
        while idx < len(params):
            rets += self.__format_one_variable_handle(params[idx],ptrvar,obaddrvar,szvar,pcvar,tabs + 1)
            idx += 1
        rets += format_line('', tabs+1)
        rets += format_line('}while(0);', tabs)
        return rets
##extractcode_end