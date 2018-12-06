int crc32_calc(unsigned char *message,unsigned int size, unsigned char* pval, int valsize)
{
    unsigned int i;
    int j;
    unsigned int byte, crc, mask;

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
        for (i=0;i<4;i++) {
            pval[i] = ((crc >> (i * 8)) & 0xff);
        }
    }
    return 4;
}
