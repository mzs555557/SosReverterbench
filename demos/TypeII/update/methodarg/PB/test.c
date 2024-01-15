#include <stdio.h>
int vulcodeA(int n, int m)
{
	int k = 0;
	int a =5, b =4;

	return a * n + m *b;
}

int main(void)
{
	int a,b,check = 10,digit=20;
	scanf("%d", &a);
	scanf("%d", &b);
	int vul_numver = vulcodeA(check,digit);
	printf("fib number is %d", vul_numver);
	return 0;
}