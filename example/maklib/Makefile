
TOPDIR=$(shell readlink -f ../.. )
CURDIR=$(shell readlink -f .)
PYTHON=python

include ${TOPDIR}/obcode.mak
#include ${CURDIR}/v.mak

FILES=$(call OB_MAK_FILE,c.cpp d.cpp)
OBJECTS=$(patsubst %.cpp,%.o, ${FILES})

all:command

command:${OBJECTS}
	gcc -Wall -o $@ ${OBJECTS}

$(patsubst %.cpp,%.o, $(call OB_MAK_FILE,c.cpp)):$(call OB_MAK_FILE,c.cpp)

$(patsubst %.cpp,%.o, $(call OB_MAK_FILE,d.cpp)):$(call OB_MAK_FILE,d.cpp)

%.o:%.cpp
	@gcc -Wall -c $< -o $@
	echo $(call UNOB_MAK_FILE,$<)
	echo $(call UNOB_MAK_FILE_SHORT,$<)


clean:
	rm -f ${OBJECTS}
	rm -f command

