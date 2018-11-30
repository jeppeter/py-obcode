#include "callc.h"
#include <stdio.h>
#include <stdlib.h>

#define OUTP(...) do{fprintf(stdout,"[%s:%d] ",__FILE__,__LINE__); fprintf(stdout,__VA_ARGS__);fprintf(stdout,"\n");}while(0)

#if 1
int call_a(void)
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

int call_b(void)
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
#endif

int call_c(void)
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

void dump_func(FILE* fp, void* funcaddr, int size, const char* fmt,...)
{
    int i;
    unsigned char* ptr = (unsigned char*)funcaddr;
    unsigned char* plast = ptr;
    va_list ap;
    fprintf(fp,"addr [%p] size[0x%x:%d]", funcaddr, size,size);
    if (fmt != NULL) {
        va_start(ap,fmt);
        vfprintf(fp,fmt,ap);
    }
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
            }
            fprintf(fp, "\n");
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

unsigned char* get_func_call(unsigned char* p)
{
    unsigned char* pretp = p;
    signed int* pjmp;
    if (*pretp == 0xe9) {
        pjmp = (signed int*) (pretp + 1);
        pretp += (sizeof(*pjmp) + 1);
        pretp += (*pjmp);
    }
    return pretp;
}
