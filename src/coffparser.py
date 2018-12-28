#! /usr/bin/env python

import coff
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from objparser import *


##extractcode_start

class CoffParser(ObjParser):
	def __init__(self,fname):
		ObjParser.__init__(self)
		self.__coff = coff.Coff(fname)
		self.__symvalues = dict()
		self.__symnames = dict()
		self.__relocvalues = dict()
		for k in self.__coff.symtables.keys():
			self.__symvalues[k] = []
			self.__symnames[k] = []
			self.__symvalues[k] = sorted(self.__coff.symtables[k], key = lambda sym: sym.value)
			self.__symnames[k] = sorted(self.__coff.symtables[k], key = lambda sym: sym.name)
		for k in self.__coff.relocs.keys():
			self.__relocvalues[k] = []
			self.__relocvalues[k] = sorted(self.__coff.relocs[k], key = lambda rel: rel.vaddr)
			#logging.info('[%s] size [%s]'%(k,len(self.__relocvalues[k])))
			#if len(self.__relocvalues[k]) > 0:
			#	logging.info('[0].%s [-1].%s'%(self.__relocvalues[k][0], self.__relocvalues[k][-1]))
		self.__data = []
		if sys.version[0] == '3':
			fin = open(fname,'rb')
		else:
			fin = open(fname,'r')
		self.__data = fin.read()
		fin.close()
		fin = None
		return

	def close(self):
		ObjParser.close(self)
		return


	def _find_sym(self,name,symtbl):
		minidx = 0
		maxidx = len(symtbl) -1
		while minidx < maxidx:
			curidx = int((minidx + maxidx) / 2)
			if symtbl[curidx].name == name:
				return symtbl[curidx]
			elif symtbl[minidx].name == name:
				return symtbl[minidx]
			elif symtbl[maxidx].name == name:
				return symtbl[maxidx]
			if symtbl[curidx].name > name:
				maxidx = curidx
			elif symtbl[curidx].name < name:
				minidx = curidx
			if (minidx + 1) >= maxidx:
				break
		if symtbl[minidx].name == name:
			return symtbl[minidx]
		elif symtbl[maxidx].name == name:
			return symtbl[maxidx]
		return None

	def _func_off(self,name):
		if self.__coff is None:
			return -1
		for k in self.__symnames.keys():
			sym = self._find_sym(name,self.__symnames[k])
			if sym is not None:				
				return sym
		return None

	def func_offset(self,name):
		sym = self._func_off(name)
		if sym is None:
			return -1
		sections = self.__coff.sections
		idx = int(sym.sectnum)
		assert(idx <= len(sections))
		#logging.info('sections [%d] %s'%(idx,sections[(idx-1)]))
		return sym.value + sections[(idx-1)].offdata


	def func_vaddr(self,name):
		sym = self._func_off(name)
		if sym is None:
			return -1
		return sym.value

	def func_size(self,name):
		if self.__coff is None:
			return -1
		for k in self.__symnames.keys():
			sym = self._find_sym(name,self.__symnames[k])
			if sym is not None:
				return sym.size 
		return -1

	def _is_in_rel(self,rel,vaddr):
		if vaddr < rel.vaddr:
			return False
		if vaddr >= (rel.vaddr + rel.size):
			return False
		#logging.info('vaddr [0x%x]%s'%(vaddr, rel))
		return True

	def _find_rel_in(self,reltbl,vaddr):
		minidx = 0
		maxidx = len(reltbl) - 1
		while minidx < maxidx:
			curidx = int((minidx + maxidx) /2)
			if self._is_in_rel(reltbl[curidx],vaddr):
				return reltbl[curidx]
			elif self._is_in_rel(reltbl[minidx],vaddr):
				return reltbl[minidx]
			elif self._is_in_rel(reltbl[maxidx], vaddr):
				return reltbl[maxidx]
			if vaddr < reltbl[curidx].vaddr:
				maxidx = curidx
			else:
				minidx = curidx
			if (minidx+1) >= maxidx:
				break
		if self._is_in_rel(reltbl[minidx],vaddr):
			return reltbl[minidx]
		elif self._is_in_rel(reltbl[maxidx], vaddr):
			return reltbl[maxidx]
		return None

	def _is_forbid_rel(self,relinfo):
		if self.__coff.header.id != 0x14c:
			return False
		if relinfo.type == coff.IMAGE_REL_I386_DIR32:
			return True
		return False


	def is_in_reloc(self,vaddr,name):
		if self.__coff is None:
			return OBJ_RELOC_FORBID
		findsym = None
		findk = None
		for k in self.__symnames.keys():
			sym = self._find_sym(name,self.__symnames[k])
			if sym is not None:
				findsym = sym
				findk = k
				break
		if findsym is None:
			return OBJ_RELOC_NONE

		if vaddr < findsym.value or vaddr >= (findsym.value + findsym.size):
			return OBJ_RELOC_FORBID
		if len(self.__relocvalues[findk]) > 0:
			#logging.info('reloc [%s] len(%s) [%s] [%s] [%s]'%(findk, len(self.__relocvalues[findk]), self.__relocvalues[findk][0], self.__relocvalues[findk][-1], name))
			pass
		else:
			# nothing to find ,so no reloc
			return OBJ_RELOC_NONE

		relinfo = self._find_rel_in(self.__relocvalues[findk], vaddr)
		if relinfo is None:
			return OBJ_RELOC_NONE
		if self._is_forbid_rel(relinfo):
			return OBJ_RELOC_FORBID
		return OBJ_RELOC_ON

	def get_data(self):
		return bytes_to_ints(self.__data)

	def get_text_file_off(self,data,rels,symname=''):
		return ObjParser.get_text_file_off(self,data,rels,symname,self.__data)

##extractcode_end