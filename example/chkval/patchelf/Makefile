
CURDIR=$(shell readlink -f .)
ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../..)
endif
-include ${TOPDIR}/obcode.mak

OB_CHKVAL_TIMES=5

main_data_SRCS := $(shell ${PYTHON} ${TOPDIR}/obchkval.py  chkvaldatafiles main)
main_exit_SRCS := $(shell ${PYTHON} ${TOPDIR}/obchkval.py  chkvalexitfiles main)

main_SRCS=${CURDIR}/main.c ${CURDIR}/callc.c ${CURDIR}/main_unpatch.c ${main_data_SRCS} ${main_exit_SRCS}
main_OBJS=$(patsubst ${CURDIR}/%.c,${CURDIR}/%.o,${main_SRCS})

main2_data_SRCS := $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvaldatafiles main2)
main2_exit_SRCS := $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvalexitfiles main2)

main2_SRCS=${CURDIR}/main2.c ${CURDIR}/callc2.c ${CURDIR}/main2_unpatch.c ${main2_data_SRCS} ${main2_exit_SRCS}
main2_OBJS=$(patsubst ${CURDIR}/%.c,${CURDIR}/%.o,${main2_SRCS})

CFLAGS= -I${TOPDIR}/include  -DOB_DEBUG_MODE=1 -DOB_MMAP=1 -include stdio.h -include  stdlib.h
LDFLAGS=
COMMA=,
COLON=;

ifeq (${CHKVAL_TIMES},)
CHKVAL_TIMES=5
endif

export CHKVAL_TIMES

all:${CURDIR}/main ${CURDIR}/main2

${CURDIR}/main:${main_OBJS}
	$(call OB_CHKVAL_DUMP_FUNCS_ELF, --obchkkey main)
	gcc -Wall ${LDFLAGS} -o $@ ${main_OBJS}
	@$(call OB_ELF_PATCH, -o $@ ${CURDIR}/main.o ${CURDIR}/main_unpatch.o ${CURDIR}/callc.o)
	$(call OB_CHKVAL_FILL_FUNCS_ELF,'output;${CURDIR}/main' --obchkkey main)

${CURDIR}/main2:${main2_OBJS}
	$(call OB_CHKVAL_DUMP_FUNCS_ELF, --obchkkey main2)
	gcc -Wall ${LDFLAGS} -o $@ ${main2_OBJS}
	@$(call OB_ELF_PATCH, -o $@ ${CURDIR}/main2.o ${CURDIR}/main2_unpatch.o ${CURDIR}/callc2.o)
	$(call OB_CHKVAL_FILL_FUNCS_ELF,'output;${CURDIR}/main2' --obchkkey main2)

${CURDIR}/%.o:${CURDIR}/%.c ${CURDIR}/chk_main.h ${CURDIR}/chk_main2.h ${CURDIR}/handle_exit.h
	gcc -Wall ${CFLAGS} -c $< -o $@

${CURDIR}/chk_main.h:$(shell ${PYTHON} ${TOPDIR}/obchkval.py  chkvaldatafiles main)
	$(call OB_CHKVAL_FMT_HEADER,-o $@ --obchkkey main)

${CURDIR}/chk_main2.h:$(shell ${PYTHON} ${TOPDIR}/obchkval.py  chkvaldatafiles main2)
	$(call OB_CHKVAL_FMT_HEADER,-o $@ --obchkkey main2)


${CURDIR}/handle_exit.h:$(shell ${PYTHON} ${TOPDIR}/obchkval.py  chkvalexitfiles   main main2)
	$(call OB_CHKVAL_FMT_EXIT_HEADER,-o $@ main main2)


${CURDIR}/main.c:${CURDIR}/main_bak.c ${CURDIR}/chk_main.h ${CURDIR}/handle_exit.h
	$(call OB_CHKVAL_REPLS,-o $@ -i ${CURDIR}/main_bak.c  --obchkkey main)

