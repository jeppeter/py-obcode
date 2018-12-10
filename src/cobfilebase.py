#! /usr/bin/env python

import re
import logging
import sys
import os


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from filehdl import *
from cobattr import *
##importdebugend



##extractcode_start
class COBFileBase(object):
    def __init__(self,sfile,dfile,cfg=None):
        self.__define_expr = []
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
            self.base_cfg = CompoundAttr()
        self.in_lines = get_file_lines(sfile)
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
##extractcode_end