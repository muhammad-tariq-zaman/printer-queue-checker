"""Printer queue checker: real system queue where available, honest fallback."""
import platform
import shutil
import subprocess
import sys


def check_queue():
    system = platform.system()
    if system == "Windows":
        tool = "powershell"
        if not shutil.which("powershell"):
            return {"available": False, "platform": system,
                    "manual_steps": ["Open Settings > Bluetooth & devices > Printers & scanners",
                                     "Select the printer and open its print queue."]}
        try:
            out = subprocess.run(["powershell", "-NoProfile", "-Command",
                                  "Get-Printer | Select-Object Name, PrinterStatus | Format-Table -AutoSize | Out-String"],
                                 capture_output=True, text=True, timeout=15)
            return {"available": True, "platform": system, "output": out.stdout.strip(),
                    "manual_steps": []}
        except (OSError, subprocess.SubprocessError) as exc:
            return {"available": False, "platform": system, "error": str(exc),
                    "manual_steps": ["Open Settings > Printers & scanners and check the queue manually."]}
    if shutil.which("lpstat"):
        try:
            out = subprocess.run(["lpstat", "-o"], capture_output=True, text=True, timeout=15)
            jobs = [l for l in out.stdout.splitlines() if l.strip()]
            return {"available": True, "platform": system, "jobs": jobs,
                    "output": out.stdout.strip(), "manual_steps": []}
        except (OSError, subprocess.SubprocessError) as exc:
            return {"available": False, "platform": system, "error": str(exc),
                    "manual_steps": ["Run 'lpstat -o' in a terminal to view the print queue."]}
    return {"available": False, "platform": system,
            "manual_steps": ["No print-queue tool (lpstat) found on this system.",
                             "On Linux/macOS install CUPS and run 'lpstat -o'.",
                             "On Windows open Settings > Printers & scanners and check the queue."]}


def main():
    r = check_queue()
    print(f"Platform: {r['platform']}")
    if r["available"]:
        print("Print queue tool available.")
        print(r.get("output", ""))
        if r.get("jobs") is not None:
            print(f"{len(r['jobs'])} job(s) in queue.")
    else:
        print("No live print queue available on this system (no fake data shown).")
        for step in r["manual_steps"]:
            print(f"- {step}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
