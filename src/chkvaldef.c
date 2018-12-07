

typedef struct __chkvalue 
{
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
#define  CHECK_VALUE_CHKVAL_FAILED            -5

#define  CRC32_VALUE_SIZE                     4
#define  MD5_VALUE_SIZE                       16
#define  SHA256_VALUE_SIZE                    32
#define  SHA3_VALUE_SIZE                      64

typedef void (*m_check_fail_func_t)(int errcode,char* name);
typedef int (*m_calc_value_func_t)(unsigned char* ptr,unsigned int len,unsigned char* pval,int valsize);
typedef int (*m_checkvalue_func_t)(unsigned char* ptr,unsigned int size, m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize);
