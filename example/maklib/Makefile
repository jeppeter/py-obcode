
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


${CURDIR}/%.o:${CURDIR}/%.cpp
	gcc -Wall -c $< -o $@

%.o:%.cpp
	gcc -Wall -c $< -o $@

clean:
	rm -f ${OBJECTS}
	rm -f command

