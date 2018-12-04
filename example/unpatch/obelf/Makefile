
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

ifeq (${CNT},)
CNT=0
endif

all:${CURDIR}/main ${CURDIR}/main2

${CURDIR}/main:${main_OBJECTS}
	gcc -Wall -o $@ ${main_OBJECTS}
	@$(call OB_ELF_PATCH,'dump${COLON}${CURDIR}/unpatch.json' 'output${COLON}${CURDIR}/main' ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o)

${CURDIR}/main2:${main2_OBJECTS}
	gcc -Wall -o $@ ${main2_OBJECTS}
	@$(call OB_ELF_PATCH,'dump${COLON}${CURDIR}/unpatch.json' 'output${COLON}${CURDIR}/main2' ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc.o)


${CURDIR}/%.o:${CURDIR}/%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

${CURDIR}/unpatch.json:${CURDIR}/main_unpatch.c ${CURDIR}/main2_unpatch.c

${CURDIR}/main_unpatch.c:${CURDIR}/main.o ${CURDIR}/callc.o
	cp ${CURDIR}/main.o ${CURDIR}/main_orig.o
	@$(call OB_ELF_UNPATCH, --times ${CNT} 'includefiles${COLON}main.h${COMMA}unpatch.h${COMMA}callc.h' 'dump${COLON}${CURDIR}/unpatch.json' 'output${COLON}${CURDIR}/main_unpatch.c' ${main_FORMAT_CLAUSE})

${CURDIR}/main2_unpatch.c:${CURDIR}/main2.o ${CURDIR}/callc.o
	cp ${CURDIR}/main2.o ${CURDIR}/main2_orig.o	
	@$(call OB_ELF_UNPATCH, --times ${CNT} 'includefiles${COLON}main2.h${COMMA}unpatch.h${COMMA}callc.h' 'dump${COLON}${CURDIR}/unpatch.json' 'output${COLON}${CURDIR}/main2_unpatch.c' ${main2_FORMAT_CLAUSE})


clean:
	rm -f ${main_OBJECTS} ${CURDIR}/main_orig.o
	rm -f ${main2_OBJECTS} ${CURDIR}/main2_orig.o
	rm -f ${CURDIR}/unpatch.json ${CURDIR}/main_unpatch.c ${CURDIR}/main2_unpatch.c
	rm -f ${CURDIR}/main ${CURDIR}/main2