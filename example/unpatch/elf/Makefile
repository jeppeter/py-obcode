
OBJECTS=main.o unpatch.o
TOPDIR=$(shell readlink -f ../../.. )
CURDIR=$(shell readlink -f .)

all:main

main:${OBJECTS}
	gcc -Wall -o $@ ${OBJECTS}
ifneq (${PATCH},)
	python ${TOPDIR}/obcode.py -D unpatch.json obpatchelf $@ -vvvv
endif


%.o:%.c
	gcc -Wall -I${TOPDIR}/include -c $< -o $@

unpatch.c:unpatch.json

unpatch.json:main.o
	cp main.o main_orig.o	
ifeq (${PATCH},)
	echo "int unpatch_handler(){ return 0;}" > unpatch.c
	echo "{}" > unpatch.json
else
	#python ${TOPDIR}/obcode.py --times 1 --includefiles main.h -D unpatch.json -o unpatch.c -vvvvv obunpatchelf '${CURDIR}/main.o:print_out_a,print_out_b' 
	python ${TOPDIR}/obcode.py --times 1 --includefiles main.h -D unpatch.json -o unpatch.c -vvvvv obunpatchelf '${CURDIR}/main.o:print_out_a'
endif

clean:
	rm -f ${OBJECTS} main_orig.o
	rm -f unpatch.json unpatch.c
	rm -f main