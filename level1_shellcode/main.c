#include <stdio.h>
#include <unistd.h>

int main(){
    
    char buf [128];
    write(1, "Shellcode: ", 11);
    read(0,buf,sizeof(buf));

    ((void(*)())buf)();

    return 0;
}