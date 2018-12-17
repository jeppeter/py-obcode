/*********************************************************************
* Filename:   aes.c
* Author:     Brad Conte (brad AT bradconte.com)
* Copyright:
* Disclaimer: This code is presented "as is" without any guarantees.
* Details:    This code is the implementation of the AES algorithm and
              the CTR, CBC, and CCM modes of operation it can be used in.
               AES is, specified by the NIST in in publication FIPS PUB 197,
              availible at:
               * http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf .
              The CBC and CTR modes of operation are specified by
              NIST SP 800-38 A, available at:
               * http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf .
              The CCM mode of operation is specified by NIST SP80-38 C, available at:
               * http://csrc.nist.gov/publications/nistpubs/800-38C/SP800-38C_updated-July20_2007.pdf
*********************************************************************/

/****************************** MACROS ******************************/
// The least significant unsigned char of the unsigned int is rotated to the end.
#define KE_ROTWORD(x) (((x) << 8) | ((x) >> 24))

#define TRUE  1
#define FALSE 0

/**************************** DATA TYPES ****************************/
#define AES_128_ROUNDS 10
#define AES_192_ROUNDS 12
#define AES_256_ROUNDS 14
#define AES_BLOCK_SIZE 16

/**************************** VARIABLES *****************************/
// This is the specified AES SBox. To look up a substitution value, put the first
// nibble in the first index (row) and the second nibble in the second index (column).
static const unsigned char OB_RANDOM_NAME(aes_sbox)[16][16] = {
	{0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76},
	{0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0},
	{0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15},
	{0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75},
	{0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84},
	{0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF},
	{0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8},
	{0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2},
	{0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73},
	{0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB},
	{0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79},
	{0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08},
	{0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A},
	{0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E},
	{0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF},
	{0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16}
};

static const unsigned char OB_RANDOM_NAME(aes_invsbox)[16][16] = {
	{0x52,0x09,0x6A,0xD5,0x30,0x36,0xA5,0x38,0xBF,0x40,0xA3,0x9E,0x81,0xF3,0xD7,0xFB},
	{0x7C,0xE3,0x39,0x82,0x9B,0x2F,0xFF,0x87,0x34,0x8E,0x43,0x44,0xC4,0xDE,0xE9,0xCB},
	{0x54,0x7B,0x94,0x32,0xA6,0xC2,0x23,0x3D,0xEE,0x4C,0x95,0x0B,0x42,0xFA,0xC3,0x4E},
	{0x08,0x2E,0xA1,0x66,0x28,0xD9,0x24,0xB2,0x76,0x5B,0xA2,0x49,0x6D,0x8B,0xD1,0x25},
	{0x72,0xF8,0xF6,0x64,0x86,0x68,0x98,0x16,0xD4,0xA4,0x5C,0xCC,0x5D,0x65,0xB6,0x92},
	{0x6C,0x70,0x48,0x50,0xFD,0xED,0xB9,0xDA,0x5E,0x15,0x46,0x57,0xA7,0x8D,0x9D,0x84},
	{0x90,0xD8,0xAB,0x00,0x8C,0xBC,0xD3,0x0A,0xF7,0xE4,0x58,0x05,0xB8,0xB3,0x45,0x06},
	{0xD0,0x2C,0x1E,0x8F,0xCA,0x3F,0x0F,0x02,0xC1,0xAF,0xBD,0x03,0x01,0x13,0x8A,0x6B},
	{0x3A,0x91,0x11,0x41,0x4F,0x67,0xDC,0xEA,0x97,0xF2,0xCF,0xCE,0xF0,0xB4,0xE6,0x73},
	{0x96,0xAC,0x74,0x22,0xE7,0xAD,0x35,0x85,0xE2,0xF9,0x37,0xE8,0x1C,0x75,0xDF,0x6E},
	{0x47,0xF1,0x1A,0x71,0x1D,0x29,0xC5,0x89,0x6F,0xB7,0x62,0x0E,0xAA,0x18,0xBE,0x1B},
	{0xFC,0x56,0x3E,0x4B,0xC6,0xD2,0x79,0x20,0x9A,0xDB,0xC0,0xFE,0x78,0xCD,0x5A,0xF4},
	{0x1F,0xDD,0xA8,0x33,0x88,0x07,0xC7,0x31,0xB1,0x12,0x10,0x59,0x27,0x80,0xEC,0x5F},
	{0x60,0x51,0x7F,0xA9,0x19,0xB5,0x4A,0x0D,0x2D,0xE5,0x7A,0x9F,0x93,0xC9,0x9C,0xEF},
	{0xA0,0xE0,0x3B,0x4D,0xAE,0x2A,0xF5,0xB0,0xC8,0xEB,0xBB,0x3C,0x83,0x53,0x99,0x61},
	{0x17,0x2B,0x04,0x7E,0xBA,0x77,0xD6,0x26,0xE1,0x69,0x14,0x63,0x55,0x21,0x0C,0x7D}
};

