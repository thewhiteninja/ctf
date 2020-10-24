#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <time.h>
#include "blowfish.h"

typedef struct BRUTE_CTX {
	unsigned int print;
	unsigned char* currString;
	unsigned int* currIdx;
	unsigned int length;
	unsigned int finished;
	unsigned int found;
	unsigned int only;
} brute_ctx, *pBrute_ctx;

////////////////////////////////////////////////////////////////////////////////

char* charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-!$%*+[]()";
pBrute_ctx bctx;
BLOWFISH_CTX ctx;

////////////////////////////////////////////////////////////////////////////////

void swapEndian(unsigned long *i){
	unsigned long o = 0;
	o |= *i >> 24;
	o |= (*i & 0x00ff0000) >> 8;
	o |= (*i & 0x0000ff00) << 8;
	o |= *i << 24;
	*i=o;
}

void updateEndOfString(){
	int o;
	for(o=4; o<16; o++){
		bctx->currString[o] = charset[bctx->currString[o-1]%62];
	}
}

void deblowfish(char* in, char* pass, char* out){
	unsigned long L, R;
	printf("[+] Decrypting image  ... ");
	Blowfish_Init (&ctx, (unsigned char*)(pass), strlen(pass));
    FILE* enc = fopen ("bf-encrypted.jpg", "rb");
    FILE* dec = fopen ("bf-decrypted.jpg", "wb");
	if (enc && dec){
		while (!feof(enc)){
			fread(&L, 1, sizeof(unsigned long), enc);
			fread(&R, 1, sizeof(unsigned long), enc);
			swapEndian(&L); swapEndian(&R);
			Blowfish_Decrypt(&ctx, &L, &R);
			swapEndian(&L); swapEndian(&R);
			fwrite(&L, 1, sizeof(unsigned long), dec);
			fwrite(&R, 1, sizeof(unsigned long), dec);
		}
		fclose(enc);
		fclose(dec);
	}
	printf("ok\n");
}

void usage(char* name){
	printf("Usage : %s [-print] [-only X]\n", name);
	free(bctx);
	exit(0);
}

////////////////////////////////////////////////////////////////////////////////

void bruteInit(int argc, char** args){
	bctx = (brute_ctx*)malloc(sizeof(brute_ctx));
	bctx->length = 4;
	bctx->print = bctx->found = bctx->only = 0;
	int i;
	
	for(i=0; i<argc; i++){
		if (!strcmp(args[i], "-print")){
			bctx->print = 1;
		}
		if (!strcmp(args[i], "-only")){
			bctx->only = atoi(args[++i]);
			bctx->length = 3;
		}
		if (!strcmp(args[i], "-h") || !strcmp(args[i], "-help") || !strcmp(args[i], "/h")){
			usage(args[0]);
		}		
	}	

	printf("[+] Bruteforce init   ... ");
	
	bctx->currString = (char*)malloc(32);
	memset(bctx->currString, 0, 32);
	bctx->currString[3] = charset[bctx->only];
	updateEndOfString();
	bctx->currIdx = (int*)malloc(bctx->length);
	for(i=0; i<bctx->length; i++) {
		bctx->currIdx[i] = 0;
		bctx->currString[i] = charset[0];
	}
	bctx->currIdx[3] = bctx->only;
	bctx->currIdx[0] = -1;
	bctx->finished = 0;
	printf("ok\n");
}

void bruteDeInit(){
	printf("[+] Bruteforce deinit ... ");
	free(bctx->currString);
	free(bctx->currIdx);
	free(bctx);
	printf("ok\n");
}

char* bruteNext(){
	int i = 0;
	bctx->currIdx[i]++;
	bctx->currString[i] = charset[bctx->currIdx[i]];
	while (bctx->currIdx[i] == 62){
		bctx->currIdx[i] = 0;
		bctx->currString[i] = charset[0];
		i++;
		if (i<bctx->length) {
			bctx->currIdx[i]++;
			bctx->currString[i] = charset[bctx->currIdx[i]];
			if (i==3) updateEndOfString();
		}else{			
			bctx->finished = 1;
			break;
		}	
	}
	if (bctx->print) printf("    %s\n", bctx->currString);
	return bctx->currString;
}

int bruteTest(){
	Blowfish_Init (&ctx, (unsigned char*)(bctx->currString), 16);
	unsigned long L = 0x0F92A86D, R = 0x1F15A3C8;
	Blowfish_Decrypt(&ctx, &L, &R);
	return (L == 0xFFD8FFE0);
}

int main(int argc, char** argv) {
	bruteInit(argc, argv);
	
	printf("[+] Bruteforcing key ...\n");
	time_t t1 = time(NULL);
	while(!bctx->finished){
		if (bruteTest(bruteNext())){
				printf("[*] Key found : %s\n", bctx->currString);
				bctx->found = 1;
				break;
		}	
	}
	if (bctx->finished) printf("[*] Key not found, Damn it !\n");
	time_t t2 = time(NULL);
	printf("[-] Elapsed time : %ldmin %02lds\n", (t2-t1)/60, (t2-t1)%60);	
	
	if (bctx->found) deblowfish("bf-encrypted.jpg", bctx->currString, "bf-decrypted.jpg");

	bruteDeInit();
	return 0;
}
