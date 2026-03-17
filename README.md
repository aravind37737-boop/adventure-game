# PIXEL QUEST — Level Adventure Game

A retro pixel-art platformer with 10 levels, persistent leaderboard, and a Python backend server.

---

## Quick Start

### Option 1 — Open directly in browser
Just double-click `index.html` — no server needed!
The leaderboard stores data in your browser's localStorage.

### Option 2 — Run with Python server (recommended)
```bash
python server.py
# Then open: http://localhost:8080
```
Optional flags:
```bash
python server.py --port 3000
python server.py --host 0.0.0.0 --port 8080  # LAN accessible
```

---

## Controls

| Key | Action |
|-----|--------|
| ← → / A D | Move left / right |
| ↑ / W / Space | Jump |
| P / Esc | Pause |

---

## How to Win Each Level

1. **Collect all ★ coins** — the exit portal unlocks when all coins are gathered
2. **Reach the exit portal** — glowing green door
3. **Avoid enemies** — red creatures patrol platforms
4. **Stomp enemies** by jumping on their heads for +50 points
5. **Don't fall** into the void — you lose 1 HP per fall

## Star Rating

| Stars | Condition |
|-------|-----------|
| ★☆☆ | Complete the level |
| ★★☆ | Collect ALL coins |
| ★★★ | All coins + finish within time limit |

---

## API Endpoints (Python server)

```
GET    /                    → Game HTML
GET    /api/leaderboard     → Get top scores (JSON)
POST   /api/leaderboard     → Submit score
DELETE /api/leaderboard     → Clear all scores
GET    /api/stats           → Server statistics
```

### Submit a score:
```bash
curl -X POST http://localhost:8080/api/leaderboard \
  -H "Content-Type: application/json" \
  -d '{"name":"HERO","score":1500,"levels":5,"stars":12}'
```

---

## File Structure

```
adventure-game/
├── index.html          ← The complete game (HTML+CSS+JS)
├── server.py           ← Python HTTP server + Leaderboard API
├── leaderboard.json    ← Leaderboard data (auto-created)
└── README.md           ← This file
```

---

## Levels

| # | Name | Difficulty |
|---|------|-----------|
| 1 | THE OUTPOST | ⭐ Easy |
| 2 | RISING TOWERS | ⭐⭐ Easy |
| 3 | THE GAUNTLET | ⭐⭐ Medium |
| 4 | SKY ISLANDS | ⭐⭐⭐ Medium |
| 5 | THE ABYSS | ⭐⭐⭐ Hard |
| 6 | NEON DUNGEON | ⭐⭐⭐ Hard |
| 7 | STORM HEIGHTS | ⭐⭐⭐⭐ Hard |
| 8 | CHAOS FACTORY | ⭐⭐⭐⭐ Very Hard |
| 9 | THE VOID | ⭐⭐⭐⭐⭐ Expert |
| 10 | FINAL ARENA | ⭐⭐⭐⭐⭐ Boss |

---

Built with pure HTML, CSS, JavaScript, and Python. No external dependencies required.
