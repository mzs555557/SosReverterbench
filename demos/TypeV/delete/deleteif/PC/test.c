#include <stdio.h>
int vulcode(int n, int m)
{
	int k = 0;
	int a =5, b =4;

	return a * n + m *b;
}

int main(void)
{
	int a,b, c = 20;
	scanf("%d", &a);
	scanf("%d", &b);
    int vul_numver = vulcode(a,b);
    
    if (a>0 && b >10) {
        c = a + b -c;
        printf("fib number is %d", vul_numver);
    }
	return 0;
}