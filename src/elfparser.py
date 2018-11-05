#! /usr/bin/env python

import logging
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from elftools.elf.relocation import RelocationSection
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *



##extractcode_start
class FuncInfo(object):
	def __init__(self,vaddr,offset,size,name):
		self.__vaddr = vaddr
		self.__offset = offset
		self.__name = name
		self.__size = size
		self.__hash = get_name_hash(name)
		return

	def __str__(self):
		return '[%s].vaddr=[0x%x] .offset[0x%x]'%(self.name,self.vaddr,self.offset)

	def __repr__(self):
		return str(self)

	def __getattr__(self,keyname):
		if keyname == 'vaddr':
			return self.__vaddr
		elif keyname == 'offset':
			return self.__offset
		elif keyname == 'name':
			return self.__name
		elif keyname == 'size':
			return self.__size
		elif keyname == 'hash':
			return self.__hash
		else:
			if keyname in self.__dict__.keys():
				return self.__dict__[keyname]
		raise Exception('not [%s]'%(keyname))
		return None

	def __setattr(self,k,v):
		if k == 'vaddr' or k == 'offset' or \
			k == 'size' or k=='name' or k == 'hash':
			raise Exception('can not set [%s]'%(k))
		else:
			if k in self.__dict__.keys():
				self.__dict__[k] = v
		raise Exception('not set [%s] =[%s]'%(k,v))

	def __eq__(self,other):
		if self.name != other.name:
			return False
		if self.vaddr != other.vaddr:
			return False
		if self.offset != other.offset:
			return False
		if self.size != other.size:
			return False
		return True

class RelocInfo(object):
	def __init__(self,name,vaddr,typestr):
		self.__name = name
		self.__vaddr = vaddr
		self.__type =  typestr
		self.__size = 4
		self.__hash = vaddr
		return

	def __eq__(self,other):
		return str(self) == str(other)

	def __str__(self):
		return '[%s].vaddr [0x%x] .type[0x%x] size[0x%x]'%(self.name, self.vaddr,self.type, self.size)

	def __repr__(self):
		return str(self)

	def __getattr__(self,k):
		if k == 'name':
			return self.__name
		elif k == 'vaddr':
			return self.__vaddr
		elif k == 'type':
			return self.__type
		elif k == 'size':
			return self.__size
		elif k == 'hash':
			return self.__hash
		else:
			if k in self.__dict__.keys():
				return self.__dict__[k]
		raise Exception('[%s] not getable'%(k))
		return None

	def __setattr__(self,k,v):
		if k == 'vaddr' or 	k=='name' or k == 'hash' or k == 'size':
			raise Exception('can not set [%s]'%(k))
		self.__dict__[k] = v
		return


