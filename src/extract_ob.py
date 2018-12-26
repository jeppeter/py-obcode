#! /usr/bin/env python

import re
import logging
import sys
import os


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
##importdebugend


##extractcode_start
class ExtractOb(object):
	def __init__(self,infile=None):
		s = read_file(infile)
		self.__lines = []
		for l in re.split('\n',s):
			l = l.rstrip('\r\n')
			self.__lines.append(l)
		return

	def __get_ob_func(self,funcname):
		retfunc = funcname
		rstr = '^\s*#\s*define\s+%s\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$'%(funcname)
		#logging.info('rstr [%s]'%(rstr))
		expr = re.compile(rstr)
		for l in self.__lines:
			m = expr.findall(l)
			#logging.info('[%s] [%s] ret[%s]'%(l,funcname,m))
			if m is not None and len(m) > 0:
				retfunc = m[0]
				break
		return retfunc

	def get_ob_funcs(self,funcs=[]):
		retfuncs = dict()
		for f in funcs:
			retfuncs[f] = self.__get_ob_func(f)
		return retfuncs

##extractcode_end