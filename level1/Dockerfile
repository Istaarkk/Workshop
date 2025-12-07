FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends socat \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /service

COPY vuln       ./vuln
COPY flag.txt   ./flag.txt
COPY docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 1337
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
