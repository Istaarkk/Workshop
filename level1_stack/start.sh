#!/bin/sh
set -e
exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/home/ctf/vuln,stderr
