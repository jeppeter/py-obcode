#include <obcode.h>
#include "antidbg.h"
#include <stdio.h>


int is_debug_present()
{
	_PPEB peb = get_peb_ptr();
	if (peb->bBeingDebugged) {
		return 1;
	}
	return 0;
}

int is_ntgflags_set()
{
	_PPEB peb = get_peb_ptr();
	if (peb->dwNtGlobalFlag & 0x70) {
		return 1;
	}
	return 0;
}

int check_remote_debug(void)
{
	HANDLE hcurproc=NULL;
	BOOL bret;
	BOOL bfound=FALSE;

	hcurproc = GetCurrentProcess();
	bret = CheckRemoteDebuggerPresent(hcurproc,&bfound);
	if (!bret) {
		return 1;
	}
	if (bfound) {
		return 1;
	}
	return 0;
}