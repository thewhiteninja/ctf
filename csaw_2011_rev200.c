#include <stdio.h>

int ROUND = 64;
unsigned int KEY[] = {1929540644U, 2488374377U, 339237175U, 54625381U};

void usage(){
	printf("Usage : decrypt file");
	exit(0);
}

/*
    private static uunsigned int[] ProcessBlock(uunsigned int num_rounds, uunsigned int[] v, uunsigned int[] key)
    {
      if (key.Length != 4)
        throw new ArgumentException();
      if (v.Length != 2)
        throw new ArgumentException();
      uunsigned int num1 = v[0];
      uunsigned int num2 = v[1];
      uunsigned int num3 = 0U;
      uunsigned int num4 = 2654435769U;
      for (uunsigned int index = 0U; index < num_rounds; ++index)
      {
        uunsigned int num5 = (num2 << 4 ^ num2 >> 5) + num2;
        uunsigned int num6 = num3 + key[(unsigned intPtr) (num3 & 3U)];
        num1 += num5 ^ num6;
        num3 += num4;
        uunsigned int num7 = (num1 << 4 ^ num1 >> 5) + num1;
        uunsigned int num8 = num3 + key[(unsigned intPtr) (num3 >> 11 & 3U)];
        num2 += num7 ^ num8;
      }
      v[0] = num1;
      v[1] = num2;
      return v;
    }
  }
*/

void decrypt(int* v, int round, int* key){
	int i;
	unsigned int num3 = 0;
	unsigned int num4 = 2654435769U;
	for(i=0; i<ROUND; i++) num3 += num4; 
	unsigned int num1 = v[0];
	unsigned int num2 = v[1];
	unsigned int num5, num6, num7, num8;
	for(i=0; i<ROUND; i++){
		num8 = num3 + key[(unsigned int)(num3 >> 11 & 3U)];
		num7 = (num1 << 4 ^ num1 >> 5) + num1;		
		num2 -= num7 ^ num8;
		num3 -= num4;
		num6 = num3 + key[(unsigned int)(num3 & 3U)];
		num5 = (num2 << 4 ^ num2 >> 5) + num2;		
		num1 -= num5 ^ num6;	
	}
	v[0] = num1;
	v[1] = num2;
}

void processFile(char* filename, unsigned int encryption){
	FILE* f = fopen(filename, "rb");
	FILE* fo = fopen("out.txt", "wb");
	if (f && fo){
		unsigned int v[2];
		fseek (f , 0 , SEEK_END);
		long lSize = ftell(f);
		rewind(f);
		long count=0;
		while (count<lSize){
			fread(v, 8, 1, f);
			decrypt(v, ROUND, KEY);
			fwrite(v, 8, 1, fo);
			count += 8;
		}
		fclose(f);
		fclose(fo);
	}
}

int main(int argc, char* argv[]){
	if (argc < 2) {
		usage();
	}else{
		processFile(argv[1], atoi(argv[2]));
	}
	return 0;
}

