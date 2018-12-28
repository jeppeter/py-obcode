#! /usr/bin/env python

import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from objparser import *


##extractcode_start

OBJ_RELOC_NONE=0
OBJ_RELOC_ON=1
OBJ_RELOC_FORBID=2

class ObjParser(object):
	def __init__(self):
		self.dataoffdict = None
		self.sbyte = []
		return

	def close(self):
		if self.dataoffdict is not None:
			self.dataoffdict = None
			self.sbyte = []
		return


	def prepare_offdict(self,data):
		if self.dataoffdict is None:
			self.sbyte = bytes_to_ints(data)
			self.dataoffdict = dict()
			pos = 0
			while pos < len(self.sbyte):
				curbyte = self.sbyte[pos]
				if curbyte not in self.dataoffdict.keys():
					self.dataoffdict[curbyte] = []
				self.dataoffdict[curbyte].append(pos)
				pos += 1
		return

	def get_text_file_off(self,data,rels,symname,datas):
		if len(data) != len(rels):
			raise Exception('len(data) [%d] != len(rels)[%d]'%(len(data),len(rels)))
		self.prepare_offdict(datas)
		firstbyte = None
		fidx = 0
		while fidx < len(rels):
			if rels[fidx] == 0:
				break
			fidx += 1
		if fidx >= len(rels):
			raise Exception('all rels')
		firstbyte = data[fidx]
		retoff = -1
		if firstbyte in self.dataoffdict.keys():
			posarr = self.dataoffdict[firstbyte]
			idx = 0
			while idx < len(posarr):
				curpos = posarr[idx]
				if curpos >= fidx and (curpos + len(rels) - fidx) < len(self.sbyte):
					jdx = fidx
					while jdx < len(rels):
						if rels[jdx] == 0 and self.sbyte[(curpos + jdx - fidx)] != data[jdx]:
							logging.info('[%s].[+0x%x] [+0x%x] [0x%02x] != [0x%02x]'%(symname,jdx,(curpos + jdx - fidx),data[jdx], self.sbyte[(curpos+jdx - fidx)]))
							break
						jdx += 1
					if jdx == len(rels):
						if retoff >= 0:
							outexpstr = ''
							outexpstr += 'double match at [%s].[%s]\n'%(self.__fname, symname)
							outexpstr += '%s\n'%(format_bytes_debug(self.sbyte[retoff:(retoff+len(data))], 'retoff [0x%x:%d]'%(retoff,retoff)))
							outexpstr += '%s'%(format_bytes_debug(self.sbyte[(curpos-fidx):(curpos+len(data) - fidx)], 'idx [0x%x:%d]'%(curpos - fidx,curpos - fidx)))
							raise Exception(outexpstr)
						retoff = (curpos - fidx)
				idx += 1
		if retoff < 0:
			raise Exception('can not find [%s] code\nrels\n%s\ndata\n%s\n'%(symname, dump_ints(rels), dump_ints(data)))
		return retoff


##extractcode_end