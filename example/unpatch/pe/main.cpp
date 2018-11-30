#include <stdio.h>
#include <stdlib.h>
#include "main.h"
#include "unpatch.h"
#include "callc.h"
#include <Windows.h>

OB_INSERT();


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





int print_out_b(void)
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

int print_out_c(void)
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
    dump_func(stdout,get_func_call((unsigned char*)&print_out_a),0x1f0,"print_out_a");
    dump_func(stdout,get_func_call((unsigned char*)&print_out_b),0x1f0,"print_out_b");
    dump_func(stdout,get_func_call((unsigned char*)&print_out_c),0x1f0,"print_out_c");
    dump_func(stdout,get_func_call((unsigned char*)&call_a),0x1f0,"call_a");
    dump_func(stdout,get_func_call((unsigned char*)&call_b),0x1f0,"call_b");
    dump_func(stdout,get_func_call((unsigned char*)&call_c),0x1f0,"call_c");
#endif
    print_out_a();
    print_out_b();
    print_out_c();
    call_a();
    call_b();
    call_c();
    return 0;
}