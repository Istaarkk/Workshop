FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ctf
COPY vuln /home/ctf/vuln
RUN chmod 755 /home/ctf/vuln

RUN useradd -m ctf
COPY flag.txt /home/ctf/flag.txt
RUN chown root:ctf /home/ctf/flag.txt \
    && chmod 640 /home/ctf/flag.txt

COPY start.sh /start.sh
RUN chmod 755 /start.sh

EXPOSE 9999
USER ctf
CMD ["/start.sh"]
