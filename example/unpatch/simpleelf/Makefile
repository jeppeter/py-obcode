
OBJECTS=main.o unpatch.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)
include ${TOPDIR}/obcode.mak

COLON=;
COMMA=,

all:main

main:${OBJECTS}
	gcc -Wall -o $@ ${OBJECTS}
	@$(call OB_ELF_PATCH,'dump${COLON}unpatch.json' 'output${COLON}main' ${CURDIR}/main.o ${CURDIR}/unpatch.o)


%.o:%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

unpatch.c:unpatch.json

unpatch.json:main.o
	@$(call OB_ELF_UNPATCH,'includefiles${COLON}main.h' 'dump${COLON}unpatch.json' 'output${COLON}unpatch.c' '${CURDIR}/main.o${COLON}print_out_a')

clean:
	rm -f ${OBJECTS} main_orig.o
	rm -f unpatch.json unpatch.c
	rm -f main