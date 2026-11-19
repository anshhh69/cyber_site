"""
ULTRON APP OPENER
==================
Chhota helper program jo background mein chalta hai aur
Ultron (jarvis_hud.html) ko real Windows apps kholne deta hai.

Kaise chalayein:
    python ultron_opener.py

Ye "python -m http.server 8000" wale Command Prompt se ALAG
ek naya Command Prompt window mein chalana hai - dono ek saath
chalte rehne chahiye jab Ultron use kar rahe ho.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

PORT = 5005

# Yahan apne apps add/edit kar sakte ho.
# Format: "naam jo bologe": "windows command jo chalega"
APP_MAP = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "chrome": "start chrome",
    "edge": "start msedge",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "cmd": "start cmd",
    "command prompt": "start cmd",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "settings": "start ms-settings:",
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt",
    "vscode": "code",
    "visual studio code": "code",
    "spotify": "start spotify:",
    # apna khud ka app add karne ke liye yahan naya line banao:
    # "myapp": "C:\\Path\\To\\App.exe",
}


class OpenerHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        if parsed.path == '/open':
            app_name = params.get('app', [''])[0].strip().lower()
            if app_name in APP_MAP:
                os.system(APP_MAP[app_name])
                self.wfile.write(f"opened {app_name}".encode('utf-8'))
                print(f"[Ultron Opener] Opened: {app_name}")
            else:
                self.wfile.write(f"unknown app: {app_name}".encode('utf-8'))
                print(f"[Ultron Opener] Unknown app requested: {app_name}")
        else:
            self.wfile.write(b"Ultron App Opener is running.")

    def log_message(self, format, *args):
        pass  # keep the console clean


if __name__ == "__main__":
    print(f"Ultron App Opener running at http://localhost:{PORT}")
    print("Is window ko band mat karna jab tak Ultron use kar rahe ho.")
    print("Bandh karne ke liye Ctrl+C dabao.\n")
    HTTPServer(('localhost', PORT), OpenerHandler).serve_forever()
