
main_OBJECTS=main.o main_unpatch.o callc.o
main2_OBJECTS=main2.o main2_unpatch.o callc.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)
COMMA=,
COLON=;

-include ${TOPDIR}/obcode.mak

ifeq (${CNT},)
CNT=0
endif

all:main main2

main:${main_OBJECTS}
	gcc -Wall -o $@ ${main_OBJECTS}
ifneq (${OB_REPATCH},)
	python ${TOPDIR}/obcode.py obrepatchelf ${OB_VERBOSE} 'dump${COLON}${OB_REPATCH}' 'output${COLON}${CURDIR}/main' ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o
else
	@$(call OB_ELF_PATCH,'dump${COLON}unpatch.json' 'output${COLON}${CURDIR}/main' ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o)
endif

main2:${main2_OBJECTS}
	gcc -Wall -o $@ ${main2_OBJECTS}
ifneq (${OB_REPATCH},)
	python ${TOPDIR}/obcode.py obrepatchelf ${OB_VERBOSE} 'dump${COLON}${OB_REPATCH}' 'output${COLON}${CURDIR}/main2' ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc.o
else
	@$(call OB_ELF_PATCH,'dump${COLON}unpatch.json' 'output${COLON}${CURDIR}/main2' ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc.o)
endif


%.o:%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

ifeq (${OB_REPATCH},)
unpatch.json:main_unpatch.c main2_unpatch.c
endif

main_unpatch.c:main.o callc.o
	cp main.o main_orig.o
ifneq (${OB_REPATCH},)
	python ${TOPDIR}/obcode.py obreunpatchelf ${OB_VERBOSE} 'includefiles${COLON}main.h${COMMA}callc.h${COMMA}unpatch.h' 'dump${COLON}${OB_REPATCH}' 'output${COLON}main_unpatch.c' '${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c'
else
	@$(call OB_ELF_UNPATCH, --times ${CNT} 'includefiles${COLON}main.h${COMMA}callc.h${COMMA}unpatch.h' 'dump${COLON}unpatch.json' 'output${COLON}main_unpatch.c' '${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')
endif

main2_unpatch.c:main2.o callc.o
	cp main2.o main2_orig.o
ifneq (${OB_REPATCH},)
	python ${TOPDIR}/obcode.py obreunpatchelf ${OB_VERBOSE} 'includefiles${COLON}main2.h${COMMA}callc.h${COMMA}unpatch.h' 'dump${COLON}${OB_REPATCH}' 'output${COLON}main2_unpatch.c' '${CURDIR}/main2.o${COLON}ccprint_out_a${COMMA}ccprint_out_b${COMMA}ccprint_out_c' '${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c'
else
	@$(call OB_ELF_UNPATCH, --times ${CNT} 'includefiles${COLON}main2.h${COMMA}callc.h${COMMA}unpatch.h' 'dump${COLON}unpatch.json' 'output${COLON}main2_unpatch.c' '${CURDIR}/main2.o${COLON}ccprint_out_a${COMMA}ccprint_out_b${COMMA}ccprint_out_c' '${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c')
endif


clean:
	rm -f ${main_OBJECTS} main_orig.o
	rm -f ${main2_OBJECTS} main2_orig.o
	rm -f unpatch.json main_unpatch.c main2_unpatch.c
	rm -f main main2