# Pantry Inventory & Recipe Assistant

Personal inventory-driven cooking assistant. Scan groceries, track what you have, and find keto recipes from your pantry.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Spoonacular API key (free at https://spoonacular.com/food-api)

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

## Starting the server

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The app will be available at `http://localhost:8000`.

From a phone on the same network, use your machine's local IP instead:

```
http://192.168.1.xx:8000
```

### Run with auto-reload (development)

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Stopping the server

Press `Ctrl+C` in the terminal where the server is running.

---

## Running in the background (Raspberry Pi)

To keep the server running after you close the terminal:

```bash
nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

To stop it:

```bash
pkill -f "uvicorn app.main"
```

To check if it's running:

```bash
pgrep -a -f "uvicorn app.main"
```

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
