#! /usr/bin/env python

import logging
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from elftools.elf.relocation import RelocationSection
from elftools.elf.enums import *
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from objparser import *


##extractcode_start
class FuncInfo(object):
	def __init__(self,vaddr,offset,size,name,secidx):
		self.__vaddr = vaddr
		self.__offset = offset
		self.__name = name
		self.__size = size
		self.__secidx = secidx
		self.__hash = get_name_hash(name)
		return

	def __str__(self):
		return '[%s].vaddr=[0x%x] .offset[0x%x] .secidx[%s]'%(self.name,self.vaddr,self.offset, self.secidx)

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
		elif keyname == 'secidx':
			return self.__secidx
		else:
			if keyname in self.__dict__.keys():
				return self.__dict__[keyname]
		raise Exception('not [%s]'%(keyname))
		return None

	def __setattr__(self,k,v):
		if k == 'vaddr' or k == 'offset' or \
			k == 'size' or k=='name' or k == 'hash' or k == 'secidx':
			raise Exception('can not set [%s]'%(k))
		else:
			self.__dict__[k] = v

	def __eq__(self,other):
		if self.name != other.name:
			return False
		if self.vaddr != other.vaddr:
			return False
		if self.offset != other.offset:
			return False
		if self.size != other.size:
			return False
		if self.secidx != other.secidx:
			return False
		return True

class RelocInfo(object):
	def __init__(self,name,vaddr,typestr,secidx):
		self.__name = name
		self.__vaddr = vaddr
		self.__type =  typestr
		self.__size = 4
		self.__secidx = secidx
		self.__hash = vaddr
		return

	def __eq__(self,other):
		return str(self) == str(other)

	def __str__(self):
		return '[%s].vaddr [0x%x] .type[0x%x] .size[0x%x] .secidx[%s]'%(self.name, self.vaddr,self.type, self.size, self.secidx)

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
		elif k == 'secidx':
			return self.__secidx
		else:
			if k in self.__dict__.keys():
				return self.__dict__[k]
		raise Exception('[%s] not getable'%(k))
		return None

	def __setattr__(self,k,v):
		if k == 'vaddr' or 	k=='name' or k == 'hash' or k == 'size' or k == 'secidx':
			raise Exception('can not set [%s]'%(k))
		self.__dict__[k] = v
		return


