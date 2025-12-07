#include <pty.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>    

void call_me(){
    char *const args[] = {"/bin/sh", NULL};
    execve("/bin/sh", args, NULL);
}

int main(void) {
    char buf[64];

    setvbuf(stdout, NULL, _IONBF, 0);      
    puts("you are pleased to enter any value");
    fgets(buf, 255, stdin);                
    printf("Buffer value is : ");
    printf(buf);

    puts("\nnow give me more");
    fgets(buf, 255, stdin);                
    return 0;
}
