
TOPDIR=$(shell readlink -f ../../../..)

CFLAGS=-I${TOPDIR}/include -Wall

all:main

main:main.o
	gcc ${CFLAGS} -o $@ $<

%.o:%.c
	gcc ${CFLAGS} -c $< -o $@

clean:
	rm -f main *.o