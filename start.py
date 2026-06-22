"""Single-command launcher: installs deps if needed, then starts both servers.

Usage (from the subscription-tracker/ directory):
    python start.py

Both servers shut down cleanly on Ctrl+C.
"""
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"

# On Windows, npm lives as npm.cmd; on Unix it's just npm.
NPM = "npm.cmd" if sys.platform == "win32" else "npm"


def _run(*cmd, cwd):
    """Run a command synchronously, raising on non-zero exit."""
    subprocess.run(list(cmd), cwd=cwd, check=True)


def _ensure_deps():
    print("▶  Installing backend Python dependencies…")
    _run(sys.executable, "-m", "pip", "install", "-r", "requirements.txt", cwd=BACKEND_DIR)

    if not (FRONTEND_DIR / "node_modules").exists():
        print("▶  Installing frontend npm dependencies (first run)…")
        _run(NPM, "install", cwd=FRONTEND_DIR)
    else:
        print("▶  Frontend node_modules already present — skipping npm install.")


def main():
    print("\n── Subscription Tracker ──────────────────────────────────────")
    _ensure_deps()

    print("\n▶  Starting FastAPI backend on http://127.0.0.1:8000 …")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
    )

    print("▶  Starting React frontend on http://localhost:5173 …")
    frontend = subprocess.Popen(
        [NPM, "run", "dev"],
        cwd=FRONTEND_DIR,
    )

    print("\n✓  Dashboard → http://localhost:5173")
    print("   API docs  → http://localhost:8000/docs")
    print("   Press Ctrl+C to stop both servers.\n")

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\nShutting down…")
    finally:
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Servers stopped.")


if __name__ == "__main__":
    main()
