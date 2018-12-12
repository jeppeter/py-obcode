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
#define  OB_RANDOM_NAME(x)                  x
#define  OB_RANDOM_NAME_SPEC(c,x)           x
#define  OB_EXPAND_CODE(...)                do{}while(0)
#define  OB_EXPAND_CODE_SPEC(...)           do{}while(0)

/*to make the configuration for this file*/
#define  OB_CONFIG(x)

/*to make the insert code notification*/
#define  OB_INSERT()
#define  OB_INSERT_SPEC(x)

#define  OB_CONSTANT_STR(...)           __VA_ARGS__
#define  OB_CONSTANT_WSTR(...)          __VA_ARGS__

#define  OB_CONSTANT_STR_SPEC(x,...)    __VA_ARGS__
#define  OB_CONSTANT_WSTR_SPEC(x,...)   __VA_ARGS__

#define  OB_MIXED_STR(x)                x
#define  OB_MIXED_STR_SPEC(c,x)         x
#define  OB_MIXED_WSTR(x)               x
#define  OB_MIXED_WSTR_SPEC(c,x)        x



#if defined(_MSC_VER)
#include <Windows.h>
#define  OB_TYPEOF(x)                       decltype(x)
#define  OB_LL_VALUE(x)                     x##UL

#ifdef _M_X64
typedef UINT64                              OB_ADDR;
#else
typedef UINT32                              OB_ADDR;
#endif

#elif defined(__GNUC__)
#define  OB_TYPEOF(x)                       typeof(x)

#define OB_ADDR                             unsigned long int
#define OB_LL_VALUE(x)                      x##ULL
#else
#error "not supported compilers"
#endif


#define OB_MAP_EXEC                   1
#define OB_MAP_READ                   2
#define OB_MAP_WRITE                  4

typedef int (*map_prot_func_t)(void* addr, int size, int prot);

#define  OB_PAGE_ALIGN                     4096
#define  OB_PAGE_MASK                      (OB_PAGE_ALIGN - 1)


#if defined(OB_MMAP)

#if defined(_MSC_VER)

#include <Windows.h>

#define OB_MAP_FUNCTION()                                                                         \
int win_map_prot(void* addr, int size, int prot)                                                  \
{                                                                                                 \
	DWORD origprot;                                                                               \
	DWORD setprot=0;                                                                              \
	BOOL bret;                                                                                    \
	OB_ADDR pstartalign = (OB_ADDR) addr;                                                         \
	OB_ADDR pendalign = (OB_ADDR) addr;                                                           \
	SIZE_T mapsize=0;                                                                             \
	pendalign += size;                                                                            \
	pstartalign &= (OB_ADDR)(~(OB_ADDR)OB_PAGE_MASK);                                             \
	pendalign += OB_PAGE_MASK;                                                                    \
	pendalign &= (OB_ADDR)(~(OB_ADDR)OB_PAGE_MASK);                                               \
	mapsize = (SIZE_T)(pendalign - pstartalign);                                                  \
	if (prot== (OB_MAP_EXEC | OB_MAP_READ)) {                                                     \
		setprot = PAGE_EXECUTE_READ;                                                              \
	} else if (prot == (OB_MAP_READ | OB_MAP_EXEC | OB_MAP_WRITE)) {                              \
		setprot = PAGE_EXECUTE_WRITECOPY;                                                         \
	} else {                                                                                      \
		return -1;                                                                                \
	}                                                                                             \
	bret = VirtualProtect((LPVOID)pstartalign, mapsize, setprot,&origprot);                       \
	if (!bret) {                                                                                  \
		return -2;                                                                                \
	}                                                                                             \
	return 0;                                                                                     \
}

#define OB_MAP_FUNC   win_map_prot


#elif defined(__GNUC__)

#include <sys/mman.h>


