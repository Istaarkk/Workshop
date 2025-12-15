#include <pty.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>    

void call_me(){
    char *const args[] = {"/bin/sh", NULL};
    execve("/bin/sh", args, NULL);  
}

int main(int argc, char *argv[])
{
	char buf[64];
		
	printf("you are pleased to enter any value");
	fgets(buf,255,stdin);
	
	printf("Buffer value is : ");
	printf(buf);
	return 0;
}
