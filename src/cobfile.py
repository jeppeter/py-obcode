#! /usr/bin/env python

import re
import logging
import sys
import os


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from fmthdl import *
from cobattr import *
from cobfilebase import *
##importdebugend


##extractcode_start

class COBFile(COBFileBase):
    def __should_expand_ob_code(self):
        self.cur_line = 0
        for l in self.in_lines:
            self.cur_line += 1
            if self.get_filter_expr_not_defined(l,self.__ob_code_expr):
                return True
            if self.get_filter_expr_not_defined(l, self.__ob_code_spec_expr):
                return True
        return False

    def __prepare_config(self):
        self.cur_line = 0
        for l in self.in_lines:
            self.cur_line += 1
            if self.get_filter_expr_not_defined(l, self.__ob_config_expr):
                m = self.__ob_config_expr.findall(l)
                assert(len(m) == 1)
                assert(len(m[0]) > 1)
                sbyte = string_to_ints(m[0][1])
                params , lbyte = parse_param(sbyte)
                if len(params) != 1 :
                    raise Exception('[%d][%s]no params in OB_CONFIG'%(self.cur_line, l))
                sbyte = string_to_ints(params[0])
                rbyte , lbyte = parse_raw_string(sbyte)
                self.base_cfg = CompoundAttr(ints_to_string(rbyte))
            if self.get_filter_expr_not_defined(l, self.__ob_insert_expr):
                self.__insert_line = self.cur_line
        return


    def __prepare_mix_sbyte(self,sbyte,cfg):
        cb = MixedString(sbyte, cfg,self.cur_line)
        k = '%s'%(cb.hash)
        if k in self.__ob_mixed_str_dicts.keys():
            for curb in self.__ob_mixed_str_dicts[k]:
                if curb.hash == cb.hash and curb.equal_byte(sbyte):
                    if len(sbyte) >=4 and sbyte[-1] == 0 and sbyte[-2] == 0 and sbyte[-3] == 0 and sbyte[-4] == 0:
                        logging.info('at [%d] %s [%s] already inserted'%(self.cur_line, sbyte, uni32_to_string(sbyte)))
                    elif len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
                        logging.info('at [%d] %s [%s] already inserted'%(self.cur_line, sbyte, uni16_to_string(sbyte)))
                    else:
                        logging.info('at [%d] %s [%s] already inserted'%(self.cur_line, sbyte, ints_to_string(sbyte)))
                    return
        else:
            self.__ob_mixed_str_dicts[k] = []
        if len(sbyte) >=4 and sbyte[-1] == 0 and sbyte[-2] == 0 and sbyte[-3] == 0 and sbyte[-4] == 0:
            logging.info('%s [%s] into %s'%(sbyte, uni32_to_string(sbyte),cb.funcname))
        elif len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
            logging.info('%s [%s] into %s'%(sbyte, uni16_to_string(sbyte),cb.funcname))
        else:
            logging.info('%s [%s] into %s'%(sbyte, ints_to_string(sbyte),cb.funcname))
        self.__ob_mixed_str_dicts[k].append(cb)
        return


    def __prepared_mixed_str_funcs(self,l):
        cfg , params, before, after = self.get_variables(l, self.__ob_mixed_str_expr)
        assert(len(params) == 1)
        cbyte = string_to_ints(params[0])
        logging.info('params[%s]'%(params[0]))
        cbyte = string_to_ints(params[0])
        sbyte,lbyte = parse_string(cbyte)
        cs = ints_to_string(sbyte)
        sbyte = string_to_ints(cs)
        self.__prepare_mix_sbyte(sbyte, cfg)
        newl = '%sinbyte%s'%(before,after)
        return newl

    def __prepare_mixed_str_spec_funcs(self,l):
        cfg ,params, before , after = self.get_spec_config_variables(l, self.__ob_mixed_str_spec_expr)
        assert(len(params) == 1)
        logging.info('params [%s]'%(params[0]))        
        cbyte = string_to_ints(params[0])
        sbyte,lbyte = parse_string(cbyte)
        cs = ints_to_string(sbyte)
        sbyte = string_to_ints(cs)
        self.__prepare_mix_sbyte(sbyte, cfg)
        newl = '%sinbyte%s'%(before,after)
        return newl

    def __prepare_mixed_wstr_funcs(self,l):
        cfg , params, before, after = self.get_variables(l, self.__ob_mixed_wstr_expr)
        assert(len(params) == 1)
        cbyte = string_to_ints(params[0])
        assert(len(cbyte) >= 3)
        assert(cbyte[0] == ord('L'))
        nbyte,lbyte = parse_string(cbyte[1:])
        rs = ints_to_string(nbyte)
        if cfg.unicodewidth == 32:
            sbyte = string_to_uni32(rs)
        else:
            sbyte = string_to_uni16(rs)
        self.__prepare_mix_sbyte(sbyte, cfg)
        newl = '%sinbyte%s'%(before,after)
        return newl

    def __prepare_mixed_wstr_spec_funcs(self,l):
        cfg ,params , before , after = self.get_spec_config_variables(l, self.__ob_mixed_wstr_spec_expr)
        assert(len(params) == 1)
        cbyte = string_to_ints(params[0])
        assert(len(cbyte) >= 3)
        assert(cbyte[0] == ord('L'))
        nbyte,lbyte = parse_string(cbyte[1:])
        rs = ints_to_string(nbyte)
        if cfg.unicodewidth == 32:
            sbyte = string_to_uni32(rs)
        else:
            sbyte = string_to_uni16(rs)
        self.__prepare_mix_sbyte(sbyte, cfg)
        newl = '%sinbyte%s'%(before,after)
        return newl

    def __preare_mixstr_function(self,l):
        curl = l
        while True:
            if self.get_filter_expr_not_defined(curl, self.__ob_mixed_str_expr):
                logging.info('at [%d] [%s]'%(self.cur_line, l))
                curl = self.__prepared_mixed_str_funcs(curl)
            elif self.get_filter_expr_not_defined(curl, self.__ob_mixed_str_spec_expr):
                logging.info('at [%d] [%s]'%(self.cur_line, l))
                curl = self.__prepare_mixed_str_spec_funcs(curl)
            elif self.get_filter_expr_not_defined(curl, self.__ob_mixed_wstr_expr):
                logging.info('at [%d] [%s]'%(self.cur_line, l))
                curl = self.__prepare_mixed_wstr_funcs(curl)
            elif self.get_filter_expr_not_defined(curl, self.__ob_mixed_wstr_spec_expr):
                logging.info('at [%d] [%s]'%(self.cur_line, l))
                curl = self.__prepare_mixed_wstr_spec_funcs(curl)
            else:
                break
        return

    def __prepare_mixstr(self):
        self.cur_line = 0
        for l in self.in_lines:
            self.cur_line += 1
            logging.info('[%d][%s]'%(self.cur_line, l))
            if self.get_filter_expr_not_defined(l, self.__ob_mixed_str_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_str_spec_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_wstr_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_wstr_spec_expr):
                self.__preare_mixstr_function(l)
        return

    def __prepare(self):
        self.__prepare_config()
        self.__prepare_mixstr()
        if self.__should_expand_ob_code():
            funcstr, funcname = format_xor_encode_function(self.base_cfg.prefix,random.randint(self.base_cfg.namemin,self.base_cfg.namemax),0, self.base_cfg.debug)
            self.__xor_enc_functions[funcname] = funcstr
            funcstr, funcname = format_xor_decode_function(self.base_cfg.prefix, random.randint(self.base_cfg.namemin,self.base_cfg.namemax),0, self.base_cfg.debug)
            self.__xor_dec_functions[funcname] = funcstr


            cnt = random.randint(self.base_cfg.funcmin, self.base_cfg.funcmax)
            idx = 0
            while idx < cnt:
                curdict = dict()
                xorcode = get_xor_code(self.base_cfg.xorsize)
                funcstr,funcname = format_key_ctr_function(xorcode,self.base_cfg.prefix,random.randint(self.base_cfg.namemin,self.base_cfg.namemax),self.base_cfg.maxround,0,self.base_cfg.debug)
                curdict['code'] = xorcode
                curdict['ctr']  = funcstr
                curdict['ctr_name'] = funcname                
                funcstr,funcname = format_key_dtr_function(xorcode,self.base_cfg.prefix,random.randint(self.base_cfg.namemin,self.base_cfg.namemax),self.base_cfg.maxround,0,self.base_cfg.debug)
                curdict['dtr'] = funcstr
                curdict['dtr_name'] = funcname
                self.__xor_codes.append(curdict)                
                idx = idx + 1
        return
        

    def __init__(self,sfile,dfile=None,cfg=None):
        COBFileBase.__init__(self,sfile,dfile,cfg)
        self.__xor_enc_functions = dict()
        self.__xor_dec_functions = dict()
        self.__var_replace = dict()
        self.__var_decl_replace = dict()
        self.__func_replace = dict()
        self.__xor_codes = []
        self.__srcfile = sfile
        self.__dstfile = dfile
        self.base_cfg = COBAttr()
        self.__insert_line = -1
        if cfg is not None:
            self.base_cfg = cfg

        # we change the ( to \x28 ) \x29 for it will give error on shell in make file
        self.__ob_code_expr = re.compile('\s+(OB_CODE\s*(\\\x28.*))$')
        self.__ob_code_spec_expr = re.compile('\s+(OB_CODE_SPEC\s*(\\\x28.*))$')
        self.__ob_func_expr = re.compile('\s+OB_FUNC\s+([a-zA-Z0-9_]+)\s*\\\x28')
        self.__ob_func_spec_expr = re.compile('\s+(OB_FUNC_SPEC\s*(\\\x28.*)).*$')
        self.__ob_var_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_VAR\s*(\\\x28.*))$')
        self.__ob_var_spec_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_VAR_SPEC\s*(\\\x28.*))$')
        self.__ob_decl_var_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_DECL_VAR\s*(\\\x28.*))$')
        self.__ob_decl_var_spec_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_DECL_VAR_SPEC\s*(\\\x28.*))$')
        self.__ob_insert_expr = re.compile('^[\s]*(OB_INSERT\s*\\\x28\\\x29)')
        self.__ob_constant_str_expr = re.compile('.*(OB_CONSTANT_STR\s*(\\\x28.*))$')
        self.__ob_constant_wstr_expr = re.compile('.*(OB_CONSTANT_WSTR\s*(\\\x28.*))$')
        self.__ob_constant_str_spec_expr = re.compile('.*(OB_CONSTANT_STR_SPEC\s*(\\\x28.*))$')
        self.__ob_constant_wstr_spec_expr = re.compile('.*(OB_CONSTANT_WSTR_SPEC\s*(\\\x28.*))$')
        self.__ob_mixed_str_expr = re.compile('.*(OB_MIXED_STR\s*(\\\x28.*))$')
        self.__ob_mixed_str_spec_expr = re.compile('.*(OB_MIXED_STR_SPEC\s*(\\\x28.*))$')
        self.__ob_mixed_wstr_expr = re.compile('.*(OB_MIXED_WSTR\s*(\\\x28.*))$')
        self.__ob_mixed_wstr_spec_expr = re.compile('.*(OB_MIXED_WSTR_SPEC\s*(\\\x28.*))$')

        self.__ob_mixed_str_dicts = dict()

        self.__ob_config_expr = re.compile('^\W*(OB_CONFIG(\\\x28.*))$')


        self.__quote_expr = re.compile('"([^"]*)"')
        self.__include_expr = re.compile('^\s*\#\s*include\s+["<]')

        self.__prepare()
        return




    def __format_ob_code_inner(self,varsarr,cfg,tabs=0):
        s = ''
        assert(len(varsarr) > 0)
        vcnames = []
        ptrnames = []
        varcodes = dict()
        for i in varsarr:
            vcnames.append('%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax))))
            ptrnames.append('%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax))))
        s += format_line('do {',tabs)
        s += format_debug_line('variables:prefix %s variables:namemax %d'%(cfg.prefix,random.randint(cfg.namemin,cfg.namemax)), tabs + 1 , cfg.debug)
        for i in range(len(varsarr)):
            s += format_line('void* %s = (void*)&(%s);'%(ptrnames[i], varsarr[i]), tabs + 1)
            s += format_line('unsigned long long %s = (unsigned long long)((OB_ADDR)(%s));'%(vcnames[i], ptrnames[i]), tabs+1)
        bufname = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        sizename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        lenname = '%s_%s'%(cfg.prefix, get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        s += format_line('unsigned char %s[%d];'%(bufname,self.base_cfg.xorsize),tabs + 1)
        s += format_line('int %s=%d;'%(sizename,self.base_cfg.xorsize), tabs + 1)
        s += format_line('int %s;'%(lenname),tabs + 1)
        s += format_line('',tabs + 1)
        for k in self.__xor_enc_functions.keys():
            encname = k
            break
        pair_dict = []
        ctimes = random.randint(cfg.funcmin, cfg.funcmax)
        for i in range(ctimes):
            curi = random.randint(0, len(self.__xor_codes)-1)
            curxor = self.__xor_codes[curi]
            s += format_line('', tabs + 1)
            s += format_line('%s = %s(%s,%s);'%(lenname,curxor['ctr_name'],bufname,sizename), tabs+1)
            curj = random.randint(0, len(varsarr) - 1)
            s += format_line('%s(((unsigned char*)&%s),sizeof(%s),%s,%s);'%(encname, vcnames[curj], vcnames[curj], bufname,lenname), tabs+1)
            s += format_line('%s(%s,%s);'%(curxor['dtr_name'], bufname,lenname), tabs + 1)
            d = dict()
            d['xor_idx'] = curi
            d['var_idx'] = curj
            pair_dict.append(d)

        s += format_debug_line('format [%d] times'%(ctimes),tabs + 1,cfg.debug)

        for k in self.__xor_dec_functions.keys():
            decname = k
            break
        while len(pair_dict)>0:
            curi = random.randint(0, len(pair_dict)-1)
            d = pair_dict[curi]
            xor_idx = d['xor_idx']
            var_idx = d['var_idx']
            del pair_dict[curi]
            curxor = self.__xor_codes[xor_idx]
            s += format_line('',tabs + 1)
            s += format_line('%s = %s(%s,%s);'%(lenname,curxor['ctr_name'],bufname, sizename), tabs + 1)
            s += format_line('%s(((unsigned char*)&%s),sizeof(%s), %s,%s);'%(decname,vcnames[var_idx], vcnames[var_idx], bufname,lenname), tabs + 1)
            s += format_line('%s(%s,%s);'%(curxor['dtr_name'], bufname, lenname), tabs + 1)

        s += format_line('',tabs+1)
        for i in range(len(varsarr)):
            s += format_line('%s = (void*)((OB_ADDR)(%s));'%(ptrnames[i],vcnames[i]), tabs + 1)

        s += format_line('',tabs+1)
        for i in range(len(varsarr)):
            s += format_line('%s = (OB_TYPEOF(%s)) *(((OB_TYPEOF(%s)*)(%s)));'%(varsarr[i], varsarr[i], varsarr[i], ptrnames[i]), tabs+ 1)
        s += format_line('} while(0);',tabs)        
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.cur_line+1,quote_string(self.__srcfile)),0)
        return s

    def __output_ob_header_comment(self,l,cfg,tabs):
        s = ''
        if cfg.noline == 0:
            s += format_line('/*#lineno:%d*/'%(self.cur_line), tabs)
            s += format_line('/*[%s]*/'%(format_comment_line(l)), tabs)
        return s

    def __format_ob_code_spec(self,l):
        s = ''
        curcfg, cvars, before, after = self.get_spec_config_variables(l,self.__ob_code_spec_expr)
        if len(cvars) == 0:
            raise Exception('[%d][%s] not valid code'%(self.cur_line,l))
        tabs = count_tabs(l)
        s += format_line('',tabs)
        s += self.__output_ob_header_comment(l,curcfg,tabs)
        s += self.__format_ob_code_inner(cvars,curcfg, tabs)
        return s

    def __format_ob_code(self,l):
        s = ''
        cfg , varsarr, before,after = self.get_variables(l, self.__ob_code_expr)
        tabs = count_tabs(l)
        s += format_line('',tabs)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_code_inner(varsarr, cfg,tabs)
        return s

    def __format_ob_func_inner(self,l,funcname,cfg,tabs,isspec):
        s = ''
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        s += format_line('#define %s %s'%(funcname, replacename), tabs)
        s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l), 0)
        self.__func_replace[funcname] = replacename
        return s

    def __format_ob_func(self,l):
        s = ''
        m = self.__ob_func_expr.findall(l)
        funcname = m[0]
        tabs = count_tabs(l)
        cfg = self.base_cfg
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_func_inner(l,funcname,cfg,tabs,False)
        return s

    def __format_ob_func_spec(self,l):
        s = ''
        m = self.__ob_func_spec_expr.findall(l)
        assert(m is not None)
        assert(len(m) == 1)
        assert(len(m[0]) > 1)
        sbyte = string_to_ints(m[0][1])
        params , lbyte = parse_param(sbyte)
        if len(params) != 1:
            raise Exception('[%d][%s] not valid OB_FUNC_SPEC'%(self.cur_line,l))
        cfgstr = params[0]
        # now to get the left
        funcbyte = []
        start = 0
        idx = 0
        while idx < len(lbyte):
            cbyte = lbyte[idx]
            idx += 1
            if  start == 0:
                if is_space_char(cbyte):
                    continue
                else:
                    if is_normal_char(cbyte):
                        if is_decimal_char(cbyte):
                            raise Exception('[%d][%s]function name [%s] not valid'%(self.cur_line,l,ints_to_string(lbyte)))
                        start += 1
                        funcbyte.append(cbyte)
                    else:
                        raise Exception('[%d][%s]not valid function name [%s]'%(self.cur_line,l,ints_to_string(lbyte)))
            else:
                if is_normal_char(cbyte):
                    funcbyte.append(cbyte)
                else:
                    break
        funcname = ints_to_string(funcbyte)
        sbyte = string_to_ints(cfgstr)
        cfgbyte , lbyte = parse_raw_string(sbyte)
        cfgstr = ints_to_string(cfgbyte)
        cfg = self.base_cfg.get_file_config(cfgstr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_func_inner(l, funcname, cfg, tabs,True)
        return s

    def __format_ob_var_inner(self,l,cfg,leftvars,isspec,tabs):
        s = ''
        if len(leftvars) != 1:
            raise Exception('[%d][%s] not valid '%(self.cur_line,l))
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        #if isspec:
        #    s += format_line('#undef OB_VAR_SPEC',tabs)
        #    s += format_line('#define OB_VAR_SPEC(a,x) %s'%(replacename), tabs)            
        #else:
        #    s += format_line('#undef OB_VAR', tabs)
        #    s += format_line('#define OB_VAR(x) %s'%(replacename), tabs)
        s += format_line('#define %s %s'%(leftvars[0],replacename), tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l),0)
        self.__var_replace[leftvars[0]] = replacename
        return s

    def __format_ob_var_spec(self,l):
        s = ''
        cfg, leftvars, before,after = self.get_spec_config_variables(l, self.__ob_var_spec_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_var_inner(l,cfg,leftvars,True,tabs)
        return s

    def __format_ob_var(self,l):
        s = ''
        cfg ,leftvars, before, after = self.get_variables(l, self.__ob_var_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_var_inner(l,cfg,leftvars,False,tabs)
        return s

    def __format_ob_decl_var_inner(self,l,cfg,leftvars,isspec,tabs):
        s = ''
        if len(leftvars) != 1:
            raise Exception('[%d][%s] not valid '%(self.cur_line,l))
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        #if isspec:
        #    s += format_line('#undef OB_DECL_VAR_SPEC',tabs)
        #    s += format_line('#define OB_DECL_VAR_SPEC(a,x) %s'%(replacename), tabs)
        #else:
        #    s += format_line('#undef OB_DECL_VAR', tabs)
        #    s += format_line('#define OB_DECL_VAR(x) %s'%(replacename), tabs)
        s += format_line('#define %s %s'%(leftvars[0],replacename),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l),0)
        self.__var_decl_replace[leftvars[0]] = replacename
        return s


    def __format_ob_decl_var(self,l):
        s = ''
        cfg, leftvars, before, after = self.get_variables(l, self.__ob_decl_var_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_decl_var_inner(l,cfg,leftvars,False,tabs)
        return s

    def __format_ob_decl_var_spec(self,l):
        s = ''
        cfg, leftvars, before ,after = self.get_spec_config_variables(l, self.__ob_decl_var_spec_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_decl_var_inner(l,cfg,leftvars,True,tabs)
        return s

    def __format_ob_constant_str_inner(self,l,cfg,before,after,tabs):
        s = ''
        s += format_line('/*[%s]*/'%(format_comment_line(l)),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)        
        s += '%s"[%%s:%%d]\\n",__FILE__,__LINE__%s\n'%(before,after)
        return s

    def __format_ob_constant_str(self,l):
        s = ''
        cfg , leftvars, before , after = self.get_variables(l, self.__ob_constant_str_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_str_inner(l,cfg,before,after,tabs)
        return s

    def __format_ob_constant_str_spec(self,l):
        s = ''
        cfg , leftvars, before , after = self.get_spec_config_variables(l, self.__ob_constant_str_spec_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_str_inner(l,cfg,before,after,tabs)
        return s


    def __format_ob_constant_wstr_inner(self,l,cfg,before,after,tabs):
        s = ''
        s += format_line('/*[%s]*/'%(format_comment_line(l)),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)        
        s += '%sL"[%%hs:%%d]\\n",__FILE__,__LINE__%s\n'%(before,after)
        return s


    def __format_ob_constant_wstr(self,l):
        s = ''
        cfg , leftvars , before , after = self.get_variables(l, self.__ob_constant_wstr_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_wstr_inner(l,cfg,before,after,tabs)
        return s

    def __format_ob_constant_wstr_spec(self,l):
        s = ''
        cfg , leftvars , before , after = self.get_spec_config_variables(l, self.__ob_constant_wstr_spec_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_wstr_inner(l,cfg,before,after,tabs)
        return s


    def __output_pre_functions(self,cfg):
        rets = ''
        hasidx = 0
        # to insert mixed strings
        for k in self.__ob_mixed_str_dicts.keys():
            curbs = self.__ob_mixed_str_dicts[k]
            for cb in curbs:
                rets += format_line('',0)
                rets += format_line('',0)
                rets += cb.afunc
                rets += format_line('',0)
                rets += format_line('',0)
                rets += cb.bfunc
                rets += format_line('',0)
                rets += format_line('',0)
                rets += cb.func
                hasidx += 1

        # now to put the get include function
        for k in self.__xor_enc_functions.keys():
            rets += format_line('',0)
            rets += format_line('',0)
            rets += self.__xor_enc_functions[k]
            hasidx += 1

        for k in self.__xor_dec_functions.keys():
            rets += format_line('',0)
            rets += format_line('',0)
            rets += self.__xor_dec_functions[k]
            hasidx += 1

        # now we should give the include
        idx = 0
        while idx < len(self.__xor_codes):
            rets += format_line('',0)
            rets += format_line('',0)
            curdict = self.__xor_codes[idx]
            rets += curdict['ctr']
            rets += format_line('',0)
            rets += format_line('',0)
            rets += curdict['dtr']
            idx = idx + 1
            hasidx += 1

        if hasidx > 0:
            rets += format_line('',0)
            rets += format_line('',0)
        if len(rets) > 0 and cfg.noline == 0:
            rets += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)

        return rets

    def __format_ob_mixed_str_inner(self,l,dc,params,cfg,before,after):
        assert(len(params) == 1)
        bs = string_to_ints(params[0])
        sbyte,lbyte = parse_string(bs)
        assert(len(lbyte) <= 1)
        if len(lbyte) > 0 :
            assert(lbyte[0] == 0)
        rs = ints_to_string(sbyte)
        sbyte = string_to_ints(rs)
        vn ,vfunc = dc.add_bytes(sbyte,cfg)
        rets = ''
        if vfunc is not None:
            # now 
            tabs = count_tabs(l)
            rets += format_line('char %s[%d];'%(vn,len(sbyte)),tabs)
            rets += format_line('%s((unsigned char*)%s,%d);'%(vfunc,vn,len(sbyte)), tabs)
        # now replace
        newl = before
        newl += vn
        newl += after
        return newl,rets

    def __format_ob_mixed_str_func(self,l,dc):
        cfg , params, before ,after = self.get_variables(l, self.__ob_mixed_str_expr)
        return self.__format_ob_mixed_str_inner(l,dc,params,cfg,before,after)

    def __format_ob_mixed_str_spec_func(self,l,dc):
        cfg ,params,before ,after = self.get_spec_config_variables(l,self.__ob_mixed_str_spec_expr)
        return self.__format_ob_mixed_str_inner(l,dc,params,cfg,before,after)

    def __format_ob_mixed_wstr_inner(self,l,dc,params,cfg,before,after):
        assert(len(params) == 1)
        sbyte = string_to_ints(params[0])
        assert(len(sbyte) > 1)
        assert(sbyte[0] == ord('L'))
        sbyte,lbyte = parse_string(sbyte[1:])
        assert(len(lbyte) <= 1)
        if len(lbyte) >0:
            assert(lbyte[0]== 0)
        rs = ints_to_string(sbyte)
        if cfg.unicodewidth == 32:
            sbyte = string_to_uni32(rs)
        else:
            sbyte = string_to_uni16(rs)
        vn ,vfunc = dc.add_bytes(sbyte,cfg)
        rets = ''
        if vfunc is not None:
            # now 
            tabs = count_tabs(l)
            if cfg.unicodewidth == 32:
                rets += format_line('%s %s[%d];'%(cfg.widechartype,vn,len(sbyte)/4),tabs)
            else:
                rets += format_line('%s %s[%d];'%(cfg.widechartype,vn,len(sbyte)/2),tabs)
            rets += format_line('%s((unsigned char*)%s,%d);'%(vfunc,vn,len(sbyte)), tabs)
        # now replace
        newl = before
        newl += vn
        newl += after
        return newl,rets

    def __format_ob_mixed_wstr_func(self,l,dc):
        cfg , params, before ,after = self.get_variables(l, self.__ob_mixed_wstr_expr)
        return self.__format_ob_mixed_wstr_inner(l,dc,params,cfg,before,after)

    def __format_ob_mixed_wstr_spec_func(self,l,dc):
        cfg ,params,before ,after = self.get_spec_config_variables(l,self.__ob_mixed_wstr_spec_expr)
        return self.__format_ob_mixed_wstr_inner(l,dc,params,cfg,before,after)

    def __format_ob_mixed(self,l):
        s = ''
        dc = MixedStrVariable(self.__ob_mixed_str_dicts)
        newl = l
        tabs = count_tabs(l)
        s += format_debug_line('origin line [%s]'%(l),tabs, self.base_cfg.debug)
        while True:
            if self.get_filter_expr_not_defined(newl, self.__ob_mixed_str_expr):
                newl,rets = self.__format_ob_mixed_str_func(newl,dc)
                s += rets
            elif self.get_filter_expr_not_defined(newl, self.__ob_mixed_str_spec_expr):
                newl ,rets = self.__format_ob_mixed_str_spec_func(newl,dc)
                s += rets
            elif self.get_filter_expr_not_defined(newl, self.__ob_mixed_wstr_expr):
                newl,rets = self.__format_ob_mixed_wstr_func(newl,dc)
                s += rets
            elif self.get_filter_expr_not_defined(newl, self.__ob_mixed_wstr_spec_expr):
                newl, rets = self.__format_ob_mixed_wstr_spec_func(newl,dc)
                s += rets
            else:
                break
        if not self.base_cfg.noline:
            s += format_line('#line %d "%s"'%(self.cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(newl),0)
        return s


    def out_str(self):
        rets = ''
        self.cur_line = 0
        startinclude = 0
        if self.__insert_line >= 0:
            startinclude = 2
        for l in self.in_lines:
            self.cur_line += 1
            #logging.info('[%d][%s]'%(self.cur_line, l))
            if  startinclude == 0:
                m = self.__include_expr.findall(l)
                rets += format_line('%s'%(l),0)
                if m is not None and len(m) > 0:
                    startinclude = 1
                continue
            elif startinclude == 1:
                ls = l.rstrip(' \t')
                ls = ls.strip(' \t')
                if len(ls) == 0:
                    rets += self.__output_pre_functions(self.base_cfg)
                    startinclude = 2
                else:
                    rets += format_line('%s'%(l),0)
                    continue

            if self.__insert_line >= 0 and self.__insert_line == self.cur_line:
                rets += self.__output_pre_functions(self.base_cfg)
                rets += format_line('%s'%(l), 0)
                continue

            if self.get_filter_expr_not_defined(l, self.__ob_code_expr):
                logging.info('')
                rets += self.__format_ob_code(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_code_spec_expr):
                logging.info('')
                rets += self.__format_ob_code_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_func_expr):
                logging.info('')
                rets += self.__format_ob_func(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_func_spec_expr):
                logging.info('')
                rets += self.__format_ob_func_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_var_expr):
                logging.info('')
                rets += self.__format_ob_var(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_var_spec_expr):
                logging.info('')
                rets += self.__format_ob_var_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_decl_var_expr):
                logging.info('')
                rets += self.__format_ob_decl_var(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_decl_var_spec_expr):
                logging.info('')
                rets += self.__format_ob_decl_var_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_constant_str_expr):
                logging.info('')
                rets += self.__format_ob_constant_str(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_constant_wstr_expr):
                logging.info('l [%s]'%(l))
                rets += self.__format_ob_constant_wstr(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_constant_str_spec_expr):
                logging.info('')
                rets += self.__format_ob_constant_str_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_constant_wstr_spec_expr):
                logging.info('l [%s]'%(l))
                rets += self.__format_ob_constant_wstr_spec(l)
            elif self.get_filter_expr_not_defined(l, self.__ob_mixed_str_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_wstr_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_str_spec_expr) or \
                self.get_filter_expr_not_defined(l, self.__ob_mixed_wstr_spec_expr):
                logging.info('l [%s]'%(l))
                rets += self.__format_ob_mixed(l)
            else:
                rets += format_line('%s'%(l),0)
        return rets

    def get_replace_json(self):
        d = dict()
        encname = ''
        for k in self.__xor_enc_functions.keys():
            encname = k
            break
        d['encode_function'] = encname
        decname = ''
        for k in self.__xor_dec_functions.keys():
            decname = k
            break
        d['decode_function'] = decname
        d['xorcodes'] = []
        for k in self.__xor_codes:
            c = dict()
            c['ctr_name'] = k['ctr_name']
            c['dtr_name'] = k['dtr_name']
            c['code'] = k['code']
            d['xorcodes'].append(c)
        d['functions'] = self.__func_replace
        d['vars'] = self.__var_replace
        d['vars_decl'] = self.__var_decl_replace
        odict = dict()
        odict[self.__srcfile] = d
        return odict


class cobparam(object):
    def __init__(self,srcdir,dstdir,configfile=None):
        self.srcdir = srcdir
        self.dstdir = dstdir
        self.__handle_exprs = []
        self.__filter_exprs = []
        self.__handle_strs = []
        self.__filter_strs = []
        self.config=CompoundAttr()
        if configfile is not None:
            self.config.load_file(configfile)
        return

    def append_handle(self,instr):
        expr = re.compile(instr)
        self.__handle_exprs.append(expr)
        self.__handle_strs.append(instr)
        return

    def append_filter(self,instr):
        expr = re.compile(instr)
        self.__filter_exprs.append(expr)
        self.__filter_strs.append(instr)
        return

    def is_in_filter(self,sfile):
        news = '%r'%(self.srcdir)
        patstr = re.sub(news, '', sfile)
        if os.sep == '/':
            patsarr = re.split('/', patstr)
        elif os.sep == '\\':
            patsarr = re.split('\\\\', patstr)
        idx = 0
        while idx < len(self.__filter_exprs):
            c = self.__filter_exprs[idx]
            for cl in patsarr:
                if len(cl) > 0:
                    if c.match(cl):
                        #logging.info('patstr [%s] filted [%s]'%(patstr, self.__filter_strs[idx]))
                        return True
            idx = idx + 1
        return False

    def is_in_handle(self,sfile):
        news = '%r'%(self.srcdir)
        patstr = re.sub(news,'',sfile)
        idx = 0
        while idx < len(self.__handle_exprs):
            c = self.__handle_exprs[idx]
            m = c.findall(patstr)
            if m is not None and len(m) > 0:
                #logging.info('[%s] match [%s]'%(patstr, self.__handle_strs[idx]))
                return True
            idx = idx + 1
        return False
##extractcode_end