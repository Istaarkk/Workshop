FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf
COPY chall /home/ctf/chall
RUN chown root:root /home/ctf/chall && chmod 755 /home/ctf/chall

ARG FLAG="CTF{dummy_flag}"
RUN echo "$FLAG" > /flag && chmod 444 /flag

EXPOSE 1337

USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/ctf/chall,stderr,pty,raw,echo=0"]
