#include "somain1.h"
#include <stdio.h>
#include <stdlib.h>
#include "unpatch.h"
#include "callc.h"

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)


int main1_print_out_a(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello a");
	OUTP("hello a");
	OUTP("hello a");
	return ret;
}


int main1_print_out_b(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello b");
	OUTP("hello b");
	OUTP("hello b");
	return ret;
}

int main1_print_out_c(void)
{
	int ret=0;

	OB_CODE(ret);
	OUTP("hello c");
	OUTP("hello c");
	OUTP("hello c");
	return ret;
}

OB_MAP_FUNCTION()


BOOL DllMain(HINSTANCE hinst,DWORD reason,LPVOID lpReserved)
{
	int ret=0;

	hinst = hinst;
	reason = reason;
	lpReserved = lpReserved;

	ret = unpatch_handler(OB_MAP_FUNC);
	if (ret < 0) {
		return FALSE;
	}
	main1_print_out_a();
	main1_print_out_b();
	main1_print_out_c();
	call_a();
	call_b();
	call_c();
	return TRUE;
}

