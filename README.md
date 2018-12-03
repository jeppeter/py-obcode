# obcode for obfuscated code

>  this project is to obfuscated for the c code

## release history
* Dec 3rd 2018  release 0.3.4 to add OB_ELF_PATCH and OB_ELF_UNPATCH macro into obcode.mak.tmpl
* Nov 30th 2018 release 0.3.2 to make x86 and x64 linux windows all ok
* Nov 28th 2018 release 0.3.0 to make get obunfunc with obcode.mak ok and make multiple object to handle for objects
* Nov 27th 2018 release 0.2.6 to fixup bug when used OB_MMAP to include OB_PATCH
* Nov 16th 2018 release 0.2.4 to make the unpatch coding in the elf and pe format
* Oct 29th 2018 release 0.2.2 to make OB_MIXED_STR OB_MIXED_STR_SPEC OB_MIXED_WSTR OB_MIXED_WSTR_SPEC ok
* Oct 25th 2018 release 0.1.8 to make OB_CONSTANT_STR OB_CONSTANT_STR_SPEC OB_CONSTANT_WSTR OB_CONSTANT_WSTR_SPEC
* Oct 24th 2018 release 0.1.6 to make new parse for parameter with parse_param function
* Sep 21st 2018 release 0.1.4 to make trans handler to obtrans handler
* Sep 21st 2018 release 0.1.2 to make oblist handler in obcode.py
* Sep 20th 2018 release 0.1.0 to make UNOB_MAK_FILE with file reversemap
* Sep 20th 2018 release 0.0.8 to make OB_MAK_FILE with file handle
* Sep 18th 2018 release 0.0.6 to use OB_INSERT with insert ok
* Sep 14th 2018 release 0.0.4 to make ok on #line and README ok
* Sep 13th 2018 release 0.0.2 to support for OB code

## howto cob

> first you should include the file obcode.h in the direcotry of include
> then you changed the file or function

```c
#include <obcode.h>
#include <stdio.h>

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5");

int CallNew()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf("[%s:%d] up hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	return 0;
}

extern int OB_VAR(newvar2);
int OB_DECL_VAR(newvar)=2;

int OB_FUNC PrintFunc()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	OB_CODE(a,b,c);
	printf("[%s:%d] hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	OB_CODE_SPEC("funcmax=3,funcmin=1,debug=10",a,b,c);
	printf("[%s:%d] hello world again %d %d %d\n",__FILE__,__LINE__,a,b,c);
	CallNew();
	return 0;
}

int main(int argc,char* argv[])
{
	newvar = 0;
	PrintFunc();
	return 0;
}
```

> first compile in normal mode
```shell
gcc -Wall -Ipath_of_obcode/include -o main -c main.c
```

> the output is 
```shell
$./main
[d.c:26] hello world 1 2 3
[d.c:28] hello world again 1 2 3
[d.c:12] up hello world 1 2 3
```

> if you run obfuscated 
```shell
python obcode.py cob main.c main_ob.c
```