// This table stores pre-calculated values for all possible GF(2^8) calculations.This
// table is only used by the (Inv)MixColumns steps.
// USAGE: The second index (column) is the coefficient of multiplication. Only 7 different
// coefficients are used: 0x01, 0x02, 0x03, 0x09, 0x0b, 0x0d, 0x0e, but multiplication by
// 1 is negligible leaving only 6 coefficients. Each column of the table is devoted to one
// of these coefficients, in the ascending order of value, from values 0x00 to 0xFF.
static const unsigned char OB_RANDOM_NAME(gf_mul)[256][6] = {
	{0x00,0x00,0x00,0x00,0x00,0x00},{0x02,0x03,0x09,0x0b,0x0d,0x0e},
	{0x04,0x06,0x12,0x16,0x1a,0x1c},{0x06,0x05,0x1b,0x1d,0x17,0x12},
	{0x08,0x0c,0x24,0x2c,0x34,0x38},{0x0a,0x0f,0x2d,0x27,0x39,0x36},
	{0x0c,0x0a,0x36,0x3a,0x2e,0x24},{0x0e,0x09,0x3f,0x31,0x23,0x2a},
	{0x10,0x18,0x48,0x58,0x68,0x70},{0x12,0x1b,0x41,0x53,0x65,0x7e},
	{0x14,0x1e,0x5a,0x4e,0x72,0x6c},{0x16,0x1d,0x53,0x45,0x7f,0x62},
	{0x18,0x14,0x6c,0x74,0x5c,0x48},{0x1a,0x17,0x65,0x7f,0x51,0x46},
	{0x1c,0x12,0x7e,0x62,0x46,0x54},{0x1e,0x11,0x77,0x69,0x4b,0x5a},
	{0x20,0x30,0x90,0xb0,0xd0,0xe0},{0x22,0x33,0x99,0xbb,0xdd,0xee},
	{0x24,0x36,0x82,0xa6,0xca,0xfc},{0x26,0x35,0x8b,0xad,0xc7,0xf2},
	{0x28,0x3c,0xb4,0x9c,0xe4,0xd8},{0x2a,0x3f,0xbd,0x97,0xe9,0xd6},
	{0x2c,0x3a,0xa6,0x8a,0xfe,0xc4},{0x2e,0x39,0xaf,0x81,0xf3,0xca},
	{0x30,0x28,0xd8,0xe8,0xb8,0x90},{0x32,0x2b,0xd1,0xe3,0xb5,0x9e},
	{0x34,0x2e,0xca,0xfe,0xa2,0x8c},{0x36,0x2d,0xc3,0xf5,0xaf,0x82},
	{0x38,0x24,0xfc,0xc4,0x8c,0xa8},{0x3a,0x27,0xf5,0xcf,0x81,0xa6},
	{0x3c,0x22,0xee,0xd2,0x96,0xb4},{0x3e,0x21,0xe7,0xd9,0x9b,0xba},
	{0x40,0x60,0x3b,0x7b,0xbb,0xdb},{0x42,0x63,0x32,0x70,0xb6,0xd5},
	{0x44,0x66,0x29,0x6d,0xa1,0xc7},{0x46,0x65,0x20,0x66,0xac,0xc9},
	{0x48,0x6c,0x1f,0x57,0x8f,0xe3},{0x4a,0x6f,0x16,0x5c,0x82,0xed},
	{0x4c,0x6a,0x0d,0x41,0x95,0xff},{0x4e,0x69,0x04,0x4a,0x98,0xf1},
	{0x50,0x78,0x73,0x23,0xd3,0xab},{0x52,0x7b,0x7a,0x28,0xde,0xa5},
	{0x54,0x7e,0x61,0x35,0xc9,0xb7},{0x56,0x7d,0x68,0x3e,0xc4,0xb9},
	{0x58,0x74,0x57,0x0f,0xe7,0x93},{0x5a,0x77,0x5e,0x04,0xea,0x9d},
	{0x5c,0x72,0x45,0x19,0xfd,0x8f},{0x5e,0x71,0x4c,0x12,0xf0,0x81},
	{0x60,0x50,0xab,0xcb,0x6b,0x3b},{0x62,0x53,0xa2,0xc0,0x66,0x35},
	{0x64,0x56,0xb9,0xdd,0x71,0x27},{0x66,0x55,0xb0,0xd6,0x7c,0x29},
	{0x68,0x5c,0x8f,0xe7,0x5f,0x03},{0x6a,0x5f,0x86,0xec,0x52,0x0d},
	{0x6c,0x5a,0x9d,0xf1,0x45,0x1f},{0x6e,0x59,0x94,0xfa,0x48,0x11},
	{0x70,0x48,0xe3,0x93,0x03,0x4b},{0x72,0x4b,0xea,0x98,0x0e,0x45},
	{0x74,0x4e,0xf1,0x85,0x19,0x57},{0x76,0x4d,0xf8,0x8e,0x14,0x59},
	{0x78,0x44,0xc7,0xbf,0x37,0x73},{0x7a,0x47,0xce,0xb4,0x3a,0x7d},
	{0x7c,0x42,0xd5,0xa9,0x2d,0x6f},{0x7e,0x41,0xdc,0xa2,0x20,0x61},
	{0x80,0xc0,0x76,0xf6,0x6d,0xad},{0x82,0xc3,0x7f,0xfd,0x60,0xa3},
	{0x84,0xc6,0x64,0xe0,0x77,0xb1},{0x86,0xc5,0x6d,0xeb,0x7a,0xbf},
	{0x88,0xcc,0x52,0xda,0x59,0x95},{0x8a,0xcf,0x5b,0xd1,0x54,0x9b},
	{0x8c,0xca,0x40,0xcc,0x43,0x89},{0x8e,0xc9,0x49,0xc7,0x4e,0x87},
	{0x90,0xd8,0x3e,0xae,0x05,0xdd},{0x92,0xdb,0x37,0xa5,0x08,0xd3},
	{0x94,0xde,0x2c,0xb8,0x1f,0xc1},{0x96,0xdd,0x25,0xb3,0x12,0xcf},
	{0x98,0xd4,0x1a,0x82,0x31,0xe5},{0x9a,0xd7,0x13,0x89,0x3c,0xeb},
	{0x9c,0xd2,0x08,0x94,0x2b,0xf9},{0x9e,0xd1,0x01,0x9f,0x26,0xf7},
	{0xa0,0xf0,0xe6,0x46,0xbd,0x4d},{0xa2,0xf3,0xef,0x4d,0xb0,0x43},
	{0xa4,0xf6,0xf4,0x50,0xa7,0x51},{0xa6,0xf5,0xfd,0x5b,0xaa,0x5f},
	{0xa8,0xfc,0xc2,0x6a,0x89,0x75},{0xaa,0xff,0xcb,0x61,0x84,0x7b},
	{0xac,0xfa,0xd0,0x7c,0x93,0x69},{0xae,0xf9,0xd9,0x77,0x9e,0x67},
	{0xb0,0xe8,0xae,0x1e,0xd5,0x3d},{0xb2,0xeb,0xa7,0x15,0xd8,0x33},
	{0xb4,0xee,0xbc,0x08,0xcf,0x21},{0xb6,0xed,0xb5,0x03,0xc2,0x2f},
	{0xb8,0xe4,0x8a,0x32,0xe1,0x05},{0xba,0xe7,0x83,0x39,0xec,0x0b},
	{0xbc,0xe2,0x98,0x24,0xfb,0x19},{0xbe,0xe1,0x91,0x2f,0xf6,0x17},
	{0xc0,0xa0,0x4d,0x8d,0xd6,0x76},{0xc2,0xa3,0x44,0x86,0xdb,0x78},
	{0xc4,0xa6,0x5f,0x9b,0xcc,0x6a},{0xc6,0xa5,0x56,0x90,0xc1,0x64},
	{0xc8,0xac,0x69,0xa1,0xe2,0x4e},{0xca,0xaf,0x60,0xaa,0xef,0x40},
	{0xcc,0xaa,0x7b,0xb7,0xf8,0x52},{0xce,0xa9,0x72,0xbc,0xf5,0x5c},
	{0xd0,0xb8,0x05,0xd5,0xbe,0x06},{0xd2,0xbb,0x0c,0xde,0xb3,0x08},
	{0xd4,0xbe,0x17,0xc3,0xa4,0x1a},{0xd6,0xbd,0x1e,0xc8,0xa9,0x14},
	{0xd8,0xb4,0x21,0xf9,0x8a,0x3e},{0xda,0xb7,0x28,0xf2,0x87,0x30},
	{0xdc,0xb2,0x33,0xef,0x90,0x22},{0xde,0xb1,0x3a,0xe4,0x9d,0x2c},
	{0xe0,0x90,0xdd,0x3d,0x06,0x96},{0xe2,0x93,0xd4,0x36,0x0b,0x98},
	{0xe4,0x96,0xcf,0x2b,0x1c,0x8a},{0xe6,0x95,0xc6,0x20,0x11,0x84},
	{0xe8,0x9c,0xf9,0x11,0x32,0xae},{0xea,0x9f,0xf0,0x1a,0x3f,0xa0},
	{0xec,0x9a,0xeb,0x07,0x28,0xb2},{0xee,0x99,0xe2,0x0c,0x25,0xbc},
	{0xf0,0x88,0x95,0x65,0x6e,0xe6},{0xf2,0x8b,0x9c,0x6e,0x63,0xe8},
	{0xf4,0x8e,0x87,0x73,0x74,0xfa},{0xf6,0x8d,0x8e,0x78,0x79,0xf4},
	{0xf8,0x84,0xb1,0x49,0x5a,0xde},{0xfa,0x87,0xb8,0x42,0x57,0xd0},
	{0xfc,0x82,0xa3,0x5f,0x40,0xc2},{0xfe,0x81,0xaa,0x54,0x4d,0xcc},
	{0x1b,0x9b,0xec,0xf7,0xda,0x41},{0x19,0x98,0xe5,0xfc,0xd7,0x4f},
	{0x1f,0x9d,0xfe,0xe1,0xc0,0x5d},{0x1d,0x9e,0xf7,0xea,0xcd,0x53},
	{0x13,0x97,0xc8,0xdb,0xee,0x79},{0x11,0x94,0xc1,0xd0,0xe3,0x77},
	{0x17,0x91,0xda,0xcd,0xf4,0x65},{0x15,0x92,0xd3,0xc6,0xf9,0x6b},
	{0x0b,0x83,0xa4,0xaf,0xb2,0x31},{0x09,0x80,0xad,0xa4,0xbf,0x3f},
	{0x0f,0x85,0xb6,0xb9,0xa8,0x2d},{0x0d,0x86,0xbf,0xb2,0xa5,0x23},
	{0x03,0x8f,0x80,0x83,0x86,0x09},{0x01,0x8c,0x89,0x88,0x8b,0x07},
	{0x07,0x89,0x92,0x95,0x9c,0x15},{0x05,0x8a,0x9b,0x9e,0x91,0x1b},
	{0x3b,0xab,0x7c,0x47,0x0a,0xa1},{0x39,0xa8,0x75,0x4c,0x07,0xaf},
	{0x3f,0xad,0x6e,0x51,0x10,0xbd},{0x3d,0xae,0x67,0x5a,0x1d,0xb3},
	{0x33,0xa7,0x58,0x6b,0x3e,0x99},{0x31,0xa4,0x51,0x60,0x33,0x97},
	{0x37,0xa1,0x4a,0x7d,0x24,0x85},{0x35,0xa2,0x43,0x76,0x29,0x8b},
	{0x2b,0xb3,0x34,0x1f,0x62,0xd1},{0x29,0xb0,0x3d,0x14,0x6f,0xdf},
	{0x2f,0xb5,0x26,0x09,0x78,0xcd},{0x2d,0xb6,0x2f,0x02,0x75,0xc3},
	{0x23,0xbf,0x10,0x33,0x56,0xe9},{0x21,0xbc,0x19,0x38,0x5b,0xe7},
	{0x27,0xb9,0x02,0x25,0x4c,0xf5},{0x25,0xba,0x0b,0x2e,0x41,0xfb},
	{0x5b,0xfb,0xd7,0x8c,0x61,0x9a},{0x59,0xf8,0xde,0x87,0x6c,0x94},
	{0x5f,0xfd,0xc5,0x9a,0x7b,0x86},{0x5d,0xfe,0xcc,0x91,0x76,0x88},
	{0x53,0xf7,0xf3,0xa0,0x55,0xa2},{0x51,0xf4,0xfa,0xab,0x58,0xac},
	{0x57,0xf1,0xe1,0xb6,0x4f,0xbe},{0x55,0xf2,0xe8,0xbd,0x42,0xb0},
	{0x4b,0xe3,0x9f,0xd4,0x09,0xea},{0x49,0xe0,0x96,0xdf,0x04,0xe4},
	{0x4f,0xe5,0x8d,0xc2,0x13,0xf6},{0x4d,0xe6,0x84,0xc9,0x1e,0xf8},
	{0x43,0xef,0xbb,0xf8,0x3d,0xd2},{0x41,0xec,0xb2,0xf3,0x30,0xdc},
	{0x47,0xe9,0xa9,0xee,0x27,0xce},{0x45,0xea,0xa0,0xe5,0x2a,0xc0},
	{0x7b,0xcb,0x47,0x3c,0xb1,0x7a},{0x79,0xc8,0x4e,0x37,0xbc,0x74},
	{0x7f,0xcd,0x55,0x2a,0xab,0x66},{0x7d,0xce,0x5c,0x21,0xa6,0x68},
	{0x73,0xc7,0x63,0x10,0x85,0x42},{0x71,0xc4,0x6a,0x1b,0x88,0x4c},
	{0x77,0xc1,0x71,0x06,0x9f,0x5e},{0x75,0xc2,0x78,0x0d,0x92,0x50},
	{0x6b,0xd3,0x0f,0x64,0xd9,0x0a},{0x69,0xd0,0x06,0x6f,0xd4,0x04},
	{0x6f,0xd5,0x1d,0x72,0xc3,0x16},{0x6d,0xd6,0x14,0x79,0xce,0x18},
	{0x63,0xdf,0x2b,0x48,0xed,0x32},{0x61,0xdc,0x22,0x43,0xe0,0x3c},
	{0x67,0xd9,0x39,0x5e,0xf7,0x2e},{0x65,0xda,0x30,0x55,0xfa,0x20},
	{0x9b,0x5b,0x9a,0x01,0xb7,0xec},{0x99,0x58,0x93,0x0a,0xba,0xe2},
	{0x9f,0x5d,0x88,0x17,0xad,0xf0},{0x9d,0x5e,0x81,0x1c,0xa0,0xfe},
	{0x93,0x57,0xbe,0x2d,0x83,0xd4},{0x91,0x54,0xb7,0x26,0x8e,0xda},
	{0x97,0x51,0xac,0x3b,0x99,0xc8},{0x95,0x52,0xa5,0x30,0x94,0xc6},
	{0x8b,0x43,0xd2,0x59,0xdf,0x9c},{0x89,0x40,0xdb,0x52,0xd2,0x92},
	{0x8f,0x45,0xc0,0x4f,0xc5,0x80},{0x8d,0x46,0xc9,0x44,0xc8,0x8e},
	{0x83,0x4f,0xf6,0x75,0xeb,0xa4},{0x81,0x4c,0xff,0x7e,0xe6,0xaa},
	{0x87,0x49,0xe4,0x63,0xf1,0xb8},{0x85,0x4a,0xed,0x68,0xfc,0xb6},
	{0xbb,0x6b,0x0a,0xb1,0x67,0x0c},{0xb9,0x68,0x03,0xba,0x6a,0x02},
	{0xbf,0x6d,0x18,0xa7,0x7d,0x10},{0xbd,0x6e,0x11,0xac,0x70,0x1e},
	{0xb3,0x67,0x2e,0x9d,0x53,0x34},{0xb1,0x64,0x27,0x96,0x5e,0x3a},
	{0xb7,0x61,0x3c,0x8b,0x49,0x28},{0xb5,0x62,0x35,0x80,0x44,0x26},
	{0xab,0x73,0x42,0xe9,0x0f,0x7c},{0xa9,0x70,0x4b,0xe2,0x02,0x72},
	{0xaf,0x75,0x50,0xff,0x15,0x60},{0xad,0x76,0x59,0xf4,0x18,0x6e},
	{0xa3,0x7f,0x66,0xc5,0x3b,0x44},{0xa1,0x7c,0x6f,0xce,0x36,0x4a},
	{0xa7,0x79,0x74,0xd3,0x21,0x58},{0xa5,0x7a,0x7d,0xd8,0x2c,0x56},
	{0xdb,0x3b,0xa1,0x7a,0x0c,0x37},{0xd9,0x38,0xa8,0x71,0x01,0x39},
	{0xdf,0x3d,0xb3,0x6c,0x16,0x2b},{0xdd,0x3e,0xba,0x67,0x1b,0x25},
	{0xd3,0x37,0x85,0x56,0x38,0x0f},{0xd1,0x34,0x8c,0x5d,0x35,0x01},
	{0xd7,0x31,0x97,0x40,0x22,0x13},{0xd5,0x32,0x9e,0x4b,0x2f,0x1d},
	{0xcb,0x23,0xe9,0x22,0x64,0x47},{0xc9,0x20,0xe0,0x29,0x69,0x49},
	{0xcf,0x25,0xfb,0x34,0x7e,0x5b},{0xcd,0x26,0xf2,0x3f,0x73,0x55},
	{0xc3,0x2f,0xcd,0x0e,0x50,0x7f},{0xc1,0x2c,0xc4,0x05,0x5d,0x71},
	{0xc7,0x29,0xdf,0x18,0x4a,0x63},{0xc5,0x2a,0xd6,0x13,0x47,0x6d},
	{0xfb,0x0b,0x31,0xca,0xdc,0xd7},{0xf9,0x08,0x38,0xc1,0xd1,0xd9},
	{0xff,0x0d,0x23,0xdc,0xc6,0xcb},{0xfd,0x0e,0x2a,0xd7,0xcb,0xc5},
	{0xf3,0x07,0x15,0xe6,0xe8,0xef},{0xf1,0x04,0x1c,0xed,0xe5,0xe1},
	{0xf7,0x01,0x07,0xf0,0xf2,0xf3},{0xf5,0x02,0x0e,0xfb,0xff,0xfd},
	{0xeb,0x13,0x79,0x92,0xb4,0xa7},{0xe9,0x10,0x70,0x99,0xb9,0xa9},
	{0xef,0x15,0x6b,0x84,0xae,0xbb},{0xed,0x16,0x62,0x8f,0xa3,0xb5},
	{0xe3,0x1f,0x5d,0xbe,0x80,0x9f},{0xe1,0x1c,0x54,0xb5,0x8d,0x91},
	{0xe7,0x19,0x4f,0xa8,0x9a,0x83},{0xe5,0x1a,0x46,0xa3,0x97,0x8d}
};

