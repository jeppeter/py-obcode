#include <obcode.h>
#include <sys/ptrace.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <syscall.h>


int catch_trace(int bfirst)
{
	int ret;
	int tracenot=0;
	int fd=-1;
	char buf[4];
	int v;
	if (bfirst) {
		fd = open((const char*)OB_MIXED_STR("/proc/sys/kernel/yama/ptrace_scope"), O_RDONLY);
		if (fd >= 0) {
			ret = read(fd,buf,sizeof(buf));
			if (ret >= 0) {
				if (ret >= sizeof(buf)) {
					buf[ret-1] = 0;
				} else {
					buf[ret] = 0;	
				}
				v = atoi(buf);
				if (v == 3) {
					tracenot = 1;
				}
			}
			close(fd);
			fd = -1;
		}


		if (tracenot == 0) {
			ret = syscall(SYS_ptrace,PTRACE_TRACEME,0,1,0);
			if (ret != 0) {
				return -1;
			}			
		}
		ret = syscall(SYS_ptrace,PTRACE_TRACEME,0,1,0);
		if (ret  == 0) {
			return -1;
		}
	} else {
		ret = syscall(SYS_ptrace,PTRACE_TRACEME,0,1,0);
		if (ret  == 0) {
			return -1;
		}
	}
	return 0;
}

int main(int argc,char* argv[])
{
	int ret;
	int cnt=0;
	ret = catch_trace(1);
	if (ret < 0) {
		return ret;
	}
	while(1) {
		ret = catch_trace(0);
		if (ret < 0) {
			return ret;
		}
		sleep(1);
		printf("call catch %d\n", cnt);
		cnt ++;
	}
	return 0;
}