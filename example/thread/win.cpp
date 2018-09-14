#include <obcode.h>
#include <Windows.h>
#include <stdio.h>

typedef struct __thread_arg{
	int m_times;
	int m_a;
	int m_b;
	int m_c;
} thread_arg_t,*pthread_arg_t;

DWORD thread_func(void* arg)
{
	DWORD dret=0;
	pthread_arg_t pargs = (pthread_arg_t)arg;
	int i;

	for (i=0;i< pargs->m_times;i++) {
		OB_CODE_SPEC("funcmax=20,funcmin=10,debug=4", pargs->m_a,pargs->m_b,pargs->m_c);
		printf("a=%d;b=%d;c=%d;\n", pargs->m_a,pargs->m_b,pargs->m_c);
	}

	return dret;
}

int main(int argc,char* argv[])
{
	int numthrs = 4;
	int numtimes = 100;
	HANDLE *pthreads=NULL;
	int a=1;
	int b=2;
	int c=3;
	int i;
	pthread_arg_t pargs=NULL;
	int ret=0;

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

	pthreads = (HANDLE*)malloc(sizeof(HANDLE)*numthrs);
	if (pthreads == NULL) {
		ret = -1;
		fprintf(stderr, "alloc threads error\n");
		goto out;
	}
	memset(pthreads, 0, sizeof(HANDLE)*numthrs);

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
		pthreads[i] = CreateThread(NULL,0,thread_func,pargs,0,NULL);
		if (pthreads[i] == NULL) {
			ret = -3;
			fprintf(stderr,"create [%d] error\n", i);
			goto out;
		}
	}

	WaitForMultipleObjects(numthrs, pthreads,TRUE,INFINITE);

	ret = 0;
out:
	if (pthreads) {
		for (i=0;i<numthrs;i++) {
			if (pthreads[i] != NULL) {
				CloseHandle(pthreads[i]);
			}
			pthreads[i] = NULL;
		}
		free(pthreads);
	}
	pthreads = NULL;

	if (pargs) {
		free(pargs);
	}
	return ret;
}

