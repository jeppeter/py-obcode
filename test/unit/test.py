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
import json
import shutil

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

def make_tempdir(prefix='prefix',basedir=None):
    tmpd = tempfile.mkdtemp(prefix=prefix,dir=basedir)
    return tmpd


class obcode_test(unittest.TestCase):
    def setUp(self):
        keyname = '_%s__logger'%(self.__class__.__name__)
        if getattr(self,keyname,None) is None:
            self.__logger = _LoggerObject('obcode')
        self.__tmp_files = []
        self.__tmp_descrs = []
        self.__tmpd = []
        self.__tmpd_descrs = []
        if 'MAKOB_FILE' in os.environ.keys():
            del os.environ['MAKOB_FILE']
        self.runOk= False
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
        ok = self.runOk
        if 'OBCODE_TEST_RESERVED' in os.environ.keys():
            ok = False
        if filename is not None and ok:
            os.remove(filename)
        elif filename is not None:
            self.error('%s %s'%(description,filename))
        return

    def __remove_dir_ok(self,dname,description=''):
        ok = self.runOk
        if 'OBCODE_TEST_RESERVED' in os.environ.keys():
            ok = False
        if dname is not None and ok:
            shutil.rmtree(dname)
        elif dname is not None:
            self.error('%s %s'%(description,dname))
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
        if len(self.__tmpd) > 0:
            idx = 0
            assert(len(self.__tmpd) == len(self.__tmpd_descrs))
            while idx < len(self.__tmpd):
                c = self.__tmpd[idx]
                d = self.__tmpd_descrs[idx]
                self.__remove_dir_ok(c,d)
                idx += 1
        self.__tmpd = []
        self.__tmpd_descrs = []
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

    def __make_tempd(self,description=''):
        tmpd = make_tempdir()
        self.__tmpd.append(tmpd)
        self.__tmpd_descrs.append(description)
        return tmpd

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
            cmds = ['cl.exe','/nologo','/Zi','/Os','/Wall','/wd','4668', '/wd','4820','/wd','4710', '/wd','5045', '/wd','4774','/wd','4132']

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

    def __compare_not_same_output(self,content,obcmds=[],includedir=[],libs=[],appcmds=[],libdir=None):
        sfile,dfile = self.__trans_obcode(content,obcmds)
        slines , soutfile = self.__get_write_file(sfile,None,includedir,libs,appcmds,libdir)
        dlines , doutfile = self.__get_write_file(dfile,None,includedir,libs,appcmds,libdir)
        samed = True
        if len(slines) != len(dlines):
            samed = False
        idx = 0
        while  samed and (idx < len(slines)):
            if slines[idx] != dlines[idx]:
                samed = False
            idx += 1
        self.assertEqual(samed, False)
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
        self.runOk=True
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
        self.runOk=True
        return

    def test_A003(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','obv','obv.cpp'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        self.runOk=True
        return

    def test_A004(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','obv','insert.cpp'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        self.runOk=True
        return

    def test_A005(self):
        if sys.platform == 'win32':
            self.runOk=True
            return
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','maklib')
        makejson = os.path.join(exampledir,'makob.json')
        if os.path.exists(makejson):
            os.remove(makejson)
        cmds = ['make','-C',exampledir,'O=1','clean']
        stdnull = open(os.devnull,'w')
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'O=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(exampledir,'command')
        jsonfile = os.path.join(exampledir,'makob.json')        
        cdict = dict()
        with open(jsonfile) as f:
            cdict = json.load(f)
        s = read_file(jsonfile)
        # this will give the coding 
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            valid = False
            for k in cdict['files'].keys():
                v = cdict['files'][k]
                if v == l:
                    valid = True
            self.assertEqual(valid, True)
        # now we should get the trans
        cmds = [sys.executable,obcodepy,'obtrans','--obtrans-srcdir',exampledir, makejson]
        subprocess.check_call(cmds,stdout=stdnull)
        # now to copy the file
        # write again
        write_file(s, makejson)
        cmds = ['make','-C',exampledir,'O=1','distclean']
        subprocess.check_call(cmds,stdout=stdnull)
        stdnull.close()
        stdnull = None
        self.runOk=True
        return

    def test_A006(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','srcdir','d.c'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        self.runOk=True
        return

    def test_A007(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','srcdir','const.c'))
        content = self.__get_content(fname)
        self.__compare_not_same_output(content)
        self.runOk=True
        return

    def test_A008(self):
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','example','srcdir','mixed.c'))
        content = self.__get_content(fname)
        self.__compare_output(content)
        self.runOk=True
        return

    def test_A009(self):
        if sys.platform == 'win32':
            self.runOk=True
            return
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','unpatch','elf')
        stdnull = open(os.devnull,'w')

        # patch mode
        cmds = ['make','-C',exampledir,'OB_PATCH=1','clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'OB_PATCH=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        errorbakjson = os.path.join(exampledir,'error_bak.json')
        unpatchjson = os.path.join(exampledir,'unpatch.json')
        errorjson = os.path.join(exampledir,'error.json')
        cmds = ['cp',unpatchjson, errorbakjson]
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(exampledir,'main')
        oblines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            oblines.append(l)
        ob2lines = []
        cmdbin = os.path.join(exampledir,'main2')
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            ob2lines.append(l)
        # no patch mode
        cmds = ['make','-C',exampledir,'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(exampledir,'main')
        normlines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            normlines.append(l)
        cmdbin = os.path.join(exampledir,'main2')
        norm2lines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            norm2lines.append(l)
        cmds = ['make','-C',exampledir,'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['cp', errorbakjson,errorjson]
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'OB_REPATCH=%s'%(errorjson),'all']
        subprocess.check_call(cmds,stdout=stdnull)
        repatchlines = []
        cmdbin = os.path.join(exampledir,'main')
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            repatchlines.append(l)
        repatch2lines = []
        cmdbin = os.path.join(exampledir,'main2')
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            repatch2lines.append(l)
        cmds = ['make','-C',exampledir,'clean']
        subprocess.check_call(cmds,stdout=stdnull)

        self.assertEqual(normlines,oblines)
        self.assertEqual(norm2lines, ob2lines)
        self.assertEqual(normlines,repatchlines)
        self.assertEqual(norm2lines,repatch2lines)
        cmds = ['rm','-f',errorbakjson,errorjson]
        subprocess.check_call(cmds,stdout=stdnull)
        stdnull.close()
        stdnull = None
        self.runOk=True
        return

    def test_A010(self):
        if sys.platform != 'win32':
            self.runOk=True
            return
        stdnull = None
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','unpatch','pe')
        stdnull = open(os.devnull,'w')

        # patch mode
        origdir = os.getcwd()
        os.chdir(exampledir)
        try:
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','OB_PATCH=1','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','OB_PATCH=1','all']
            subprocess.check_call(cmds,stdout=stdnull)
            errorbakjson = os.path.join(exampledir,'error_bak.json')
            errorjson = os.path.join(exampledir,'error.json')
            unpatchjson = os.path.join(exampledir,'unpatch.json')
            cmds = ['copy','/Y',unpatchjson, errorbakjson]
            subprocess.check_call(cmds,stdout=stdnull,shell=True)
            cmds = ['copy','/Y',unpatchjson, errorjson]
            subprocess.check_call(cmds,stdout=stdnull,shell=True)
            cmdbin = os.path.join(exampledir,'main.exe')
            oblines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                oblines.append(l)
            cmdbin = os.path.join(exampledir,'main2.exe')
            ob2lines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                ob2lines.append(l)
            # no patch mode
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','all']
            subprocess.check_call(cmds,stdout=stdnull)
            cmdbin = os.path.join(exampledir,'main.exe')
            normlines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                normlines.append(l)
            cmdbin = os.path.join(exampledir,'main2.exe')
            norm2lines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                norm2lines.append(l)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            cmds = ['nmake.exe', '/NOLOGO','/f','makefile.win','OB_REPATCH=%s'%(errorjson),'all']
            subprocess.check_call(cmds,stdout=stdnull)
            cmdbin = os.path.join(exampledir,'main.exe')
            repatchlines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                repatchlines.append(l)
            cmdbin = os.path.join(exampledir,'main2.exe')
            repatch2lines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                repatch2lines.append(l)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','clean']
            subprocess.check_call(cmds,stdout=stdnull)

            self.assertEqual(normlines,oblines)
            self.assertEqual(norm2lines,ob2lines)
            self.assertEqual(norm2lines,repatch2lines)
            self.assertEqual(normlines,repatchlines)
            cmds = ['del','/F','/Q',errorjson]
            subprocess.check_call(cmds,stdout=stdnull,shell=True)
            cmds = ['del','/F','/Q',errorbakjson]
            subprocess.check_call(cmds,stdout=stdnull,shell=True)
            self.runOk=True
        finally:
            if stdnull is not None:
                stdnull.close()
            stdnull = None
            os.chdir(origdir)
        return

    def test_A011(self):
        if sys.platform == 'win32':
            self.runOk=True
            return
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','unpatch','obelf')
        stdnull = open(os.devnull,'w')
        tmpd = self.__make_tempd('obelf')

        # patch mode
        cmds = ['make','-C',exampledir,'OB_PATCH=1','clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'OB_PATCH=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(exampledir,'main')
        oblines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            oblines.append(l)
        cmdbin = os.path.join(exampledir,'main2')
        ob2lines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            ob2lines.append(l)
        # no patch mode
        cmds = ['make','-C',exampledir,'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = [sys.executable,obcodepy,'cob', exampledir, tmpd]
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',tmpd,'TOPDIR=%s'%(topdir),'OB_PATCH=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(tmpd,'main')
        normlines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            normlines.append(l)
        cmdbin = os.path.join(tmpd,'main2')
        norm2lines = []
        for l in cmdpack.run_cmd_output([cmdbin]):
            l = l.rstrip('\r\n')
            norm2lines.append(l)
        cmds = ['make','-C',tmpd,'TOPDIR=%s'%(topdir),'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        self.assertEqual(normlines,oblines)
        self.assertEqual(norm2lines,ob2lines)
        stdnull.close()
        stdnull = None
        self.runOk=True
        return


    def test_A012(self):
        if sys.platform == 'win32':
            self.runOk=True
            return
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','unpatch','soelf')
        stdnull = open(os.devnull,'w')
        tmpd = self.__make_tempd('soelf')

        # patch mode
        cmds = ['make','-C',exampledir,'OB_PATCH=1','clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',exampledir,'OB_PATCH=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(exampledir,'main')
        oblines = []
        copyenv = os.environ.copy()
        copyenv['LD_LIBRARY_PATH'] = exampledir
        for l in cmdpack.run_cmd_output([cmdbin],copyenv=copyenv):
            l = l.rstrip('\r\n')
            oblines.append(l)
        # no patch mode
        cmds = ['make','-C',exampledir,'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = [sys.executable,obcodepy,'cob', exampledir, tmpd]
        subprocess.check_call(cmds,stdout=stdnull)
        cmds = ['make','-C',tmpd,'TOPDIR=%s'%(topdir),'OB_PATCH=1','all']
        subprocess.check_call(cmds,stdout=stdnull)
        cmdbin = os.path.join(tmpd,'main')
        normlines = []
        copyenv['LD_LIBRARY_PATH'] = tmpd
        for l in cmdpack.run_cmd_output([cmdbin],copyenv=copyenv):
            l = l.rstrip('\r\n')
            normlines.append(l)
        cmds = ['make','-C',tmpd,'TOPDIR=%s'%(topdir),'clean']
        subprocess.check_call(cmds,stdout=stdnull)
        self.assertTrue(len(normlines) > 2)
        self.assertEqual(normlines,oblines)
        stdnull.close()
        stdnull = None
        self.runOk=True
        return

    def test_A013(self):
        if sys.platform != 'win32':
            self.runOk=True
            return
        stdnull = None
        # now we should compare
        topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        obcodepy = os.path.join(topdir,'obcode.py')
        exampledir = os.path.join(topdir,'example','unpatch','dllpe')
        stdnull = open(os.devnull,'w')

        # patch mode
        origdir = os.getcwd()
        os.chdir(exampledir)
        try:
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','OB_PATCH=1','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','OB_PATCH=1','all']
            subprocess.check_call(cmds,stdout=stdnull)
            cmdbin = os.path.join(exampledir,'main.exe')
            oblines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                oblines.append(l)
            # no patch mode
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','all']
            subprocess.check_call(cmds,stdout=stdnull)
            cmdbin = os.path.join(exampledir,'main.exe')
            normlines = []
            for l in cmdpack.run_cmd_output([cmdbin]):
                l = l.rstrip('\r\n')
                normlines.append(l)
            cmds = ['nmake.exe','/NOLOGO','/f','makefile.win','clean']
            subprocess.check_call(cmds,stdout=stdnull)
            self.assertTrue(len(normlines) > 2)
            self.assertEqual(normlines,oblines)
            self.runOk=True
        finally:
            if stdnull is not None:
                stdnull.close()
            stdnull = None
            os.chdir(origdir)
        return


def main():
    unittest.main()
    return

if __name__ == '__main__':
    main()