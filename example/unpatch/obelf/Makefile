
ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../.. )
endif
-include ${TOPDIR}/obcode.mak

CURDIR=$(shell readlink -f .)
COMMA=,
COLON=;
main_OBJECTS_BASE=main.o main_unpatch.o callc.o
main_OBJECTS=$(patsubst %,${CURDIR}/%,${main_OBJECTS_BASE})
main_FORMAT_CLAUSE=$(call UNOB_FUNC, '${CURDIR}/main.h${COLON}${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/callc.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')

main2_OBJECTS_BASE=main2.o main2_unpatch.o callc.o
main2_OBJECTS=$(patsubst %,${CURDIR}/%,${main2_OBJECTS_BASE})
main2_FORMAT_CLAUSE=$(call UNOB_FUNC, '${CURDIR}/main2.h${COLON}${CURDIR}/main2.o${COLON}ccprint_out_a${COMMA}ccprint_out_b${COMMA}ccprint_out_c' '${CURDIR}/callc.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')


all:${CURDIR}/main ${CURDIR}/main2

${CURDIR}/main:${main_OBJECTS}
	gcc -Wall -o $@ ${main_OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D ${CURDIR}/unpatch.json -o $@ obpatchelf ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o
endif

${CURDIR}/main2:${main2_OBJECTS}
	gcc -Wall -o $@ ${main2_OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D ${CURDIR}/unpatch.json -o $@ obpatchelf ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc.o
endif


${CURDIR}/%.o:${CURDIR}/%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

${CURDIR}/unpatch.json:${CURDIR}/main_unpatch.c ${CURDIR}/main2_unpatch.c

${CURDIR}/main_unpatch.c:${CURDIR}/main.o ${CURDIR}/callc.o
	cp ${CURDIR}/main.o ${CURDIR}/main_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"unpatch.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >${CURDIR}/main_unpatch.c
	/bin/echo "{}" >${CURDIR}/unpatch.json
else
	/bin/echo ${main_FORMAT_CLAUSE}
	python ${TOPDIR}/obcode.py --includefiles main.h --includefiles unpatch.h --includefiles callc.h -D ${CURDIR}/unpatch.json -o ${CURDIR}/main_unpatch.c obunpatchelf ${main_FORMAT_CLAUSE}
endif

${CURDIR}/main2_unpatch.c:${CURDIR}/main2.o ${CURDIR}/callc.o
	cp ${CURDIR}/main2.o ${CURDIR}/main2_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"unpatch.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >${CURDIR}/main2_unpatch.c
	/bin/echo "{}" >${CURDIR}/unpatch.json
else
	/bin/echo ${main2_FORMAT_CLAUSE}
	python ${TOPDIR}/obcode.py --includefiles main2.h --includefiles unpatch.h --includefiles callc.h -D ${CURDIR}/unpatch.json -o ${CURDIR}/main2_unpatch.c obunpatchelf ${main2_FORMAT_CLAUSE}
endif


clean:
	rm -f ${main_OBJECTS} ${CURDIR}/main_orig.o
	rm -f ${main2_OBJECTS} ${CURDIR}/main2_orig.o
	rm -f ${CURDIR}/unpatch.json ${CURDIR}/main_unpatch.c ${CURDIR}/main2_unpatch.c
	rm -f ${CURDIR}/main ${CURDIR}/main2