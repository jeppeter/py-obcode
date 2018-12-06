
SRCDIR:=$(shell dirname $(lastword $(MAKEFILE_LIST)))

ifeq ($(MAKECMDGOALS),static)
STATICLIB=1
endif

CLIBS_DIR=${SRCDIR}/clibs
DYNAMICDIR=${CLIBS_DIR}/dynamiclib
STATICDIR=${CLIBS_DIR}/staticlib

include ${SRCDIR}/baseop.mak


CHKINTEGRITY_SRCS= main.cpp
CHKINTEGRITY_OFILES=$(patsubst %.cpp,%.o,${CHKINTEGRITY_SRCS})

INCLUDE_CFLAGS= -I${CLIBS_DIR}/uxlib -I${CLIBS_DIR}/common -I${CLIBS_DIR}/common/jsonlib -I${CLIBS_DIR}/common/extargslib

#$(info "SRCDIR ${SRCDIR} $(MAKEFILE_LIST)")
ifeq (${STATICLIB},)
unexport STATICLIB
else
export STATICLIB
endif

ifeq (${STATICLIB},)


all:dynamic

dynamic:chkintegrity

chkintegrity:${CHKINTEGRITY_OFILES} ${DYNAMICDIR}/libuxlib.so ${DYNAMICDIR}/libextargs.so ${DYNAMICDIR}/libjson.so
	$(call call_exec,${CC} ${LDFLAGS} -o $@ ${CHKINTEGRITY_OFILES} -L${DYNAMICDIR} -lextargs -ljson -luxlib,"LINK    $@")

${DYNAMICDIR}/libuxlib.so:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/uxlib all,"GEN     libuxlib.so")

${DYNAMICDIR}/libextargs.so:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/extargslib all,"GEN     libextargslib.so")

${DYNAMICDIR}/libjson.so:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/jsonlib all,"GEN     libjson.so")

else

all:static

static:chkintegrity_static


chkintegrity_static:${CHKINTEGRITY_OFILES} ${STATICDIR}/libuxlib.a ${STATICDIR}/libextargs.a ${STATICDIR}/libjson.a
	$(call call_exec,${CC} ${LDFLAGS} -o $@ ${CHKINTEGRITY_OFILES}  -L${STATICDIR} -lextargs -ljson -luxlib,"LINK    $@")


${STATICDIR}/libuxlib.a:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/uxlib all,"GEN     libuxlib.a")

${STATICDIR}/libextargs.a:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/extargslib all,"GEN     libextargs.a")

${STATICDIR}/libjson.a:${CLIBS_DIR}
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/jsonlib all,"GEN     libjson.a")

endif


main.o:main.cpp

main.cpp:args_options.cpp

args_options.cpp:args_options.cpp.tmpl ${CLIBS_DIR}/common/extargslib
	$(call call_exec,${PYTHON} ${CLIBS_DIR}/coutput.py -j ${SRCDIR}/chkintegrity.json -i $< cmdstruct | \
		${PYTHON} ${CLIBS_DIR}/coutput.py -j ${SRCDIR}/chkintegrity.json -i - -o $@ freefunc,"GEN     $@")

${CLIBS_DIR}/common/extargslib:${CLIBS_DIR}

${CLIBS_DIR}:
	$(call call_exec,${GIT} clone https://github.com/jeppeter/clibs.git ${CLIBS_DIR},"CLONE   clibs")

%.o:%.cpp
	$(call call_exec,${CXX} -Wall ${INCLUDE_CFLAGS} -c $< -o $@,"CXX     $<")

clean_extargslib:
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/extargslib clean,"CLEAN   extargslib")

clean_json:
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/common/jsonlib clean,"CLEAN   jsonlib")

clean_uxlib:
	$(call call_exec,${MAKE} ${MAKE_PRINT_FLAG} -C ${CLIBS_DIR}/uxlib clean,"CLEAN   uxlib")

clean:clean_extargslib clean_uxlib clean_json
	$(call call_exec,${RM} -f chkintegrity chkintegrity_static, "RM      chkintegrity")
	$(call call_exec,${RM} -f args_options.cpp,"RM      args_options.cpp")
	$(call call_exec,${RM} -f ${CHKINTEGRITY_OFILES}, "RM      *.o")