> the output maybe like this because obcode used random ,so it will give not the exactly the code
```c
#include <obcode.h>
#include <stdio.h>


int prefix_1_GncxB4(unsigned char* pbuf,int size,unsigned char* pxorcode, int xorsize)
{
    int i,curi;

    for (i=0;i<size;i++){
        curi = (i % xorsize);
        pbuf[i] = pbuf[i] ^ pxorcode[curi];
    }

    return size;
}


int prefix_1_o4JNG(unsigned char* pbuf,int size,unsigned char* pxorcode, int xorsize)
{
    int i,curi;

    for (i=0;i<size;i++){
        curi = (i % xorsize);
        pbuf[i] = pbuf[i] ^ pxorcode[curi];
    }

    return size;
}


int prefix_1_GsaIZ(unsigned char* pbuf,int size)
{


    if ( 0 < size) {
        pbuf[0] = 130;
    }
    if ( 1 < size) {
        pbuf[1] = 186;
    }
    if ( 2 < size) {
        pbuf[2] = 74;
    }
    if ( 3 < size) {
        pbuf[3] = 198;
    }
    if ( 4 < size) {
        pbuf[4] = 210;
    }

    if ( 5 < size) {
        pbuf[5] = 70;
    }
    if ( 6 < size) {
        pbuf[6] = 205;
    }
    if ( 7 < size) {
        pbuf[7] = 194;
    }
    if ( 8 < size) {
        pbuf[8] = 144;
    }
    if ( 9 < size) {
        pbuf[9] = 122;
    }

    if ( 10 < size) {
        pbuf[10] = 32;
    }
    if ( 11 < size) {
        pbuf[11] = 193;
    }
    if ( 12 < size) {
        pbuf[12] = 108;
    }
    if ( 13 < size) {
        pbuf[13] = 28;
    }
    if ( 14 < size) {
        pbuf[14] = 137;
    }

    if ( 15 < size) {
        pbuf[15] = 56;
    }

    if (11 < size && 8 < size){
        pbuf[11] = pbuf[11] ^ pbuf[8];
    }
    if (13 < size && 14 < size){
        pbuf[13] = pbuf[13] ^ pbuf[14];
    }
    if (13 < size && 10 < size){
        pbuf[13] = pbuf[13] ^ pbuf[10];
    }
    if (3 < size && 14 < size){
        pbuf[3] = pbuf[3] ^ pbuf[14];
    }
    if (1 < size && 9 < size){
        pbuf[1] = pbuf[1] ^ pbuf[9];
    }

    if (2 < size && 8 < size){
        pbuf[2] = pbuf[2] ^ pbuf[8];
    }
    if (14 < size && 0 < size){
        pbuf[14] = pbuf[14] ^ pbuf[0];
    }
    if (13 < size && 14 < size){
        pbuf[13] = pbuf[13] ^ pbuf[14];
    }
    if (4 < size && 8 < size){
        pbuf[4] = pbuf[4] ^ pbuf[8];
    }
    if (4 < size && 7 < size){
        pbuf[4] = pbuf[4] ^ pbuf[7];
    }

    if (8 < size){
        pbuf[0] = pbuf[0] ^ pbuf[8];
        pbuf[0] = pbuf[0] ^ 40;
    }
    if (0 < size){
        pbuf[1] = pbuf[1] ^ pbuf[0];
        pbuf[1] = pbuf[1] ^ 132;
    }
    if (13 < size){
        pbuf[2] = pbuf[2] ^ pbuf[13];
        pbuf[2] = pbuf[2] ^ 205;
    }

    if (7 < size){
        pbuf[3] = pbuf[3] ^ pbuf[7];
        pbuf[3] = pbuf[3] ^ 117;
    }
    if (11 < size){
        pbuf[4] = pbuf[4] ^ pbuf[11];
        pbuf[4] = pbuf[4] ^ 75;
    }
    if (2 < size){
        pbuf[5] = pbuf[5] ^ pbuf[2];
        pbuf[5] = pbuf[5] ^ 206;
    }

    if (12 < size){
        pbuf[6] = pbuf[6] ^ pbuf[12];
        pbuf[6] = pbuf[6] ^ 117;
    }
    if (3 < size){
        pbuf[7] = pbuf[7] ^ pbuf[3];
        pbuf[7] = pbuf[7] ^ 96;
    }
    if (7 < size){
        pbuf[8] = pbuf[8] ^ pbuf[7];
        pbuf[8] = pbuf[8] ^ 109;
    }

    if (10 < size){
        pbuf[9] = pbuf[9] ^ pbuf[10];
        pbuf[9] = pbuf[9] ^ 206;
    }
    if (7 < size){
        pbuf[10] = pbuf[10] ^ pbuf[7];
        pbuf[10] = pbuf[10] ^ 91;
    }
    if (4 < size){
        pbuf[11] = pbuf[11] ^ pbuf[4];
        pbuf[11] = pbuf[11] ^ 86;
    }

    if (2 < size){
        pbuf[12] = pbuf[12] ^ pbuf[2];
        pbuf[12] = pbuf[12] ^ 94;
    }
    if (13 < size){
        pbuf[13] = pbuf[13] ^ pbuf[13];
        pbuf[13] = pbuf[13] ^ 5;
    }
    if (2 < size){
        pbuf[14] = pbuf[14] ^ pbuf[2];
        pbuf[14] = pbuf[14] ^ 131;
    }

    if (5 < size){
        pbuf[15] = pbuf[15] ^ pbuf[5];
        pbuf[15] = pbuf[15] ^ 205;
    }

    return 16 < size ? 16 : size;
}


void prefix_1_ppJ4VOEy(unsigned char* pbuf,int size)
{


    if (15 < size && 4 < size){
        pbuf[15] = pbuf[15] ^ pbuf[4];
    }
    if (5 < size && 4 < size){
        pbuf[5] = pbuf[5] ^ pbuf[4];
    }
    if (10 < size && 7 < size){
        pbuf[10] = pbuf[10] ^ pbuf[7];
    }
    if (13 < size && 12 < size){
        pbuf[13] = pbuf[13] ^ pbuf[12];
    }
    if (0 < size && 7 < size){
        pbuf[0] = pbuf[0] ^ pbuf[7];
    }

    if (1 < size && 1 < size){
        pbuf[1] = pbuf[1] ^ pbuf[1];
    }
    if (6 < size && 0 < size){
        pbuf[6] = pbuf[6] ^ pbuf[0];
    }
    if (13 < size && 4 < size){
        pbuf[13] = pbuf[13] ^ pbuf[4];
    }
    if (9 < size && 15 < size){
        pbuf[9] = pbuf[9] ^ pbuf[15];
    }
    if (4 < size && 9 < size){
        pbuf[4] = pbuf[4] ^ pbuf[9];
    }

    return;
}


#line 3 "/home/bt/sources/py-obcode/example/srcdir/d.c"

OB_CONFIG("maxround=10,funcmax=1,funcmin=1,namemax=10,namemin=5");

int CallNew()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
	printf("[%s:%d] up hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
	return 0;
}

/*#lineno:16*/
/*[extern int OB_VAR(newvar2);]*/
#define newvar2 prefix_1_pkcqGBAy
#line 16 "/home/bt/sources/py-obcode/example/srcdir/d.c"
extern int OB_VAR(newvar2);
/*#lineno:17*/
/*[int OB_DECL_VAR(newvar)=2;]*/
#define newvar prefix_1_1nNc4Xom2c
#line 17 "/home/bt/sources/py-obcode/example/srcdir/d.c"
int OB_DECL_VAR(newvar)=2;

/*#lineno:19*/
/*[int OB_FUNC PrintFunc()]*/
#define PrintFunc prefix_1_x13qBdAwt
#line 19 "/home/bt/sources/py-obcode/example/srcdir/d.c"
int OB_FUNC PrintFunc()
{
	int a,b,c;
	a = 1;
	b = 2;
	c = 3;
    
    /*#lineno:25*/
    /*[	OB_CODE(a,b,c);]*/
    do {
        void* prefix_1_7L3R9 = (void*)&(a);
        unsigned long long prefix_1_K2dENr3Z = (unsigned long long)prefix_1_7L3R9;
        void* prefix_1_n5n4sVfppq = (void*)&(b);
        unsigned long long prefix_1_dw1X3fR = (unsigned long long)prefix_1_n5n4sVfppq;
        void* prefix_1_t9orkQcE4k = (void*)&(c);
        unsigned long long prefix_1_6N1pkJud = (unsigned long long)prefix_1_t9orkQcE4k;
        unsigned char prefix_1_48Q8FwG[16];
        int prefix_1_vqqSEY=16;
        int prefix_1_Vt8Ft;
        
        
        prefix_1_Vt8Ft = prefix_1_GsaIZ(prefix_1_48Q8FwG,prefix_1_vqqSEY);
        prefix_1_GncxB4(((unsigned char*)&prefix_1_6N1pkJud),sizeof(prefix_1_6N1pkJud),prefix_1_48Q8FwG,prefix_1_Vt8Ft);
        prefix_1_ppJ4VOEy(prefix_1_48Q8FwG,prefix_1_Vt8Ft);
        
        prefix_1_Vt8Ft = prefix_1_GsaIZ(prefix_1_48Q8FwG,prefix_1_vqqSEY);
        prefix_1_o4JNG(((unsigned char*)&prefix_1_6N1pkJud),sizeof(prefix_1_6N1pkJud), prefix_1_48Q8FwG,prefix_1_Vt8Ft);
        prefix_1_ppJ4VOEy(prefix_1_48Q8FwG,prefix_1_Vt8Ft);
        
        prefix_1_7L3R9 = (void*) prefix_1_K2dENr3Z;
        prefix_1_n5n4sVfppq = (void*) prefix_1_dw1X3fR;
        prefix_1_t9orkQcE4k = (void*) prefix_1_6N1pkJud;
        
        a = (OB_TYPEOF(a)) *(((OB_TYPEOF(a)*)(prefix_1_7L3R9)));
        b = (OB_TYPEOF(b)) *(((OB_TYPEOF(b)*)(prefix_1_n5n4sVfppq)));
        c = (OB_TYPEOF(c)) *(((OB_TYPEOF(c)*)(prefix_1_t9orkQcE4k)));
    } while(0);
#line 26 "/home/bt/sources/py-obcode/example/srcdir/d.c"
	printf("[%s:%d] hello world %d %d %d\n",__FILE__,__LINE__,a,b,c);
    
    /*#lineno:27*/
    /*[	OB_CODE_SPEC("funcmax=3,funcmin=1,debug=10",a,b,c);]*/
    do {
        /* variables:prefix prefix_2 variables:namemax 14 */
        void* prefix_2_1CfUbQbsjhirW = (void*)&(a);
        unsigned long long prefix_2_a5afhfVFW6Qf5EoVi9 = (unsigned long long)prefix_2_1CfUbQbsjhirW;
        void* prefix_2_EfHBJvyjgZqQmQBZfb = (void*)&(b);
        unsigned long long prefix_2_Mgtua = (unsigned long long)prefix_2_EfHBJvyjgZqQmQBZfb;
        void* prefix_2_tXpCuuK8GHeLbwVgCS = (void*)&(c);
        unsigned long long prefix_2_EP0b8BAfitz3TaYhFr = (unsigned long long)prefix_2_tXpCuuK8GHeLbwVgCS;
        unsigned char prefix_2_ksHmtOMrMpEVu[16];
        int prefix_2_ZOHXCMv3dihKg4dzFZ=16;
        int prefix_2_9l3CYqQv42egT;
        
        
        prefix_2_9l3CYqQv42egT = prefix_1_GsaIZ(prefix_2_ksHmtOMrMpEVu,prefix_2_ZOHXCMv3dihKg4dzFZ);
        prefix_1_GncxB4(((unsigned char*)&prefix_2_Mgtua),sizeof(prefix_2_Mgtua),prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        prefix_1_ppJ4VOEy(prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        
        prefix_2_9l3CYqQv42egT = prefix_1_GsaIZ(prefix_2_ksHmtOMrMpEVu,prefix_2_ZOHXCMv3dihKg4dzFZ);
        prefix_1_GncxB4(((unsigned char*)&prefix_2_Mgtua),sizeof(prefix_2_Mgtua),prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        prefix_1_ppJ4VOEy(prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        /* format [2] times */
        
        prefix_2_9l3CYqQv42egT = prefix_1_GsaIZ(prefix_2_ksHmtOMrMpEVu,prefix_2_ZOHXCMv3dihKg4dzFZ);
        prefix_1_o4JNG(((unsigned char*)&prefix_2_Mgtua),sizeof(prefix_2_Mgtua), prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        prefix_1_ppJ4VOEy(prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        
        prefix_2_9l3CYqQv42egT = prefix_1_GsaIZ(prefix_2_ksHmtOMrMpEVu,prefix_2_ZOHXCMv3dihKg4dzFZ);
        prefix_1_o4JNG(((unsigned char*)&prefix_2_Mgtua),sizeof(prefix_2_Mgtua), prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        prefix_1_ppJ4VOEy(prefix_2_ksHmtOMrMpEVu,prefix_2_9l3CYqQv42egT);
        
        prefix_2_1CfUbQbsjhirW = (void*) prefix_2_a5afhfVFW6Qf5EoVi9;
        prefix_2_EfHBJvyjgZqQmQBZfb = (void*) prefix_2_Mgtua;
        prefix_2_tXpCuuK8GHeLbwVgCS = (void*) prefix_2_EP0b8BAfitz3TaYhFr;
        
        a = (OB_TYPEOF(a)) *(((OB_TYPEOF(a)*)(prefix_2_1CfUbQbsjhirW)));
        b = (OB_TYPEOF(b)) *(((OB_TYPEOF(b)*)(prefix_2_EfHBJvyjgZqQmQBZfb)));
        c = (OB_TYPEOF(c)) *(((OB_TYPEOF(c)*)(prefix_2_tXpCuuK8GHeLbwVgCS)));
    } while(0);
#line 28 "/home/bt/sources/py-obcode/example/srcdir/d.c"
	printf("[%s:%d] hello world again %d %d %d\n",__FILE__,__LINE__,a,b,c);
	CallNew();
	return 0;
}

int main(int argc,char* argv[])
{
	newvar = 0;
	PrintFunc();
	return 0;
}
```

