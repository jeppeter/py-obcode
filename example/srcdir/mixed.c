#include <obcode.h>
#include <stdio.h>
#include <wchar.h>

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5,debug=5");
OB_INSERT();

int CallNew()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf(OB_STR_MIXED("[%s:%d] up hello world %d %d %d\n"),__FILE__,__LINE__,a,b,c);
	return 0;
}

extern int newvar2;
extern int newvar5;
int newvar=2;
int newvv=20;

int PrintFunc()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf(OB_MIXED_STR_SPEC("funcname=17","[%s:%d] hello world %d %d %d\n"),__FILE__,__LINE__,a,b,c);
	printf(OB_MIXED_STR_SPEC("funcmin=10,funcmax=30","[%s:%d] hello world again %d %d %d\n"),__FILE__,__LINE__,a,b,c);
	fwprintf(stderr,OB_MIXED_WSTR(L"[%hs:%d] hello world wide %d %d %d\n"),OB_MIXED_STR_SPEC("funcmin=10,funcmax=30","cc again"),__LINE__,a,b,c);
	fwprintf(stderr,OB_MIXED_WSTR_SPEC("funcname=30",L"[%hs:%d] hello world wide %d %d %d\n"),OB_MIXED_STR("cc again"),__LINE__,a,b,c);
	CallNew();
	return 0;
}

int PrintFunc2()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf("[%s:%d] hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	printf("[%s:%d] hello world again %d %d %d\n",__FILE__,__LINE__,a,b,c);
	CallNew();
	return 0;	
}

int main(int argc,char* argv[])
{
	newvar = 0;
	argc = argc;
	argv = argv;
	PrintFunc();
	return 0;
}