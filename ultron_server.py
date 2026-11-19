"""Ultron helper server.
Setup:  pip install psutil
Run:    python ultron_server.py   then open http://localhost:8000/jarvis_hud.html
"""
import json, os, subprocess, sys
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import psutil

# Add your own apps here: spoken name -> command
APPS = {
    "notepad": "notepad", "calculator": "calc", "chrome": "chrome",
    "vscode": "code", "code": "code", "paint": "mspaint", "explorer": "explorer",
    "word": "winword", "excel": "excel", "spotify": "spotify",
}

def open_app(name):
    cmd = APPS.get(name.lower())
    if not cmd:
        return False
    try:
        if sys.platform.startswith("win"):
            os.system(f"start {cmd}")
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", cmd])
        else:
            subprocess.Popen([cmd])
        return True
    except Exception:
        return False

class H(SimpleHTTPRequestHandler):
    def _json(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/stats":
            b = psutil.sensors_battery()
            return self._json({
                "cpu": psutil.cpu_percent(interval=None),
                "ram": psutil.virtual_memory().percent,
                "battery": round(b.percent) if b else None,
            })
        if u.path == "/open":
            app = parse_qs(u.query).get("app", [""])[0]
            return self._json({"ok": open_app(app)})
        super().do_GET()

if __name__ == "__main__":
    print("Ultron server running on http://localhost:8000/jarvis_hud.html")
    HTTPServer(("localhost", 8000), H).serve_forever()
