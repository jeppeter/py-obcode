#define _GNU_SOURCE
#include <obcode.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


void sig_trap(int exno)
{
	printf("call sig trap\n");
	return;
}

int main(int argc,char* argv[])
{
	sighandler_t sigret=SIG_ERR;

	sigret = signal(SIGTRAP,sig_trap);
	if (sigret == SIG_ERR) {
		return -1;
	}

	while(1) {
		sleep(1);
		printf("hello \n");
	}
	return 0;
}