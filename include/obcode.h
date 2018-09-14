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

#define  OB_CONFIG(x)

#if defined(_MSC_VER)
#define  OB_TYPEOF(x)                       decltype(x)
#elif defined(__GNUC__)
#define  OB_TYPEOF(x)                       typeof(x)
#else
#error "not supported compilers"
#endif

#ifdef __cplusplus
};
#endif /* __cplusplus*/

#endif /* __OBCODE_H_A55150068F40BD6E23606B22C17D3F67__ */
