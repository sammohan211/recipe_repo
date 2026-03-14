# Pantry Inventory & Recipe Assistant

Personal inventory-driven cooking assistant. Scan groceries, track what you have, and find keto recipes from your pantry.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Spoonacular API key (free at https://spoonacular.com/food-api)
- ngrok (for phone camera access — see below)

---

## Setup

**1. Install dependencies**

```bash
uv sync
```

**2. Create your `.env` file**

```bash
cp .env.example .env
```

Then edit `.env` and add your Spoonacular API key:

```
SPOONACULAR_API_KEY=your_key_here
```

---

## Daily usage

| Command | What it does |
|---|---|
| `make dev` | Start server + open ngrok HTTPS tunnel (use this) |
| `make stop` | Stop the server |
| `make restart` | Restart the server |
| `make status` | Check if server is running |
| `make logs` | Tail the server log |
| `make tunnel` | Open ngrok tunnel only (if server already running) |

**Typical session:**

```bash
make dev
```

ngrok will print a URL like `https://abc123.ngrok-free.app` — open that on your phone. Press `Ctrl+C` to close the tunnel, then `make stop` to shut down the server.

---

## ngrok setup (one-time)

Mobile browsers require HTTPS to access the camera. ngrok provides a temporary HTTPS tunnel to your local server.

1. Sign up free at https://ngrok.com
2. Install ngrok:
   ```bash
   curl -Lo /tmp/ngrok.tgz https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
   tar -xzf /tmp/ngrok.tgz -C /tmp
   sudo mv /tmp/ngrok /usr/local/bin/ngrok
   ```
3. Add your auth token (from ngrok dashboard):
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

> Note: the ngrok URL changes each session on the free plan. For a permanent setup, configure HTTPS on the Raspberry Pi instead.

---

## Running tests

```bash
uv run pytest
```

---

## App screens

| Screen | URL |
|---|---|
| Pantry inventory | `/inventory` |
| Barcode scan | `/scan` |
| Recipe suggestions | `/recipes` |
| Grocery list | `/grocery` |
| API health check | `/health` |
