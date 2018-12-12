#include "main.h"
#include "callc.h"
#include "chk_main.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

void failfunc_main_1(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main_2(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main_3(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}

void failfunc_main_4(int exitcode, char* name)
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
	ret = OB_CHKVAL_FUNC(failfunc_main_2);
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
	ret = OB_CHKVAL_FUNC(failfunc_main_3);
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
	ret = OB_CHKVAL_FUNC(failfunc_main_4);
	if (ret < 0) {
		return ret;
	}
	print_out_a();
	print_out_b();
	print_out_c();
	callc_a();
	callc_b();
	callc_c();
	return 0;
}