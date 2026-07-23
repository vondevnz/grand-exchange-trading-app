# Grand Exchange Trading Application

A full-stack price-tracking application for Old School RuneScape's Grand
Exchange, built on the OSRS Wiki's real-time pricing API. A scheduled
background job continuously ingests live price data into PostgreSQL, and a
React frontend provides searchable, paginated access to it.

Live app: https://grand-exchange-trading-app.vercel.app   
API: https://grand-exchange-trading-app.onrender.com/docs   


> Note: the backend runs on a free-tier instance. A keep-alive job pings it
> every 10 minutes to prevent it from spinning down, but an occasional slow
> first load is still possible.

## Features

- **Live price ingestion** — a scheduled background job polls the OSRS Wiki
  API every 10 minutes and upserts current buy/sell prices for all ~4,450
  tradeable items
- **Search** — case-insensitive, partial-match search by item name, handled
  server-side via SQL `ILIKE`
- **Pagination** — configurable page size (20/50/100), with page-number
  navigation and total-result counts
- **Relative timestamps** — "5 mins ago" / "2 hours ago" style display for
  last trade times
- **Fully containerised** — one command (`docker-compose up`) brings up the
  API, database, and background poller together
- **Historical price charts** - Each item has historical data and volume data
  a graph dropdown menu

## Currently Working On

- **Batch Inserts** - Currently takes 5 minutes for each insert into database, will optimise this to fix congestion issues

## Future Features

 
- Live UI updates — the frontend reflects data as of the last page load,
  not the last poll (a manual refresh shows current data)  
- Filtering system for each column
- User login to favourite items to trade
- Data models to find an edge in the market for profit gains

## Screenshot

![Grand Exchange Trading Application screenshot](docs/app-screenshot-2.png)

## Architecture

```
                Internet
                    |
                    v
      +--------------------------+
      |   OSRS Wiki Prices API   |
      |  /latest    /mapping     |
      +-------------+------------+
                    |
                    | polled every 10 min (APScheduler)
                    v
      +--------------------------+
      |   FastAPI Application    |
      |   (deployed on Render)   |
      |                          |
      |  Scheduled ingestion job |
      |  - fetch latest prices   |
      |  - resolve item names/   |
      |    icons                 |
      |  - upsert into Postgres  |
      |                          |
      |  REST API                |
      |  - GET /api/prices/latest|
      |    (search, pagination)  |
      +-------------+------------+
                    |
                    | SQLAlchemy (async) / asyncpg, SSL
                    v
      +--------------------------+
      |      PostgreSQL          |
      |    (hosted on Neon)      |
      |  items                   |
      |  item_time_stamp         |
      +--------------------------+
                    ^
                    | REST (JSON)
                    |
      +--------------------------+
      |   React (Vite) Frontend  |
      |   (deployed on Vercel)   |
      |  - searchable, paginated |
      |    item table            |
      +--------------------------+
```

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| ORM | SQLAlchemy 2.0 (async), asyncpg |
| Database | PostgreSQL 15 (hosted on [Neon](https://neon.tech)) |
| Scheduling | APScheduler (`AsyncIOScheduler`) |
| Frontend | React, Vite |
| Dependency management | uv |
| Containerisation | Docker, Docker Compose |
| Hosting — backend | [Render](https://render.com) (Docker web service) |
| Hosting — frontend | [Vercel](https://vercel.com) |
| Uptime | cron-job.org (keep-alive ping) |

## Getting started
 
### Prerequisites
 
- Docker Desktop
- Node.js (for running the frontend dev server)
- A `.env` file (see below) — the app won't start without one, since the
  OSRS Wiki API requires a descriptive `User-Agent` on every request
By default, `docker-compose.yml` runs a local PostgreSQL container — no
external database account is required to run this locally. The deployed
version instead points `DATABASE_URL` at a hosted [Neon](https://neon.tech)
Postgres instance; see [Deployment](#deployment) below.
 
### Backend
 
```bash
git clone https://github.com/vondevnz/grand-exchange-trading-app.git
cd grand-exchange-trading-app
cp .env.example .env
# edit .env and set USER_AGENT_TEXT to identify your own instance
docker-compose up --build
```
 
This starts:
- a PostgreSQL container (`db`)
- the FastAPI app (`app`) on `http://localhost:8000`
On startup, the app creates any missing database tables and starts the
scheduled polling job automatically — no manual data-loading step required.
Prices begin populating within the first polling interval.
 
Interactive API docs are available at `http://localhost:8000/docs`.
 
### Frontend
 
```bash
cd frontend
cp .env.example .env
# edit .env if needed — VITE_API_URL defaults to the local backend
npm install
npm run dev
```
 
Runs on `http://localhost:5173` by default (Vite's dev server), and talks to
the backend URL configured in `VITE_API_URL`.
 
## Deployment
 
The live version is split across three free-tier services:
 
| Service | Role |
|---|---|
| [Neon](https://neon.tech) | Managed PostgreSQL — chosen over Render's own free Postgres, which is hard-deleted 30 days after creation |
| [Render](https://render.com) | Hosts the FastAPI backend as a Docker web service, built directly from this repo |
| [Vercel](https://vercel.com) | Hosts the React frontend, built from the `frontend/` subdirectory |
 
**Environment variables** are set directly in each platform's dashboard
(Render and Vercel), rather than committed — the same variables used
locally (`DATABASE_URL`, `USER_AGENT_TEXT` on the backend; `VITE_API_URL`
on the frontend), pointed at the production database and API instead.
 
**Keep-alive.** Render's free web services spin down after 15 minutes of
inactivity, causing a 30–60 second cold start on the next request. A
scheduled cron-job pings the API every 10 minutes to keep it warm.
 
## API
 
### `GET /api/prices/latest`
 
Returns a paginated, optionally filtered list of items with current prices.
 
**Query parameters**
 
| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | `1` | Page number |
| `page_size` | int | `20` | Items per page (20 / 50 / 100) |
| `search` | string | — | Case-insensitive partial match on item name |
 
**Example response**
 
```json
{
  "items": [
    {
      "item_id": 4151,
      "name": "Abyssal whip",
      "item_image": "https://oldschool.runescape.wiki/images/Abyssal_whip.png",
      "instabuy": 2750000,
      "instasell": 2700000,
      "last_instabuy_time": "2026-07-15T09:59:52+00:00",
      "last_instasell_time": "2026-07-15T10:26:37+00:00"
    }
  ],
  "total": 4452,
  "page": 1,
  "page_size": 20,
  "total_pages": 223
}
```

## Design decisions

**Upsert over insert-then-update.** Price ingestion uses a single atomic
`INSERT ... ON CONFLICT DO UPDATE` statement per item rather than a
check-then-branch pattern, avoiding an extra round-trip and a race condition
between concurrent writes.

**Backend-driven search and pagination.** With ~4,450 items, returning the
full dataset to the client on every request isn't practical. Filtering and
paging happen in SQL, so the client only ever receives the data it needs to
render.

**Debounced client-side search.** The frontend waits for a pause in typing
before issuing a request, rather than firing one on every keystroke —
reducing redundant network calls and avoiding out-of-order response races.

**Defensive data handling.** The OSRS Wiki API occasionally omits fields
for a small number of items (missing price data, missing icon mappings,
missing name mappings). Rather than allowing these to crash the ingestion
job, affected items are skipped for that polling cycle rather than inserted
with invalid or partial data.