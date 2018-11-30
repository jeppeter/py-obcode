#include <stdlib.h>
#include <stdio.h>
#include <Windows.h>
#include <obcode.h>

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

int pcc(void)
{
    int x = 1, b = 2, c = 3;
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    return 0;
}

unsigned char* get_func_call(unsigned char* p)
{
	unsigned char* pretp = p;
	signed int* pjmp;
	if (*pretp == 0xe9) {
		pjmp = (signed int*) (pretp + 1);
		pretp += (sizeof(*pjmp) + 1);
		pretp += (*pjmp);
	}
	OUTP("pretp [%p]", pretp);
	return pretp;
}

int main(int argc,char* argv[])
{
	argc = argc;
	argv = argv;
	get_func_call((unsigned char*)pcc);
	return 0;
}