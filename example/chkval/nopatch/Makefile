
CURDIR=$(shell readlink -f .)
ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../..)
endif

main_SRCS=${CURDIR}/main.cpp ${CURDIR}/callc.cpp ${CURDIR}/chk_main_1.cpp ${CURDIR}/chk_main_2.cpp
main_OBJS=$(patsubst ${CURDIR}/%.cpp,${CURDIR}/%.o,${main_SRCS})
main2_SRCS=${CURDIR}/main2.cpp ${CURDIR}/callc2.cpp ${CURDIR}/chk_main2_1.cpp ${CURDIR}/chk_main2_2.cpp
main2_OBJS=$(patsubst ${CURDIR}/%.cpp,${CURDIR}/%.o,${main2_SRCS})

CFLAGS= -I${TOPDIR}/include  -DOB_DEBUG_MODE=1 -include stdio.h -include  stdlib.h
LDFLAGS=

all:${CURDIR}/main ${CURDIR}/main2

${CURDIR}/main:${main_OBJS}
	gcc -Wall ${LDFLAGS} -o $@ ${main_OBJS}
	python ${TOPDIR}/obcode.py chkvalfillelf -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/main' '${CURDIR}/chk_main_1.o' '${CURDIR}/chk_main_2.o'


${CURDIR}/main2:${main2_OBJS}
	gcc -Wall ${LDFLAGS} -o $@ ${main2_OBJS}
	python ${TOPDIR}/obcode.py chkvalfillelf -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/main2' '${CURDIR}/chk_main2_1.o' '${CURDIR}/chk_main2_2.o'


${CURDIR}/%.o:${CURDIR}/%.cpp ${CURDIR}/chk_main.h ${CURDIR}/chk_main2.h 
	gcc -Wall ${CFLAGS} -c $< -o $@


${CURDIR}/chk_main_1.o:${CURDIR}/chk_main_1.cpp ${CURDIR}/main.o ${CURDIR}/callc.o  ${CURDIR}/chk_main.h
	gcc -Wall ${CFLAGS} -c $< -o $@
	python ${TOPDIR}/obcode.py chkvaldumpfuncself -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/chk_main_1.o' '${CURDIR}/callc.o' '${CURDIR}/main.o'

${CURDIR}/chk_main_2.o:${CURDIR}/chk_main_2.cpp ${CURDIR}/main.o ${CURDIR}/callc.o  ${CURDIR}/chk_main.h
	gcc -Wall ${CFLAGS} -c $< -o $@
	python ${TOPDIR}/obcode.py chkvaldumpfuncself -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/chk_main_2.o' '${CURDIR}/callc.o' '${CURDIR}/main.o'

${CURDIR}/chk_main2_1.o:${CURDIR}/chk_main2_1.cpp ${CURDIR}/main2.o ${CURDIR}/callc2.o  ${CURDIR}/chk_main2.h
	gcc -Wall ${CFLAGS} -c $< -o $@
	python ${TOPDIR}/obcode.py chkvaldumpfuncself -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/chk_main2_1.o' '${CURDIR}/callc2.o' '${CURDIR}/main2.o'

${CURDIR}/chk_main2_2.o:${CURDIR}/chk_main2_2.cpp ${CURDIR}/main2.o ${CURDIR}/callc2.o  ${CURDIR}/chk_main2.h
	gcc -Wall ${CFLAGS} -c $< -o $@
	python ${TOPDIR}/obcode.py chkvaldumpfuncself -vvvvv 'dump;${CURDIR}/dump.json' 'output;${CURDIR}/chk_main2_2.o' '${CURDIR}/callc2.o' '${CURDIR}/main2.o'


${CURDIR}/chk_main.h:${CURDIR}/chk_main_1.cpp ${CURDIR}/chk_main_2.cpp
	python ${TOPDIR}/obcode.py chkvalheader -vvvv 'output;${CURDIR}/chk_main.h' 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main_1.o' '${CURDIR}/chk_main_2.o'

${CURDIR}/chk_main2.h:${CURDIR}/chk_main2_1.cpp ${CURDIR}/chk_main2_2.cpp
	python ${TOPDIR}/obcode.py chkvalheader -vvvv  'output;${CURDIR}/chk_main2.h' 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main2_1.o' '${CURDIR}/chk_main2_2.o'

