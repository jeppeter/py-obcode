#include <stdio.h>
#include <stdlib.h>
#include "main.h"

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

int print_out_a(void)
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


OB_MAP_FUNCTION();

int main(int argc, char* argv[])
{
    int ret;
    argc =argc;
    argv =argv;
    ret = unpatch_handler(OB_MAP_FUNC);
    if (ret < 0) {
        OUTP("can not unpatch");
        return ret;
    }
    //dump_func(stdout,&print_out_a,0x1f0);
    print_out_a();
    return 0;
}