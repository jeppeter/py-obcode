
TOPDIR=$(shell readlink -f ../../../..)

CFLAGS=-I${TOPDIR}/include -Wall

all:traceme

traceme:main.o
	gcc ${CFLAGS} -o $@ $<

%.o:%.c
	gcc ${CFLAGS} -c $< -o $@

clean:
	rm -f traceme *.o