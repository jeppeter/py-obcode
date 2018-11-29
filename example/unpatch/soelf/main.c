#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <errno.h>

int main(int argc,char* argv[])
{
	void* somain1=NULL;
	void* somain2=NULL;

	somain2 = dlopen("somain2.so",RTLD_NOW);
	if (somain2 == NULL) {
		fprintf(stderr,"can not load somain2 error[%d]\n", errno);
		goto fail;
	}

	somain1 = dlopen("somain1.so", RTLD_NOW);
	if (somain1 == NULL) {
		fprintf(stderr,"can not load somain1 error[%d]\n", errno);
		goto fail;		
	}

	if (somain1 != NULL) {
		dlclose(somain1);
		somain1 = NULL;	
	}
	
	if (somain2 != NULL) {
		dlclose(somain2);
		somain2 = NULL;	
	}
	return 0;
fail:
	if (somain1 != NULL) {
		dlclose(somain1);
		somain1 = NULL;	
	}
	
	if (somain2 != NULL) {
		dlclose(somain2);
		somain2 = NULL;	
	}
	return -1;
}