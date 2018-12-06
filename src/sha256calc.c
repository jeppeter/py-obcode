
#define SHA256_BLOCK_SIZE 32            // SHA256 outputs a 32 unsigned char digest


typedef struct {
	unsigned char data[64];
	unsigned int datalen;
	unsigned long long bitlen;
	unsigned int state[8];
} sha256_ctx;

/*********************** FUNCTION DECLARATIONS **********************/
void OB_RANDOM_NAME(sha256_init)(sha256_ctx *ctx);
void OB_RANDOM_NAME(sha256_update)(sha256_ctx *ctx, const unsigned char data[], unsigned int len);
void OB_RANDOM_NAME(sha256_final)(sha256_ctx *ctx, unsigned char hash[]);




/****************************** MACROS ******************************/
#define SHA256_ROTLEFT(a,b) (((a) << (b)) | ((a) >> (32-(b))))
#define SHA256_ROTRIGHT(a,b) (((a) >> (b)) | ((a) << (32-(b))))

#define SHA256_CH(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define SHA256_MAJ(x,y,z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define SHA256_EP0(x) (SHA256_ROTRIGHT(x,2) ^ SHA256_ROTRIGHT(x,13) ^ SHA256_ROTRIGHT(x,22))
#define SHA256_EP1(x) (SHA256_ROTRIGHT(x,6) ^ SHA256_ROTRIGHT(x,11) ^ SHA256_ROTRIGHT(x,25))
#define SHA256_SIG0(x) (SHA256_ROTRIGHT(x,7) ^ SHA256_ROTRIGHT(x,18) ^ ((x) >> 3))
#define SHA256_SIG1(x) (SHA256_ROTRIGHT(x,17) ^ SHA256_ROTRIGHT(x,19) ^ ((x) >> 10))

/**************************** VARIABLES *****************************/
static const unsigned int OB_RANDOM_NAME(sha256_k)[64] = {
	0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
	0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
	0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
	0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
	0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
	0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
	0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
	0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
};

/*********************** FUNCTION DEFINITIONS ***********************/
void OB_RANDOM_NAME(sha256_transform)(sha256_ctx *ctx, const unsigned char data[])
{
	unsigned int a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];

	for (i = 0, j = 0; i < 16; ++i, j += 4){
		m[i] = 0;
		m[i] |= ((unsigned int)(data[j] << 24));
		m[i] |= ((unsigned int)(data[j + 1] << 16));
		m[i] |= ((unsigned int)(data[j + 2] << 8));
		m[i] |= ((unsigned int)(data[j + 3]));
	}
	for ( ; i < 64; ++i){		
		m[i] = SHA256_SIG1(m[i - 2]) + m[i - 7] + SHA256_SIG0(m[i - 15]) + m[i - 16];
	}

	a = ctx->state[0];
	b = ctx->state[1];
	c = ctx->state[2];
	d = ctx->state[3];
	e = ctx->state[4];
	f = ctx->state[5];
	g = ctx->state[6];
	h = ctx->state[7];

	for (i = 0; i < 64; ++i) {
		t1 = h + SHA256_EP1(e) + SHA256_CH(e,f,g) + OB_RANDOM_NAME(sha256_k)[i] + m[i];
		t2 = SHA256_EP0(a) + SHA256_MAJ(a,b,c);
		h = g;
		g = f;
		f = e;
		e = d + t1;
		d = c;
		c = b;
		b = a;
		a = t1 + t2;
	}

	ctx->state[0] += a;
	ctx->state[1] += b;
	ctx->state[2] += c;
	ctx->state[3] += d;
	ctx->state[4] += e;
	ctx->state[5] += f;
	ctx->state[6] += g;
	ctx->state[7] += h;
}

void OB_RANDOM_NAME(sha256_init)(sha256_ctx *ctx)
{
	ctx->datalen = 0;
	ctx->bitlen = 0;
	ctx->state[0] = 0x6a09e667;
	ctx->state[1] = 0xbb67ae85;
	ctx->state[2] = 0x3c6ef372;
	ctx->state[3] = 0xa54ff53a;
	ctx->state[4] = 0x510e527f;
	ctx->state[5] = 0x9b05688c;
	ctx->state[6] = 0x1f83d9ab;
	ctx->state[7] = 0x5be0cd19;
}

#define sha256_memset(p,ch,sz)                                                                    \
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

void OB_RANDOM_NAME(sha256_update)(sha256_ctx *ctx, const unsigned char data[], unsigned int len)
{
	unsigned int i;

	for (i = 0; i < len; ++i) {
		ctx->data[ctx->datalen] = data[i];
		ctx->datalen++;
		if (ctx->datalen == 64) {
			OB_RANDOM_NAME(sha256_transform)(ctx, ctx->data);
			ctx->bitlen += 512;
			ctx->datalen = 0;
		}
	}
}

void OB_RANDOM_NAME(sha256_final)(sha256_ctx *ctx, unsigned char hash[])
{
	unsigned int i;

	i = ctx->datalen;

	// Pad whatever data is left in the buffer.
	if (ctx->datalen < 56) {
		ctx->data[i++] = 0x80;
		while (i < 56)
			ctx->data[i++] = 0x00;
	}
	else {
		ctx->data[i++] = 0x80;
		while (i < 64)
			ctx->data[i++] = 0x00;
		OB_RANDOM_NAME(sha256_transform)(ctx, ctx->data);
		sha256_memset(ctx->data, 0, 56);
	}

	// Append to the padding the total message's length in bits and transform.
	ctx->bitlen += ctx->datalen * 8;
	ctx->data[63] = (unsigned char)(ctx->bitlen & 0xff);
	ctx->data[62] = (unsigned char)((ctx->bitlen >> 8) & 0xff);
	ctx->data[61] = (unsigned char)((ctx->bitlen >> 16) & 0xff);
	ctx->data[60] = (unsigned char)((ctx->bitlen >> 24) & 0xff);
	ctx->data[59] = (unsigned char)((ctx->bitlen >> 32) & 0xff);
	ctx->data[58] = (unsigned char)((ctx->bitlen >> 40) & 0xff);
	ctx->data[57] = (unsigned char)((ctx->bitlen >> 48) & 0xff);
	ctx->data[56] = (unsigned char)((ctx->bitlen >> 56) & 0xff);
	OB_RANDOM_NAME(sha256_transform)(ctx, ctx->data);

	// Since this implementation uses little endian byte ordering and SHA uses big endian,
	// reverse all the bytes when copying the final state to the output hash.
	for (i = 0; i < 4; ++i) {
		hash[i]      = (ctx->state[0] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 4]  = (ctx->state[1] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 8]  = (ctx->state[2] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 12] = (ctx->state[3] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 16] = (ctx->state[4] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 20] = (ctx->state[5] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 24] = (ctx->state[6] >> (24 - i * 8)) & 0x000000ff;
		hash[i + 28] = (ctx->state[7] >> (24 - i * 8)) & 0x000000ff;
	}
}

int OB_RANDOM_NAME(sha256_calc)(unsigned char* message, unsigned int len,unsigned char* pval, int valsize)
{
	sha256_ctx ctx;
	if (valsize < 32) {
		return -1;
	}
	OB_RANDOM_NAME(sha256_init)(&ctx);
	OB_RANDOM_NAME(sha256_update)(&ctx,message,len);
	OB_RANDOM_NAME(sha256_final)(&ctx,pval);
	return 32;
}