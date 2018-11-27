
OBJECTS=main.o unpatch.o callc.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)

all:main

main:${OBJECTS}
	gcc -Wall -o $@ ${OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D unpatch.json obpatchelf $@
endif


%.o:%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

unpatch.c:unpatch.json

unpatch.json:main.o callc.o
	cp main.o main_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"main.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >unpatch.c
	/bin/echo "{}" >unpatch.json
else
	python ${TOPDIR}/obcode.py --includefiles main.h -D unpatch.json -o unpatch.c obunpatchelf '${CURDIR}/main.o;print_out_a,print_out_b,print_out_c' '${CURDIR}/callc.o;call_a,call_b,call_c'
endif

clean:
	rm -f ${OBJECTS} main_orig.o
	rm -f unpatch.json unpatch.c
	rm -f main