FROM ubuntu:22.04 AS build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY main.c .
RUN gcc -fno-stack-protector -z execstack -no-pie -O2 -o chall main.c

FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall -s /usr/sbin/nologin chall
WORKDIR /home/chall

COPY --from=build /build/chall /home/chall/chall
RUN chown root:root /home/chall/chall \
    && chmod 555 /home/chall/chall \
    && chmod 755 /home/chall

EXPOSE 1337
USER chall
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:/home/chall/chall,stderr"]
