
#define FAIL_RET(retval ,name)                                                                    \
do{                                                                                               \
	if (failfunc != ((void*)0)) {                                                                 \
		failfunc((retval), (char*)(name));                                                        \
	}                                                                                             \
	return (retval);                                                                              \
}while(0)

int OB_RANDOM_NAME(format_name)(unsigned char* pstored, unsigned int size, unsigned char* xor1, unsigned char* xor2)
{
	unsigned int i;
	for (i=0;i<size;i++) {
		pstored[i] = (unsigned char)(xor1[i] ^ xor2[i]);
	}
	return (int)size;
}

int OB_RANDOM_NAME(check_value_func)(unsigned char* ptr,unsigned int size,m_calc_value_func_t calcfunc, unsigned char* pchkval, int calcsize)
{
	int ret=0;
	unsigned char calcvalue[64];
	int i;

	OB_EXPAND_CODE(ret);

	ret = calcfunc(ptr,size,calcvalue,calcsize);
	if (ret < 0) {
		return ret;
	}
	if (ret != calcsize) {
		return -2;
	}

	for (i=0;i<calcsize;i++) {
		if (calcvalue[i] != pchkval[i]) {
			return -3;
		}
	}
	return 0;
}

unsigned char* OB_RANDOM_NAME(get_func_address)(unsigned char* ptr)
{
	unsigned char* pretval = ptr;
	signed int* pjmp;
	if (*pretval == 0xe9) {
		pjmp = (signed int*)(pretval + 1);
		pretval += sizeof(*pjmp) + 1;
		pretval += *pjmp;
	}
	return pretval;
}

int OB_RANDOM_NAME(aes_decrypt_block)(pchkvalue_t pinput,pchkvalue_t poutput,unsigned char* pkey,unsigned char* piv)
{
	unsigned int schedkeys[64];
	unsigned char* plastiv;
	if ((sizeof(*pinput) % AES_BLOCK_SIZE) != 0) {
		return -1;
	}
	OB_RANDOM_NAME(aes_key_setup)(pkey,schedkeys,256);
	OB_RANDOM_NAME(aes_decrypt_cbc)((unsigned char*)pinput,sizeof(*pinput),(unsigned char*)poutput,schedkeys,256,piv);
	/*to copy the initial vector for next use*/
	plastiv = (unsigned char*) pinput;
	plastiv += sizeof(*pinput);
	plastiv -= AES_BLOCK_SIZE;

	aes_memcpy(piv,plastiv,AES_BLOCK_SIZE);
	return (int)sizeof(*poutput);
}

int OB_RANDOM_NAME(check_crc32_value)(m_check_fail_func_t failfunc)
{
	unsigned char* pcurptr;
	int i;
	pchkvalue_t pchk;
	int ret;
	unsigned char fname[sizeof(pchk->m_namexor1)];
	chkvalue_t outval;
	unsigned char ivval[AES_BLOCK_SIZE];
	unsigned char* pkeyptr;
	ret = OB_RANDOM_NAME(check_chkval_value)(failfunc);
	if (ret < 0) {
		return ret;
	}

	aes_memcpy(ivval,&(OB_RANDOM_NAME(func_checks_end)[0]),AES_BLOCK_SIZE);
	pkeyptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_start)[0]);

	for (i=0;;i++){
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(aes_decrypt_block)(pchk,&outval,pkeyptr,ivval);
		if (ret < 0) {
			FAIL_RET(CHECK_VALUE_CHKVAL_AES_FAILED,failfunc);
		}
		pchk = &outval;
		if (pchk->m_size == 0) {
			break;
		}
		pcurptr = OB_RANDOM_NAME(get_func_address)((unsigned char*)OB_RANDOM_NAME(check_value_func));
		pcurptr += pchk->m_offset;
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, (unsigned int)(pchk->m_size), OB_RANDOM_NAME(crc32_calc),pchk->m_crc32val,CRC32_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			FAIL_RET(CHECK_VALUE_CRC32_FAILED,fname);
		}
	}
	return 0;
}

int OB_RANDOM_NAME(check_md5_value)(m_check_fail_func_t failfunc)
{
	unsigned char* pcurptr;
	int i;
	pchkvalue_t pchk;
	int ret;
	unsigned char fname[sizeof(pchk->m_namexor1)];
	chkvalue_t outval;
	unsigned char ivval[AES_BLOCK_SIZE];
	unsigned char* pkeyptr;
	ret = OB_RANDOM_NAME(check_chkval_value)(failfunc);
	if (ret < 0) {
		return ret;
	}

	aes_memcpy(ivval,&(OB_RANDOM_NAME(func_checks_end)[0]),AES_BLOCK_SIZE);
	pkeyptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_start)[0]);

	for (i=0;;i++){
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(aes_decrypt_block)(pchk,&outval,pkeyptr,ivval);
		if (ret < 0) {
			FAIL_RET(CHECK_VALUE_CHKVAL_AES_FAILED,failfunc);
		}
		pchk = &outval;
		if (pchk->m_size == 0) {
			break;
		}
		pcurptr = OB_RANDOM_NAME(get_func_address)((unsigned char*)OB_RANDOM_NAME(check_value_func));
		pcurptr += pchk->m_offset;
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, (unsigned int)pchk->m_size, OB_RANDOM_NAME(md5_calc),pchk->m_md5val,MD5_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			FAIL_RET(CHECK_VALUE_MD5_FAILED,fname);
		}
	}
	return 0;
}

