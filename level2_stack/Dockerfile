FROM ubuntu:22.04

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    socat \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 ctf
WORKDIR /home/ctf

COPY chall /home/ctf/chall
COPY libc.so.6 /home/ctf/libc.so.6
COPY ld-linux-x86-64.so.2 /home/ctf/ld-linux-x86-64.so.2
COPY run.sh /home/ctf/run.sh

COPY flag.txt /home/ctf/flag.txt
RUN chown -R ctf:ctf /home/ctf \
  && chmod 640 /home/ctf/flag.txt

USER ctf
EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/ctf/run.sh,pty,stderr,setsid,sigint,sane"]
