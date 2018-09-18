# obcode for obfuscated code

>  this project is to obfuscated for the c code

## release history
> Sep 18th 2018 release 0.0.6 to use OB_INSERT with insert ok
> Sep 14th 2018 release 0.0.4 to make ok on #line and README ok
> Sep 13th 2018 release 0.0.2 to support for OB code

## howto 

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

