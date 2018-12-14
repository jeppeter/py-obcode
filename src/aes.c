
// The following lookup tables and functions are for internal use only!
unsigned char OB_RANDOM_NAME(AES_Sbox)[] = {
  99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,
  118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,
  147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,
  7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,
  47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,
  251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,
  188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,
  100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,
  50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,
  78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,
  116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,
  158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,
  137,13,191,230,66,104,65,153,45,15,176,84,187,22
};
 
unsigned char OB_RANDOM_NAME(AES_ShiftRowTab)[] = {0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11};
 
unsigned char OB_RANDOM_NAME(AES_Sbox_Inv)[256];
unsigned char OB_RANDOM_NAME(AES_ShiftRowTab_Inv)[16];
unsigned char  OB_RANDOM_NAME(AES_xtime)[256];
 
void OB_RANDOM_NAME(AES_SubBYTE)(unsigned char state[], unsigned char sbox[]) {
  int i;
  for(i = 0; i < 16; i++)
    state[i] = sbox[state[i]];
}
 
void OB_RANDOM_NAME(AES_AddRoundKey)(unsigned char state[], unsigned char rkey[]) {
  int i;
  for(i = 0; i < 16; i++)
    state[i] ^= rkey[i];
}
 
void OB_RANDOM_NAME(AES_ShiftRows)(unsigned char state[], unsigned char shifttab[]) {
  unsigned char h[16];
  memcpy(h, state, 16);
  int i;
  for(i = 0; i < 16; i++)
    state[i] = h[shifttab[i]];
}
 
void OB_RANDOM_NAME(AES_MixColumns)(unsigned char state[]) {
  int i;
  for(i = 0; i < 16; i += 4) {
    unsigned char s0 = state[i + 0], s1 = state[i + 1];
    unsigned char s2 = state[i + 2], s3 = state[i + 3];
    unsigned char h = (unsigned char)(s0 ^ s1 ^ s2 ^ s3);
    state[i + 0] ^= h ^ OB_RANDOM_NAME(AES_xtime)[s0 ^ s1];
    state[i + 1] ^= h ^ OB_RANDOM_NAME(AES_xtime)[s1 ^ s2];
    state[i + 2] ^= h ^ OB_RANDOM_NAME(AES_xtime)[s2 ^ s3];
    state[i + 3] ^= h ^ OB_RANDOM_NAME(AES_xtime)[s3 ^ s0];
  }
}
 
void OB_RANDOM_NAME(AES_MixColumns_Inv)(unsigned char state[]) {
  int i;
  for(i = 0; i < 16; i += 4) {
    unsigned char s0 = state[i + 0], s1 = state[i + 1];
    unsigned char s2 = state[i + 2], s3 = state[i + 3];
    unsigned char h = (unsigned char)(s0 ^ s1 ^ s2 ^ s3);
    unsigned char xh = OB_RANDOM_NAME(AES_xtime)[h];
    unsigned char h1 = (unsigned char)(OB_RANDOM_NAME(AES_xtime)[OB_RANDOM_NAME(AES_xtime)[xh ^ s0 ^ s2]] ^ h);
    unsigned char h2 = (unsigned char)(OB_RANDOM_NAME(AES_xtime)[OB_RANDOM_NAME(AES_xtime)[xh ^ s1 ^ s3]] ^ h);
    state[i + 0] ^= h1 ^ OB_RANDOM_NAME(AES_xtime)[s0 ^ s1];
    state[i + 1] ^= h2 ^ OB_RANDOM_NAME(AES_xtime)[s1 ^ s2];
    state[i + 2] ^= h1 ^ OB_RANDOM_NAME(AES_xtime)[s2 ^ s3];
    state[i + 3] ^= h2 ^ OB_RANDOM_NAME(AES_xtime)[s3 ^ s0];
  }
}
 
// AES_Init: initialize the tables needed at runtime. 
// Call this function before the (first) key expansion.
void OB_RANDOM_NAME(AES_Init)() {
  int i;
  for(i = 0; i < 256; i++){
    OB_RANDOM_NAME(AES_Sbox_Inv)[OB_RANDOM_NAME(AES_Sbox)[i]] = (unsigned char)(i);
  }
   
  for(i = 0; i < 16; i++){
    OB_RANDOM_NAME(AES_ShiftRowTab_Inv)[OB_RANDOM_NAME(AES_ShiftRowTab)[i]] = (unsigned char)(i);
  }
 
  for(i = 0; i < 128; i++) {
    OB_RANDOM_NAME(AES_xtime)[i] = (unsigned char)(i << 1);
    OB_RANDOM_NAME(AES_xtime)[128 + i] = (unsigned char)((i << 1) ^ 0x1b);
  }
}

