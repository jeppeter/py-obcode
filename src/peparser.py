#! /usr/bin/env python

import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from objparser import *



##extractcode_start
class PEParser(ObjParser):
	def __init__(self,fname):
		ObjParser.__init__(self)
		fin = open(fname,'rb')
		self.__fname= fname
		self.__data = fin.read()
		fin.close()
		fin = None
		return

	def close(self):
		ObjParser.close(self)
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
		return ObjParser.get_text_file_off(self,data,rels,symname,self.__data)

##extractcode_end