#!/usr/bin/env python3
from pwn import *
elf = ELF("./chall")

context.binary = elf
context.arch = 'amd64'


def conn():
    if args.LOCAL:
        r = process([context.binary.path])
        if args.GDB:
            gdb.attach(r)
        return r
    return remote("127.0.0.1", 4000)


r = conn()

