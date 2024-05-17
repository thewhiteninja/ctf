#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>
#include <math.h>

double count[256];
double size = 0;

double computeEntropy(double size){
    double ent = 0;
    long i;
    for(i=0; i<256; i++){
        if (count[i]){
            count[i] /= size;
            ent -= (count[i]*(log10l(count[i]) / log10l(256)));
        }
    }
    return ent;
}

int main(int argc, char** argv){
    FILE* inf = NULL;
    char* inb = NULL;
    char* in = NULL;
    long bsize = 0;
    long i, currentPos=0, limit=0;

    for(i=1;i<argc;i++){
        if(strstr(argv[i], "bsize=")==argv[i]) sscanf(argv[i], "bsize=%ld", &bsize);
        else in = argv[i];
    }
    
    if (in){
        inf = fopen(argv[1], "rb");
        if (!inf){
            inb = _strdup(argv[1]);
            size = strlen(inb);
            inf = NULL;
        }else{
            fseek(inf, 0, SEEK_END);
            size = ftell(inf);
            fseek(inf, 0, SEEK_SET);
        }
        if (!bsize) bsize = (long)floor(size);

        while(currentPos < size){

            memset(count, 0, 256*sizeof(double));

            if (!inf){
                for(i=currentPos; i<currentPos+bsize; i++){
                    count[inb[i]]++;           
                }
                currentPos += bsize;
            }else {
                limit += bsize;
                while (!feof(inf) && currentPos<limit){
                    i = fgetc(inf);
                    count[i]++;
                    currentPos++;
                }                
            }

            printf("%f", computeEntropy(bsize));
            if (currentPos < size) printf("\n");

        }
    }else    
        printf("%f", 0);

    return 0;
}