${CURDIR}/main2.c:${CURDIR}/main2_bak.c ${CURDIR}/chk_main2.h ${CURDIR}/handle_exit.h
	$(call OB_CHKVAL_REPLS,-o $@ -i ${CURDIR}/main2_bak.c --obchkkey main2)

${CURDIR}/callc.c:${CURDIR}/callc_bak.c ${CURDIR}/chk_main.h ${CURDIR}/handle_exit.h
	$(call OB_CHKVAL_REPLS,-o $@ -i ${CURDIR}/callc_bak.c --obchkkey main)

${CURDIR}/callc2.c:${CURDIR}/callc_bak.c ${CURDIR}/chk_main2.h ${CURDIR}/handle_exit.h
	$(call OB_CHKVAL_REPLS, -o $@ -i ${CURDIR}/callc_bak.c --obchkkey main2)


${main_exit_SRCS}:${CURDIR}/handle_exit.c.tmpl
	$(call OB_CHKVAL_EXIT_FMT,-i ${CURDIR}/handle_exit.c.tmpl --obchkkey main)

${main2_exit_SRCS}:${CURDIR}/handle_exit.c.tmpl
	$(call OB_CHKVAL_EXIT_FMT,-i ${CURDIR}/handle_exit.c.tmpl --obchkkey main2)


${main_data_SRCS}:
	$(call OB_CHKVAL_FMT_CHKVAL,--obchkkey main 'includefiles;chk_main.h' 'includefiles;main.h' 'includefiles;callc.h' '${CURDIR}/callc.o;callc_a${COMMA}callc_b${COMMA}callc_c' '${CURDIR}/main.o;print_out_a${COMMA}print_out_b${COMMA}print_out_c')


${main2_data_SRCS}:
	$(call OB_CHKVAL_FMT_CHKVAL,--obchkkey main2 'includefiles;chk_main2.h' 'includefiles;main2.h' 'includefiles;callc.h' '${CURDIR}/callc2.o;callc_a${COMMA}callc_b${COMMA}callc_c' '${CURDIR}/main2.o;print_out2_a${COMMA}print_out2_b${COMMA}print_out2_c')

${CURDIR}/main_unpatch.c:${CURDIR}/callc.o ${CURDIR}/main.o
	@$(call OB_ELF_UNPATCH, 'includefiles${COLON}main.h${COMMA}callc.h${COMMA}unpatch.h' -o $@ '${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/callc.o${COLON}callc_a${COMMA}callc_b${COMMA}callc_c')


${CURDIR}/main2_unpatch.c:${CURDIR}/callc2.o ${CURDIR}/main2.o
	@$(call OB_ELF_UNPATCH, 'includefiles${COLON}main2.h${COMMA}callc.h${COMMA}unpatch.h' -o $@ '${CURDIR}/main2.o${COLON}print_out2_a${COMMA}print_out2_b${COMMA}print_out2_c' '${CURDIR}/callc2.o${COLON}callc_a${COMMA}callc_b${COMMA}callc_c')

clean:
	rm -f ${CURDIR}/main ${CURDIR}/main2
	rm -f ${main_OBJS} ${main2_OBJS}
	rm -f $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvalexitfiles main) 
	rm -f $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvalexitfiles main2)
	rm -f $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvaldatafiles main)
	rm -f $(shell ${PYTHON} ${TOPDIR}/obchkval.py chkvaldatafiles main2)
	rm -f ${CURDIR}/main_unpatch.c ${CURDIR}/main2_unpatch.c
	rm -f ${CURDIR}/obcode.json
	rm -f ${CURDIR}/main.c ${CURDIR}/main2.c
	rm -f ${CURDIR}/callc.c ${CURDIR}/callc2.c
	rm -f ${CURDIR}/handle_exit.h
	rm -f ${CURDIR}/chk_main.h ${CURDIR}/chk_main2.h
