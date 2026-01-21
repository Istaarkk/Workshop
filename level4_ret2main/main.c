#include <stdio.h>
#include <unistd.h>


void coupon_scanner(void) {
    __asm__("pop %rdi\n"
            "ret\n");

}

void setup_io(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void maintenance(){

    char buffer[128];
    puts("Welcome to the maintenance console!");
    puts("Please enter the access code:");
    ssize_t n = read(0,buffer,256);
    if (n < 0 ){
        puts("Error reading input!");
        return;
    }
    puts("Access code accepted. You may now enter commands.");
}

int main(){

    setup_io();
    puts("Booting...");
    puts("1) Maintenance");
    puts("2) Quitter");
    puts("> ");

    char choice[8] = {0};
    read(0, choice, sizeof(choice)-1);

    if (choice[0] == '1') {
        maintenance();
    } else {
        puts("Bye.");
    }

    return 0;
}
