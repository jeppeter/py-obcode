#include "main.h"
#include "callc.h"
#include "chk_main.h"
#include "handle_exit.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

void failfunc_main_1(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}


int print_out_a(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main_1);
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out_b(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out_c(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC_SPEC("namemin=10");
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}


int print_out_d(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out_e(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out_f(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out_g(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_TOTAL_FUNC();
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int main(int argc,char* argv[])
{
	int ret;
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