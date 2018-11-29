#include "somain2.h"
#include <stdio.h>
#include <stdlib.h>
#include "unpatch.h"
#include "callc.h"

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)


int main2_print_out_a(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello2 a");
	OUTP("hello2 a");
	OUTP("hello2 a");
	return ret;
}


int main2_print_out_b(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello2 b");
	OUTP("hello2 b");
	OUTP("hello2 b");
	return ret;
}

int main2_print_out_c(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello2 c");
	OUTP("hello2 c");
	OUTP("hello2 c");
	return ret;
}

OB_MAP_FUNCTION()


void init_func() __attribute__ ((constructor (101)));

void init_func()
{
	int ret;
	ret = unpatch_handler(OB_MAP_FUNC);
	if (ret < 0) {
		return;
	}
	main2_print_out_a();
	main2_print_out_b();
	main2_print_out_c();
	call_a();
	call_b();
	call_c();
	return;
}