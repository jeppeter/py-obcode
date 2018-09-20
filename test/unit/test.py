#! /usr/bin/env python

import extargsparse
import os
import sys
import logging
import tempfile
import subprocess
import cmdpack
import unittest
import re

def read_file(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'r+b')
    rets = ''
    for l in fin:
        s = l
        if 'b' in fin.mode:
            if sys.version[0] == '3':
                s = l.decode('utf-8')
        rets += s

    if fin != sys.stdin:
        fin.close()
    fin = None
    return rets

def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'w+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 


class _LoggerObject(object):
    def __init__(self,cmdname='extargsparse'):
        self.__logger = logging.getLogger(cmdname)
        if len(self.__logger.handlers) == 0:
            loglvl = logging.WARN
            lvlname = '%s_LOGLEVEL'%(cmdname)
            lvlname = lvlname.upper()
            if lvlname in os.environ.keys():
                v = os.environ[lvlname]
                vint = 0
                try:
                    vint = int(v)
                except:
                    vint = 0
                if vint >= 4:
                    loglvl = logging.DEBUG
                elif vint >= 3:
                    loglvl = logging.INFO
            handler = logging.StreamHandler()
            fmt = "%(levelname)-8s %(message)s"
            fmtname = '%s_LOGFMT'%(cmdname)
            fmtname = fmtname.upper()
            if fmtname in os.environ.keys():
                v = os.environ[fmtname]
                if v is not None and len(v) > 0:
                    fmt = v
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)
            self.__logger.setLevel(loglvl)
            # we do not want any more output debug
            self.__logger.propagate = False

    def format_string(self,arr):
        s = ''
        if isinstance(arr,list):
            i = 0
            for c in arr:
                s += '[%d]%s\n'%(i,c)
                i += 1
        elif isinstance(arr,dict):
            for c in arr.keys():
                s += '%s=%s\n'%(c,arr[c])
        else:
            s += '%s'%(arr)
        return s

    def format_call_msg(self,msg,callstack):
        inmsg = ''  
        if callstack is not None:
            try:
                frame = sys._getframe(callstack)
                inmsg += '[%-10s:%-20s:%-5s] '%(frame.f_code.co_filename,frame.f_code.co_name,frame.f_lineno)
            except:
                inmsg = ''
        inmsg += msg
        return inmsg

    def info(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.info('%s'%(inmsg))

    def error(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.error('%s'%(inmsg))

    def warn(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.warn('%s'%(inmsg))

    def debug(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.debug('%s'%(inmsg))

    def fatal(self,msg,callstack=1):
        inmsg = msg
        if callstack is not None:
            inmsg = self.format_call_msg(msg,(callstack + 1))
        return self.__logger.fatal('%s'%(inmsg))

    def call_func(self,funcname,*args,**kwargs):
        mname = '__main__'
        fname = funcname
        try:
            if '.' not in funcname:
                m = importlib.import_module(mname)
            else:
                sarr = re.split('\.',funcname)
                mname = '.'.join(sarr[:-1])
                fname = sarr[-1]
                m = importlib.import_module(mname)
        except ImportError as e:
            self.error('can not load %s'%(mname))
            return None

        for d in dir(m):
            if d == fname:
                val = getattr(m,d)
                if hasattr(val,'__call__'):
                    return val(*args,**kwargs)
        self.error('can not call %s'%(funcname))
        return None


class obcode_test(unittest.TestCase):
    def setUp(self):
        keyname = '_%s__logger'%(self.__class__.__name__)
        if getattr(self,keyname,None) is None:
            self.__logger = _LoggerObject('obcode')
        self.__tmp_files = []
        self.__tmp_descrs = []
        if 'MAKOB_FILE' in os.environ.keys():
            del os.environ['MAKOB_FILE']
        return

    def info(self,msg,callstack=1):
        return self.__logger.info(msg,(callstack + 1))

    def error(self,msg,callstack=1):
        return self.__logger.error(msg,(callstack + 1))

    def warn(self,msg,callstack=1):
        return self.__logger.warn(msg,(callstack + 1))

    def debug(self,msg,callstack=1):
        return self.__logger.debug(msg,(callstack + 1))

    def fatal(self,msg,callstack=1):
        return self.__logger.fatal(msg,(callstack + 1))

    def __remove_file_ok(self,filename,description=''):
        ok = True
        if 'OBCODE_TEST_RESERVED' in os.environ.keys():
            ok = False
        if filename is not None and ok:
            os.remove(filename)
        elif filename is not None:
            self.error('%s %s'%(description,filename))
        return

    def tearDown(self):
        if len(self.__tmp_files) > 0:
            idx = 0
            assert(len(self.__tmp_descrs) == len(self.__tmp_files))
            while idx < len(self.__tmp_files):
                c = self.__tmp_files[idx]
                d = self.__tmp_descrs[idx]
                self.__remove_file_ok(c,d)
                idx += 1                
        self.__tmp_files = []
        self.__tmp_descrs = []
        return

    @classmethod
    def setUpClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __write_temp_file(self,content,description='',suffix_add=None):
        if suffix_add is None:
            if sys.platform == 'win32':
                suffix_add = '.cpp'
            else:
                suffix_add = '.c'
        fd , tempf = tempfile.mkstemp(suffix=suffix_add,prefix='parse',dir=None,text=True)
        os.close(fd)
        with open(tempf,'w') as f:
            f.write('%s'%(content))
        self.info('tempf %s'%(tempf))
        self.__tmp_files.append(tempf)
        self.__tmp_descrs.append(description)
        return tempf

    def __compile_c_file(self,sfile,outfile=None,includedir=[],libs=[],libdir=None):
        cmds = []
        if outfile is None:
            if sys.platform == 'win32' or sys.platform == 'cygwin':
                outfile = self.__write_temp_file('',description='out exe for [%s]'%(sfile),suffix_add='.exe')
            else:
                outfile = self.__write_temp_file('',description='out exe for [%s]'%(sfile),suffix_add='')
        obdir = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),'..','..','include'))
        if sys.platform == 'win32':
            objfile = self.__write_temp_file('',description='obj file for [%s]'%(sfile), suffix_add='.obj')
            cmds = ['cl.exe','/nologo','/Zi','/Os','/Wall','/wd','4668','/wd','4710', '/wd','5045']

            if len(includedir) > 0:
                for c in includedir:
                    cmds.extend(['/I',c])
            cmds.extend(['/I',obdir])
            cmds.extend(['-c','-Fo%s'%(objfile),sfile])
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
            cmds = ['link.exe','/nologo','-out:%s'%(outfile), objfile]
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
        elif sys.platform == 'cygwin':
            objfile = self.__write_temp_file('',description='obj file for [%s]'%(sfile), suffix_add='.o')
            cmds = ['gcc', '-Wall','-Os']
            if len(includedir) > 0:
                for c in includedir:
                    cmds.append('-I%s'%(c))
            cmds.append('-I%s'%(obdir))
            cmds.extend(['-c',sfile, '-o', objfile])
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
            cmds = ['gcc', '-Wall','-o',outfile,objfile]
            if libdir is not None:
                cmds.append('-L%s'%(libdir))
            if len(libs) > 0:
                for c in libs:
                    cmds.append('-l%s'%(c))
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            objfile = self.__write_temp_file('',description='obj file for [%s]'%(sfile), suffix_add='.o')
            cmds = ['gcc', '-Wall','-Os']
            if len(includedir) > 0:
                for c in includedir:
                    cmds.append('-I%s'%(c))
            cmds.append('-I%s'%(obdir))
            cmds.extend(['-c',sfile, '-o', objfile])
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
            cmds = ['gcc', '-Wall','-o',outfile,objfile]
            if libdir is not None:
                cmds.append('-L%s'%(libdir))
            if len(libs) > 0:
                for c in libs:
                    cmds.append('-l%s'%(c))
            self.info('run cmds %s'%(cmds))
            subprocess.check_call(cmds)
        else:
            raise Exception('not supported platform [%s]'%(sys.platform))
        return outfile

    def __get_output(self,cmds):
        return cmdpack.run_cmd_output(cmds)

    def __get_write_file(self,sfile,outfile=None,includedir=[],libs=[],appcmds=[],libdir=None):
        outfile = self.__compile_c_file(sfile,outfile,includedir,libs,libdir)
        cmds = [outfile]
        cmds.extend(appcmds)
        rlines = []
        for l in self.__get_output(cmds):
            l = l.rstrip('\r\n')
            rlines.append(l)
        return rlines,outfile

    def __get_content(self,fname):
        scon = read_file(fname)
        if sys.platform == 'win32':
            sarr = re.split('\n', scon)
            scon = ''
            for l in sarr:
                l = l.rstrip('\r\n')
                scon += '%s\n'%(l)
        return scon


    def __trans_obcode(self,content,obcmds=[]):
        sfile = self.__write_temp_file(content,description='source file')
        dfile = self.__write_temp_file('',description='dst file')
        vbose = None
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        cmds = [sys.executable,obcodepy,'cob']
        if 'OBCODE_LOGLEVEL' in os.environ.keys():
            vint = 0
            try:
                vint = int(os.environ['OBCODE_LOGLEVEL'])
            except:
                pass
            if vint > 0:
                vbose = '-'
                for c in range(vint):
                    vbose += 'v'
                cmds.append(vbose)
        cmds.extend(obcmds)
        cmds.extend([sfile,dfile])
        subprocess.check_call(cmds)
        return sfile,dfile

    def __compare_output(self,content,obcmds=[],includedir=[],libs=[],appcmds=[],libdir=None):
        sfile,dfile = self.__trans_obcode(content,obcmds)
        slines , soutfile = self.__get_write_file(sfile,None,includedir,libs,appcmds,libdir)
        dlines , doutfile = self.__get_write_file(dfile,None,includedir,libs,appcmds,libdir)
        self.assertEqual(len(slines), len(dlines))
        idx = 0
        while idx < len(slines):
            self.assertEqual(slines[idx], dlines[idx])
            idx += 1
        return

    def __compare_output_thread(self,content,obcmds=[],includedir=[],libs=[],appcmds=[],libdir=None):
        sfile,dfile = self.__trans_obcode(content,obcmds)
        threadlibs=[]
        if sys.platform == 'linux' or sys.platform == 'cygwin' or sys.platform == 'linux2':
            threadlibs.append('pthread')
        libs.extend(threadlibs)
        slines , soutfile = self.__get_write_file(sfile,None,includedir,libs,appcmds,libdir)
        dlines , doutfile = self.__get_write_file(dfile,None,includedir,libs,appcmds,libdir)
        self.assertEqual(len(slines), len(dlines))
        idx = 0
        while idx < len(slines):
            self.assertEqual(slines[idx], dlines[idx])
            idx += 1
        return


    def test_A001(self):
        writecontent='''
        #include <obcode.h>
        #include <stdio.h>

        int OB_VAR(ccn) = 2;
        int OB_FUNC PrintFunc()
        {
            int a=1,b=2,c=3;

            OB_CODE(a,b,c);
            printf("a=%d;b=%d;c=%d;\\n",a,b,c);
            OB_CODE(a,b,c);
            printf("again a=%d;b=%d;c=%d;\\n",a,b,c);
            return 0;
        }

        int main()
        {
            PrintFunc();
            return 0;
        }
        '''
        self.__compare_output(writecontent)
        return

    def test_A002(self):
        unix_content=''
        win_content=''
        if sys.platform == 'win32':
            winfile = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','thread','win.cpp'))
            content = self.__get_content(winfile)
        else:
            unixfile = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','thread','unix.cpp'))
            content = self.__get_content(unixfile)
        self.__compare_output_thread(content,appcmds=['10','100','199','391','51'])
        return

    def test_A003(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','obv','obv.cpp'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        return

    def test_A004(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','obv','insert.cpp'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        return

    def test_A005(self):
    	if sys.platform == 'win32':
    		return
    	# now we should compare
    	topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    	exampledir = os.path.join(topdir,'example','makelib')
    	makejson = os.path.join(exampledir,'makob.json')
    	os.remove(makejson)
    	cmds = ['make','-C',exampledir,'O=1','clean']
    	subprocess.check_call(cmds)
    	cmds = ['make','-C',exampledir,'O=1','all']
    	subprocess.check_call(cmds)
    	return



def main():
	unittest.main()
	return

if __name__ == '__main__':
	main()