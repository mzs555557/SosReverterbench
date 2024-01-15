#include <stdio.h>

int vulcode(int n, int m)
{

	int a =5, b =4;

	return a * n + m *b;
}


int main(void)
{
	int a,b;
	scanf("%d", &a);
	scanf("%d", &b);
	int fib_number = vulcode(a,b);
	printf("fib number is %d", fib_number);
	return 0;
}