${CURDIR}/chk_main_1.cpp:
	python ${TOPDIR}/obcode.py -o $@ -vvvv fmtchkval 'objfile;${CURDIR}/chk_main_1.o' 'includefiles;chk_main.h' 'includefiles;main.h' 'dump;${CURDIR}/dump.json' 'includefiles;callc.h' '${CURDIR}/callc.o;callc_a,callc_b,callc_c' '${CURDIR}/main.o;print_out_a,print_out_b,print_out_c'

${CURDIR}/chk_main_2.cpp:
	python ${TOPDIR}/obcode.py -o $@ -vvvv fmtchkval 'objfile;${CURDIR}/chk_main_2.o' 'includefiles;chk_main.h' 'includefiles;main.h' 'dump;${CURDIR}/dump.json' 'includefiles;callc.h' '${CURDIR}/callc.o;callc_a,callc_b,callc_c' '${CURDIR}/main.o;print_out_a,print_out_b,print_out_c'

${CURDIR}/chk_main2_1.cpp:
	python ${TOPDIR}/obcode.py -o $@ -vvvv fmtchkval 'objfile;${CURDIR}/chk_main2_1.o' 'includefiles;chk_main2.h' 'includefiles;main2.h' 'dump;${CURDIR}/dump.json' 'includefiles;callc.h' '${CURDIR}/callc2.o;callc_a,callc_b,callc_c' '${CURDIR}/main2.o;print_out2_a,print_out2_b,print_out2_c'

${CURDIR}/chk_main2_2.cpp:
	python ${TOPDIR}/obcode.py -o $@ -vvvv fmtchkval 'objfile;${CURDIR}/chk_main2_2.o' 'includefiles;chk_main2.h' 'includefiles;main2.h' 'dump;${CURDIR}/dump.json' 'includefiles;callc.h' '${CURDIR}/callc2.o;callc_a,callc_b,callc_c' '${CURDIR}/main2.o;print_out2_a,print_out2_b,print_out2_c'

${CURDIR}/main.cpp:${CURDIR}/main_bak.cpp ${CURDIR}/chk_main.h 
	python ${TOPDIR}/obcode.py -o $@ -i ${CURDIR}/main_bak.cpp -vvvv replchkval 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main_1.o' '${CURDIR}/chk_main_2.o'

${CURDIR}/main2.cpp:${CURDIR}/main2_bak.cpp ${CURDIR}/chk_main2.h 
	python ${TOPDIR}/obcode.py -o $@ -i ${CURDIR}/main2_bak.cpp -vvvv replchkval 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main2_1.o' '${CURDIR}/chk_main2_2.o'

${CURDIR}/callc.cpp:${CURDIR}/callc_bak.cpp ${CURDIR}/chk_main.h
	python ${TOPDIR}/obcode.py -o $@ -i ${CURDIR}/callc_bak.cpp -vvvv replchkval 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main_1.o' '${CURDIR}/chk_main_2.o'

${CURDIR}/callc2.cpp:${CURDIR}/callc_bak.cpp ${CURDIR}/chk_main2.h
	python ${TOPDIR}/obcode.py -o $@ -i ${CURDIR}/callc_bak.cpp -vvvv replchkval 'dump;${CURDIR}/dump.json' '${CURDIR}/chk_main2_1.o' '${CURDIR}/chk_main2_2.o'

clean:
	rm -f ${CURDIR}/main ${CURDIR}/main2
	rm -f ${main_OBJS} ${main2_OBJS}
	rm -f ${CURDIR}/chk_main.h  ${CURDIR}/chk_main2.h 
	rm -f ${CURDIR}/chk_main_1.cpp ${CURDIR}/chk_main_2.cpp
	rm -f ${CURDIR}/chk_main2_1.cpp ${CURDIR}/chk_main2_2.cpp
	rm -f ${CURDIR}/dump.json
	rm -f ${CURDIR}/main.cpp ${CURDIR}/main2.cpp
	rm -f ${CURDIR}/callc.cpp ${CURDIR}/callc2.cpp