#define aes_memcpy(pdst, psrc, size)                                                              \
do{                                                                                               \
    unsigned char* __dst=(unsigned char*) (pdst);                                                 \
    unsigned char* __src=(unsigned char*) (psrc);                                                 \
    int __size=(int)(size);                                                                       \
    int __i;                                                                                      \
    for (__i=0;__i<__size;__i++) {                                                                \
        __dst[__i] = __src[__i];                                                                  \
    }                                                                                             \
}while(0)
 
// AES_Done: release memory reserved by AES_Init. 
// Call this function after the last encryption/decryption operation.
void OB_RANDOM_NAME(AES_Done)() {}
 
/* AES_ExpandKey: expand a cipher key. Depending on the desired encryption 
   strength of 128, 192 or 256 bits 'key' has to be a unsigned char array of length 
   16, 24 or 32, respectively. The key expansion is done "in place", meaning 
   that the array 'key' is modified.
*/  
int OB_RANDOM_NAME(AES_ExpandKey)(unsigned char key[], int keyLen) {
  int kl = keyLen, ks, Rcon = 1, i, j;
  unsigned char temp[4], temp2[4];
  switch (kl) {
    case 16: ks = 16 * (10 + 1); break;
    case 24: ks = 16 * (12 + 1); break;
    case 32: ks = 16 * (14 + 1); break;
    default:
    	return -1;
  }
  for(i = kl; i < ks; i += 4) {
    aes_memcpy(temp, &key[i-4], 4);
    if (i % kl == 0) {
      temp2[0] =(unsigned char) (OB_RANDOM_NAME(AES_Sbox)[temp[1]] ^ Rcon);
      temp2[1] = OB_RANDOM_NAME(AES_Sbox)[temp[2]];
      temp2[2] = OB_RANDOM_NAME(AES_Sbox)[temp[3]];
      temp2[3] = OB_RANDOM_NAME(AES_Sbox)[temp[0]];
      aes_memcpy(temp, temp2, 4);
      if ((Rcon <<= 1) >= 256)
        Rcon ^= 0x11b;
    }
    else if ((kl > 24) && (i % kl == 16)) {
      temp2[0] = OB_RANDOM_NAME(AES_Sbox)[temp[0]];
      temp2[1] = OB_RANDOM_NAME(AES_Sbox)[temp[1]];
      temp2[2] = OB_RANDOM_NAME(AES_Sbox)[temp[2]];
      temp2[3] = OB_RANDOM_NAME(AES_Sbox)[temp[3]];
      aes_memcpy(temp, temp2, 4);
    }
    for(j = 0; j < 4; j++)
      key[i + j] = (unsigned char)(key[i + j - kl] ^ temp[j]);
  }
  return ks;
}
 
// AES_Encrypt: encrypt the 16 unsigned char array 'block' with the previously expanded key 'key'.
void OB_RANDOM_NAME(AES_Encrypt)(unsigned char block[], unsigned char key[], int keyLen) {
  int l = keyLen, i;
  OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[0]);
  for(i = 16; i < l - 16; i += 16) {
    OB_RANDOM_NAME(AES_SubBYTE)(block, OB_RANDOM_NAME(AES_Sbox));
    OB_RANDOM_NAME(AES_ShiftRows)(block, OB_RANDOM_NAME(AES_ShiftRowTab));
    OB_RANDOM_NAME(AES_MixColumns)(block);
    OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[i]);
  }
  OB_RANDOM_NAME(AES_SubBYTE)(block, OB_RANDOM_NAME(AES_Sbox));
  OB_RANDOM_NAME(AES_ShiftRows)(block, OB_RANDOM_NAME(AES_ShiftRowTab));
  OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[i]);
}
 
// AES_Decrypt: decrypt the 16 unsigned char array 'block' with the previously expanded key 'key'.
void OB_RANDOM_NAME(AES_Decrypt)(unsigned char block[], unsigned char key[], int keyLen) {
  int l = keyLen, i;
  OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[l - 16]);
  OB_RANDOM_NAME(AES_ShiftRows)(block, OB_RANDOM_NAME(AES_ShiftRowTab_Inv));
  OB_RANDOM_NAME(AES_SubBYTE)(block, OB_RANDOM_NAME(AES_Sbox_Inv));
  for(i = l - 32; i >= 16; i -= 16) {
    OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[i]);
    OB_RANDOM_NAME(AES_MixColumns_Inv)(block);
    OB_RANDOM_NAME(AES_ShiftRows)(block, OB_RANDOM_NAME(AES_ShiftRowTab_Inv));
    OB_RANDOM_NAME(AES_SubBYTE)(block, OB_RANDOM_NAME(AES_Sbox_Inv));
  }
  OB_RANDOM_NAME(AES_AddRoundKey)(block, &key[0]);
}