> now compile the code ,run it 
```shell
$gcc -Wall -Ipath_of_obode/include -o main main_ob.c
$./main
[d.c:26] hello world 1 2 3
[d.c:28] hello world again 1 2 3
[d.c:12] up hello world 1 2 3
```

## keyword specification
> some keywords will used
-----------------
Key  | function |  Example |
| :------------: |:---------------|:---------------|
OB_VAR | to give the variable obfuscated | OB_VAR(x) |
OB_VAR_SPEC | to give the variable obfuscated with config | OB_VAR_SPEC("namemin=10,namemax=20",x) |
OB_VAR_DECL  | to give the variable obfuscated in declaration | extern int OB_VAR_DECL(x) |
OB_VAR_DECL_SPEC  | to give the variable obfuscated in declaration with config | extern int OB_VAR_DECL_SPEC("namemin=10,namemax=20",x) |
OB_FUNC | to give function obfuscated | int OB_FUNC print_function(const char* fmt) |
OB_FUNC_SPEC | to give function obfuscated with config | int OB_FUNC_SPEC("namemin=30,namemax=60") print_function(const char* fmt) |
OB_CODE | to insert non-sense code  with current used variable| OB_CODE(x,b,c) |
OB_CODE_SPEC | to insert non-sense code  with current used variable with config | OB_CODE_SPEC("funcmin=10,funcmax=20",x,b,c) |
OB_CONFIG | to give the configuration for current c file | OB_CONFIG("namemin=30,namemax=90") |
OB_INSERT | give the insert line in the file ,if no this ,will insert after #include appearing first empty line | OB_INSERT() |
OB_CONSTANT_STR | give the constant replace for the original format  | OB_CONSTANT_STR("hello world %s\n", "good"); |
OB_CONSTANT_STR_SPEC | give the constant replace for the original format  with specified config | OB_CONSTANT_STR_SPEC("funcname=10","hello world %s\n", "good"); |
OB_CONSTANT_WSTR | give the constant replace for the original format of wide string  | OB_CONSTANT_WSTR(L"hello world %hs\n", "good"); |
OB_CONSTANT_WSTR_SPEC | give the constant replace for the original format of wide string with specified config | OB_CONSTANT_WSTR_SPEC("funcname=10",L"hello world %hs\n", "good"); |
OB_MIXED_STR | to give the replace string constant with dynamic string | OB_MIXED_STR("hello world") |
OB_MIXED_STR_SPEC | to give the replace string constant with dynamic string  with config| OB_MIXED_STR_SPEC("funcname=10","hello world") |
OB_MIXED_WSTR | to give the replace wide string constant with dynamic wide string | OB_MIXED_WSTR(L"hello world") |
OB_MIXED_WSTR_SPEC | to give the replace wide string constant with dynamic wide string  with config| OB_MIXED_WSTR_SPEC("funcname=10",L"hello world") |


