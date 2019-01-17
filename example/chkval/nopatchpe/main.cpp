#include "main.h"
#include "callc.h"
#include "chk_main.h"
#include "handle_exit.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",C_FILE,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

#define SVAL           0x11223344
#define RVAL           0x55667788

void failfunc_main_1(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}


int print_out_a(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main_1);
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}

int print_out_b(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}

int print_out_c(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC_SPEC("namemin=10");
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}


int print_out_d(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}

int print_out_e(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}

int print_out_f(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}

int print_out_g(void)
{
	int a=1,b=2,c=SVAL;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	OUTP("a=%d;b=%d;c=0x%x;",a,b,c);
	return 0;
}


OB_MAP_FUNCTION()

int change_value(unsigned char* pstart, int size, unsigned int sval, unsigned int rval)
{
	int ret = 0;
	int chged=0;
	unsigned int* piptr;
	unsigned char* pptr;
	int i;

	ret = OB_MAP_FUNC(pstart, size, OB_MAP_READ | OB_MAP_WRITE | OB_MAP_EXEC);
	if (ret < 0) {
		fprintf(stderr,"not writable for [%p] - [%p] error[%d]\n", pstart, pstart+size, ret);
		goto fail;
	}

	for (pptr = pstart ,i = 0; i < size ;i ++ , pptr++) {
		piptr = (unsigned int*) pptr;
		if (*piptr == sval) {
			*piptr = rval;
			chged = 1;
			break;
		}
	}

	ret = OB_MAP_FUNC(pstart, size, OB_MAP_READ | OB_MAP_EXEC);
	if (ret < 0) {
		fprintf(stderr,"not readonly for [%p] - [%p] error[%d]\n", pstart, pstart+size, ret);
		goto fail;
	}
	return chged;
fail:	
	return ret;
}

unsigned char* get_func_address(unsigned char* ptr)
{
	unsigned char* pretval = ptr;
	signed int* pjmp;
	if (*pretval == 0xe9) {
		pjmp = (signed int*)(pretval + 1);
		pretval += sizeof(*pjmp) + 1;
		pretval += *pjmp;
	}
	return pretval;
}


int change_values()
{
	int ret = 0;
	ret = change_value(get_func_address((unsigned char*)&print_out_a), (int)(get_func_address((unsigned char*)&print_out_b) - get_func_address((unsigned char*)&print_out_a)), SVAL ,RVAL);
	if (ret < 0) {
		return ret;
	}
	ret = change_value(get_func_address((unsigned char*)&print_out_b), (int)(get_func_address((unsigned char*)&print_out_c) - get_func_address((unsigned char*)&print_out_b)), SVAL ,RVAL);
	if (ret < 0) {
		return ret;
	}
	ret = change_value(get_func_address((unsigned char*)&print_out_c), (int)(get_func_address((unsigned char*)&print_out_d) - get_func_address((unsigned char*)&print_out_c)), SVAL ,RVAL);
	if (ret < 0) {
		return ret;
	}
	return 0;
}


int main(int argc,char* argv[])
{
	int ret;
	if (argc > 1) {
		change_values();
	}
	argc = argc;
	argv = argv;
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	print_out_a();
	print_out_b();
	print_out_c();
	print_out_d();
	print_out_e();
	print_out_f();
	print_out_g();
	callc_a();
	callc_b();
	callc_c();
	callc_d();
	callc_e();
	callc_f();
	return 0;
}