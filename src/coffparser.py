#! /usr/bin/env python

import coff
import logging


##extractcode_start

class CoffParser(object):
	def __init__(self,fname):
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
		return

	def close(self):
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
				return sym.value
		return -1

	def func_offset(self,name):
		return self._func_off(name)


	def func_vaddr(self,name):
		return self._func_off(name)

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
		logging.info('vaddr [0x%x]%s'%(vaddr, rel))
		return True

	def _find_rel_in(self,reltbl,vaddr):
		minidx = 0
		maxidx = len(reltbl) - 1
		while minidx < maxidx:
			curidx = int((minidx + maxidx) /2)
			if self._is_in_rel(reltbl[curidx],vaddr):
				return True
			elif self._is_in_rel(reltbl[minidx],vaddr):
				return True
			elif self._is_in_rel(reltbl[maxidx], vaddr):
				return True
			if vaddr < reltbl[curidx].vaddr:
				maxidx = curidx
			else:
				minidx = curidx
			if (minidx+1) >= maxidx:
				break
		if self._is_in_rel(reltbl[minidx],vaddr):
			return True
		elif self._is_in_rel(reltbl[maxidx], vaddr):
			return True
		return False


	def is_in_reloc(self,vaddr,name):
		if self.__coff is None:
			return True
		findsym = None
		findk = None
		for k in self.__symnames.keys():
			sym = self._find_sym(name,self.__symnames[k])
			if sym is not None:
				findsym = sym
				findk = k
				break
		if findsym is None:
			return True

		if vaddr < findsym.value or vaddr >= (findsym.value + findsym.size):
			return True
		return self._find_rel_in(self.__relocvalues[k], vaddr)

##extractcode_end