## config specification
> OB_CONFIG to make config for the file ,you can specified the value of some good
Option Keys
--------

Key  | Default Value | Comment |
| :------------: |:-------:| :-----------------------:|
prefix | 'prefix' | prefix  to specified for the name must not [] |
namemin | 5 | minimum name must >= 0 |
namemax  | 20 | name to specified length|
funcmin | 3 | minimum encode times  in OB_CODE or OB_CODE_SPEC |
funcmax | 20 | maximum xor encode in OB_CODE or OB_CODE_SPEC |
xorsize | 16 | xor bytes number |
maxround  | 32 | to form xor bytes times call |
debug | 0 | debug more information to c file  >= 3 will enable |
noline | 0 | 1 for not let #line into the file |

## howto makob
> this file will to run ./release.sh and include obcode.mak
> it will set PYTHON environment variable and depends on MAKOB_FILE 
> 

### example
```make

TOPDIR=$(shell readlink -f ../.. )
CURDIR=$(shell readlink -f .)
PYTHON=python

include ${TOPDIR}/obcode.mak
#include ${CURDIR}/v.mak

FILES=$(call OB_MAK_FILE,c.cpp d.cpp)
OBJECTS=$(patsubst %.cpp,%.o, ${FILES})

all:command

command:${OBJECTS}
    gcc -Wall -o $@ ${OBJECTS}

$(patsubst %.cpp,%.o, $(call OB_MAK_FILE,c.cpp)):$(call OB_MAK_FILE,c.cpp)

$(patsubst %.cpp,%.o, $(call OB_MAK_FILE,d.cpp)):$(call OB_MAK_FILE,d.cpp)

%.o:%.cpp
    gcc -Wall -c $< -o $@
    echo $(call UNOB_MAK_FILE,$<)
    echo $(call UNOB_MAK_FILE_SHORT,$<)


clean:
    rm -f ${OBJECTS}
    rm -f command

```

