# printer-queue-checker

Check the print queue via system commands where available (`lpstat` on
Linux/macOS, PowerShell on Windows). Where no queue tool exists, it says so
plainly and lists manual steps — it never invents fake queue data.

## How to run

```bash
python3 main.py
```

## Example output (sample from test fixture data)

```text
Platform: Linux
Print queue tool available.
printer1-1 user 1024
1 job(s) in queue.
```

Fallback example:

```text
Platform: Linux
No live print queue available on this system (no fake data shown).
- No print-queue tool (lpstat) found on this system.
```

Tests mock the system commands, so they run without a real printer.
