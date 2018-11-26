#include <obcode.h>
#include "antidbg.h"
#include <stdio.h>

#define DBG_OUT(...)  do{fprintf(stderr,"[%s:%d] ",__FILE__,__LINE__); fprintf(stderr,__VA_ARGS__); fprintf(stderr,"\n");}while(0)

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

int is_debugger_present(void)
{
	BOOL bret;

	bret = IsDebuggerPresent();
	if (bret) {
		return 1;
	}
	return 0;	
}

typedef NTSTATUS(__stdcall *_NtQueryInformationProcess)(_In_ HANDLE, _In_  unsigned int, _Out_ PVOID, _In_ ULONG, _Out_ PULONG);



int is_querydbg(void)
{
	HMODULE hmod=NULL;
	int ret = 1;
	HANDLE hcurproc=NULL;
	NTSTATUS status;
	DWORD dval=0;
	_NtQueryInformationProcess queryinformationproc=NULL;

	hmod = LoadLibraryA(OB_MIXED_STR("ntdll.dll"));
	if (hmod == NULL) {	
		DBG_OUT(" ");
		goto out;
	}

	queryinformationproc = (_NtQueryInformationProcess)GetProcAddress(hmod,OB_MIXED_STR("NtQueryInformationProcess"));
	if (queryinformationproc == NULL) {
		DBG_OUT(" ");
		goto out;
	}

	hcurproc = GetCurrentProcess();
	dval = 0;
	/*for DebugPort query*/
	status = queryinformationproc(hcurproc,0x7,&dval,sizeof(dval),NULL);
	if (status == 0 && dval != 0) {
		DBG_OUT(" ");
		goto out;
	}

	dval = 0;
	/*for DebugFlags query*/
	status = queryinformationproc(hcurproc,0x1f, &dval,sizeof(dval),NULL);
	if (status == 0 && dval != 0) {
		DBG_OUT("status 0x%lx dval 0x%lx", status, dval);
		goto out;
	}

	/*to make ok*/
	ret = 0;
out:
	if (hmod != NULL) {
		FreeLibrary(hmod);
	}
	hmod = NULL;
	return ret;
}