> run shell
```shell
make clean
make all
```

> get the result 
```shell
rm -f c.o d.o
rm -f command
gcc -Wall -c c.cpp -o c.o
echo c.cpp
c.cpp
echo c.cpp
c.cpp
gcc -Wall -c d.cpp -o d.o
echo d.cpp
d.cpp
echo d.cpp
d.cpp
gcc -Wall -o command c.o d.o
```

> if run shell with OBCODE
```shell
make O=1 clean && make O=1 all

rm -f /home/bt/sources/py-obcode/example/maklib/k4rFRfIHbT.o /home/bt/sources/py-obcode/example/maklib/5tfIVcEWgU.o
rm -f command
gcc -Wall -c /home/bt/sources/py-obcode/example/maklib/k4rFRfIHbT.cpp -o /home/bt/sources/py-obcode/example/maklib/k4rFRfIHbT.o
echo /home/bt/sources/py-obcode/example/maklib/c.cpp
/home/bt/sources/py-obcode/example/maklib/c.cpp
echo c.cpp
c.cpp
gcc -Wall -c /home/bt/sources/py-obcode/example/maklib/5tfIVcEWgU.cpp -o /home/bt/sources/py-obcode/example/maklib/5tfIVcEWgU.o
echo /home/bt/sources/py-obcode/example/maklib/d.cpp
/home/bt/sources/py-obcode/example/maklib/d.cpp
echo d.cpp
d.cpp
gcc -Wall -o command /home/bt/sources/py-obcode/example/maklib/k4rFRfIHbT.o /home/bt/sources/py-obcode/example/maklib/5tfIVcEWgU.o
```

