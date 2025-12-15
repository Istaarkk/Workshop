# Repository Guidelines

## Project Structure & Module Organization
- `main.c`: vulnerable service entrypoint; compiled into `vuln` for exploitation practice.
- `vuln`: built ELF with symbols intact for local debugging.
- `solve.py`: Pwntools exploit harness; supports `LOCAL` and `DEBUG` flags.
- `cyc`: cyclic pattern file useful for offset discovery.
- `input/`: hold any crafted payloads or transcripts; keep new samples small and labeled.

## Build, Test, and Development Commands
- Build (recreate `vuln`): `gcc -g -no-pie -fno-stack-protector -z execstack -o vuln main.c`
  - Keep `-g` and relaxed protections to mirror current challenge behavior.
- Run service: `./vuln`
- Exploit locally: `python3 solve.py LOCAL`
- Debug run: `python3 solve.py LOCAL DEBUG` (opens GDB on the process)
- Disassembly/inspection: `objdump -d vuln | less`, symbols via `nm vuln`

## Coding Style & Naming Conventions
- C: 4-space indentation, braces on new lines for functions, prefer `snprintf`/`fgets` over unsafe IO when hardening; name helpers with verb prefixes (`build_payload`, `print_usage`).
- Python: 4 spaces, snake_case functions, keep functions small; favor explicit imports (`from pwn import *` already used—avoid unused wildcards elsewhere).
- Binary artifacts: commit only the intended `vuln` build; avoid transient core dumps or pwntools caches.

## Testing Guidelines
- Functional check: `python3 solve.py LOCAL` should drop to an interactive shell; if hardening code, confirm exploit still demonstrates intended learning outcome or update solve script accordingly.
- For offset work, regenerate patterns with Pwntools (`cyclic 200`) and document new offsets in comments.
- Add small regression snippets instead of heavy test suites; keep payloads reproducible in `input/`.

## Commit & Pull Request Guidelines
- Commits: short imperative subject (“Add hardening mode”), group related edits; include context for changed offsets or mitigations in the body.
- PRs: describe behavior change, reproduction steps, and exploit impact; link any related ticket. Include screenshots or terminal transcripts when UI/interaction differs (e.g., new prompts).
- Keep diffs minimal; do not rewrite the binary unless needed—note compiler flags if it changes.

## Security & Configuration Notes
- Network targets are placeholder (`addr:1337`); avoid committing real endpoints or credentials.
- If introducing protections (RELRO, PIE, canaries), document required flags and update `solve.py` to match.
- Verify tools: Pwntools ≥4, GCC on x86_64; note any deviations in PRs.
