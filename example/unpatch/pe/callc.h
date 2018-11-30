#ifndef __CALLC_H_33B8187EC3E1B69927CC2DB30134EF75__
#define __CALLC_H_33B8187EC3E1B69927CC2DB30134EF75__

#include <obcode.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus*/

int OB_FUNC call_a(void);
int OB_FUNC call_b(void);
int OB_FUNC call_c(void);
void OB_FUNC dump_func(FILE* fp, void* funcaddr, int size, const char* fmt,...);
unsigned char* get_func_call(unsigned char* p);

#ifdef __cplusplus
};
#endif /* __cplusplus*/

#endif /* __CALLC_H_33B8187EC3E1B69927CC2DB30134EF75__ */