int OB_RANDOM_NAME(check_sha256_value)(m_check_fail_func_t failfunc)
{
	unsigned char* pcurptr;
	int i;
	pchkvalue_t pchk;
	int ret;
	unsigned char fname[sizeof(pchk->m_namexor1)];
	chkvalue_t outval;
	unsigned char ivval[AES_BLOCK_SIZE];
	unsigned char* pkeyptr;
	ret = OB_RANDOM_NAME(check_chkval_value)(failfunc);
	if (ret < 0) {
		return ret;
	}

	aes_memcpy(ivval,&(OB_RANDOM_NAME(func_checks_end)[0]),AES_BLOCK_SIZE);
	pkeyptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_start)[0]);

	for (i=0;;i++){
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(aes_decrypt_block)(pchk,&outval,pkeyptr,ivval);
		if (ret < 0) {
			FAIL_RET(CHECK_VALUE_CHKVAL_AES_FAILED,failfunc);
		}
		pchk = &outval;
		if (pchk->m_size == 0) {
			break;
		}
		pcurptr = OB_RANDOM_NAME(get_func_address)((unsigned char*)OB_RANDOM_NAME(check_value_func));
		pcurptr += pchk->m_offset;
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, (unsigned int)pchk->m_size, OB_RANDOM_NAME(sha256_calc),pchk->m_sha256val,SHA256_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			FAIL_RET(CHECK_VALUE_SHA256_FAILED,fname);
		}
	}
	return 0;
}

int OB_RANDOM_NAME(check_sha3_value)(m_check_fail_func_t failfunc)
{
	unsigned char* pcurptr;
	int i;
	pchkvalue_t pchk;
	int ret;
	unsigned char fname[sizeof(pchk->m_namexor1)];
	chkvalue_t outval;
	unsigned char ivval[AES_BLOCK_SIZE];
	unsigned char* pkeyptr;
	ret = OB_RANDOM_NAME(check_chkval_value)(failfunc);
	if (ret < 0) {
		return ret;
	}

	aes_memcpy(ivval,&(OB_RANDOM_NAME(func_checks_end)[0]),AES_BLOCK_SIZE);
	pkeyptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_start)[0]);

	for (i=0;;i++){
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(aes_decrypt_block)(pchk,&outval,pkeyptr,ivval);
		if (ret < 0) {
			FAIL_RET(CHECK_VALUE_CHKVAL_AES_FAILED,failfunc);
		}
		pchk = &outval;
		if (pchk->m_size == 0) {
			break;
		}
		pcurptr = OB_RANDOM_NAME(get_func_address)((unsigned char*)OB_RANDOM_NAME(check_value_func));
		pcurptr += pchk->m_offset;
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, (unsigned int)pchk->m_size, OB_RANDOM_NAME(sha3_calc),pchk->m_sha3val,SHA3_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			FAIL_RET(CHECK_VALUE_SHA3_FAILED,fname);
		}
	}
	return 0;
}

#ifdef __cplusplus
extern "C" {
#endif


/* we put here to declare  is just to including the last function in the text sections it will be  not compiled optimization in windows cl.exe*/
int OB_RANDOM_NAME(check_end_func)(m_check_fail_func_t failfunc);

#ifdef __cplusplus
};
#endif

int OB_RANDOM_NAME(check_chkval_value)(m_check_fail_func_t failfunc)
{
	unsigned char *pcurptr,*pendptr;
	unsigned int size;
	unsigned char crcval[4];
	int ret;
	int i;
	pchkvalue_t pchkval;
	pcurptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_start)[0]);
	pendptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_end)[0]);
	size = (unsigned int)(pendptr - pcurptr);
	pchkval = &(OB_RANDOM_NAME(value_checks)[0]);
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(crc32_calc),pchkval->m_crc32val,CRC32_VALUE_SIZE);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_CRC32_FAILED," ");
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(md5_calc),pchkval->m_md5val,MD5_VALUE_SIZE);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_MD5_FAILED," ");
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(sha256_calc),pchkval->m_sha256val,SHA256_VALUE_SIZE);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_SHA256_FAILED," ");
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(sha3_calc),pchkval->m_sha3val,SHA3_VALUE_SIZE);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_SHA3_FAILED," ");
	}
	/*now check for the value*/
	pcurptr = OB_RANDOM_NAME(get_func_address)((unsigned char*) OB_RANDOM_NAME(crc32_calc));
	pendptr = OB_RANDOM_NAME(get_func_address)((unsigned char*) OB_RANDOM_NAME(check_end_func));
	size = (unsigned int)(pendptr - pcurptr);
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(sha3_calc), pchkval->m_namexor1,SHA3_VALUE_SIZE);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_FUNCS_FAILED," ");
	}

	pcurptr = OB_RANDOM_NAME(func_checks_start);
	pendptr = OB_RANDOM_NAME(value_checks_total_end);
	size = (unsigned int)(pendptr - pcurptr);
	ret = OB_RANDOM_NAME(crc_sum)(pcurptr,size,crcval,4);
	if (ret < 0) {
		FAIL_RET(CHECK_VALUE_CHKVAL_DATAS_FAILED," ");
	}
	for (i=0;i<4;i++) {
		if (crcval[i] != 0) {
			FAIL_RET(CHECK_VALUE_CHKVAL_DATAS_FAILED," ");
		}
	}
	return 0;
}

int OB_RANDOM_NAME(check_end_func)(m_check_fail_func_t failfunc)
{	
	int ret =0;
	OB_EXPAND_CODE(ret);
	return ret;
}