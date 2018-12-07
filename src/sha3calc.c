

/* 'Words' here refers to unsigned long long */
#define SHA3_KECCAK_SPONGE_WORDS \
	(((1600)/8/*bits to byte*/)/sizeof(unsigned long long))
typedef struct sha3_context_ {
    unsigned long long saved;   /* the portion of the input message that we
                                 * didn't consume yet */
    union {                     /* Keccak's state */
        unsigned long long s[SHA3_KECCAK_SPONGE_WORDS];
        unsigned char sb[SHA3_KECCAK_SPONGE_WORDS * 8];
    };
    unsigned byteIndex;         /* 0..7--the next byte after the set one
                                 * (starts from 0; 0--none are buffered) */
    unsigned wordIndex;         /* 0..24--the next word to integrate input
                                 * (starts from 0) */
    unsigned capacityWords;     /* the double size of the hash output in
                                 * words (e.g. 16 for Keccak 512) */
} sha3_context;


/* For Init or Reset call these: */
void OB_RANDOM_NAME(sha3_init512)(void *priv);
void OB_RANDOM_NAME(sha3_update)(void *priv, void const *bufIn, unsigned int len);
void OB_RANDOM_NAME(sha3_final)(void *priv, unsigned char* pval);





/* 
 * Define SHA3_USE_KECCAK to run "pure" Keccak, as opposed to SHA3.
 * The tests that this macro enables use the input and output from [Keccak]
 * (see the reference below). The used test vectors aren't correct for SHA3, 
 * however, they are helpful to verify the implementation.
 * SHA3_USE_KECCAK only changes one line of code in Finalize.
 */

#if defined(_MSC_VER)
#define SHA3_CONST(x) x
#else
#define SHA3_CONST(x) x##L
#endif

#ifndef SHA3_ROTL64
#define SHA3_ROTL64(x, y) \
    (((x) << (y)) | ((x) >> ((sizeof(unsigned long long)*8) - (y))))
#endif

static const unsigned long long OB_RANDOM_NAME(keccakf_rndc)[24] = {
    SHA3_CONST(0x0000000000000001UL), SHA3_CONST(0x0000000000008082UL),
    SHA3_CONST(0x800000000000808aUL), SHA3_CONST(0x8000000080008000UL),
    SHA3_CONST(0x000000000000808bUL), SHA3_CONST(0x0000000080000001UL),
    SHA3_CONST(0x8000000080008081UL), SHA3_CONST(0x8000000000008009UL),
    SHA3_CONST(0x000000000000008aUL), SHA3_CONST(0x0000000000000088UL),
    SHA3_CONST(0x0000000080008009UL), SHA3_CONST(0x000000008000000aUL),
    SHA3_CONST(0x000000008000808bUL), SHA3_CONST(0x800000000000008bUL),
    SHA3_CONST(0x8000000000008089UL), SHA3_CONST(0x8000000000008003UL),
    SHA3_CONST(0x8000000000008002UL), SHA3_CONST(0x8000000000000080UL),
    SHA3_CONST(0x000000000000800aUL), SHA3_CONST(0x800000008000000aUL),
    SHA3_CONST(0x8000000080008081UL), SHA3_CONST(0x8000000000008080UL),
    SHA3_CONST(0x0000000080000001UL), SHA3_CONST(0x8000000080008008UL)
};

static const unsigned OB_RANDOM_NAME(keccakf_rotc)[24] = {
    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 2, 14, 27, 41, 56, 8, 25, 43, 62,
    18, 39, 61, 20, 44
};

static const unsigned OB_RANDOM_NAME(keccakf_piln)[24] = {
    10, 7, 11, 17, 18, 3, 5, 16, 8, 21, 24, 4, 15, 23, 19, 13, 12, 2, 20,
    14, 22, 9, 6, 1
};

/* generally called after SHA3_KECCAK_SPONGE_WORDS-ctx->capacityWords words 
 * are XORed into the state s 
 */
