#include <obcode.h>
#include <stdio.h>
#include <wchar.h>

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5,debug=5");
OB_INSERT();

int CallNew()
{
    int a, b, c;
    a = 1;
    b = 2;
    c = 3;
    printf(OB_MIXED_STR("[%s:%d] up hello world %d %d %d\n"), __FILE__, __LINE__, a, b, c);
    return 0;
}

extern int newvar2;
extern int newvar5;
int newvar = 2;
int newvv = 20;
void output_buffer(const char* file, int line, unsigned char* pbuf, int buflen)
{
    unsigned char* ptr = pbuf, *plast = pbuf;
    int i;
    fprintf(stdout, "[%s:%d] ", file, line);
    for (i = 0; i < buflen; i++, ptr++) {
        if ((i % 16) == 0) {
            if (i > 0) {
                fprintf(stdout, "    ");
                while (plast != ptr) {
                    if (*plast >= ' ' && *plast <= '~') {
                        fprintf(stdout, "%c", *plast);
                    } else {
                        fprintf(stdout, ".");
                    }
                    plast ++;
                }
            }
            fprintf(stdout, "\n0x%08x", i);
        }
        fprintf(stdout, " 0x%02x", *ptr);
    }

    if (plast != ptr) {
        while ((i % 16) != 0) {
            fprintf(stdout, "     ");
            i ++;
        }
        fprintf(stdout, "    ");
        while (plast != ptr) {
            if (*plast >= ' ' && *plast <= '~') {
                fprintf(stdout, "%c", *plast);
            } else {
                fprintf(stdout, ".");
            }
            plast ++;
        }
    }
    fprintf(stdout, "\n");
    return;
}

int PrintFunc()
{
    int a, b, c;
    a = 1;
    b = 2;
    c = 3;
    printf(OB_MIXED_STR_SPEC("funcname=17", "[%s:%d] hello world %d %d %d\n"), __FILE__, __LINE__, a, b, c);
    printf(OB_MIXED_STR_SPEC("funcmin=10,funcmax=30", "[%s:%d] hello world again %d %d %d\n"), __FILE__, __LINE__, a, b, c);
    fwprintf(stderr, OB_MIXED_WSTR(L"[%hs:%d] hello world wide %d %d %d\n"), OB_MIXED_STR_SPEC("funcmin=10,funcmax=30", "cc again"), __LINE__, a, b, c);
    fwprintf(stderr, OB_MIXED_WSTR_SPEC("funcname=30", L"[%hs:%d] hello world wide %d %d %d\n"), OB_MIXED_STR("cc again"), __LINE__, a, b, c);
    output_buffer(__FILE__,__LINE__,(unsigned char*)OB_MIXED_WSTR(L"[%hs:%d] hello world wide %d %d %d\n"),144);
    CallNew();
    return 0;
}

int PrintFunc2()
{
    int a, b, c;
    a = 1;
    b = 2;
    c = 3;
    printf("[%s:%d] hello world %d %d %d\n", __FILE__, __LINE__, a, b, c);
    printf("[%s:%d] hello world again %d %d %d\n", __FILE__, __LINE__, a, b, c);
    CallNew();
    return 0;
}

int main(int argc, char* argv[])
{
    newvar = 0;
    argc = argc;
    argv = argv;
    PrintFunc();
    return 0;
}