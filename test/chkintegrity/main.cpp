#include <stdio.h>
#include <stdlib.h>
#include <extargs.h>
#include <cmn_err.h>
#include <cmn_output_debug.h>
#include <cmn_args.h>
#include <cmn_fileop.h>
#include <string.h>
#include <obcode.h>


typedef struct __args_options {
    int m_verbose;
    char* m_input;
    char* m_output;
} args_options_t, *pargs_options_t;


#if defined(_WIN32) || defined(_WIN64)
#pragma comment(lib,"Advapi32.lib")
#endif


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

#include <crc32calc.c>

int crc32_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i;
    char* infile;
    unsigned int crcval;
    pargs_options_t pargs = (pargs_options_t) popt;
    argc = argc;
    argv = argv;
    init_log_verbose(pargs);

    for (i = 0; parsestate->leftargs != NULL && parsestate->leftargs[i] != NULL; i++) {
        infile = parsestate->leftargs[i];
        ret = read_file_whole(infile, &pfilebuf, &filesize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", infile, ret);
            goto out;
        }
        filelen = ret;
        ret = crc32_calc((unsigned char*)pfilebuf, (unsigned int)filelen, (unsigned char*)&crcval,sizeof(crcval));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        fprintf(stdout, "[%s] crc32 [0x%x:%d]\n", infile, crcval, crcval);
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}

#include <md5calc.c>

int md5_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i,j;
    char* infile;
    unsigned char md5val[16];
    pargs_options_t pargs = (pargs_options_t) popt;
    argc = argc;
    argv = argv;

    init_log_verbose(pargs);

    for (i = 0; parsestate->leftargs != NULL && parsestate->leftargs[i] != NULL; i++) {
        infile = parsestate->leftargs[i];
        ret = read_file_whole(infile, &pfilebuf, &filesize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", infile, ret);
            goto out;
        }
        filelen = ret;
        ret = md5_calc((unsigned char*)pfilebuf, (unsigned int)filelen, md5val,sizeof(md5val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        fprintf(stdout, "[%s] md5 ", infile);
        for (j=0;j<16;j++) {
            fprintf(stdout,"%02x", md5val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}

#include <sha256calc.c>

int sha256_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i,j;
    char* infile;
    unsigned char sha256val[32];
    pargs_options_t pargs = (pargs_options_t) popt;
    argc = argc;
    argv = argv;

    init_log_verbose(pargs);

    for (i = 0; parsestate->leftargs != NULL && parsestate->leftargs[i] != NULL; i++) {
        infile = parsestate->leftargs[i];
        ret = read_file_whole(infile, &pfilebuf, &filesize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", infile, ret);
            goto out;
        }
        filelen = ret;
        ret = sha256_calc((unsigned char*)pfilebuf, (unsigned int)filelen, sha256val,sizeof(sha256val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        fprintf(stdout, "[%s] sha256 ", infile);
        for (j=0;j<(int)sizeof(sha256val);j++) {
            fprintf(stdout,"%02x", sha256val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}

#include <sha3calc.c>

int sha3_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i,j,retval;
    char* infile;
    unsigned char sha3val[64];
    pargs_options_t pargs = (pargs_options_t) popt;
    argc = argc;
    argv = argv;

    init_log_verbose(pargs);

    for (i = 0; parsestate->leftargs != NULL && parsestate->leftargs[i] != NULL; i++) {
        infile = parsestate->leftargs[i];
        ret = read_file_whole(infile, &pfilebuf, &filesize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", infile, ret);
            goto out;
        }
        filelen = ret;
        ret = sha3_calc((unsigned char*)pfilebuf, (unsigned int)filelen, sha3val,sizeof(sha3val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        retval = ret;
        fprintf(stdout, "[%s] sha256 ", infile);
        for (j=0;j<retval;j++) {
            fprintf(stdout,"%02x", sha3val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
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