#define  _GNU_SOURCE
#include <obcode.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

typedef struct __thread_arg{
	int m_times;
	int m_a;
	int m_b;
	int m_c;
} thread_arg_t,*pthread_arg_t;

void* thread_func(void* arg)
{
	unsigned long dret=0;
	pthread_arg_t pargs = (pthread_arg_t)arg;
	int i;

	for (i=0;i< pargs->m_times;i++) {
		OB_CODE_SPEC("funcmax=20,funcmin=10,debug=4", pargs->m_a,pargs->m_b,pargs->m_c);
		printf("a=%d;b=%d;c=%d;\n", pargs->m_a,pargs->m_b,pargs->m_c);
	}

	return (void*)dret;
}

typedef struct __thread_info {
	pthread_t m_thid;
	int m_running;
} thread_info_t,*pthread_info_t;

int main(int argc,char* argv[])
{
	int numthrs = 4;
	int numtimes = 100;
	pthread_info_t pthreads=NULL;
	int a=1;
	int b=2;
	int c=3;
	int i;
	pthread_arg_t pargs=NULL;
	int ret=0;
	int leftthrs=0;
	void* ptrres=NULL;
	int exited = 0;

	if (argc > 1) {
		numthrs = atoi(argv[1]);
	}
	if (argc > 2) {
		numtimes = atoi(argv[2]);
	}
	if (argc > 3) {
		a = atoi(argv[3]);
	}
	if (argc > 4) {
		b = atoi(argv[4]);
	}
	if (argc > 5) {
		c = atoi(argv[5]);
	}

	pthreads = (pthread_info_t)malloc(sizeof(thread_info_t)*numthrs);
	if (pthreads == NULL) {
		ret = -1;
		fprintf(stderr, "alloc threads error\n");
		goto out;
	}
	memset(pthreads, 0, sizeof(thread_info_t)*numthrs);

	pargs = (pthread_arg_t)malloc(sizeof(*pargs));
	if (pargs == NULL) {
		ret = -2;
		fprintf(stderr, "alloc pargs error\n");
		goto out;
	}
	memset(pargs, 0 ,sizeof(*pargs));

	pargs->m_times = numtimes;
	pargs->m_a = a;
	pargs->m_b = b;
	pargs->m_c = c;

	for (i=0;i<numthrs;i++) {
		ret = pthread_create(&(pthreads[i].m_thid), NULL,thread_func,pargs);
		if (ret < 0) {
			ret = -3;
			fprintf(stderr,"create [%d] error\n", i);
			goto out;
		}
		pthreads[i].m_running = 1;
	}

	leftthrs = numthrs;

	while(leftthrs > 0) {
		for (i=0;i<numthrs;i++) {
			if (pthreads[i].m_running != 0) {
				errno = 0;
				ret = pthread_tryjoin_np(pthreads[i].m_thid,&ptrres);
				if (ret == 0) {
					free(ptrres);
					pthreads[i].m_running = 0;
					leftthrs --;
				} 
			}
		}
		if (leftthrs > 0) {
			usleep(10 * 1000);
		}
	}

	ret = 0;
out:
	if (pthreads) {
		exited = 0;
		while(exited == 0) {
			exited = 1;
			for (i=0;i<numthrs;i++) {
				if (pthreads[i].m_running != 0) {
					ret = pthread_join(pthreads[i].m_thid,&ptrres);
					if (ret == 0) {
						free(ptrres);
						ptrres = NULL;
						pthreads[i].m_running = 0;
					} else {
						exited = 0;
					}
				}
			}

			if (exited == 0) {
				usleep(10*1000);
			}
		}
		free(pthreads);
	}
	pthreads = NULL;

	if (pargs) {
		free(pargs);
	}
	return ret;
}

