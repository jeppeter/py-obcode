#include <stdio.h>
#include <stdlib.h>
#include "main2.h"
#include "unpatch.h"
#include "callc.h"
#include <Windows.h>

OB_INSERT();

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

int ccprint_out_a(void)
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





int ccprint_out_b(void)
{
    int x = 3, b = 3, c = 3;
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

int ccprint_out_c(void)
{
    int x = 3, b = 3, c = 3;
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
    int ret=0;
    argc =argc;
    argv =argv;
    ret = unpatch_handler(OB_MAP_FUNC);
    if (ret < 0) {
        OUTP("can not unpatch");
        return ret;
    }
#if 0
    dump_func(stdout,get_func_call((unsigned char*)&ccprint_out_a),0x1f0,"ccprint_out_a");
    dump_func(stdout,get_func_call((unsigned char*)&ccprint_out_b),0x1f0,"ccprint_out_b");
    dump_func(stdout,get_func_call((unsigned char*)&ccprint_out_c),0x1f0,"ccprint_out_c");
    dump_func(stdout,get_func_call((unsigned char*)&call_a),0x1f0,"call_a");
    dump_func(stdout,get_func_call((unsigned char*)&call_b),0x1f0,"call_b");
    dump_func(stdout,get_func_call((unsigned char*)&call_c),0x1f0,"call_c");
#endif
    ccprint_out_a();
    ccprint_out_b();
    ccprint_out_c();
    call_a();
    call_b();
    call_c();
    return 0;
}