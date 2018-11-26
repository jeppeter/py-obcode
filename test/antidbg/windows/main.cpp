#include <Windows.h>
#include <stdlib.h>
#include <stdio.h>
#include "antidbg.h"

#ifdef __cplusplus
extern "C" {
#endif

int isdbg_cmd(int argc,char* argv[]);

#ifdef __cplusplus
};
#endif


void usage(int ec, const char* fmt,...)
{
	FILE* fp = stderr;
	if (ec == 0) {
		fp = stdout;
	}

	if (fmt != NULL) {
		va_list ap;
		va_start(ap,fmt);
		vfprintf(fp,fmt,ap);
		fprintf(fp,"\n");
	}

	fprintf(fp,"antidbg [CMDS]\n");
	fprintf(fp,"\n");
	fprintf(fp,"[CMDS]\n");
	fprintf(fp,"\tisdbg                  to test bBeingDebugged in PEB\n");
	//fprintf(fp,"\t\n");
	//fprintf(fp,"\t\n");

	exit(ec);
}

int isdbg_cmd(int argc,char* argv[])
{
	int ret;
	argc = argc;
	argv = argv;
	ret = is_debug_present();
	fprintf(stdout,"debug present [%s]\n", ret ? "true" : "false");
	return 0;
}

int main(int argc,char* argv[])
{
	int ret=-1;
	if (argc < 2) {
		usage(3,"need an cmd");
	}

	if (strcmp(argv[1],"-h")==0 || 
		strcmp(argv[1],"--help") == 0) {
		usage(0,NULL);
	} else if (strcmp(argv[1], "isdbg") == 0) {
 		ret = isdbg_cmd(argc,argv);
	} else {
		usage(3,"not support cmd[%s]", argv[1]);
	}
	return ret;
}