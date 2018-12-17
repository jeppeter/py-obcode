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
int check_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int aesenc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int aesdec_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int aesenccbc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);
int aesdeccbc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt);

#ifdef __cplusplus
};
#endif

#include "args_options.cpp"

#include <chkvaldef.c>

#include <crc32calc.c>
#include <md5calc.c>
#include <sha256calc.c>
#include <sha3calc.c>
#include <aes.c>


unsigned char OB_RANDOM_NAME(func_checks_start)[] = { 0x92, 0x62};

chkvalue_t OB_RANDOM_NAME(func_checks)[] = {
    {
        /* function callc_a */
        /* m_offset */
        (signed long long) OB_LL_VALUE(0xc85c2dd871129150),
        /*  m_size value */
        (unsigned long long) OB_ULL_VALUE(0x394c8986fb0df9f4),
        /* m_crc32val */
        {0x55, 0x2b, 0xdc, 0x73, 0x7f, 0x98, 0x7e, 0x2c, 0x97, 0xa6, 0xd4, 0x00, 0x4f, 0x5a, 0x46, 0xe2},
        /* m_sha256val */
        {0x73, 0x67, 0x0a, 0x49, 0x48, 0xf5, 0x17, 0x5e, 0x0f, 0xca, 0x7f, 0x06, 0xb9, 0x2f, 0x9c, 0x9b, 0x13, 0x72, 0xbc, 0x35, 0x78, 0xbf, 0x63, 0x70, 0x8a, 0x16, 0xdd, 0xde, 0xba, 0xef, 0x76, 0x2a},
        /* m_namexor1 */
        {0x3c, 0x4b, 0x19, 0xe0, 0x30, 0x1d, 0x91, 0xc1, 0x25, 0xd9, 0xc3, 0x4c, 0x31, 0x53, 0x20, 0xa7, 0xc0, 0x74, 0x69, 0x4d, 0x49, 0x10, 0x71, 0xed, 0x86, 0xa6, 0xb9, 0x66, 0xe9, 0x76, 0x4b, 0xcf, 0xf3, 0x21, 0x91, 0x0f, 0xbe, 0x29, 0xdd, 0x18, 0xeb, 0x88, 0xe9, 0x8b, 0xdf, 0x65, 0x8e, 0xc2, 0x6a, 0x52, 0x05, 0xd8, 0x73, 0x0b, 0x49, 0x4f, 0x74, 0x7d, 0xfa, 0x7e, 0xe5, 0x9d, 0x84, 0x80},
        /* m_namexor2 */
        {0x5f, 0x2a, 0x75, 0x8c, 0x53, 0x42, 0xf0, 0xc1, 0x25, 0x32, 0x4e, 0x6e, 0xfb, 0x19, 0x86, 0x0b, 0x4c, 0xa0, 0xff, 0x78, 0xfd, 0xa8, 0x29, 0x50, 0xfa, 0x02, 0x6b, 0xeb, 0x87, 0xcc, 0x0b, 0xd2, 0x35, 0x3b, 0x28, 0x7b, 0xe2, 0x9c, 0xa3, 0xae, 0x0e, 0xf5, 0x3c, 0x9d, 0xce, 0x95, 0x49, 0x65, 0x80, 0x51, 0x72, 0x67, 0x24, 0x29, 0xdf, 0xd1, 0x8f, 0x00, 0x4d, 0x13, 0x0a, 0x36, 0xc7, 0x62},
        /* m_sha3val */
        {0x6f, 0x9b, 0x5f, 0xc4, 0x6d, 0x5c, 0x61, 0xaa, 0x0d, 0x15, 0x96, 0xd1, 0x5c, 0xa3, 0xfa, 0x90, 0xf1, 0x04, 0x00, 0xdf, 0x0f, 0x30, 0x55, 0xb7, 0xb4, 0xab, 0x0c, 0x8d, 0xaa, 0x17, 0x2f, 0x8f, 0x4b, 0x80, 0xc4, 0x7e, 0xc7, 0xc6, 0xa7, 0x9c, 0x8a, 0x47, 0x1a, 0xbf, 0x48, 0x52, 0x24, 0x98, 0xc6, 0xff, 0x7a, 0x83, 0x6f, 0xf9, 0xbf, 0x02, 0xe2, 0x2c, 0x4e, 0xe9, 0xe8, 0xf5, 0x88, 0xed},
        /* m_md5val */
        {0xa3, 0xdc, 0x0c, 0x72, 0x9a, 0xb4, 0xfb, 0x42, 0x44, 0xca, 0x27, 0xf0, 0xe9, 0x53, 0xe6, 0xe3, 0xce, 0x31, 0xe9, 0xea, 0xc7, 0x30, 0x15, 0xa3, 0x58, 0x51, 0x9c, 0xf7, 0x83, 0x97, 0x99, 0x8d}
    },
    {
        /* function callc_a */
        /* m_offset */
        (signed long long) OB_LL_VALUE(0xc85c2dd871129150),
        /*  m_size value */
        (unsigned long long) OB_ULL_VALUE(0x394c8986fb0df9f4),
        /* m_crc32val */
        {0x55, 0x2b, 0xdc, 0x73, 0x7f, 0x98, 0x7e, 0x2c, 0x97, 0xa6, 0xd4, 0x00, 0x4f, 0x5a, 0x46, 0xe2},
        /* m_sha256val */
        {0x73, 0x67, 0x0a, 0x49, 0x48, 0xf5, 0x17, 0x5e, 0x0f, 0xca, 0x7f, 0x06, 0xb9, 0x2f, 0x9c, 0x9b, 0x13, 0x72, 0xbc, 0x35, 0x78, 0xbf, 0x63, 0x70, 0x8a, 0x16, 0xdd, 0xde, 0xba, 0xef, 0x76, 0x2a},
        /* m_namexor1 */
        {0x3c, 0x4b, 0x19, 0xe0, 0x30, 0x1d, 0x91, 0xc1, 0x25, 0xd9, 0xc3, 0x4c, 0x31, 0x53, 0x20, 0xa7, 0xc0, 0x74, 0x69, 0x4d, 0x49, 0x10, 0x71, 0xed, 0x86, 0xa6, 0xb9, 0x66, 0xe9, 0x76, 0x4b, 0xcf, 0xf3, 0x21, 0x91, 0x0f, 0xbe, 0x29, 0xdd, 0x18, 0xeb, 0x88, 0xe9, 0x8b, 0xdf, 0x65, 0x8e, 0xc2, 0x6a, 0x52, 0x05, 0xd8, 0x73, 0x0b, 0x49, 0x4f, 0x74, 0x7d, 0xfa, 0x7e, 0xe5, 0x9d, 0x84, 0x80},
        /* m_namexor2 */
        {0x5f, 0x2a, 0x75, 0x8c, 0x53, 0x42, 0xf0, 0xc1, 0x25, 0x32, 0x4e, 0x6e, 0xfb, 0x19, 0x86, 0x0b, 0x4c, 0xa0, 0xff, 0x78, 0xfd, 0xa8, 0x29, 0x50, 0xfa, 0x02, 0x6b, 0xeb, 0x87, 0xcc, 0x0b, 0xd2, 0x35, 0x3b, 0x28, 0x7b, 0xe2, 0x9c, 0xa3, 0xae, 0x0e, 0xf5, 0x3c, 0x9d, 0xce, 0x95, 0x49, 0x65, 0x80, 0x51, 0x72, 0x67, 0x24, 0x29, 0xdf, 0xd1, 0x8f, 0x00, 0x4d, 0x13, 0x0a, 0x36, 0xc7, 0x62},
        /* m_sha3val */
        {0x6f, 0x9b, 0x5f, 0xc4, 0x6d, 0x5c, 0x61, 0xaa, 0x0d, 0x15, 0x96, 0xd1, 0x5c, 0xa3, 0xfa, 0x90, 0xf1, 0x04, 0x00, 0xdf, 0x0f, 0x30, 0x55, 0xb7, 0xb4, 0xab, 0x0c, 0x8d, 0xaa, 0x17, 0x2f, 0x8f, 0x4b, 0x80, 0xc4, 0x7e, 0xc7, 0xc6, 0xa7, 0x9c, 0x8a, 0x47, 0x1a, 0xbf, 0x48, 0x52, 0x24, 0x98, 0xc6, 0xff, 0x7a, 0x83, 0x6f, 0xf9, 0xbf, 0x02, 0xe2, 0x2c, 0x4e, 0xe9, 0xe8, 0xf5, 0x88, 0xed},
        /* m_md5val */
        {0xa3, 0xdc, 0x0c, 0x72, 0x9a, 0xb4, 0xfb, 0x42, 0x44, 0xca, 0x27, 0xf0, 0xe9, 0x53, 0xe6, 0xe3, 0xce, 0x31, 0xe9, 0xea, 0xc7, 0x30, 0x15, 0xa3, 0x58, 0x51, 0x9c, 0xf7, 0x83, 0x97, 0x99, 0x8d}
    }
};

