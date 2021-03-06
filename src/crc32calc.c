int OB_RANDOM_NAME(crc32_calc)(unsigned char *message, unsigned int size, unsigned char* pval, int valsize)
{
    unsigned int i;
    int j;
    unsigned int byte=0, crc=0, mask=0;

    OB_EXPAND_CODE(byte,crc,mask);
    i = 0;
    crc = 0xFFFFFFFF;
    while (i < size) {
        byte = message[i];            // Get next byte.
        crc = crc ^ byte;
        for (j = 7; j >= 0; j--) {    // Do eight times.
            mask = 0;
            if (crc & 1) {
                mask = 0xffffffff;
            }
            //mask = - (crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
        i = i + 1;
    }
    crc = ~crc;
    if (pval && valsize >= 4) {
        for (i = 0; i < 4; i++) {
            pval[i] = ((crc >> (i * 8)) & 0xff);
        }
    }
    return 4;
}

int OB_RANDOM_NAME(crc_sum)(unsigned char* message, unsigned int size, unsigned char* pval, int valsize)
{
    unsigned int crc = 0;
    unsigned int* pival = (unsigned int*) message;
    unsigned char* pcc;
    unsigned int ival;
    int i,j;
    if (valsize < 4) {
        return -1;
    }
    i = (int)size;
    while (i > 0) {
        ival = *pival;
        if ( i < (int)(sizeof(unsigned int))) {
            ival = 0;
            pcc = (unsigned char*) pival;
            for (j=0;j<i;j++, pcc++) {
                ival += (unsigned int)(((unsigned int)(*pcc))<< (j * 8));
            }
        }
        crc += ival;
        i -= sizeof(unsigned int);
        pival ++;
    }
    for (i = 0; i < 4; i++) {
        pval[i] = (unsigned char)((crc >> (i * 8)) & 0xff);
    }
    return 4;
}
