

typedef struct __chkvalue 
{
	signed long long m_offset;
	unsigned char m_namexor1[64];
	unsigned char m_namexor2[64];
	unsigned int m_size;
	unsigned char m_crc32val[8];
	unsigned char m_md5val[16];
	unsigned char m_sha256val[32];
	unsigned char m_sha3val[64];
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

#define  CRC32_VALUE_SIZE                     4
#define  MD5_VALUE_SIZE                       16
#define  SHA256_VALUE_SIZE                    32
#define  SHA3_VALUE_SIZE                      64

typedef void (*m_check_fail_func_t)(int errcode,char* name);
typedef int (*m_calc_value_func_t)(unsigned char* ptr,unsigned int len,unsigned char* pval,int valsize);
typedef int (*m_checkvalue_func_t)(unsigned char* ptr,unsigned int size, m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize);

int OB_RANDOM_NAME(check_value_func)(unsigned char* ptr,unsigned int size,m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize);
int OB_RANDOM_NAME(check_end_func)(m_check_fail_func_t failfunc);