> the output filename is random, so when you really run a little different

## howto patch code and unpatch code

> in pe format main.cpp
```c
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
```

> main.h
```c
#ifndef __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__
#define __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__

#include <obcode.h>

#ifdef __cplusplus
extern "C" {
#endif

int OB_FUNC unpatch_handler(map_prot_func_t protfunc);
int print_out_a(void);

#ifdef __cplusplus
};
#endif


#endif /* __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__ */
```

> makefile.win
```makefile
CURDIR=$(MAKEDIR)
TOPDIR=$(CURDIR)\..\..\..

CC      = cl.exe
LD      = link.exe
AR      = lib.exe
RM      = del
PYTHON  = python.exe
CP      = copy /Y



QUIETCMD=@
NOLOGO_CFLAGS=/nologo
NOLOGO_LDFLAGS=/nologo
NOLOGO_MAKEFLAGS=/NOLOGO
GIT_VERBOSE=--quiet

STATIC_LIB_CFLAGS=/MT
INC_LDFLAGS=


INC_CFLAGS = /I"$(TOPDIR)\include"
COM_CFLAGS = /DOB_MMAP=1 /Wall /wd"4820" /wd"4668" /wd"4127" /wd"4510" /wd"4512" /wd"4610" /wd"4710" /wd"5045"
REL_CFLAGS = 
DBG_CFLAGS = /Z7 /Od 


REL_LDFLAGS = 

CFLAGS  =  $(NOLOGO_CFLAGS) $(STATIC_LIB_CFLAGS) $(INC_CFLAGS) $(COM_CFLAGS) $(REL_CFLAGS) $(DBG_CFLAGS)
LDFLAGS = $(NOLOGO_LDFLAGS) $(INC_LDFLAGS) $(REL_LDFLAGS) -DEBUG

SOURCES=main.cpp unpatch.cpp
OBJECTS=$(SOURCES:.cpp=.obj)

!IF "$(PLATFORM)" == "X86"
main_CLAUSE= "$(CURDIR)\main.obj;print_out_a" "win32;"
!ELSE
main_CLAUSE= "$(CURDIR)\main.obj;print_out_a"
!ENDIF

all:main.exe

!IFDEF OB_PATCH
main.exe:$(OBJECTS)
    $(QUIETCMD) echo "call static $(OBJECTS)"
    $(QUIETCMD)$(LD) -out:$@  $(LDFLAGS)  $(OBJECTS)
    $(QUIETCMD)echo "use static lib"
    $(QUIETCMD)$(PYTHON) $(TOPDIR)\obcode.py -o $(CURDIR)\main.exe obpatchpe -D $(CURDIR)\unpatch.json  $(CURDIR)\main.obj $(CURDIR)\unpatch.obj
!ELSE
main.exe:$(OBJECTS)
    $(QUIETCMD) echo "call static $(OBJECTS)"
    $(QUIETCMD)$(LD) -out:$@  $(LDFLAGS)  $(OBJECTS)
    $(QUIETCMD)echo "use static lib"
!ENDIF

.cpp.obj:
    $(QUIETCMD)$(CC) $(CFLAGS) -c -Fo$@ $<

unpatch.cpp:unpatch.json


!IFDEF OB_PATCH
unpatch.json:main.obj
    $(QUIETCMD)$(PYTHON) $(TOPDIR)\obcode.py --includefiles main.h -D unpatch.json -o unpatch.cpp obunpatchcoff  $(main_CLAUSE)
!ELSE
unpatch.json:main.obj
    $(QUIETCMD)echo {} >unpatch.json
    $(QUIETCMD)echo #include "main.h" >unpatch.cpp
    $(QUIETCMD)echo int unpatch_handler(map_prot_func_t protfunc) { protfunc = protfunc;return 0;} >>unpatch.cpp
!ENDIF



clean:
    $(QUIETCMD) $(RM) *.exe *.obj *.pdb 2>NUL
    $(QUIETCMD) $(RM) unpatch.cpp unpatch.json 2>NUL
```