static void OB_RANDOM_NAME(keccakf)(unsigned long long s[25])
{
    int i, j, round;
    unsigned long long t, bc[5];
#define KECCAK_ROUNDS 24

    for(round = 0; round < KECCAK_ROUNDS; round++) {

        /* Theta */
        for(i = 0; i < 5; i++)
            bc[i] = s[i] ^ s[i + 5] ^ s[i + 10] ^ s[i + 15] ^ s[i + 20];

        for(i = 0; i < 5; i++) {
            t = bc[(i + 4) % 5] ^ SHA3_ROTL64(bc[(i + 1) % 5], 1);
            for(j = 0; j < 25; j += 5)
                s[j + i] ^= t;
        }

        /* Rho Pi */
        t = s[1];
        for(i = 0; i < 24; i++) {
            j = (int)OB_RANDOM_NAME(keccakf_piln)[i];
            bc[0] = s[j];
            s[j] = SHA3_ROTL64(t, keccakf_rotc[i]);
            t = bc[0];
        }

        /* Chi */
        for(j = 0; j < 25; j += 5) {
            for(i = 0; i < 5; i++)
                bc[i] = s[j + i];
            for(i = 0; i < 5; i++)
                s[j + i] ^= (~bc[(i + 1) % 5]) & bc[(i + 2) % 5];
        }

        /* Iota */
        s[0] ^= OB_RANDOM_NAME(keccakf_rndc)[round];
    }
}

/* *************************** Public Inteface ************************ */

#define sha3_memset(p,ch,sz)                                                                      \
do                                                                                                \
{                                                                                                 \
    unsigned char* __p=(unsigned char*)(p);                                                       \
    unsigned char __ch = (unsigned char)(ch);                                                     \
    unsigned int __sz = (unsigned int)(sz);                                                       \
    unsigned int __i;                                                                             \
    for (__i=0;__i < __sz;__i++) {                                                                \
        __p[__i] = __ch;                                                                          \
    }                                                                                             \
}while(0)


#define sha3_memcpy(pdst, psrc, size)                                                             \
do{                                                                                               \
    unsigned char* __dst=(unsigned char*) (pdst);                                                 \
    unsigned char* __src=(unsigned char*) (psrc);                                                 \
    int __size=(int)(size);                                                                       \
    int __i;                                                                                      \
    for (__i=0;__i<__size;__i++) {                                                                \
        __dst[__i] = __src[__i];                                                                  \
    }                                                                                             \
}while(0)



void OB_RANDOM_NAME(sha3_init512)(sha3_context *ctx)
{
    sha3_memset(ctx, 0, sizeof(*ctx));
    ctx->capacityWords = 2 * 512 / (8 * sizeof(unsigned long long));
}

void OB_RANDOM_NAME(sha3_update)(sha3_context *ctx, const unsigned char *buf, unsigned int len)
{
    /* 0...7 -- how much is needed to have a word */
    unsigned old_tail = (8 - ctx->byteIndex) & 7;

    unsigned int words;
    unsigned tail;
    unsigned int i;



    if(len < old_tail) {        /* have no complete word or haven't started 
                                 * the word yet */
        /* endian-independent code follows: */
        while (len--)
            ctx->saved |= (unsigned long long) (*(buf++)) << ((ctx->byteIndex++) * 8);
        return;
    }

    if(old_tail) {              /* will have one word to process */
        /* endian-independent code follows: */
        len -= old_tail;
        while (old_tail--)
            ctx->saved |= (unsigned long long) (*(buf++)) << ((ctx->byteIndex++) * 8);

        /* now ready to add saved to the sponge */
        ctx->s[ctx->wordIndex] ^= ctx->saved;
        ctx->byteIndex = 0;
        ctx->saved = 0;
        if(++ctx->wordIndex ==
                (SHA3_KECCAK_SPONGE_WORDS - ctx->capacityWords)) {
            OB_RANDOM_NAME(keccakf)(ctx->s);
            ctx->wordIndex = 0;
        }
    }

    /* now work in full words directly from input */

    words = len / sizeof(unsigned long long);
    tail = len - words * sizeof(unsigned long long);

    for(i = 0; i < words; i++, buf += sizeof(unsigned long long)) {
        const unsigned long long t = (unsigned long long) (buf[0]) |
                ((unsigned long long) (buf[1]) << 8 * 1) |
                ((unsigned long long) (buf[2]) << 8 * 2) |
                ((unsigned long long) (buf[3]) << 8 * 3) |
                ((unsigned long long) (buf[4]) << 8 * 4) |
                ((unsigned long long) (buf[5]) << 8 * 5) |
                ((unsigned long long) (buf[6]) << 8 * 6) |
                ((unsigned long long) (buf[7]) << 8 * 7);
        ctx->s[ctx->wordIndex] ^= t;
        if(++ctx->wordIndex ==
                (SHA3_KECCAK_SPONGE_WORDS - ctx->capacityWords)) {
            OB_RANDOM_NAME(keccakf)(ctx->s);
            ctx->wordIndex = 0;
        }
    }


    /* finally, save the partial word */
    while (tail--) {
        ctx->saved |= (unsigned long long) (*(buf++)) << ((ctx->byteIndex++) * 8);
    }
}

