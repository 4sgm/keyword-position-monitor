<<<<<<< HEAD
# Keyword Position Monitor (Keyword.com API)

A no-frills web app to monitor **Google positions for specific URLs** using the **Keyword.com API (v2)**.  
Backend: FastAPI + SQLite + APScheduler.  
UI: Minimal HTML + Chart.js.

> ⚠️ **Configure the exact endpoints & auth scheme from the official docs**: https://docs.keyword.com/

---

## Quickstart

```bash
# 1) Create & activate a virtualenv (optional but recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r backend/requirements.txt

# 3) Copy .env.example to .env and fill values
cp .env.example .env
# Edit .env with your Keyword.com API key and confirm endpoint paths + auth scheme

# 4) Run
uvicorn backend.app:app --reload
# open http://127.0.0.1:8000/
```

### Docker (optional)

```bash
docker compose up --build
```

---

## Configure `.env`

```ini
# Server
APP_NAME="Keyword Position Monitor"
DEBUG=true

# Keyword.com API
KEYWORD_COM_BASE_URL="https://api.keyword.com/v2"
KEYWORD_COM_API_KEY="YOUR_API_KEY"
KEYWORD_COM_AUTH_SCHEME="Bearer"         # Check docs.keyword.com; some accounts use "Token"
KEYWORD_COM_AUTH_HEADER="Authorization"  # Or "X-API-Key" if required

# Endpoint paths per docs.keyword.com
ENDPOINT_LIST_PROJECTS="/projects"
ENDPOINT_CREATE_PROJECT="/projects"
ENDPOINT_LIST_PROJECT_KEYWORDS="/projects/{project_id}/keywords"
ENDPOINT_ADD_KEYWORDS="/projects/{project_id}/keywords"
ENDPOINT_GET_KEYWORD_HISTORY="/keywords/{keyword_id}/history"
ENDPOINT_REFRESH_SERP="/projects/{project_id}/refresh"

# Scheduler
SCHEDULE_CRON="0 7 * * *"
TIMEZONE="America/Los_Angeles"

# Database
SQLITE_URL="sqlite:///./monitor.db"

# Basic auth for admin endpoints
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin"
```

> **Note**: The exact endpoint paths may vary slightly by API version or account. Use the official docs to confirm your correct routes and payload shapes: https://docs.keyword.com/

---

## What it does

- Save **monitors**: (keyword + target URL, optional project_id & keyword_id).
- If `project_id` is supplied and `keyword_id` is blank, the app will attempt to **add the keyword to that project** via the Keyword.com API and store the new `keyword_id`.
- A background scheduler runs on a cron (default daily @ 07:00 PT) calling the **keyword history** endpoint and extracting your target URL’s **current position**.
- Stores time series in SQLite and renders a **chart of rank over time** (lower is better).

### How the URL match works
We normalize and compare domains + path prefixes (ignoring UTM/gclid/fbclid). If your target URL has only a domain (no path), any result on that domain counts as a match. See `backend/utils.py` to adjust this logic.

---

## Mapping to Keyword.com API (Examples)

Consult **https://docs.keyword.com/** for exact payloads and responses.

- **List projects** → `GET {BASE}/projects`
- **Create project** → `POST {BASE}/projects` (body: `name`, `domain`, `location`, `search_engine`)
- **List project keywords** → `GET {BASE}/projects/{project_id}/keywords`
- **Add keywords to project** → `POST {BASE}/projects/{project_id}/keywords` (body: `keywords`, `location`, `device`)
- **Refresh SERP / on-demand update** → `POST {BASE}/projects/{project_id}/refresh`
- **Get keyword rank history** → `GET {BASE}/keywords/{keyword_id}/history` (expected to include ranked URLs + positions)

If your account uses different paths/fields, update the environment variables to match.

---

## API routes (this app)

- `GET /` — dashboard
- `POST /monitors` — add a monitor (requires Basic Auth)
- `POST /run-now` — trigger an immediate check (requires Basic Auth)
- `GET /monitors` — list monitors (JSON)
- `GET /history/{monitor_id}` — time series for charts (JSON)
- `GET /keywordcom/projects` — proxy to Keyword.com projects (requires Basic Auth)
- `GET /keywordcom/{project_id}/keywords` — proxy to keywords in a project (requires Basic Auth)

> Basic Auth defaults to `admin:admin`. Change in `.env`.

---

## Notes & Hardening

- Consider **rotating tokens** and storing secrets via a vault. Never commit `.env` to Git.
- Add rate limiting and input validation for public deployments.
- For larger volumes, consider PostgreSQL and a worker queue (e.g., RQ/Celery) instead of APScheduler.
- Extend `urls_match` in `backend/utils.py` if you require exact path match vs. domain-level match.

---

## License

MIT
=======
# keyword-position-monitor
>>>>>>> 7f808c7d97059bbe6e66d8160c3726c206ea9c55
