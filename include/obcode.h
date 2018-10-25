#ifndef __OBCODE_H_A55150068F40BD6E23606B22C17D3F67__
#define __OBCODE_H_A55150068F40BD6E23606B22C17D3F67__

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus*/

#define  OB_FUNC
#define  OB_FUNC_SPEC(x)
#define  OB_CODE(...)
#define  OB_CODE_SPEC(...)
#define  OB_VAR(x)                          x
#define  OB_VAR_SPEC(c,x)                   x
#define  OB_DECL_VAR(x)                     x
#define  OB_DECL_VAR_SPEC(c,x)              x

/*to make the configuration for this file*/
#define  OB_CONFIG(x)

/*to make the insert code notification*/
#define  OB_INSERT()
#define  OB_INSERT_SPEC(x)

#define  OB_CONSTANT_STR(...)           __VA_ARGS__
#define  OB_CONSTANT_WSTR(...)          __VA_ARGS__

#define  OB_CONSTANT_STR_SPEC(x,...)    __VA_ARGS__
#define  OB_CONSTANT_WSTR_SPEC(x,...)   __VA_ARGS__


#if defined(_MSC_VER)
#include <Windows.h>
#define  OB_TYPEOF(x)                       decltype(x)

#ifdef _M_X64
typedef UINT64                              OB_ADDR;
#else
typedef UINT32                              OB_ADDR;
#endif

#elif defined(__GNUC__)
#define  OB_TYPEOF(x)                       typeof(x)

#define OB_ADDR                             unsigned long int

#else
#error "not supported compilers"
#endif

#ifdef __cplusplus
};
#endif /* __cplusplus*/

#endif /* __OBCODE_H_A55150068F40BD6E23606B22C17D3F67__ */
