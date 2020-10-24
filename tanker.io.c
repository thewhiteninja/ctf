#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void print(int *c, int *b, int *a){
 int i;
  
 for ( i = 4; i >= 0; --i )
 {
   printf("%d", a[i]);
 }

 for ( i = 3; i >= 0; --i )
 {
   printf("%d", b[i]);
 }
 
 for ( i = 2; i >= 0; --i )
 {
   printf("%d", c[i]);
 }
  
  printf("\n");
}


__int64 add(int a1, int a2, int *a3, signed int a4)
{
  int v4; // ST2C_4
  int v5; // ecx
  __int64 result; // rax
  unsigned int v7; // [rsp+Ch] [rbp-24h]

  v7 = a4;
  v4 = a3[a2] + a1;
  a3[a2] = v4 % 10;
  v5 = v4 - v4 % 10;
  result = v5 / 10;
  if ( v5 / 10 )
  {
    result = (a2 + 1);
    if ( result < v7 )
      result = add(v5 / 10, a2 + 1, a3, v7);
  }
  return result;
}

int main(){
  int a[5]; // [rsp+10h] [rbp-40h]
  int b[4]; // [rsp+30h] [rbp-20h]
  int c[3]; // [rsp+44h] [rbp-Ch]

  memset(c, 0, 3uLL);
  b[0] = 0;
  memset(a, 0, 5uLL);
  c[0] = 2;
  c[1] = 7;
  c[2] = 0;
  b[0] = 9;
  b[1] = 1;
  b[2] = 2;
  b[3] = 3;
  a[0] = 5;
  a[1] = 6;
  a[2] = 1;
  a[3] = 4;
  a[4] = 5;
  
  print(c, b, a);
  
  unsigned long long m = 365*24*3600;
  while (m--){
    add(2, 0, c, 3);
    add(3, 0, b, 4);
    add(7, 0, a, 5);
  }

  print(c, b, a);
  
  return 0;
}

/*

Alice
061651219072
https://tanker.io/jobs/06158-1216-070?ts=1529535360&token=slfd65prLM788H


*/