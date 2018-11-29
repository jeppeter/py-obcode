ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../..)
endif

include ${TOPDIR}/obcode.mak

CURDIR=$(shell readlink -f .)
INCLUDE_FLAGS=-I${TOPDIR}/include
COMMA=,
COLON=;
somain1_FORMAT_CLAUSE=$(call UNOB_FUNC, '${CURDIR}/somain1.h${COLON}${CURDIR}/somain1.o${COLON}main1_print_out_a${COMMA}main1_print_out_b${COMMA}main1_print_out_c' '${CURDIR}/callc.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')
somain2_FORMAT_CLAUSE=$(call UNOB_FUNC, '${CURDIR}/somain2.h${COLON}${CURDIR}/somain2.o${COLON}main2_print_out_a${COMMA}main2_print_out_b${COMMA}main2_print_out_c' '${CURDIR}/callc.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')


all:${CURDIR}/main

${CURDIR}/main:${CURDIR}/main.o ${CURDIR}/somain1.so ${CURDIR}/somain2.so
	gcc -Wall -o $@ ${CURDIR}/main.o  -ldl


${CURDIR}/main.o:${CURDIR}/main.c
	gcc -Wall ${INCLUDE_FLAGS} -c $< -o $@

${CURDIR}/somain1.so:${CURDIR}/somain1.o ${CURDIR}/callc.o ${CURDIR}/somain1_unpatch.o ${CURDIR}/unpatch.json
	gcc -Wall -shared -o $@ ${CURDIR}/somain1.o ${CURDIR}/callc.o ${CURDIR}/somain1_unpatch.o
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D ${CURDIR}/unpatch.json -o $@ obpatchelf ${CURDIR}/somain1.o ${CURDIR}/somain1_unpatch.o ${CURDIR}/callc.o
endif


${CURDIR}/somain2.so:${CURDIR}/somain2.o ${CURDIR}/callc.o ${CURDIR}/somain2_unpatch.o ${CURDIR}/unpatch.json
	gcc -Wall  -shared -o $@ ${CURDIR}/somain2.o ${CURDIR}/callc.o ${CURDIR}/somain2_unpatch.o
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D ${CURDIR}/unpatch.json -o $@ obpatchelf ${CURDIR}/somain2.o ${CURDIR}/somain2_unpatch.o ${CURDIR}/callc.o
endif

${CURDIR}/%.o:${CURDIR}/%.c
	gcc -Wall ${INCLUDE_FLAGS} -DOB_MMAP -fPIC -shared -c $< -o $@

${CURDIR}/unpatch.json: ${CURDIR}/somain1_unpatch.c ${CURDIR}/somain2_unpatch.c

${CURDIR}/somain1_unpatch.c:${CURDIR}/somain1.o ${CURDIR}/callc.o
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"unpatch.h\"\n int unpatch_handler(map_prot_func_t protfunc) {return 0;}" >$@
	/bin/echo "{}" >${CURDIR}/unpatch.json
else
	python ${TOPDIR}/obcode.py --includefiles somain1.h --includefiles unpatch.h --includefiles callc.h -D ${CURDIR}/unpatch.json -o ${CURDIR}/somain1_unpatch.c obunpatchelf ${somain1_FORMAT_CLAUSE}
endif

${CURDIR}/somain2_unpatch.c:${CURDIR}/somain2.o ${CURDIR}/callc.o
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"unpatch.h\"\n int unpatch_handler(map_prot_func_t protfunc) {return 0;}" >$@
	/bin/echo "{}" >${CURDIR}/unpatch.json
else
	python ${TOPDIR}/obcode.py --includefiles somain2.h --includefiles unpatch.h --includefiles callc.h -D ${CURDIR}/unpatch.json -o ${CURDIR}/somain2_unpatch.c obunpatchelf ${somain2_FORMAT_CLAUSE}
endif


clean:
	rm -f ${CURDIR}/main ${CURDIR}/somain2.so ${CURDIR}/somain1.so
	rm -f ${CURDIR}/*.o
	rm -f ${CURDIR}/somain2_unpatch.c ${CURDIR}/somain1_unpatch.c
	rm -f ${CURDIR}/unpatch.json