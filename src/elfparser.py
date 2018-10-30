#! /usr/bin/env python

import logging
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

##extractcode_start

class ElfParser(object):
	def __init__(self,fname):
		if sys.version[0] == '3':
			self.__fin = open(fname,'rb')
		else:
			self.__fin = open(fname,'r')
		self.__fname= fname
		self.__elffile = ELFFile(self.__fin)
		return

	def _vaddr_to_off(self,vaddr,name=''):
		for section in self.__elffile.iter_sections():
			if vaddr >= section['sh_addr']  and \
				vaddr <= (section['sh_addr'] + section['sh_size']):
				return (vaddr - section['sh_addr']) + section['sh_offset']
		raise Exception('[%s]get [%s] vaddr[0x%x] not in size'%(self.__fname,name,vaddr))

	def func_offset(self,name):
		for symtab in self.__elffile.iter_sections():
			if not isinstance(symtab,SymbolTableSection):
				continue
			for sym in symtab.iter_symbols():
				if sym.name == name:
					vaddr = sym['st_value']
					return self._vaddr_to_off(vaddr,name)
		raise Exception('[%s]can not found [%s]'%(self.__fname,name))


	def func_size(self,name):
		for symtab in self.__elffile.iter_sections():
			if not isinstance(symtab,SymbolTableSection):
				continue
			for sym in symtab.iter_symbols():
				if sym.name == name:
					return sym['st_size']
		raise Exception('[%s]can not found [%s]'%(self.__fname,name))


##extractcode_end
