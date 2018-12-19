#include "callc.h"
#include "chk_main.h"
#include "chk_main2.h"
#include "handle_exit.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

void failfunc_c1(int exitcode, char* name)
{
	OUTP("fail [%d] [%s]", exitcode, name);
	exit(exitcode);
}



int callc_a(void)
{
	int a=1,b=2,c=3;
	int ret;
	OB_CODE(a,b,c);
	ret = OB_CHKVAL_FUNC(failfunc_c1);
	if (ret < 0) {
		return ret;
	}
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	OUTP("a=%d;b=%d;c=%d;",a,b,c);
	return 0;
}

int callc_b(void)
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

int callc_c(void)
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

int callc_d(void)
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

int callc_e(void)
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

int callc_f(void)
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