class ElfParser(object):
	def __init__(self,fname):
		if sys.version[0] == '3':
			self.__fin = open(fname,'rb')
			fin = open(fname,'rb')
		else:
			self.__fin = open(fname,'r')
			fin = open(fname,'rb')
		self.__fname= fname
		self.__elffile = ELFFile(self.__fin)
		self.__funcinfo = None
		self.__relocinfo = None
		self.__data = fin.read()
		fin.close()
		fin = None
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
				secidx = sym['st_shndx']				
				if self.__elffile.header['e_type'] == ENUM_E_TYPE['ET_EXEC']:
					off = self._vaddr_to_off(vaddr,sym.name)
				else:
					off = self._sec_to_off(secidx,vaddr)
				funcinfo = FuncInfo(vaddr,off,size,sym.name,secidx)
				hv = '%x'%(funcinfo.hash)
				inserted = False
				if secidx in self.__funcinfo.keys():
					if hv in self.__funcinfo[secidx]:
						for k in self.__funcinfo[secidx][hv]:
							if k == funcinfo:
								logging.info('%s already insert'%(funcinfo))
								inserted = True
								break
						if not inserted:
							self.__funcinfo[secidx][hv].append(funcinfo)
					else:
						self.__funcinfo[secidx][hv] = []
						self.__funcinfo[secidx][hv].append(funcinfo)
				else:
					self.__funcinfo[secidx] = dict()
					self.__funcinfo[secidx][hv] = []
					self.__funcinfo[secidx][hv].append(funcinfo)
		return

	def _sec_to_off(self,secidx,vaddr = 0):
		assert(self.__elffile is not None)
		idx = 0
		for section in self.__elffile.iter_sections():
			if idx == secidx:
				return section['sh_offset'] + vaddr
			idx += 1
		return 0

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
		self.__relocinfo = dict()
		ndict = dict()
		for section in self.__elffile.iter_sections():
			if not isinstance(section, RelocationSection):
				continue
			symtab = self.__elffile.get_section(section['sh_link'])
			idxnum = -1
			#logging.info('section [%s] type [%s]'%(section.name,section.header['sh_type']))
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
				relinfo = RelocInfo(name,vaddr,typeval, section.name)
				hv = '%x'%(relinfo.hash)
				inserted = False
				if section.name in ndict.keys():
					if hv in ndict[section.name].keys():
						for k in ndict[section.name][hv]:
							if k == relinfo:
								logging.info('%s already inserted'%(relinfo))
								inserted = True
								break
					else:
						ndict[section.name][hv] = []
				else:
					ndict[section.name] = dict()
					ndict[section.name][hv] = []
				if not inserted:
					#logging.info('%s %s'%(section.name, relinfo))
					ndict[section.name][hv].append(relinfo)
		for k in ndict.keys():
			self.__relocinfo[k] = []
			for v in ndict[k].keys():
				kv = ndict[k][v][0]
				self.__relocinfo[k].append(kv)
		for k in ndict.keys():
			vks = sorted(self.__relocinfo[k], key = lambda vinfo : vinfo.vaddr)
			self.__relocinfo[k] = vks
		return

	def __find_funcinfo(self,name):
		if self.__funcinfo is None:
			self.__parse_elf_funcinfo()
		hv = '%x'%(get_name_hash(name))
		for sec in self.__funcinfo.keys():
			if hv  in self.__funcinfo[sec].keys():
				for k in self.__funcinfo[sec][hv]:
					if k.name == name:
						return k
		return None
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

	def __find_relocinfo(self,vaddr,secname):
		if self.__relocinfo is None:
			self.__parse_elf_relocinfo()
		if self.__funcinfo is None:
			self.__parse_elf_funcinfo()
		if secname not in self.__relocinfo.keys():
			return None
		relsecinfos = self.__relocinfo[secname]
		minidx = 0
		maxidx = len(relsecinfos) - 1
		while minidx < maxidx:
			curidx = int((minidx + maxidx) / 2)
			if self.__is_in_relocate_addr(vaddr,relsecinfos[curidx]):
				#logging.info('[%d].%s [0x%x]'%(curidx,relsecinfos[curidx],vaddr))
				return relsecinfos[curidx]
			if self.__is_less_relocate_addr(vaddr,relsecinfos[curidx]):
				maxidx = curidx
			elif self.__is_greate_relocate_addr(vaddr,relsecinfos[curidx]):
				minidx = curidx
			if minidx >= (maxidx - 1):
				if self.__is_in_relocate_addr(vaddr,relsecinfos[minidx]):
					#logging.info('[%d].%s [0x%x]'%(curidx,relsecinfos[minidx], vaddr))
					return relsecinfos[minidx]
				if self.__is_in_relocate_addr(vaddr,relsecinfos[maxidx]):
					#logging.info('[%d].%s [0x%x]'%(curidx,relsecinfos[maxidx],vaddr))
					return relsecinfos[maxidx]
				return None
		if minidx == maxidx:
			if self.__is_in_relocate_addr(vaddr,relsecinfos[minidx]):
				#logging.info('[%d].%s [0x%x]'%(curidx,relsecinfos[minidx], vaddr))
				return relsecinfos[minidx]
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
		funcinfo = self.__find_funcinfo(name)
		if funcinfo is None:
			logging.warn('find [%s] none'%(name))
			return OBJ_RELOC_NONE
		try:
			secidx = int(funcinfo.secidx)
		except:
			logging.warn('get %s'%(funcinfo))
			return OBJ_RELOC_NONE
		# now to get the function sections
		for nidx, section in enumerate(self.__elffile.iter_sections()):
			if nidx == secidx:
				relinfo = self.__find_relocinfo(vaddr,'.rel%s'%(section.name))
				if relinfo is not None:
					return OBJ_RELOC_ON
				relinfo = self.__find_relocinfo(vaddr,'.rela%s'%(section.name))
				if relinfo is not None:
					return OBJ_RELOC_ON
		return OBJ_RELOC_NONE

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
		matchmax = 0
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
				while jdx < len(data):
					if rels[jdx] == 0 and \
						data[jdx] != sbyte[curidx]:
						if jdx > matchmax:
							logging.debug('[%s].[+0x%x] [+0x%x] [0x%02x] != [0x%02x]'%(symname,jdx,curidx,data[jdx], sbyte[curidx]))
							matchmax = jdx
						break
					jdx += 1
					curidx += 1
				if jdx == len(data):
					if retoff >= 0:
						raise Exception('double match at [0x%x] and [0x%x]'%(retoff,idx))
					retoff = idx
			idx += 1
		if retoff < 0:
			raise Exception('can not find [%s] code\nrels\n%s\ndata\n%s\n'%(symname, dump_ints(rels), dump_ints(data)))
		return retoff

##extractcode_end