void OB_RANDOM_NAME(aes_encrypt)(const unsigned char in[], unsigned char out[], const unsigned int key[], int keysize);
void OB_RANDOM_NAME(aes_decrypt)(const unsigned char in[], unsigned char out[], const unsigned int key[], int keysize);

/*********************** FUNCTION DEFINITIONS ***********************/
// XORs the in and out buffers, storing the result in out. Length is in bytes.
void OB_RANDOM_NAME(xor_buf)(const unsigned char in[], unsigned char out[], size_t len)
{
	size_t idx;

	for (idx = 0; idx < len; idx++)
		out[idx] ^= in[idx];
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

/*******************
* AES - CBC
*******************/
int OB_RANDOM_NAME(aes_encrypt_cbc)(const unsigned char in[], size_t in_len, unsigned char out[], const unsigned int key[], int keysize, const unsigned char iv[])
{
	unsigned char buf_in[AES_BLOCK_SIZE], buf_out[AES_BLOCK_SIZE], iv_buf[AES_BLOCK_SIZE];
	int blocks, idx;

	if (in_len % AES_BLOCK_SIZE != 0)
		return(FALSE);

	blocks = (int)(in_len / AES_BLOCK_SIZE);

	aes_memcpy(iv_buf, iv, AES_BLOCK_SIZE);

	for (idx = 0; idx < blocks; idx++) {
		aes_memcpy(buf_in, &in[idx * AES_BLOCK_SIZE], AES_BLOCK_SIZE);
		OB_RANDOM_NAME(xor_buf)(iv_buf, buf_in, AES_BLOCK_SIZE);
		OB_RANDOM_NAME(aes_encrypt)(buf_in, buf_out, key, keysize);
		aes_memcpy(&out[idx * AES_BLOCK_SIZE], buf_out, AES_BLOCK_SIZE);
		aes_memcpy(iv_buf, buf_out, AES_BLOCK_SIZE);
	}

	return(TRUE);
}

int OB_RANDOM_NAME(aes_encrypt_cbc_mac)(const unsigned char in[], size_t in_len, unsigned char out[], const unsigned int key[], int keysize, const unsigned char iv[])
{
	unsigned char buf_in[AES_BLOCK_SIZE], buf_out[AES_BLOCK_SIZE], iv_buf[AES_BLOCK_SIZE];
	int blocks, idx;

	if (in_len % AES_BLOCK_SIZE != 0)
		return(FALSE);

	blocks = (int)(in_len / AES_BLOCK_SIZE);

	aes_memcpy(iv_buf, iv, AES_BLOCK_SIZE);

	for (idx = 0; idx < blocks; idx++) {
		aes_memcpy(buf_in, &in[idx * AES_BLOCK_SIZE], AES_BLOCK_SIZE);
		OB_RANDOM_NAME(xor_buf)(iv_buf, buf_in, AES_BLOCK_SIZE);
		OB_RANDOM_NAME(aes_encrypt)(buf_in, buf_out, key, keysize);
		aes_memcpy(iv_buf, buf_out, AES_BLOCK_SIZE);
		// Do not output all encrypted blocks.
	}

	aes_memcpy(out, buf_out, AES_BLOCK_SIZE);   // Only output the last block.

	return(TRUE);
}

int OB_RANDOM_NAME(aes_decrypt_cbc)(const unsigned char in[], size_t in_len, unsigned char out[], const unsigned int key[], int keysize, const unsigned char iv[])
{
	unsigned char buf_in[AES_BLOCK_SIZE], buf_out[AES_BLOCK_SIZE], iv_buf[AES_BLOCK_SIZE];
	int blocks, idx;

	if (in_len % AES_BLOCK_SIZE != 0)
		return(FALSE);

	blocks = (int)(in_len / AES_BLOCK_SIZE);

	aes_memcpy(iv_buf, iv, AES_BLOCK_SIZE);

	for (idx = 0; idx < blocks; idx++) {
		aes_memcpy(buf_in, &in[idx * AES_BLOCK_SIZE], AES_BLOCK_SIZE);
		OB_RANDOM_NAME(aes_decrypt)(buf_in, buf_out, key, keysize);
		OB_RANDOM_NAME(xor_buf)(iv_buf, buf_out, AES_BLOCK_SIZE);
		aes_memcpy(&out[idx * AES_BLOCK_SIZE], buf_out, AES_BLOCK_SIZE);
		aes_memcpy(iv_buf, buf_in, AES_BLOCK_SIZE);
	}

	return(TRUE);
}


/*******************
* AES
*******************/
/////////////////
// KEY EXPANSION
/////////////////

// Substitutes a unsigned int using the AES S-Box.
unsigned int OB_RANDOM_NAME(SubWord)(unsigned int word)
{
	unsigned int result;

	result = (unsigned int)((int)OB_RANDOM_NAME(aes_sbox)[(word >> 4) & 0x0000000F][word & 0x0000000F]);
	result += (int)OB_RANDOM_NAME(aes_sbox)[(word >> 12) & 0x0000000F][(word >> 8) & 0x0000000F] << 8;
	result += (int)OB_RANDOM_NAME(aes_sbox)[(word >> 20) & 0x0000000F][(word >> 16) & 0x0000000F] << 16;
	result += (int)OB_RANDOM_NAME(aes_sbox)[(word >> 28) & 0x0000000F][(word >> 24) & 0x0000000F] << 24;
	return(result);
}

// Performs the action of generating the keys that will be used in every round of
// encryption. "key" is the user-supplied input key, "w" is the output key schedule,
// "keysize" is the length in bits of "key", must be 128, 192, or 256.
void OB_RANDOM_NAME(aes_key_setup)(const unsigned char key[], unsigned int w[], int keysize)
{
	int Nb=4,Nr,Nk,idx;
	unsigned int temp,Rcon[]={0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,
	                  0x40000000,0x80000000,0x1b000000,0x36000000,0x6c000000,0xd8000000,
	                  0xab000000,0x4d000000,0x9a000000};

	switch (keysize) {
		case 128: Nr = 10; Nk = 4; break;
		case 192: Nr = 12; Nk = 6; break;
		case 256: Nr = 14; Nk = 8; break;
		default: return;
	}

	for (idx=0; idx < Nk; ++idx) {
		w[idx] = (unsigned int)(((key[4 * idx]) << 24) | ((key[4 * idx + 1]) << 16) |
				   ((key[4 * idx + 2]) << 8) | ((key[4 * idx + 3])));
	}

	for (idx = Nk; idx < Nb * (Nr+1); ++idx) {
		temp = w[idx - 1];
		if ((idx % Nk) == 0)
			temp = OB_RANDOM_NAME(SubWord)(KE_ROTWORD(temp)) ^ Rcon[(idx-1)/Nk];
		else if (Nk > 6 && (idx % Nk) == 4)
			temp = OB_RANDOM_NAME(SubWord)(temp);
		w[idx] = w[idx-Nk] ^ temp;
	}
}

/////////////////
// ADD ROUND KEY
/////////////////

// Performs the AddRoundKey step. Each round has its own pre-generated 16-byte key in the
// form of 4 integers (the "w" array). Each integer is XOR'd by one column of the state.
// Also performs the job of InvOB_RANDOM_NAME(AddRoundKey)(); since the function is a simple XOR process,
// it is its own inverse.
void OB_RANDOM_NAME(AddRoundKey)(unsigned char state[][4], const unsigned int w[])
{
	unsigned char subkey[4];

	// memcpy(subkey,&w[idx],4); // Not accurate for big endian machines
	// Subkey 1
	subkey[0] = w[0] >> 24;
	subkey[1] = (unsigned char)(w[0] >> 16);
	subkey[2] = (unsigned char)(w[0] >> 8);
	subkey[3] = (unsigned char)w[0];
	state[0][0] ^= subkey[0];
	state[1][0] ^= subkey[1];
	state[2][0] ^= subkey[2];
	state[3][0] ^= subkey[3];
	// Subkey 2
	subkey[0] = w[1] >> 24;
	subkey[1] = (unsigned char)(w[1] >> 16);
	subkey[2] = (unsigned char)(w[1] >> 8);
	subkey[3] = (unsigned char)w[1];
	state[0][1] ^= subkey[0];
	state[1][1] ^= subkey[1];
	state[2][1] ^= subkey[2];
	state[3][1] ^= subkey[3];
	// Subkey 3
	subkey[0] = w[2] >> 24;
	subkey[1] = (unsigned char)(w[2] >> 16);
	subkey[2] = (unsigned char)(w[2] >> 8);
	subkey[3] = (unsigned char)w[2];
	state[0][2] ^= subkey[0];
	state[1][2] ^= subkey[1];
	state[2][2] ^= subkey[2];
	state[3][2] ^= subkey[3];
	// Subkey 4
	subkey[0] = w[3] >> 24;
	subkey[1] = (unsigned char)(w[3] >> 16);
	subkey[2] = (unsigned char)(w[3] >> 8);
	subkey[3] = (unsigned char)w[3];
	state[0][3] ^= subkey[0];
	state[1][3] ^= subkey[1];
	state[2][3] ^= subkey[2];
	state[3][3] ^= subkey[3];
}

/////////////////
// (Inv)SubBytes
/////////////////

// Performs the SubBytes step. All bytes in the state are substituted with a
// pre-calculated value from a lookup table.
void OB_RANDOM_NAME(SubBytes)(unsigned char state[][4])
{
	state[0][0] = OB_RANDOM_NAME(aes_sbox)[state[0][0] >> 4][state[0][0] & 0x0F];
	state[0][1] = OB_RANDOM_NAME(aes_sbox)[state[0][1] >> 4][state[0][1] & 0x0F];
	state[0][2] = OB_RANDOM_NAME(aes_sbox)[state[0][2] >> 4][state[0][2] & 0x0F];
	state[0][3] = OB_RANDOM_NAME(aes_sbox)[state[0][3] >> 4][state[0][3] & 0x0F];
	state[1][0] = OB_RANDOM_NAME(aes_sbox)[state[1][0] >> 4][state[1][0] & 0x0F];
	state[1][1] = OB_RANDOM_NAME(aes_sbox)[state[1][1] >> 4][state[1][1] & 0x0F];
	state[1][2] = OB_RANDOM_NAME(aes_sbox)[state[1][2] >> 4][state[1][2] & 0x0F];
	state[1][3] = OB_RANDOM_NAME(aes_sbox)[state[1][3] >> 4][state[1][3] & 0x0F];
	state[2][0] = OB_RANDOM_NAME(aes_sbox)[state[2][0] >> 4][state[2][0] & 0x0F];
	state[2][1] = OB_RANDOM_NAME(aes_sbox)[state[2][1] >> 4][state[2][1] & 0x0F];
	state[2][2] = OB_RANDOM_NAME(aes_sbox)[state[2][2] >> 4][state[2][2] & 0x0F];
	state[2][3] = OB_RANDOM_NAME(aes_sbox)[state[2][3] >> 4][state[2][3] & 0x0F];
	state[3][0] = OB_RANDOM_NAME(aes_sbox)[state[3][0] >> 4][state[3][0] & 0x0F];
	state[3][1] = OB_RANDOM_NAME(aes_sbox)[state[3][1] >> 4][state[3][1] & 0x0F];
	state[3][2] = OB_RANDOM_NAME(aes_sbox)[state[3][2] >> 4][state[3][2] & 0x0F];
	state[3][3] = OB_RANDOM_NAME(aes_sbox)[state[3][3] >> 4][state[3][3] & 0x0F];
}

void OB_RANDOM_NAME(InvSubBytes)(unsigned char state[][4])
{
	state[0][0] = OB_RANDOM_NAME(aes_invsbox)[state[0][0] >> 4][state[0][0] & 0x0F];
	state[0][1] = OB_RANDOM_NAME(aes_invsbox)[state[0][1] >> 4][state[0][1] & 0x0F];
	state[0][2] = OB_RANDOM_NAME(aes_invsbox)[state[0][2] >> 4][state[0][2] & 0x0F];
	state[0][3] = OB_RANDOM_NAME(aes_invsbox)[state[0][3] >> 4][state[0][3] & 0x0F];
	state[1][0] = OB_RANDOM_NAME(aes_invsbox)[state[1][0] >> 4][state[1][0] & 0x0F];
	state[1][1] = OB_RANDOM_NAME(aes_invsbox)[state[1][1] >> 4][state[1][1] & 0x0F];
	state[1][2] = OB_RANDOM_NAME(aes_invsbox)[state[1][2] >> 4][state[1][2] & 0x0F];
	state[1][3] = OB_RANDOM_NAME(aes_invsbox)[state[1][3] >> 4][state[1][3] & 0x0F];
	state[2][0] = OB_RANDOM_NAME(aes_invsbox)[state[2][0] >> 4][state[2][0] & 0x0F];
	state[2][1] = OB_RANDOM_NAME(aes_invsbox)[state[2][1] >> 4][state[2][1] & 0x0F];
	state[2][2] = OB_RANDOM_NAME(aes_invsbox)[state[2][2] >> 4][state[2][2] & 0x0F];
	state[2][3] = OB_RANDOM_NAME(aes_invsbox)[state[2][3] >> 4][state[2][3] & 0x0F];
	state[3][0] = OB_RANDOM_NAME(aes_invsbox)[state[3][0] >> 4][state[3][0] & 0x0F];
	state[3][1] = OB_RANDOM_NAME(aes_invsbox)[state[3][1] >> 4][state[3][1] & 0x0F];
	state[3][2] = OB_RANDOM_NAME(aes_invsbox)[state[3][2] >> 4][state[3][2] & 0x0F];
	state[3][3] = OB_RANDOM_NAME(aes_invsbox)[state[3][3] >> 4][state[3][3] & 0x0F];
}

/////////////////
// (Inv)ShiftRows
/////////////////

// Performs the ShiftRows step. All rows are shifted cylindrically to the left.
void OB_RANDOM_NAME(ShiftRows)(unsigned char state[][4])
{
	int t;

	// Shift left by 1
	t = state[1][0];
	state[1][0] = state[1][1];
	state[1][1] = state[1][2];
	state[1][2] = state[1][3];
	state[1][3] = (unsigned char)t;
	// Shift left by 2
	t = state[2][0];
	state[2][0] = state[2][2];
	state[2][2] = (unsigned char)t;
	t = state[2][1];
	state[2][1] = state[2][3];
	state[2][3] = (unsigned char)t;
	// Shift left by 3
	t = state[3][0];
	state[3][0] = state[3][3];
	state[3][3] = state[3][2];
	state[3][2] = state[3][1];
	state[3][1] = (unsigned char)t;
}

// All rows are shifted cylindrically to the right.
void OB_RANDOM_NAME(InvShiftRows)(unsigned char state[][4])
{
	int t;

	// Shift right by 1
	t = state[1][3];
	state[1][3] = state[1][2];
	state[1][2] = state[1][1];
	state[1][1] = state[1][0];
	state[1][0] = (unsigned char)t;
	// Shift right by 2
	t = state[2][3];
	state[2][3] = state[2][1];
	state[2][1] = (unsigned char)t;
	t = state[2][2];
	state[2][2] = state[2][0];
	state[2][0] = (unsigned char)t;
	// Shift right by 3
	t = state[3][3];
	state[3][3] = state[3][0];
	state[3][0] = state[3][1];
	state[3][1] = state[3][2];
	state[3][2] = (unsigned char)t;
}

/////////////////
// (Inv)MixColumns
/////////////////

// Performs the MixColums step. The state is multiplied by itself using matrix
// multiplication in a Galios Field 2^8. All multiplication is pre-computed in a table.
// Addition is equivilent to XOR. (Must always make a copy of the column as the original
// values will be destoyed.)
void OB_RANDOM_NAME(MixColumns)(unsigned char state[][4])
{
	unsigned char col[4];

	// Column 1
	col[0] = state[0][0];
	col[1] = state[1][0];
	col[2] = state[2][0];
	col[3] = state[3][0];
	state[0][0] = OB_RANDOM_NAME(gf_mul)[col[0]][0];
	state[0][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][1];
	state[0][0] ^= col[2];
	state[0][0] ^= col[3];
	state[1][0] = col[0];
	state[1][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][0];
	state[1][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][1];
	state[1][0] ^= col[3];
	state[2][0] = col[0];
	state[2][0] ^= col[1];
	state[2][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][0];
	state[2][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][1];
	state[3][0] = OB_RANDOM_NAME(gf_mul)[col[0]][1];
	state[3][0] ^= col[1];
	state[3][0] ^= col[2];
	state[3][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][0];
	// Column 2
	col[0] = state[0][1];
	col[1] = state[1][1];
	col[2] = state[2][1];
	col[3] = state[3][1];
	state[0][1] = OB_RANDOM_NAME(gf_mul)[col[0]][0];
	state[0][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][1];
	state[0][1] ^= col[2];
	state[0][1] ^= col[3];
	state[1][1] = col[0];
	state[1][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][0];
	state[1][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][1];
	state[1][1] ^= col[3];
	state[2][1] = col[0];
	state[2][1] ^= col[1];
	state[2][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][0];
	state[2][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][1];
	state[3][1] = OB_RANDOM_NAME(gf_mul)[col[0]][1];
	state[3][1] ^= col[1];
	state[3][1] ^= col[2];
	state[3][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][0];
	// Column 3
	col[0] = state[0][2];
	col[1] = state[1][2];
	col[2] = state[2][2];
	col[3] = state[3][2];
	state[0][2] = OB_RANDOM_NAME(gf_mul)[col[0]][0];
	state[0][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][1];
	state[0][2] ^= col[2];
	state[0][2] ^= col[3];
	state[1][2] = col[0];
	state[1][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][0];
	state[1][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][1];
	state[1][2] ^= col[3];
	state[2][2] = col[0];
	state[2][2] ^= col[1];
	state[2][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][0];
	state[2][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][1];
	state[3][2] = OB_RANDOM_NAME(gf_mul)[col[0]][1];
	state[3][2] ^= col[1];
	state[3][2] ^= col[2];
	state[3][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][0];
	// Column 4
	col[0] = state[0][3];
	col[1] = state[1][3];
	col[2] = state[2][3];
	col[3] = state[3][3];
	state[0][3] = OB_RANDOM_NAME(gf_mul)[col[0]][0];
	state[0][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][1];
	state[0][3] ^= col[2];
	state[0][3] ^= col[3];
	state[1][3] = col[0];
	state[1][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][0];
	state[1][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][1];
	state[1][3] ^= col[3];
	state[2][3] = col[0];
	state[2][3] ^= col[1];
	state[2][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][0];
	state[2][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][1];
	state[3][3] = OB_RANDOM_NAME(gf_mul)[col[0]][1];
	state[3][3] ^= col[1];
	state[3][3] ^= col[2];
	state[3][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][0];
}

void OB_RANDOM_NAME(InvMixColumns)(unsigned char state[][4])
{
	unsigned char col[4];

	// Column 1
	col[0] = state[0][0];
	col[1] = state[1][0];
	col[2] = state[2][0];
	col[3] = state[3][0];
	state[0][0] = OB_RANDOM_NAME(gf_mul)[col[0]][5];
	state[0][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][3];
	state[0][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][4];
	state[0][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][2];
	state[1][0] = OB_RANDOM_NAME(gf_mul)[col[0]][2];
	state[1][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][5];
	state[1][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][3];
	state[1][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][4];
	state[2][0] = OB_RANDOM_NAME(gf_mul)[col[0]][4];
	state[2][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][2];
	state[2][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][5];
	state[2][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][3];
	state[3][0] = OB_RANDOM_NAME(gf_mul)[col[0]][3];
	state[3][0] ^= OB_RANDOM_NAME(gf_mul)[col[1]][4];
	state[3][0] ^= OB_RANDOM_NAME(gf_mul)[col[2]][2];
	state[3][0] ^= OB_RANDOM_NAME(gf_mul)[col[3]][5];
	// Column 2
	col[0] = state[0][1];
	col[1] = state[1][1];
	col[2] = state[2][1];
	col[3] = state[3][1];
	state[0][1] = OB_RANDOM_NAME(gf_mul)[col[0]][5];
	state[0][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][3];
	state[0][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][4];
	state[0][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][2];
	state[1][1] = OB_RANDOM_NAME(gf_mul)[col[0]][2];
	state[1][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][5];
	state[1][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][3];
	state[1][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][4];
	state[2][1] = OB_RANDOM_NAME(gf_mul)[col[0]][4];
	state[2][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][2];
	state[2][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][5];
	state[2][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][3];
	state[3][1] = OB_RANDOM_NAME(gf_mul)[col[0]][3];
	state[3][1] ^= OB_RANDOM_NAME(gf_mul)[col[1]][4];
	state[3][1] ^= OB_RANDOM_NAME(gf_mul)[col[2]][2];
	state[3][1] ^= OB_RANDOM_NAME(gf_mul)[col[3]][5];
	// Column 3
	col[0] = state[0][2];
	col[1] = state[1][2];
	col[2] = state[2][2];
	col[3] = state[3][2];
	state[0][2] = OB_RANDOM_NAME(gf_mul)[col[0]][5];
	state[0][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][3];
	state[0][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][4];
	state[0][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][2];
	state[1][2] = OB_RANDOM_NAME(gf_mul)[col[0]][2];
	state[1][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][5];
	state[1][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][3];
	state[1][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][4];
	state[2][2] = OB_RANDOM_NAME(gf_mul)[col[0]][4];
	state[2][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][2];
	state[2][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][5];
	state[2][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][3];
	state[3][2] = OB_RANDOM_NAME(gf_mul)[col[0]][3];
	state[3][2] ^= OB_RANDOM_NAME(gf_mul)[col[1]][4];
	state[3][2] ^= OB_RANDOM_NAME(gf_mul)[col[2]][2];
	state[3][2] ^= OB_RANDOM_NAME(gf_mul)[col[3]][5];
	// Column 4
	col[0] = state[0][3];
	col[1] = state[1][3];
	col[2] = state[2][3];
	col[3] = state[3][3];
	state[0][3] = OB_RANDOM_NAME(gf_mul)[col[0]][5];
	state[0][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][3];
	state[0][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][4];
	state[0][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][2];
	state[1][3] = OB_RANDOM_NAME(gf_mul)[col[0]][2];
	state[1][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][5];
	state[1][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][3];
	state[1][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][4];
	state[2][3] = OB_RANDOM_NAME(gf_mul)[col[0]][4];
	state[2][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][2];
	state[2][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][5];
	state[2][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][3];
	state[3][3] = OB_RANDOM_NAME(gf_mul)[col[0]][3];
	state[3][3] ^= OB_RANDOM_NAME(gf_mul)[col[1]][4];
	state[3][3] ^= OB_RANDOM_NAME(gf_mul)[col[2]][2];
	state[3][3] ^= OB_RANDOM_NAME(gf_mul)[col[3]][5];
}

/////////////////
// (En/De)Crypt
/////////////////

void OB_RANDOM_NAME(aes_encrypt)(const unsigned char in[], unsigned char out[], const unsigned int key[], int keysize)
{
	unsigned char state[4][4];

	// Copy input array (should be 16 bytes long) to a matrix (sequential bytes are ordered
	// by row, not col) called "state" for processing.
	// *** Implementation note: The official AES documentation references the state by
	// column, then row. Accessing an element in C requires row then column. Thus, all state
	// references in AES must have the column and row indexes reversed for C implementation.
	state[0][0] = in[0];
	state[1][0] = in[1];
	state[2][0] = in[2];
	state[3][0] = in[3];
	state[0][1] = in[4];
	state[1][1] = in[5];
	state[2][1] = in[6];
	state[3][1] = in[7];
	state[0][2] = in[8];
	state[1][2] = in[9];
	state[2][2] = in[10];
	state[3][2] = in[11];
	state[0][3] = in[12];
	state[1][3] = in[13];
	state[2][3] = in[14];
	state[3][3] = in[15];

	// Perform the necessary number of rounds. The round key is added first.
	// The last round does not perform the MixColumns step.
	OB_RANDOM_NAME(AddRoundKey)(state,&key[0]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[4]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[8]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[12]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[16]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[20]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[24]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[28]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[32]);
	OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[36]);
	if (keysize != 128) {
		OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[40]);
		OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[44]);
		if (keysize != 192) {
			OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[48]);
			OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(MixColumns)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[52]);
			OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[56]);
		}
		else {
			OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[48]);
		}
	}
	else {
		OB_RANDOM_NAME(SubBytes)(state); OB_RANDOM_NAME(ShiftRows)(state); OB_RANDOM_NAME(AddRoundKey)(state,&key[40]);
	}

	// Copy the state to the output array.
	out[0] = state[0][0];
	out[1] = state[1][0];
	out[2] = state[2][0];
	out[3] = state[3][0];
	out[4] = state[0][1];
	out[5] = state[1][1];
	out[6] = state[2][1];
	out[7] = state[3][1];
	out[8] = state[0][2];
	out[9] = state[1][2];
	out[10] = state[2][2];
	out[11] = state[3][2];
	out[12] = state[0][3];
	out[13] = state[1][3];
	out[14] = state[2][3];
	out[15] = state[3][3];
}

