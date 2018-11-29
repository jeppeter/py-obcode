#include "callc.h"
#include <stdio.h>
#include <stdlib.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)


int call_a(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("call a");
	OUTP("call a");
	OUTP("call a");
	return ret;
}

int call_b(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("call b");
	OUTP("call b");
	OUTP("call b");
	return ret;
}

int call_c(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("call c");
	OUTP("call c");
	OUTP("call c");
	return ret;
}