#define OB_MAP_FUNCTION()                                                                         \
int ux_map_prot(void* addr, int size, int prot)                                                   \
{                                                                                                 \
	OB_ADDR addralign = (OB_ADDR)(addr);                                                          \
	OB_ADDR addrendalign = (addralign + size);                                                    \
	int alignsize = size;                                                                         \
	int uxprot=0;                                                                                 \
	addralign &= ~((OB_ADDR)OB_PAGE_MASK);                                                        \
	addrendalign += OB_PAGE_MASK;                                                                 \
	addrendalign &= ~((OB_ADDR)OB_PAGE_MASK);                                                     \
	alignsize = (addrendalign - addralign);                                                       \
	if (prot & OB_MAP_READ) {                                                                     \
		uxprot |= PROT_READ;                                                                      \
	}                                                                                             \
	if (prot & OB_MAP_WRITE) {                                                                    \
		uxprot |= PROT_WRITE;                                                                     \
	}                                                                                             \
	if (prot & OB_MAP_EXEC) {                                                                     \
		uxprot |= PROT_EXEC;                                                                      \
	}                                                                                             \
	return mprotect((void*)addralign,alignsize, uxprot);                                          \
}


#define OB_MAP_FUNC   ux_map_prot


#else
#error "not supported compilers"
#endif


#endif

#define   OB_CHKVAL_FUNC(failfunc)                         0
#define   OB_CHKVAL_FUNC_SPEC(cfg,failfunc)                0

typedef void (*m_check_fail_func_t)(int errcode,char* name);


#ifndef OB_PRINT_FUNC
#define OB_PRINT_FUNC     printf
#endif

#ifdef  OB_DEBUG_MODE
#define OB_DEBUG(...)                                                                             \
  do{                                                                                             \
  	OB_PRINT_FUNC("[%s:%d] ",__FILE__,__LINE__);                                                  \
  	OB_PRINT_FUNC(__VA_ARGS__);                                                                   \
  	OB_PRINT_FUNC("\n");                                                                          \
  }while(0)

#define OB_BUFFER_FMT(ptr,size,...)                                                               \
  do{                                                                                             \
  	unsigned char* __pptr = (unsigned char*) (ptr);                                               \
  	unsigned char* __lastptr=__pptr;                                                              \
  	unsigned int __curi=0;                                                                        \
  	unsigned int __csize=(unsigned int)(size);                                                    \
  	OB_PRINT_FUNC("[%s:%d] ",__FILE__,__LINE__);                                                  \
  	OB_PRINT_FUNC(__VA_ARGS__);                                                                   \
  	for (__curi=0;__curi < __csize;__curi ++,__pptr ++) {                                         \
  		if ((__curi % 16) == 0) {                                                                 \
  			if (__lastptr != __pptr) {                                                            \
  				OB_PRINT_FUNC("    ");                                                            \
  				while(__lastptr != __pptr) {                                                      \
  					if (*__lastptr >= ' ' && *__lastptr <= '~') {                                 \
  						OB_PRINT_FUNC("%c",*__lastptr);                                           \
  					} else {                                                                      \
  						OB_PRINT_FUNC(".");                                                       \
  					}                                                                             \
  					__lastptr ++;                                                                 \
  				}                                                                                 \
  			}                                                                                     \
  			OB_PRINT_FUNC("\n[%p]0x%08x:",__pptr,__curi);                                         \
  		}                                                                                         \
  		OB_PRINT_FUNC(" 0x%02x", *__pptr);                                                        \
  	}                                                                                             \
  	if (__lastptr != __pptr) {                                                                    \
  		while((__curi % 16) != 0) {                                                               \
  			OB_PRINT_FUNC( "     ");                                                              \
  			__curi ++;                                                                            \
  		}                                                                                         \
  		OB_PRINT_FUNC("    ");                                                                    \
  		while(__lastptr != __pptr) {                                                              \
  			if (*__lastptr >= ' ' && *__lastptr <= '~') {                                         \
  				OB_PRINT_FUNC("%c",*__lastptr);                                                   \
  			} else {                                                                              \
  				OB_PRINT_FUNC(".");                                                               \
  			}                                                                                     \
  			__lastptr ++;                                                                         \
  		}                                                                                         \
  		OB_PRINT_FUNC("\n");                                                                      \
  	}                                                                                             \
  }while(0)
#else
#define OB_DEBUG(...)    do{} while(0)
#define OB_BUFFER_FMT(ptr,size,...) do {}while(0)
#endif


#ifdef __cplusplus
};
#endif /* __cplusplus*/

#endif /* __OBCODE_H_A55150068F40BD6E23606B22C17D3F67__ */
