#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(void) {
    char buf[128];

    write(1, "Enter your shellcode:\n", 23);

    ssize_t n = read(0, buf, sizeof(buf) - 1);
    if (n <= 0) return 1;

    if (strlen(buf) < 48) {
        ((void(*)())buf)();
    }

    return 0;
}