unsigned char OB_RANDOM_NAME(func_checks_end)[] = {0x0};

chkvalue_t OB_RANDOM_NAME(value_checks)[] = {
    {
        /* function callc_a */
        /* m_offset */
        (signed long long) OB_LL_VALUE(0xc85c2dd871129150),
        /*  m_size value */
        (unsigned long long) OB_ULL_VALUE(0x394c8986fb0df9f4),
        /* m_crc32val */
        {0x55, 0x2b, 0xdc, 0x73, 0x7f, 0x98, 0x7e, 0x2c, 0x97, 0xa6, 0xd4, 0x00, 0x4f, 0x5a, 0x46, 0xe2},
        /* m_sha256val */
        {0x73, 0x67, 0x0a, 0x49, 0x48, 0xf5, 0x17, 0x5e, 0x0f, 0xca, 0x7f, 0x06, 0xb9, 0x2f, 0x9c, 0x9b, 0x13, 0x72, 0xbc, 0x35, 0x78, 0xbf, 0x63, 0x70, 0x8a, 0x16, 0xdd, 0xde, 0xba, 0xef, 0x76, 0x2a},
        /* m_namexor1 */
        {0x3c, 0x4b, 0x19, 0xe0, 0x30, 0x1d, 0x91, 0xc1, 0x25, 0xd9, 0xc3, 0x4c, 0x31, 0x53, 0x20, 0xa7, 0xc0, 0x74, 0x69, 0x4d, 0x49, 0x10, 0x71, 0xed, 0x86, 0xa6, 0xb9, 0x66, 0xe9, 0x76, 0x4b, 0xcf, 0xf3, 0x21, 0x91, 0x0f, 0xbe, 0x29, 0xdd, 0x18, 0xeb, 0x88, 0xe9, 0x8b, 0xdf, 0x65, 0x8e, 0xc2, 0x6a, 0x52, 0x05, 0xd8, 0x73, 0x0b, 0x49, 0x4f, 0x74, 0x7d, 0xfa, 0x7e, 0xe5, 0x9d, 0x84, 0x80},
        /* m_namexor2 */
        {0x5f, 0x2a, 0x75, 0x8c, 0x53, 0x42, 0xf0, 0xc1, 0x25, 0x32, 0x4e, 0x6e, 0xfb, 0x19, 0x86, 0x0b, 0x4c, 0xa0, 0xff, 0x78, 0xfd, 0xa8, 0x29, 0x50, 0xfa, 0x02, 0x6b, 0xeb, 0x87, 0xcc, 0x0b, 0xd2, 0x35, 0x3b, 0x28, 0x7b, 0xe2, 0x9c, 0xa3, 0xae, 0x0e, 0xf5, 0x3c, 0x9d, 0xce, 0x95, 0x49, 0x65, 0x80, 0x51, 0x72, 0x67, 0x24, 0x29, 0xdf, 0xd1, 0x8f, 0x00, 0x4d, 0x13, 0x0a, 0x36, 0xc7, 0x62},
        /* m_sha3val */
        {0x6f, 0x9b, 0x5f, 0xc4, 0x6d, 0x5c, 0x61, 0xaa, 0x0d, 0x15, 0x96, 0xd1, 0x5c, 0xa3, 0xfa, 0x90, 0xf1, 0x04, 0x00, 0xdf, 0x0f, 0x30, 0x55, 0xb7, 0xb4, 0xab, 0x0c, 0x8d, 0xaa, 0x17, 0x2f, 0x8f, 0x4b, 0x80, 0xc4, 0x7e, 0xc7, 0xc6, 0xa7, 0x9c, 0x8a, 0x47, 0x1a, 0xbf, 0x48, 0x52, 0x24, 0x98, 0xc6, 0xff, 0x7a, 0x83, 0x6f, 0xf9, 0xbf, 0x02, 0xe2, 0x2c, 0x4e, 0xe9, 0xe8, 0xf5, 0x88, 0xed},
        /* m_md5val */
        {0xa3, 0xdc, 0x0c, 0x72, 0x9a, 0xb4, 0xfb, 0x42, 0x44, 0xca, 0x27, 0xf0, 0xe9, 0x53, 0xe6, 0xe3, 0xce, 0x31, 0xe9, 0xea, 0xc7, 0x30, 0x15, 0xa3, 0x58, 0x51, 0x9c, 0xf7, 0x83, 0x97, 0x99, 0x8d}
    }
};

