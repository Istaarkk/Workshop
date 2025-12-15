#!/bin/sh
set -eu

ulimit -c 0
PORT="${PORT:-1337}"

echo "Starting vuln service on port ${PORT}"

# Spawn the vulnerable binary via socat so each connection gets a fresh process.
exec socat TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"/service/vuln,stderr",pty,ctty,echo=0