class ElfParser(object):
	def __init__(self,fname):
		if sys.version[0] == '3':
			self.__fin = open(fname,'rb')
		else:
			self.__fin = open(fname,'r')
		self.__fname= fname
		self.__elffile = ELFFile(self.__fin)
		self.__funcinfo = None
		self.__relocinfo = None
		return

	def close(self):
		if self.__elffile is not None:
			self.__elffile = None

		if self.__fin is not None:
			self.__fin.close()
			self.__fin = None

		if self.__funcinfo is not None:
			self.__funcinfo = None
		return

	def __parse_elf_funcinfo(self):
		assert(self.__elffile is not None)
		assert(self.__funcinfo is None)
		self.__funcinfo = dict()
		for symtab in self.__elffile.iter_sections():
			if not isinstance(symtab, SymbolTableSection):
				continue
			for sym in symtab.iter_symbols():
				vaddr = sym['st_value']
				size = sym['st_size']
				off = self._vaddr_to_off(vaddr,sym.name)
				funcinfo = FuncInfo(vaddr,off,size,sym.name)
				hv = '%x'%(funcinfo.hash)
				inserted = False
				if hv in self.__funcinfo.keys():
					for k in self.__funcinfo[hv]:
						if k == funcinfo:
							logging.info('%s already insert'%(funcinfo))
							inserted = True
							break
					if not inserted:
						self.__funcinfo[hv].append(funcinfo)
				else:
					self.__funcinfo[hv] = []
					self.__funcinfo[hv].append(funcinfo)
		return

	def _vaddr_to_off(self,vaddr,name=''):
		assert(self.__elffile is not None)
		for section in self.__elffile.iter_sections():
			if vaddr >= section['sh_addr']  and \
				vaddr <= (section['sh_addr'] + section['sh_size']):
				return (vaddr - section['sh_addr']) + section['sh_offset']
		return -1

	def __parse_elf_relocinfo(self):
		assert(self.__elffile is not None)
		assert(self.__relocinfo is None)
		self.__relocinfo = []
		ndict = dict()
		for section in self.__elffile.iter_sections():
			if not isinstance(section, RelocationSection):
				continue
			symtab = self.__elffile.get_section(section['sh_link'])
			idxnum = -1
			for rel in section.iter_relocations():
				idxnum += 1
				vaddr = rel['r_offset']
				typeval = rel['r_info'] + (rel['r_info_type'] << 32)
				name = '%d'%(idxnum)
				if rel['r_info_sym'] != 0:
					symbol = symtab.get_symbol(rel['r_info_sym'])
					if symbol['st_name'] == 0:
						symsec = self.__elffile.get_section(symbol['st_shndx'])
						symbol_name = symsec.name						
					else:
						symbol_name = symbol.name
					name = symbol_name
				relinfo = RelocInfo(name,vaddr,typeval)
				hv = '%x'%(relinfo.hash)
				inserted = False
				if hv in ndict.keys():
					for k in ndict[hv]:
						if k == relinfo:
							inserted = True
							break
				else:
					ndict[hv] = []
				if not inserted:
					ndict[hv].append(relinfo)
		for k in ndict.keys():
			for v in ndict[k]:
				self.__relocinfo.append(v)
		self.__relocinfo = sorted(self.__relocinfo, key=lambda vinfo:vinfo.vaddr)
		return

	def __find_funcinfo(self,name):
		retinfo = None
		if self.__funcinfo is None:
			self.__parse_elf_funcinfo()
		hv = '%x'%(get_name_hash(name))
		if hv  in self.__funcinfo.keys():
			for k in self.__funcinfo[hv]:
				if k.name == name:
					retinfo = k
					break
		return retinfo
	def __is_in_relocate_addr(self,vaddr,relinfo):
		if vaddr >= relinfo.vaddr and \
			vaddr < (relinfo.vaddr + relinfo.size):
			return True
		return False

	def __is_less_relocate_addr(self,vaddr,relinfo):
		if vaddr < relinfo.vaddr:
			return True
		return False

	def __is_greate_relocate_addr(self,vaddr,relinfo):
		if vaddr >= (relinfo.vaddr + relinfo.size):
			return True
		return False

	def __find_relocinfo(self,vaddr):
		if self.__relocinfo is None:
			self.__parse_elf_relocinfo()
		minidx = 0
		maxidx = len(self.__relocinfo) - 1
		while minidx < maxidx:
			curidx = int((minidx + maxidx) / 2)
			if self.__is_in_relocate_addr(vaddr,self.__relocinfo[curidx]):
				return self.__relocinfo[curidx]
			if self.__is_less_relocate_addr(vaddr,self.__relocinfo[curidx]):
				maxidx = curidx
			elif self.__is_greate_relocate_addr(vaddr,self.__relocinfo[curidx]):
				minidx = curidx
			if minidx >= (maxidx - 1):
				if self.__is_in_relocate_addr(vaddr,self.__relocinfo[minidx]):
					return self.__relocinfo[minidx]
				if self.__is_in_relocate_addr(vaddr,self.__relocinfo[maxidx]):
					return self.__relocinfo[maxidx]
				return None
		if minidx == maxidx:
			if self.__is_in_relocate_addr(vaddr,self.__relocinfo[minidx]):
				return self.__relocinfo[minidx]
		return None

	def func_offset(self,name):
		assert(self.__elffile is not None)
		funcinfo = self.__find_funcinfo(name)
		if funcinfo is not None:
			return funcinfo.offset
		return -1

	def func_vaddr(self,name):
		assert(self.__elffile is not None)
		funcinfo = self.__find_funcinfo(name)
		if funcinfo is not None:
			return funcinfo.vaddr
		return -1

	def func_size(self,name):
		assert(self.__elffile is not None)
		funcinfo = self.__find_funcinfo(name)
		if funcinfo is not None:
			return funcinfo.size
		return -1

	def is_in_reloc(self,vaddr,name):
		assert(self.__elffile is not None)
		relinfo = self.__find_relocinfo(vaddr)
		if relinfo is not None:
			return True
		return False


##extractcode_end
