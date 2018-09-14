#include <obcode.h>
#include <stdio.h>

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5");

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
int OB_DECL_VAR(newvar)=2;

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

int main(int argc,char* argv[])
{
	newvar = 0;
	PrintFunc();
	return 0;
}