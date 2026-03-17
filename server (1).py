#!/usr/bin/env python3
"""
PIXEL QUEST — Game Server
Run:  python server.py [--port 8080] [--host 0.0.0.0]
Then open http://localhost:8080 on PC or http://<your-ip>:8080 on mobile.
"""

import json, os, sys, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

BASE_DIR  = Path(__file__).parent
GAME_FILE = BASE_DIR / "index.html"
DATA_FILE = BASE_DIR / "leaderboard.json"
MAX_LB    = 50

def load_lb():
    if DATA_FILE.exists():
        try: return json.loads(DATA_FILE.read_text("utf-8"))
        except: pass
    return []

def save_lb(data): DATA_FILE.write_text(json.dumps(data, indent=2), "utf-8")

def upsert(name, score, levels, stars):
    lb   = load_lb()
    name = name.upper()[:12]
    e    = next((x for x in lb if x["name"] == name), None)
    now  = datetime.utcnow().isoformat()
    if e:
        e["score"]   = max(e["score"],  score)
        e["levels"]  = max(e["levels"], levels)
        e["stars"]   = max(e["stars"],  stars)
        e["updated"] = now
    else:
        lb.append({"name": name, "score": score, "levels": levels, "stars": stars, "created": now, "updated": now})
    lb.sort(key=lambda x: x["score"], reverse=True)
    save_lb(lb[:MAX_LB])
    return lb

CORS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] {self.address_string()} {fmt % a}")

    def _json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k, v in CORS.items(): self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _html(self, body):
        self.send_response(200)
        self.send_header("Content-Type",        "text/html; charset=utf-8")
        self.send_header("Content-Length",       str(len(body)))
        # Mobile / PWA friendly headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control",          "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS.items(): self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"):
            if not GAME_FILE.exists():
                return self._json({"error": "Game file not found"}, 404)
            self._html(GAME_FILE.read_bytes())
        elif p == "/api/leaderboard":
            self._json({"leaderboard": load_lb()})
        elif p == "/api/stats":
            lb  = load_lb()
            top = lb[0] if lb else None
            self._json({"players": len(lb), "top_player": top and top["name"], "top_score": top and top["score"] or 0})
        elif p == "/health":
            self._json({"status": "ok"})
        else:
            self._json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path.split("?")[0] == "/api/leaderboard":
            try:
                b = self._body()
                name   = str(b.get("name",   "ANON")).strip() or "ANON"
                score  = max(0, int(b.get("score",  0)))
                levels = max(0, int(b.get("levels", 0)))
                stars  = max(0, int(b.get("stars",  0)))
                lb     = upsert(name, score, levels, stars)
                rank   = next((i+1 for i,e in enumerate(lb) if e["name"]==name.upper()), -1)
                self._json({"success": True, "rank": rank, "leaderboard": lb[:10]})
            except Exception as exc:
                self._json({"error": str(exc)}, 400)
        else:
            self._json({"error": "Not found"}, 404)

    def do_DELETE(self):
        if self.path.split("?")[0] == "/api/leaderboard":
            save_lb([])
            self._json({"success": True})
        else:
            self._json({"error": "Not found"}, 404)

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    ap = argparse.ArgumentParser(description="Pixel Quest Server")
    ap.add_argument("--port", type=int,  default=8080)
    ap.add_argument("--host", type=str,  default="0.0.0.0")
    args = ap.parse_args()

    local_ip = get_local_ip()
    srv = HTTPServer((args.host, args.port), H)

    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║           PIXEL QUEST  ·  GAME SERVER            ║")
    print("  ╠══════════════════════════════════════════════════╣")
    print(f"  ║  PC:     http://localhost:{args.port:<24}║")
    print(f"  ║  Mobile: http://{local_ip}:{args.port:<22}║")
    print(f"  ║  API:    http://localhost:{args.port}/api/leaderboard  ║")
    print("  ║  Ctrl+C to stop                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  Goodbye!")
        srv.server_close()

if __name__ == "__main__":
    main()
