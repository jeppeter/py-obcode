ifeq (${TOPDIR},)
TOPDIR=$(shell readlink -f ../../.. )
endif
include ${TOPDIR}/obcode.mak
CURDIR=$(shell readlink -f .)
COMMA=,
COLON=;

FORMAT_CLAUSE=$(call UNOB_FUNC,'${CURDIR}/main.h${COLON}${CURDIR}/main.o${COLON}print_out_a${COMMA}print_out_b${COMMA}print_out_c' '${CURDIR}/main.h${COLON}${CURDIR}/callc.o${COLON}call_a${COMMA}call_b${COMMA}call_c' )

all:
	/bin/echo ${FORMAT_CLAUSE}