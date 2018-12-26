#! /usr/bin/env python

import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *



##extractcode_start
class PEParser(object):
	def __init__(self,fname):
		fin = open(fname,'rb')
		self.__fname= fname
		self.__data = fin.read()
		fin.close()
		fin = None
		return

	def close(self):
		return



	def func_offset(self,name):
		return -1

	def func_vaddr(self,name):
		return -1

	def func_size(self,name):
		return -1

	def is_in_reloc(self,vaddr,name):
		return True

	def get_data(self):
		return bytes_to_ints(self.__data)

	def get_text_file_off(self,data,rels,symname=''):
		if len(data) != len(rels):
			raise Exception('len(data) [%d] != len(rels)[%d]'%(len(data),len(rels)))
		sbyte = bytes_to_ints(self.__data)
		retoff = -1
		idx = 0
		jdx = 0
		fidx = 0
		while fidx < len(rels):
			if rels[fidx] == 0:
				break
			fidx += 1
		if fidx >= len(rels):
			raise Exception('all rels')
		idx = 0
		while idx < len(sbyte):
			jdx = fidx
			if sbyte[(idx+fidx)] == data[(jdx)]:
				curidx = idx + fidx + 1
				jdx += 1
				while jdx < len(data) and curidx < len(sbyte):
					if rels[jdx] == 0 and \
						data[jdx] != sbyte[curidx]:
						#logging.info('[%s].[+0x%x] [+0x%x] [0x%02x] != [0x%02x]'%(symname,jdx,curidx,data[jdx], sbyte[curidx]))
						break
					jdx += 1
					curidx += 1
				if jdx == len(data):
					if retoff >= 0:
						outexpstr = ''
						outexpstr += 'double match at [%s].[%s]\n'%(self.__fname, symname)
						outexpstr += '%s\n'%(format_bytes_debug(sbyte[retoff:(retoff+len(data))], 'retoff [0x%x:%d]'%(retoff,retoff)))
						outexpstr += '%s'%(format_bytes_debug(sbyte[idx:(idx+len(data))], 'idx [0x%x:%d]'%(idx,idx)))
						raise Exception(outexpstr)
					retoff = idx
			idx += 1
		if retoff < 0:
			raise Exception('can not find [%s] code\nrels\n%s\ndata\n%s\n'%(symname, dump_ints(rels), dump_ints(data)))
		return retoff
##extractcode_end