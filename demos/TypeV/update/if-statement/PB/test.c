#include <stdio.h>
#include <string.h>
#include <ctype.h>  

void testLocalRefA(int a, char* str){
    printf("the values are  %d %s\n", a, str);
}


int main( ) {
    int j = 2;
    if (j > 10)
        printf("RANDOM");
    if (j > 0){
        j += 3;
        testLocalRefA(j, "test");
    }

    printf("CHECK");
    return 0;
}