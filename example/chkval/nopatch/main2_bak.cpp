#include "main2.h"
#include "callc.h"
#include "chk_main2.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

void failfunc_main2_1(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_2(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_3(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_4(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}


void failfunc_main2_5(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_6(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_7(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main2_8(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

int print_out2_a(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_1);
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_b(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_2);
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_c(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_3);
	if (ret < 0) {
		return ret;
	}	
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_d(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_4);
	if (ret < 0) {
		return ret;
	}	
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_e(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_5);
	if (ret < 0) {
		return ret;
	}	
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_f(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_6);
	if (ret < 0) {
		return ret;
	}	
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int print_out2_g(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_main2_7);
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
	ret = OB_CHKVAL_FUNC(failfunc_main2_4);
	if (ret < 0) {
		return ret;
	}
	print_out2_a();
	print_out2_b();
	print_out2_c();
	print_out2_d();
	print_out2_e();
	print_out2_f();
	print_out2_g();
	callc_a();
	callc_b();
	callc_c();
	callc_d();
	callc_e();
	callc_f();
	return 0;
}