#include <obcode.h>
#include <stdio.h>

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5");
OB_INSERT();

int CallNew()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf("[%s:%d] up hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	return 0;
}

extern int OB_VAR(newvar2);
extern int OB_VAR_SPEC("namemax=100",newvar5);
int OB_DECL_VAR(newvar)=2;
int OB_DECL_VAR_SPEC("namemax=20",newvv)=20;

int OB_FUNC PrintFunc()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	OB_CODE(a,b,c);
	printf("[%s:%d] hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	OB_CODE_SPEC("funcmax=3,funcmin=1,debug=10",a,b,c);
	printf("[%s:%d] hello world again %d %d %d\n",__FILE__,__LINE__,a,b,c);
	CallNew();
	return 0;
}

int OB_FUNC_SPEC("namemin=20,namemax=30") PrintFunc2()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	OB_CODE_SPEC("funcmin=20,funcmax=30",a,b,c);
	printf("[%s:%d] hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	OB_CODE_SPEC("funcmax=3,funcmin=1,debug=10",a,b,c);
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