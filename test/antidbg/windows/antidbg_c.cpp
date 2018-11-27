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

#if _M_AMD64
typedef NTSTATUS(*_NtQueryInformationProcess)(_In_ HANDLE, _In_  unsigned int, _Out_ PVOID, _In_ ULONG, _Out_ PULONG);
#else
typedef NTSTATUS(__stdcall *_NtQueryInformationProcess)(_In_ HANDLE, _In_  unsigned int, _Out_ PVOID, _In_ ULONG, _Out_ PULONG);
#endif


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
		goto out;
	}

	queryinformationproc = (_NtQueryInformationProcess) GetProcAddress(hmod,OB_MIXED_STR("NtQueryInformationProcess"));
	if (queryinformationproc == NULL) {
		goto out;
	}

	hcurproc = GetCurrentProcess();
	dval = 0;
	/*for DebugPort query*/
	status = queryinformationproc(hcurproc,0x7,&dval,sizeof(dval),NULL);
	if (status == 0 && dval != 0) {
		goto out;
	}

	dval = 0;
	/*for DebugFlags query*/
	status = queryinformationproc(hcurproc,0x1f, &dval,sizeof(dval),NULL);
	if (status == 0 && dval == 0) {
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

int is_dr_debug(void)
{
	CONTEXT ctx;
	HANDLE hthr = GetCurrentThread();
	int i;
	BOOL bret;
	int ret = 1;
	unsigned char* pc=(unsigned char*) &ctx;
	for (i=0;i<sizeof(ctx);i++,pc++) {
		*pc = 0x0;
	}
	ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
	bret = GetThreadContext(hthr,&ctx);
	if (!bret) {
		goto out;
	}
	if (ctx.Dr0 != 0) {
		goto out;
	}
	if (ctx.Dr1 != 0) {
		goto out;
	}

	if (ctx.Dr2 !=0) {
		goto out;
	}

	if (ctx.Dr3 != 0) {
		goto out;
	}

	if (ctx.Dr6 != 0) {
		goto out;
	}

	if (ctx.Dr7 != 0) {
		goto out;
	}
	ret = 0;
out:
	return ret;
}

int is_close_handle_exp(void)
{
	HANDLE hd=(HANDLE) 0x32201121;
	int ret = 0;

	__try
	{
		CloseHandle(hd);
	}
	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		ret = 1;
	}
	return ret;
}

int is_single_step(void)
{
	int ret = 1;

	__try
	{
		set_single_step();
	}

	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		ret = 0;
	}
	return ret;
}

int is_int3(void)
{
	int ret = 1;

	__try
	{
		set_int3();
	}

	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		ret = 0;
	}
	return ret;
}

int is_prefix_hop_int3(void)
{
	int ret = 1;

	__try
	{
		prefix_hop_int3();
	}

	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		ret = 0;
	}
	return ret;
}

int is_kernel_break(void)
{
	int ret = 1;

	__try
	{
		kernel_break();
	}

	__except(EXCEPTION_EXECUTE_HANDLER)
	{
		ret = 0;
	}
	return ret;
}