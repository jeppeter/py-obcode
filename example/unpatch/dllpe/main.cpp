#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

int main(int argc,char* argv[])
{
	HMODULE somain1=NULL;
	HMODULE somain2=NULL;

	argc = argc;
	argv = argv;

	somain2 = LoadLibraryA("somain2.dll");
	if (somain2 == NULL) {
		fprintf(stderr,"can not load somain2 error[%ld]\n", GetLastError());
		goto fail;
	}

	somain1 = LoadLibraryA("somain1.dll");
	if (somain1 == NULL) {
		fprintf(stderr,"can not load somain1 error[%ld]\n", GetLastError());
		goto fail;		
	}

	if (somain1 != NULL) {
		FreeLibrary(somain1);
		somain1 = NULL;	
	}
	
	if (somain2 != NULL) {
		FreeLibrary(somain2);
		somain2 = NULL;	
	}
	return 0;
fail:
	if (somain1 != NULL) {
		FreeLibrary(somain1);
		somain1 = NULL;	
	}
	
	if (somain2 != NULL) {
		FreeLibrary(somain2);
		somain2 = NULL;	
	}
	return -1;
}