> run command
```shell
nmake /f makefile.win OB_PATCH=1 all
```

> get the main.exe it will change the byte of the function in the print_out_a and will make unpatch_handler ok
```shell
.\main.exe
[main.cpp:12] hello world x=1 b=2 c=3
[main.cpp:14] hello world x=1 b=2 c=3
[main.cpp:16] hello world x=1 b=2 c=3
[main.cpp:18] hello world x=1 b=2 c=3
[main.cpp:20] hello world x=1 b=2 c=3
```

> elf format main.c
```c
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
```

> main.h
```c
#ifndef __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__
#define __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__

#include <obcode.h>

#ifdef __cplusplus
extern "C" {
#endif

int OB_FUNC unpatch_handler(map_prot_func_t protfunc);
int print_out_a(void);

#ifdef __cplusplus
};
#endif


#endif /* __MAIN_H_B4A752BC7B8694C38FD413662A4302B4__ */
```

> Makefile
```makefile


OBJECTS=main.o unpatch.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)
include ${TOPDIR}/obcode.mak

COLON=;
COMMA=,

all:main

main:${OBJECTS}
    gcc -Wall -o $@ ${OBJECTS}
    @$(call ELF_PATCH,'dump${COLON}unpatch.json' 'output${COLON}main' ${CURDIR}/main.o ${CURDIR}/unpatch.o)


%.o:%.c
    gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

unpatch.c:unpatch.json

unpatch.json:main.o
    @$(call ELF_UNPATCH,'includefiles${COLON}main.h' 'dump${COLON}unpatch.json' 'output${COLON}unpatch.c' '${CURDIR}/main.o${COLON}print_out_a')

clean:
    rm -f ${OBJECTS} main_orig.o
    rm -f unpatch.json unpatch.c
    rm -f main
```

> run make it will change print_out_a function binary code and make unpatch_handler to unpatch
> output 
```shell
./main
[main.c:11] hello world x=1 b=2 c=3
[main.c:13] hello world x=1 b=2 c=3
[main.c:15] hello world x=1 b=2 c=3
[main.c:17] hello world x=1 b=2 c=3
[main.c:19] hello world x=1 b=2 c=3
```