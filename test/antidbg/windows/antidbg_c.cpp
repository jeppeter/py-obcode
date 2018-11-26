#include <obcode.h>
#include "antidbg.h"
#include <stdio.h>


int is_debug_present()
{
	_PPEB peb = get_peb_ptr();
	fprintf(stdout,"peb [%p]\n", peb);
	if (peb->bBeingDebugged) {
		return 1;
	}
	return 0;
}
