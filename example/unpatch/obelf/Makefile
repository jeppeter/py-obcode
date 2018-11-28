
ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../.. )
endif
-include ${TOPDIR}/obcode.mak

CURDIR=$(shell readlink -f .)
OBJECTS_BASE=main.o unpatch.o callc.o
OBJECTS=$(patsubst %,${CURDIR}/%,${OBJECTS_BASE})
COMMA=,
COLON=;
FORMAT_CLAUSE=$(call UNOB_FUNC, '${CURDIR}/main.h${COLON}${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/main.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')

all:${CURDIR}/main

${CURDIR}/main:${OBJECTS}
	gcc -Wall -o $@ ${OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D ${CURDIR}/unpatch.json obpatchelf $@
endif


${CURDIR}/%.o:${CURDIR}/%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

${CURDIR}/unpatch.c:${CURDIR}/unpatch.json

${CURDIR}/unpatch.json:${CURDIR}/main.o ${CURDIR}/callc.o
	cp ${CURDIR}/main.o ${CURDIR}/main_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"main.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >${CURDIR}/unpatch.c
	/bin/echo "{}" >${CURDIR}/unpatch.json
else
	/bin/echo ${FORMAT_CLAUSE}
	python ${TOPDIR}/obcode.py --includefiles main.h -D ${CURDIR}/unpatch.json -o ${CURDIR}/unpatch.c obunpatchelf ${FORMAT_CLAUSE}
endif

clean:
	rm -f ${OBJECTS} ${CURDIR}/main_orig.o
	rm -f ${CURDIR}/unpatch.json ${CURDIR}/unpatch.c
	rm -f ${CURDIR}/main