void OB_RANDOM_NAME(aes_decrypt)(const unsigned char in[], unsigned char out[], const unsigned int key[], int keysize)
{
	unsigned char state[4][4];

	// Copy the input to the state.
	state[0][0] = in[0];
	state[1][0] = in[1];
	state[2][0] = in[2];
	state[3][0] = in[3];
	state[0][1] = in[4];
	state[1][1] = in[5];
	state[2][1] = in[6];
	state[3][1] = in[7];
	state[0][2] = in[8];
	state[1][2] = in[9];
	state[2][2] = in[10];
	state[3][2] = in[11];
	state[0][3] = in[12];
	state[1][3] = in[13];
	state[2][3] = in[14];
	state[3][3] = in[15];

	// Perform the necessary number of rounds. The round key is added first.
	// The last round does not perform the MixColumns step.
	if (keysize > 128) {
		if (keysize > 192) {
			OB_RANDOM_NAME(AddRoundKey)(state,&key[56]);
			OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[52]);OB_RANDOM_NAME(InvMixColumns)(state);
			OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[48]);OB_RANDOM_NAME(InvMixColumns)(state);
		}
		else {
			OB_RANDOM_NAME(AddRoundKey)(state,&key[48]);
		}
		OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[44]);OB_RANDOM_NAME(InvMixColumns)(state);
		OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[40]);OB_RANDOM_NAME(InvMixColumns)(state);
	}
	else {
		OB_RANDOM_NAME(AddRoundKey)(state,&key[40]);
	}
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[36]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[32]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[28]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[24]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[20]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[16]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[12]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[8]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[4]);OB_RANDOM_NAME(InvMixColumns)(state);
	OB_RANDOM_NAME(InvShiftRows)(state);OB_RANDOM_NAME(InvSubBytes)(state);OB_RANDOM_NAME(AddRoundKey)(state,&key[0]);

	// Copy the state to the output array.
	out[0] = state[0][0];
	out[1] = state[1][0];
	out[2] = state[2][0];
	out[3] = state[3][0];
	out[4] = state[0][1];
	out[5] = state[1][1];
	out[6] = state[2][1];
	out[7] = state[3][1];
	out[8] = state[0][2];
	out[9] = state[1][2];
	out[10] = state[2][2];
	out[11] = state[3][2];
	out[12] = state[0][3];
	out[13] = state[1][3];
	out[14] = state[2][3];
	out[15] = state[3][3];
}
