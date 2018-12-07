
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
	int ret;
	unsigned char calcvalue[64];
	int i;

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

int OB_RANDOM_NAME(check_crc32_value)(m_check_fail_func_t failfunc)
{
	unsigned char* pcurptr;
	int i;
	pchkvalue_t pchk;
	int ret;
	unsigned char fname[sizeof(pchk->m_namexor1)];
	for (i=0;OB_RANDOM_NAME(func_ptrs)[i] != NULL;i++) {
		pcurptr = OB_RANDOM_NAME(func_ptrs)[i];
		pcurptr = OB_RANDOM_NAME(get_func_address)(pcurptr);
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, pchk->m_size, OB_RANDOM_NAME(crc32_calc),pchk->m_crc32val,CRC32_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			failfunc(CHECK_VALUE_CRC32_FAILED,(char*)fname);
			return CHECK_VALUE_CRC32_FAILED;
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
	for (i=0;OB_RANDOM_NAME(func_ptrs)[i] != NULL;i++) {
		pcurptr = OB_RANDOM_NAME(func_ptrs)[i];
		pcurptr = OB_RANDOM_NAME(get_func_address)(pcurptr);
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, pchk->m_size, OB_RANDOM_NAME(md5_calc),pchk->m_md5val,MD5_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			failfunc(CHECK_VALUE_MD5_FAILED,(char*)fname);
			return CHECK_VALUE_MD5_FAILED;
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
	for (i=0;OB_RANDOM_NAME(func_ptrs)[i] != NULL;i++) {
		pcurptr = OB_RANDOM_NAME(func_ptrs)[i];
		pcurptr = OB_RANDOM_NAME(get_func_address)(pcurptr);
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, pchk->m_size, OB_RANDOM_NAME(sha256_calc),pchk->m_sha256val,SHA256_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			failfunc(CHECK_VALUE_SHA256_FAILED,(char*)fname);
			return CHECK_VALUE_SHA256_FAILED;
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
	for (i=0;OB_RANDOM_NAME(func_ptrs)[i] != NULL;i++) {
		pcurptr = OB_RANDOM_NAME(func_ptrs)[i];
		pcurptr = OB_RANDOM_NAME(get_func_address)(pcurptr);
		pchk = &(OB_RANDOM_NAME(func_checks)[i]);
		ret = OB_RANDOM_NAME(check_value_func)(pcurptr, pchk->m_size, OB_RANDOM_NAME(sha3_calc),pchk->m_sha3val,SHA3_VALUE_SIZE);
		if (ret < 0) {
			OB_RANDOM_NAME(format_name)(fname,sizeof(pchk->m_namexor1), pchk->m_namexor1,pchk->m_namexor2);
			failfunc(CHECK_VALUE_SHA3_FAILED,(char*)fname);
			return CHECK_VALUE_SHA3_FAILED;
		}
	}
	return 0;
}

int OB_RANDOM_NAME(check_chkval_value)(m_check_fail_func_t failfunc)
{
	unsigned char *pcurptr,*pendptr;
	unsigned int size;
	int ret;
	pchkvalue_t pchkval;
	pcurptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks)[0]);
	pendptr = (unsigned char*)&(OB_RANDOM_NAME(func_checks_end)[0]);
	size = (unsigned int)(pendptr - pcurptr);
	pchkval = &(OB_RANDOM_NAME(value_checks)[0]);
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(crc32_calc),pchkval->m_crc32val,CRC32_VALUE_SIZE);
	if (ret < 0) {
		failfunc(CHECK_VALUE_CHKVAL_FAILED,(char*)"dummy");
		return CHECK_VALUE_CHKVAL_FAILED;
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(md5_calc),pchkval->m_md5val,MD5_VALUE_SIZE);
	if (ret < 0) {
		failfunc(CHECK_VALUE_CHKVAL_FAILED,(char*)"dummy");
		return CHECK_VALUE_CHKVAL_FAILED;
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(sha256_calc),pchkval->m_sha256val,SHA256_VALUE_SIZE);
	if (ret < 0) {
		failfunc(CHECK_VALUE_CHKVAL_FAILED,(char*)"dummy");
		return CHECK_VALUE_CHKVAL_FAILED;
	}
	ret = OB_RANDOM_NAME(check_value_func)(pcurptr, size,OB_RANDOM_NAME(sha3_calc),pchkval->m_sha3val,SHA3_VALUE_SIZE);
	if (ret < 0) {
		failfunc(CHECK_VALUE_CHKVAL_FAILED,(char*)"dummy");
		return CHECK_VALUE_CHKVAL_FAILED;
	}
	return 0;
}