/* This is simply the 'update' with the padding block.
 * The padding block is 0x01 || 0x00* || 0x80. First 0x01 and last 0x80 
 * bytes are always present, but they can be the same byte.
 */
void OB_RANDOM_NAME(sha3_final)(sha3_context *ctx, unsigned char* pval)
{
    /* Append 2-bit suffix 01, per SHA-3 spec. Instead of 1 for padding we
     * use 1<<2 below. The 0x02 below corresponds to the suffix 01.
     * Overall, we feed 0, then 1, and finally 1 to start padding. Without
     * M || 01, we would simply use 1 to start padding. */

    /* SHA3 version */
    ctx->s[ctx->wordIndex] ^=
            (ctx->saved ^ ((unsigned long long) ((unsigned long long) (0x02 | (1 << 2)) <<
                            ((ctx->byteIndex) * 8))));

    ctx->s[SHA3_KECCAK_SPONGE_WORDS - ctx->capacityWords - 1] ^=
            SHA3_CONST(0x8000000000000000UL);
    OB_RANDOM_NAME(keccakf)(ctx->s);

    /* Return first bytes of the ctx->s. This conversion is not needed for
     * little-endian platforms e.g. wrap with #if !defined(__BYTE_ORDER__)
     * || !defined(__ORDER_LITTLE_ENDIAN__) || __BYTE_ORDER__!=__ORDER_LITTLE_ENDIAN__ 
     *    ... the conversion below ...
     * #endif */
    {
        unsigned i;
        for(i = 0; i < SHA3_KECCAK_SPONGE_WORDS; i++) {
            const unsigned t1 = (uint32_t) ctx->s[i];
            const unsigned t2 = (uint32_t) ((ctx->s[i] >> 16) >> 16);
            ctx->sb[i * 8 + 0] = (unsigned char) (t1);
            ctx->sb[i * 8 + 1] = (unsigned char) (t1 >> 8);
            ctx->sb[i * 8 + 2] = (unsigned char) (t1 >> 16);
            ctx->sb[i * 8 + 3] = (unsigned char) (t1 >> 24);
            ctx->sb[i * 8 + 4] = (unsigned char) (t2);
            ctx->sb[i * 8 + 5] = (unsigned char) (t2 >> 8);
            ctx->sb[i * 8 + 6] = (unsigned char) (t2 >> 16);
            ctx->sb[i * 8 + 7] = (unsigned char) (t2 >> 24);
        }
    }

    sha3_memcpy(pval, ctx->sb, 64);
    return ;
}

int OB_RANDOM_NAME(sha3_calc)(unsigned char* message,unsigned int len, unsigned char* pval,int valsize)
{
    sha3_context ctx;
    if (valsize < 64) {
        return -1;
    }
    OB_RANDOM_NAME(sha3_init512)(&ctx);
    OB_RANDOM_NAME(sha3_update)(&ctx,message,len);
    OB_RANDOM_NAME(sha3_final)(&ctx,pval);
    return 64;
}