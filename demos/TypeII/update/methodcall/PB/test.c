#include <stdio.h>
int vulcodeB(int n, int m)
{
	int k = 0;
	int a =5, b =4;

	return a * n + m *b;
}

int main(void)
{
	int a,b;
	scanf("%d", &a);
	scanf("%d", &b);
	int vul_numver = vulcodeB(a,b);
	printf("fib number is %d", vul_numver);
	return 0;
}