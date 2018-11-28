
main_OBJECTS=main.o main_unpatch.o callc.o
main2_OBJECTS=main2.o main2_unpatch.o callc.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)

all:main main2

main:${main_OBJECTS}
	gcc -Wall -o $@ ${main_OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D unpatch.json -o $@ obpatchelf ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o
endif

main2:${main2_OBJECTS}
	gcc -Wall -o $@ ${main2_OBJECTS}
ifneq (${OB_PATCH},)
	python ${TOPDIR}/obcode.py -D unpatch.json -o $@ obpatchelf ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc.o
endif


%.o:%.c
	gcc -Wall -I${TOPDIR}/include -DOB_MMAP -c $< -o $@

unpatch.json:main_unpatch.c main2_unpatch.c


main_unpatch.c:main.o callc.o
	cp main.o main_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"main.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >main_unpatch.c
	/bin/echo "{}" >unpatch.json
else
	python ${TOPDIR}/obcode.py --includefiles main.h --includefiles callc.h --includefiles unpatch.h -D unpatch.json -o main_unpatch.c obunpatchelf '${CURDIR}/main.o;print_out_a,print_out_b,print_out_c' '${CURDIR}/callc.o;call_a,call_b,call_c'
endif

main2_unpatch.c:main2.o callc.o
	cp main2.o main2_orig.o	
ifeq (${OB_PATCH},)
	/bin/echo -e "#include \"main.h\"\nint unpatch_handler(map_prot_func_t protfunc){return 0;}" >main2_unpatch.c
	/bin/echo "{}" >unpatch.json
else
	python ${TOPDIR}/obcode.py --includefiles main2.h --includefiles callc.h --includefiles unpatch.h -D unpatch.json -o main2_unpatch.c obunpatchelf '${CURDIR}/main2.o;ccprint_out_a,ccprint_out_b,ccprint_out_c' '${CURDIR}/callc.o;call_a,call_b,call_c'
endif


clean:
	rm -f ${main_OBJECTS} main_orig.o
	rm -f ${main2_OBJECTS} main2_orig.o
	rm -f unpatch.json main_unpatch.c main2_unpatch.c
	rm -f main main2