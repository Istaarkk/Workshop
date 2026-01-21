FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 -s /bin/bash ctf
WORKDIR /home/ctf

COPY chall /home/ctf/chall
COPY ld-linux-x86-64.so.2 /home/ctf/ld-linux-x86-64.so.2
COPY libc.so.6 /home/ctf/libc.so.6

RUN chmod 755 /home/ctf/chall /home/ctf/ld-linux-x86-64.so.2 /home/ctf/libc.so.6 \
 && chown -R ctf:ctf /home/ctf

USER ctf
EXPOSE 1337

# ✅ Une seule ligne, pas de JSON => pas de parse error
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/ctf/ld-linux-x86-64.so.2 --library-path /home/ctf /home/ctf/chall",stderr

