#include <stdio.h>
#include <stdlib.h>
#include <extargs.h>
#include <cmn_err.h>
#include <cmn_output_debug.h>
#include <cmn_args.h>
#include <string.h>

typedef struct __args_options {
    int m_verbose;
    char* m_input;
    char* m_output;
} args_options_t, *pargs_options_t;


#ifdef __cplusplus
extern "C" {
#endif

int crc32_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int md5_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int sha256_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int sha3_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);

#ifdef __cplusplus
};
#endif

#include "args_options.cpp"

int init_log_verbose(pargs_options_t pargs)
{
    int loglvl = BASE_LOG_ERROR;
    int ret;
    if (pargs->m_verbose <= 0) {
        loglvl = BASE_LOG_ERROR;
    } else if (pargs->m_verbose == 1) {
        loglvl = BASE_LOG_WARN;
    } else if (pargs->m_verbose == 2) {
        loglvl = BASE_LOG_INFO;
    } else if (pargs->m_verbose == 3) {
        loglvl = BASE_LOG_DEBUG;
    } else {
        loglvl = BASE_LOG_TRACE;
    }
    ret = INIT_LOG(loglvl);
    if (ret < 0) {
        GETERRNO(ret);
        ERROR_INFO("init [%d] verbose error[%d]", pargs->m_verbose, ret);
        SETERRNO(ret);
        return ret;
    }
    return 0;
}

int crc32_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
	popt = popt;
	parsestate = parsestate;
	argv = argv;
	argc = argc;
	fprintf(stderr,"not suppport crc32 yet\n");
	return -1;
}

int md5_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
	popt = popt;
	parsestate = parsestate;
	argv = argv;
	argc = argc;
	fprintf(stderr,"not suppport md5 yet\n");
	return -1;
}


int sha256_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
	popt = popt;
	parsestate = parsestate;
	argv = argv;
	argc = argc;
	fprintf(stderr,"not suppport sha256 yet\n");
	return -1;
}

int sha3_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
	popt = popt;
	parsestate = parsestate;
	argv = argv;
	argc = argc;
	fprintf(stderr,"not suppport sha3 yet\n");
	return -1;
}
#if defined(_WIN32) || defined(_WIN64)
int _tmain(int argc, TCHAR* argv[])
#else
int main(int argc, char* argv[])
#endif
{
    char** args = NULL;
    int ret = 0;
    args_options_t argsoption;
    pextargs_state_t pextstate = NULL;

    memset(&argsoption, 0, sizeof(argsoption));

    args = copy_args(argc, argv);
    if (args == NULL) {
        GETERRNO(ret);
        fprintf(stderr, "can not copy args error[%d]\n", ret);
        goto out;
    }

    ret = EXTARGS_PARSE(argc, args, &argsoption, pextstate);
    if (ret < 0) {
        fprintf(stderr, "could not parse error(%d)", ret);
        goto out;
    }

    ret = 0;
out:
    free_extargs_state(&pextstate);
    release_extargs_output(&argsoption);
    free_args(&args);
    extargs_deinit();
    return ret;
}