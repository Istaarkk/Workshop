#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define BUFSZ 64

void vuln(){

    char buf[BUFSZ];

    puts("Entrez votre payload :");

    ssize_t n = read(STDIN_FILENO, buf, 400);
    if (n <= 0) exit(1);

    printf(buf);
    puts("");

    puts("Entrez votre ROP :");

    n = read(STDIN_FILENO, buf, 400);
    if (n <= 0) exit(1);
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    puts("Fin de programme.");
    return 0;
}
