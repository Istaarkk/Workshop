#!/bin/sh
# Run with bundled loader/libc to match local environment
exec /home/ctf/ld-linux-x86-64.so.2 --library-path /home/ctf /home/ctf/chall
