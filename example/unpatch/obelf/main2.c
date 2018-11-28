#include <stdio.h>
#include <stdlib.h>
#include "main2.h"
#include "callc.h"
#include "unpatch.h"

OB_INSERT()

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

int ccprint_out_a(void)
{
    int x = 3, b = 3, c = 3;
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    return 0;
}

#if 0

void dump_func(FILE* fp, void* funcaddr, int size)
{
    int i;
    unsigned char* ptr = (unsigned char*)funcaddr;
    unsigned char* plast = ptr;
    fprintf(fp,"addr [%p] size[0x%x:%d]\n", funcaddr, size,size);
    for (i = 0; i < size; i++) {
        if ((i % 16) == 0) {
            if (i > 0) {
                fprintf(fp, "    ");
                while (plast != ptr) {
                    if (*plast >= ' ' && *plast <= '~') {
                        fprintf(fp, "%c", *plast);
                    } else {
                        fprintf(fp, ".");
                    }
                    plast ++;
                }
                fprintf(fp, "\n");
            }
            fprintf(fp, "[%p][0x%08x]", ptr,i);
        }
        fprintf(fp, " 0x%02x", *ptr);
        ptr ++;
    }

    if (ptr != plast) {
        while ((i % 16)) {
            fprintf(fp, "     ");
            i ++;
        }
        fprintf(fp, "    ");
        while (plast != ptr) {
            if (*plast >= ' ' && *plast <= '~') {
                fprintf(fp, "%c", *plast);
            } else {
                fprintf(fp, ".");
            }
            plast ++;
        }
        fprintf(fp, "\n");
    }
    return;
}
#endif

int ccprint_out_b(void)
{
    int x = 3, b = 3, c = 3;
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    return 0;
}

int ccprint_out_c(void)
{
    int x = 3, b = 3, c = 3;
    OB_CODE(x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    OUTP("hello world x=%d b=%d c=%d", x, b, c);
    return 0;
}



OB_MAP_FUNCTION()

int main(int argc, char* argv[])
{
    unpatch_handler(OB_MAP_FUNC);
    //dump_func(stdout,&print_out_a,0x1f0);
    ccprint_out_a();
    ccprint_out_b();
    ccprint_out_c();
    call_c();
    call_a();
    call_b();
    return 0;
}