unsigned char OB_RANDOM_NAME(value_checks_total_end)[] = {0x32, 0xfc};


#include <chkval.c>

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
        ret = crc32_calc((unsigned char*)pfilebuf, (unsigned int)filelen, (unsigned char*)&crcval, sizeof(crcval));
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


int md5_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i, j;
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
        ret = md5_calc((unsigned char*)pfilebuf, (unsigned int)filelen, md5val, sizeof(md5val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        fprintf(stdout, "[%s] md5 ", infile);
        for (j = 0; j < 16; j++) {
            fprintf(stdout, "%02x", md5val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}


int sha256_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i, j;
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
        ret = sha256_calc((unsigned char*)pfilebuf, (unsigned int)filelen, sha256val, sizeof(sha256val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        fprintf(stdout, "[%s] sha256 ", infile);
        for (j = 0; j < (int)sizeof(sha256val); j++) {
            fprintf(stdout, "%02x", sha256val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}


int sha3_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    char* pfilebuf = NULL;
    int filesize = 0;
    int filelen = 0;
    int i, j, retval;
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
        ret = sha3_calc((unsigned char*)pfilebuf, (unsigned int)filelen, sha3val, sizeof(sha3val));
        if (ret < 0) {
            GETERRNO(ret);
            goto out;
        }
        retval = ret;
        fprintf(stdout, "[%s] sha256 ", infile);
        for (j = 0; j < retval; j++) {
            fprintf(stdout, "%02x", sha3val[j]);
        }
        fprintf(stdout, "\n");
    }

    ret = 0;
out:
    read_file_whole(NULL, &pfilebuf, &filesize);
    SETERRNO(ret);
    return ret;
}

int check_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    pchkvalue_t pchk = &(OB_RANDOM_NAME(func_checks)[0]);
    pargs_options_t pargs = (pargs_options_t) popt;
    unsigned int i;
    init_log_verbose(pargs);
    argc = argc;
    argv = argv;
    parsestate = parsestate;
    fprintf(stdout, "size [0x%llx:%lld]\n", pchk->m_size, pchk->m_size);
    fprintf(stdout, "m_namexor1 ");
    for (i = 0; i < sizeof(pchk->m_namexor1); i++) {
        fprintf(stdout, "%02x", pchk->m_namexor1[i]);
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "m_namexor2 ");
    for (i = 0; i < sizeof(pchk->m_namexor2); i++) {
        fprintf(stdout, "%02x", pchk->m_namexor2[i]);
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "m_crc32val ");
    for (i = 0; i < sizeof(pchk->m_crc32val); i++) {
        fprintf(stdout, "%02x", pchk->m_crc32val[i]);
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "m_md5val ");
    for (i = 0; i < sizeof(pchk->m_md5val); i++) {
        fprintf(stdout, "%02x", pchk->m_md5val[i]);
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "m_sha256val ");
    for (i = 0; i < sizeof(pchk->m_sha256val); i++) {
        fprintf(stdout, "%02x", pchk->m_sha256val[i]);
    }
    fprintf(stdout, "\n");

    fprintf(stdout, "m_sha3val ");
    for (i = 0; i < sizeof(pchk->m_sha3val); i++) {
        fprintf(stdout, "%02x", pchk->m_sha3val[i]);
    }
    fprintf(stdout, "\n");
    fprintf(stdout, "md5_handler %p\n", md5_handler);
    fprintf(stdout, "sha256_handler %p\n", sha256_handler);

    return 0;
}

void debug_c_code(FILE* fp, unsigned char* pbuf, int size, const char* fmt, ...)
{
    int i, j;
    if (fmt != NULL) {
        va_list ap;
        va_start(ap, fmt);
        vfprintf(fp, fmt, ap);
    }
    fprintf(fp, "{");

    for (i = 0, j = 0; i < size; i++, j++) {
        if ((i % 16) == 0) {
            if (i > 0) {
                fprintf(fp, ",");
            }
            fprintf(fp, "\n    ");
            j = 0;
        }
        if (j > 0) {
            fprintf(fp, ",");
        }
        fprintf(fp, "0x%02x", pbuf[i]);
    }
    fprintf(fp, "\n};\n");
    return;
}

unsigned char _get_char(char* pch)
{
    unsigned char val=0;
    if (*pch >= '0' && *pch <= '9') {
        val += ((*pch - '0'));
    } else if (*pch >= 'a' && *pch <= 'f') {
        val += ((*pch - 'a' + 10));
    } else if (*pch >= 'A' && *pch <= 'F') {
        val += ((*pch - 'A' + 10));
    }
    return val;
}

int _get_aes_key(char* keyfile, unsigned int** ppschedkey, int *psize)
{
    int keybufsize = 0;
    int keybuflen = 0;
    char* pkeybuf = NULL;
    int ret;
    unsigned char* pkey = NULL;
    int keysize = 0;
    int i, j;
    unsigned char val;
    unsigned int *pretsched = *ppschedkey;
    int retsize = *psize;

    if (keyfile == NULL) {
        if (ppschedkey && *ppschedkey) {
            free(*ppschedkey);
            *ppschedkey = NULL;
        }
        if (psize) {
            *psize = 0;
        }
        return 0;
    }

    ret = read_file_whole(keyfile, &pkeybuf, &keybufsize);
    if (ret < 0) {
        goto fail;
    }
    keybuflen = ret;

    keysize = (keybuflen / 2) + 1;
    pkey = (unsigned char*)malloc((size_t)keysize);
    if (pkey == NULL) {
        GETERRNO(ret);
        fprintf(stderr, "alloc %d error[%d]\n", keysize, ret);
        goto fail;
    }

    for (i = 0, j = 0; i < keybuflen; i += 2, j++) {
        val = 0;
        val += (_get_char(&(pkeybuf[i])) << 4);
        val += (_get_char(&(pkeybuf[i+1])));
        pkey[j] = val;
    }

    if (retsize < 256 || pretsched == NULL) {
        if (retsize < 256) {
            retsize = 256;
        }
        pretsched = (unsigned int*)malloc((size_t)retsize);
        if (pretsched == NULL) {
            GETERRNO(ret);
            fprintf(stderr, "alloc %d error[%d]\n", retsize, ret);
            goto fail;
        }
    }
    memset(pretsched, 0, (size_t)retsize);

    aes_key_setup(pkey, pretsched, 256);

    if (*ppschedkey && *ppschedkey != pretsched) {
        free(*ppschedkey);
    }
    *ppschedkey = pretsched;
    *psize = retsize;

    if (pkey) {
        free(pkey);
    }
    pkey = NULL;
    read_file_whole(NULL, &pkeybuf, &keybufsize);
    keybuflen = 0;
    return 256;

fail:
    if (pretsched && pretsched != *ppschedkey) {
        free(pretsched);
    }
    pretsched = NULL;
    retsize = 0;

    if (pkey) {
        free(pkey);
    }
    pkey = NULL;
    read_file_whole(NULL, &pkeybuf, &keybufsize);
    keybuflen = 0;
    SETERRNO(ret);
    return ret;
}

int _get_iv(char* ivfile, unsigned char** ppiv, int *psize)
{
    int ivbufsize = 0;
    int ivbuflen = 0;
    char* pivbuf = NULL;
    int ret;
    int i, j;
    unsigned char val;
    //unsigned char* pcur;
    unsigned char *pretiv = *ppiv;
    int ivlen =0;
    int retsize = *psize;

    if (ivfile == NULL) {
        if (ppiv && *ppiv) {
            free(*ppiv);
            *ppiv = NULL;
        }
        if (psize) {
            *psize = 0;
        }
        return 0;
    }

    ret = read_file_whole(ivfile, &pivbuf, &ivbufsize);
    if (ret < 0) {
        goto fail;
    }
    ivbuflen = ret;

    ivlen = (ivbuflen / 2) + 1;
    if (ivlen > retsize || pretiv == NULL) {
        if (retsize < ivlen) {
            retsize = ivlen;
        }
        pretiv = (unsigned char*)malloc((size_t)retsize);
    }
    memset(pretiv, 0, (size_t)retsize);

    for (i = 0, j = 0; i < ivbuflen; i += 2, j++) {
        val = 0;
        val += (_get_char(&(pivbuf[i])) << 4);
        val += (_get_char(&(pivbuf[i+1])));
        pretiv[j] = val;
    }
#if 0    
    fprintf(stdout, "ivbuf:\n%s\n", pivbuf);
    fprintf(stdout, "iv:\n");
    pcur = pretiv;
    for (i = 0; i < j; i++,pcur ++) {
        if (i > 0) {
            fprintf(stdout, ",");
        }
        fprintf(stdout, "0x%02x", *pcur);
    }
#endif

    if (*ppiv && *ppiv != pretiv) {
        free(*ppiv);
    }
    *ppiv = pretiv;
    *psize = retsize;

    read_file_whole(NULL, &pivbuf, &ivbufsize);
    ivbuflen = 0;
    return j;

fail:
    if (pretiv && pretiv != *ppiv) {
        free(pretiv);
    }
    pretiv = NULL;
    retsize = 0;

    read_file_whole(NULL, &pivbuf, &ivbufsize);
    ivbuflen = 0;
    SETERRNO(ret);
    return ret;
}


int aesenc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    int cnt = 0;
    char* keyfile = NULL;
    char* inputfile = NULL;
    unsigned char* inputbuf = NULL;
    int inputsize = 0;
    int inputlen = 0;
    unsigned char* outputbuf = NULL;
    int outputsize = 0;
    int outputlen = 0;
    unsigned int* pkeysched = NULL;
    int schedsize = 0;
    FILE* fout = stderr;
    int i, j;
    pargs_options_t pargs = (pargs_options_t) popt;
    init_log_verbose(pargs);
    while (parsestate->leftargs != NULL &&
            parsestate->leftargs[cnt] != NULL) {
        cnt ++;
    }
    if (cnt < 2) {
        ret  = -CMN_EINVAL;
        fprintf(stderr, "need keyfile inputfile");
        goto out;
    }
    argc = argc;
    argv = argv;

    keyfile = parsestate->leftargs[0];
    ret = _get_aes_key(keyfile, &pkeysched, &schedsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }

    if (pargs->m_output != NULL) {
        fout = fopen(pargs->m_output, "wb");
        if (fout == NULL) {
            GETERRNO(ret);
            fprintf(stderr, "open[%s] error[%d]\n", pargs->m_output, ret);
            goto out;
        }
    }

    for (i = 1; i < cnt; i++) {
        inputfile = parsestate->leftargs[i];
        ret = read_file_whole(inputfile, (char**)&inputbuf, &inputsize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", inputfile, ret);
            goto out;
        }
        inputlen = ret;
        outputlen = inputlen;
        if ((outputlen % 16) != 0) {
            outputlen = ((outputlen + 15) / 16) * 16;
        }

        if (outputsize < outputlen || outputbuf == NULL) {
            if (outputsize < outputlen) {
                outputsize = outputlen;
            }
            if (outputbuf != NULL) {
                free(outputbuf);
            }
            outputbuf = NULL;
            outputbuf = (unsigned char*)malloc((size_t)outputsize);
            if (outputbuf == NULL) {
                GETERRNO(ret);
                fprintf(stderr, "alloc [%d] error[%d]\n", outputsize, ret);
                goto out;
            }
        }
        memset(outputbuf, 0, (size_t)outputlen);
        if (inputlen > 0) {
            memcpy(outputbuf, inputbuf, (size_t)inputlen);
        }

        for (j = 0; j < outputlen; j += 16) {
            aes_encrypt(&(inputbuf[j]), &(outputbuf[j]), pkeysched, 256);
            ret = (int)fwrite(&(outputbuf[j]), (size_t)16, 1, fout);
            if (ret != 1) {
                GETERRNO(ret);
                fprintf(stderr, "can not write buffer [%d] error[%d]\n", j, ret);
                goto out;
            }
        }
    }
    ret = 0;
out:
    _get_aes_key(NULL, &pkeysched, &schedsize);

    if (outputbuf != NULL) {
        free(outputbuf);
    }
    outputbuf = NULL;
    outputsize = 0;
    outputlen = 0;
    if (fout != NULL && fout != stderr) {
        fclose(fout);
    }
    fout = NULL;
    read_file_whole(NULL, (char**)&inputbuf, &inputsize);
    inputlen = 0;
    SETERRNO(ret);
    return ret;
}

int aesdec_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    int cnt = 0;
    char* keyfile = NULL;
    char* inputfile = NULL;
    unsigned char* inputbuf = NULL;
    int inputsize = 0;
    int inputlen = 0;
    unsigned char* outputbuf = NULL;
    int outputsize = 0;
    int outputlen = 0;
    unsigned int* pkeysched = NULL;
    int schedsize = 0;
    FILE* fout = stderr;
    int i, j;
    pargs_options_t pargs = (pargs_options_t) popt;
    init_log_verbose(pargs);
    while (parsestate->leftargs != NULL &&
            parsestate->leftargs[cnt] != NULL) {
        cnt ++;
    }
    if (cnt < 2) {
        ret  = -CMN_EINVAL;
        fprintf(stderr, "need keyfile inputfile");
        goto out;
    }
    argc = argc;
    argv = argv;

    keyfile = parsestate->leftargs[0];
    ret = _get_aes_key(keyfile, &pkeysched, &schedsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }

    if (pargs->m_output != NULL) {
        fout = fopen(pargs->m_output, "wb");
        if (fout == NULL) {
            GETERRNO(ret);
            fprintf(stderr, "open[%s] error[%d]\n", pargs->m_output, ret);
            goto out;
        }
    }

    for (i = 1; i < cnt; i++) {
        inputfile = parsestate->leftargs[i];
        ret = read_file_whole(inputfile, (char**)&inputbuf, &inputsize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", inputfile, ret);
            goto out;
        }
        inputlen = ret;
        outputlen = inputlen;
        if ((outputlen % 16) != 0) {
            outputlen = ((outputlen + 15) / 16) * 16;
        }

        if (outputsize < outputlen || outputbuf == NULL) {
            if (outputsize < outputlen) {
                outputsize = outputlen;
            }
            if (outputbuf != NULL) {
                free(outputbuf);
            }
            outputbuf = NULL;
            outputbuf = (unsigned char*)malloc((size_t)outputsize);
            if (outputbuf == NULL) {
                GETERRNO(ret);
                fprintf(stderr, "alloc [%d] error[%d]\n", outputsize, ret);
                goto out;
            }
        }
        memset(outputbuf, 0, (size_t)outputlen);
        if (inputlen > 0) {
            memcpy(outputbuf, inputbuf, (size_t)inputlen);
        }

        for (j = 0; j < outputlen; j += 16) {
            aes_decrypt(&(inputbuf[j]), &(outputbuf[j]), pkeysched, 256);
            ret = (int)fwrite(&(outputbuf[j]), (size_t)16, 1, fout);
            if (ret != 1) {
                GETERRNO(ret);
                fprintf(stderr, "can not write buffer [%d] error[%d]\n", j, ret);
                goto out;
            }
        }
    }
    ret = 0;
out:
    _get_aes_key(NULL, &pkeysched, &schedsize);

    if (outputbuf != NULL) {
        free(outputbuf);
    }
    outputbuf = NULL;
    outputsize = 0;
    outputlen = 0;
    if (fout != NULL && fout != stderr) {
        fclose(fout);
    }
    fout = NULL;
    read_file_whole(NULL, (char**)&inputbuf, &inputsize);
    inputlen = 0;
    SETERRNO(ret);
    return ret;
}

int aesenccbc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    int cnt = 0;
    char* keyfile = NULL;
    char* ivfile=NULL;
    char* inputfile = NULL;
    unsigned char* inputbuf = NULL;
    int inputsize = 0;
    int inputlen = 0;
    unsigned char* outputbuf = NULL;
    int outputsize = 0;
    int outputlen = 0;
    unsigned int* pkeysched = NULL;
    int schedsize = 0;
    unsigned char* piv=NULL;
    int ivsize=0;
    FILE* fout = stderr;
    int i, j;
    pargs_options_t pargs = (pargs_options_t) popt;
    init_log_verbose(pargs);
    while (parsestate->leftargs != NULL &&
            parsestate->leftargs[cnt] != NULL) {
        cnt ++;
    }
    if (cnt < 3) {
        ret  = -CMN_EINVAL;
        fprintf(stderr, "need keyfile ivfile inputfile");
        goto out;
    }
    argc = argc;
    argv = argv;

    keyfile = parsestate->leftargs[0];
    ret = _get_aes_key(keyfile, &pkeysched, &schedsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }
    ivfile = parsestate->leftargs[1];
    ret = _get_iv(ivfile,&piv,&ivsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }

    if (pargs->m_output != NULL) {
        fout = fopen(pargs->m_output, "wb");
        if (fout == NULL) {
            GETERRNO(ret);
            fprintf(stderr, "open[%s] error[%d]\n", pargs->m_output, ret);
            goto out;
        }
    }

    for (i = 2; i < cnt; i++) {
        inputfile = parsestate->leftargs[i];
        ret = read_file_whole(inputfile, (char**)&inputbuf, &inputsize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", inputfile, ret);
            goto out;
        }
        inputlen = ret;
        outputlen = inputlen;
        if ((outputlen % 16) != 0) {
            outputlen = ((outputlen + 15) / 16) * 16;
        }

        if (outputsize < outputlen || outputbuf == NULL) {
            if (outputsize < outputlen) {
                outputsize = outputlen;
            }
            if (outputbuf != NULL) {
                free(outputbuf);
            }
            outputbuf = NULL;
            outputbuf = (unsigned char*)malloc((size_t)outputsize);
            if (outputbuf == NULL) {
                GETERRNO(ret);
                fprintf(stderr, "alloc [%d] error[%d]\n", outputsize, ret);
                goto out;
            }
        }
        memset(outputbuf, 0, (size_t)outputlen);
        if (inputlen > 0) {
            memcpy(outputbuf, inputbuf, (size_t)inputlen);
        }

        j = 0;
        for (j = 0; j < outputlen; j += AES_BLOCK_SIZE) {
            aes_encrypt_cbc(&(inputbuf[j]),(size_t)AES_BLOCK_SIZE, &(outputbuf[j]), pkeysched, 256,piv);
            ret = (int)fwrite(&(outputbuf[j]), (size_t)AES_BLOCK_SIZE, 1, fout);
            if (ret != 1) {
                GETERRNO(ret);
                fprintf(stderr, "can not write buffer [%d] error[%d]\n", j, ret);
                goto out;
            }
            memcpy(piv,&(outputbuf[j]), AES_BLOCK_SIZE);
        }
    }
    ret = 0;
out:
    _get_iv(NULL,&piv,&ivsize);
    _get_aes_key(NULL, &pkeysched, &schedsize);

    if (outputbuf != NULL) {
        free(outputbuf);
    }
    outputbuf = NULL;
    outputsize = 0;
    outputlen = 0;
    if (fout != NULL && fout != stderr) {
        fclose(fout);
    }
    fout = NULL;
    read_file_whole(NULL, (char**)&inputbuf, &inputsize);
    inputlen = 0;
    SETERRNO(ret);
    return ret;
}
int aesdeccbc_handler(int argc, char* argv[], pextargs_state_t parsestate, void* popt)
{
    int ret;
    int cnt = 0;
    char* keyfile = NULL;
    char* ivfile=NULL;
    char* inputfile = NULL;
    unsigned char* inputbuf = NULL;
    int inputsize = 0;
    int inputlen = 0;
    unsigned char* outputbuf = NULL;
    int outputsize = 0;
    int outputlen = 0;
    unsigned int* pkeysched = NULL;
    int schedsize = 0;
    unsigned char* piv=NULL;
    int ivsize=0;
    FILE* fout = stderr;
    int i, j;
    pargs_options_t pargs = (pargs_options_t) popt;
    init_log_verbose(pargs);
    while (parsestate->leftargs != NULL &&
            parsestate->leftargs[cnt] != NULL) {
        cnt ++;
    }
    if (cnt < 3) {
        ret  = -CMN_EINVAL;
        fprintf(stderr, "need keyfile ivfile inputfile");
        goto out;
    }
    argc = argc;
    argv = argv;

    keyfile = parsestate->leftargs[0];
    ret = _get_aes_key(keyfile, &pkeysched, &schedsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }
    ivfile = parsestate->leftargs[1];
    ret = _get_iv(ivfile,&piv,&ivsize);
    if (ret < 0) {
        GETERRNO(ret);
        goto out;
    }

    if (pargs->m_output != NULL) {
        fout = fopen(pargs->m_output, "wb");
        if (fout == NULL) {
            GETERRNO(ret);
            fprintf(stderr, "open[%s] error[%d]\n", pargs->m_output, ret);
            goto out;
        }
    }

    for (i = 2; i < cnt; i++) {
        inputfile = parsestate->leftargs[i];
        ret = read_file_whole(inputfile, (char**)&inputbuf, &inputsize);
        if (ret < 0) {
            GETERRNO(ret);
            fprintf(stderr, "read [%s] error[%d]\n", inputfile, ret);
            goto out;
        }
        inputlen = ret;
        outputlen = inputlen;
        if ((outputlen % 16) != 0) {
            outputlen = ((outputlen + 15) / 16) * 16;
        }

        if (outputsize < outputlen || outputbuf == NULL) {
            if (outputsize < outputlen) {
                outputsize = outputlen;
            }
            if (outputbuf != NULL) {
                free(outputbuf);
            }
            outputbuf = NULL;
            outputbuf = (unsigned char*)malloc((size_t)outputsize);
            if (outputbuf == NULL) {
                GETERRNO(ret);
                fprintf(stderr, "alloc [%d] error[%d]\n", outputsize, ret);
                goto out;
            }
        }
        memset(outputbuf, 0, (size_t)outputlen);
        if (inputlen > 0) {
            memcpy(outputbuf, inputbuf, (size_t)inputlen);
        }

        j = 0;
        for (j = 0; j < outputlen; j += AES_BLOCK_SIZE) {
            aes_decrypt_cbc(&(inputbuf[j]),(size_t)AES_BLOCK_SIZE, &(outputbuf[j]), pkeysched, 256,piv);
            ret = (int)fwrite(&(outputbuf[j]), (size_t)AES_BLOCK_SIZE, 1, fout);
            if (ret != 1) {
                GETERRNO(ret);
                fprintf(stderr, "can not write buffer [%d] error[%d]\n", j, ret);
                goto out;
            }
            memcpy(piv,&(inputbuf[j]), AES_BLOCK_SIZE);
        }
    }
    ret = 0;
out:
    _get_iv(NULL,&piv,&ivsize);
    _get_aes_key(NULL, &pkeysched, &schedsize);

    if (outputbuf != NULL) {
        free(outputbuf);
    }
    outputbuf = NULL;
    outputsize = 0;
    outputlen = 0;
    if (fout != NULL && fout != stderr) {
        fclose(fout);
    }
    fout = NULL;
    read_file_whole(NULL, (char**)&inputbuf, &inputsize);
    inputlen = 0;
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