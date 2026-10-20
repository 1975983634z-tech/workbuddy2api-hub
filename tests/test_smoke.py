import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class GatewaySmokeTest(unittest.TestCase):
    def test_starts_with_empty_isolated_data(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            accounts = temp / "accounts"
            usage = temp / "usage"
            home = temp / "home"
            accounts.mkdir()
            usage.mkdir()
            home.mkdir()
            port = free_port()
            env = os.environ.copy()
            env.update({
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "PYTHONUNBUFFERED": "1",
            })
            cmd = [
                sys.executable,
                str(ROOT / "wb_proxy.py"),
                "--host", "127.0.0.1",
                "--port", str(port),
                "--accounts-dir", str(accounts),
                "--usage-dir", str(usage),
            ]
            proc = subprocess.Popen(
                cmd,
                cwd=ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                url = f"http://127.0.0.1:{port}/health"
                deadline = time.monotonic() + 10
                last_error = None
                while time.monotonic() < deadline:
                    if proc.poll() is not None:
                        output = proc.stdout.read() if proc.stdout else ""
                        self.fail("gateway exited before startup:" + chr(10) + output)
                    try:
                        with urllib.request.urlopen(url, timeout=1) as response:
                            self.assertEqual(response.status, 200)
                            payload = json.loads(response.read().decode("utf-8"))
                            self.assertTrue(payload["ok"])
                            self.assertEqual(payload["accounts"], 0)
                            break
                    except Exception as exc:
                        last_error = exc
                        time.sleep(0.1)
                else:
                    output = ""
                    if proc.poll() is not None and proc.stdout:
                        output = proc.stdout.read()
                    self.fail("gateway did not become healthy: " + str(last_error) + chr(10) + output)
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
