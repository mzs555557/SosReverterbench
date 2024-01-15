#include <stdio.h>

int vulcode(int n, int m)
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
	int vul_num = vulcode(a,b);

	for (a = 0; a < vul_num; a++){
	    printf("fib number is %d", vul_num);
	}
	return 0;
}


