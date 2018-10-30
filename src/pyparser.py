#! /usr/bin/env python

import ast


##extractcode_start
class ImportInfo(object):
	def __init__(self,fm,m):
		self.frommodule = fm
		self.module = m
		return

	def __str__(self):
		return 'frommodule[%s] module[%s]'%(self.frommodule,self.module)

	def __repr__(self):
		return str(self)


def get_import_names(f):
	root = None
	with open(f,'r') as fin:
		root = ast.parse(fin.read(),f)
	im = []
	for n in ast.iter_child_nodes(root):
		if isinstance(n, ast.Import):
			im.append(ImportInfo('',n.names[0].name))
		elif isinstance(n,ast.ImportFrom):
			im.append(ImportInfo(n.module, n.names[0].name))
		else:
			continue
	return im

def format_import(im):
	rets = ''
	if len(im.frommodule) > 0:
		rets += 'from %s import %s'%(im.frommodule,im.module)
	else:
		rets += 'import %s'%(im.module)
	return rets

def packed_import(ims):
	retims = sorted(ims, key=lambda im : im.module)
	cont = True
	while cont:
		idx = 0
		cont = False
		while idx < len(retims):
			if idx > 0 :
				if retims[idx].frommodule == retims[(idx - 1)].frommodule and \
					retims[idx].module == retims[(idx - 1)].module:
					del retims[idx]
					cont = True
					break
			idx += 1
	return  retims
##extractcode_end