

typedef struct __chkvalue 
{
    signed long long m_offset;
    unsigned long long m_size;
    unsigned char m_crc32val[16];
    unsigned char m_sha256val[32];
    unsigned char m_namexor1[64];
    unsigned char m_namexor2[64];
    unsigned char m_sha3val[64];
    unsigned char m_md5val[32];
} chkvalue_t,*pchkvalue_t;

#define  CHECK_VALUE_CRC32_FAILED             -1
#define  CHECK_VALUE_MD5_FAILED               -2
#define  CHECK_VALUE_SHA256_FAILED            -3
#define  CHECK_VALUE_SHA3_FAILED              -4
#define  CHECK_VALUE_CHKVAL_CRC32_FAILED      -6
#define  CHECK_VALUE_CHKVAL_MD5_FAILED        -7
#define  CHECK_VALUE_CHKVAL_SHA256_FAILED     -8
#define  CHECK_VALUE_CHKVAL_SHA3_FAILED       -9
#define  CHECK_VALUE_CHKVAL_FUNCS_FAILED      -10
#define  CHECK_VALUE_CHKVAL_DATAS_FAILED      -11
#define  CHECK_VALUE_CHKVAL_AES_FAILED        -12

#define  CRC32_VALUE_SIZE                     4
#define  MD5_VALUE_SIZE                       16
#define  SHA256_VALUE_SIZE                    32
#define  SHA3_VALUE_SIZE                      64


#define  AES_KEY_SIZE                         32
#define  AES_IV_SIZE                          16

typedef int (*m_calc_value_func_t)(unsigned char* ptr,unsigned int len,unsigned char* pval,int valsize);
typedef int (*m_checkvalue_func_t)(unsigned char* ptr,unsigned int size, m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize);

#ifdef __cplusplus
extern "C" {
#endif
int OB_RANDOM_NAME(crc32_calc)(unsigned char *message, unsigned int size, unsigned char* pval, int valsize);
int OB_RANDOM_NAME(check_value_func)(unsigned char* ptr,unsigned int size,m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize);
int OB_RANDOM_NAME(check_chkval_value)(m_check_fail_func_t failfunc);

#ifdef __cplusplus
};
#endif
