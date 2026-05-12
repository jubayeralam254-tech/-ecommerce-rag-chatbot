# FastAPI Google Maps Scraper

Professional FastAPI project that scrapes business listings from Google Maps and exposes them via a REST API backed by PostgreSQL.

**Project description**

This service performs targeted scraping of Google Maps search results (by city and category), persists business records to a PostgreSQL database using SQLAlchemy, and exposes the data via a small FastAPI JSON API.

**Tech stack**

- FastAPI — HTTP API framework
- SQLAlchemy — ORM for PostgreSQL
- PostgreSQL — production datastore
- Playwright — browser automation for scraping
- Pydantic — request/response validation
- Uvicorn — ASGI server

**Repository files**

- [app/main.py](app/main.py) — FastAPI application and endpoints
- [app/models.py](app/models.py) — SQLAlchemy models
- [app/database.py](app/database.py) — DB engine and session
- [app/scraper.py](app/scraper.py) — Playwright scraper implementation
- [app/schemas.py](app/schemas.py) — Pydantic request/response schemas
- [requirements.txt](requirements.txt) — Python dependencies
- [.env.example](.env.example) — example environment variables

**Endpoints**

- GET /businesses
  - Query params (optional): `city`, `category`
  - Returns: list of businesses filtered by optional parameters
  - Example:

```http
GET /businesses?city=Boston&category=Restaurant
Accept: application/json
```

- POST /scrape
  - Request body: `{ "city": "<city>", "category": "<category>" }`
  - Starts a synchronous Playwright scrape for the given city + category, persists new businesses, and returns counts.
  - Response: `{ "scraped_count": int, "created_count": int, "skipped_count": int }`
  - Example:

```http
POST /scrape
Content-Type: application/json

{
  "city": "San Francisco",
  "category": "coffee shop"
}
```

**Setup & Run**

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Copy environment example and set your PostgreSQL `DATABASE_URL`:

```bash
copy .env.example .env
# then edit .env to point to your Postgres instance, e.g.:
# DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/business_db
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browser binaries (required):

```bash
python -m playwright install chromium
```

5. Ensure PostgreSQL is running and the database referenced in `DATABASE_URL` exists. Create it if necessary:

```sql
-- Example (psql):
CREATE DATABASE business_db;
```

6. Start the FastAPI server (development):

```bash
uvicorn app.main:app --reload
```

7. Open the interactive docs at `http://127.0.0.1:8000/docs` to exercise endpoints.

**Notes & considerations**

- The scraper uses Playwright to control a headless browser. Scraping Google Maps may be fragile: selectors can change and Google may block automated requests. Use responsibly and respect Google Terms of Service.
- The scraper runs synchronously in the current implementation and will block the worker handling the request until the scrape completes. For production use, consider running scraping tasks asynchronously via a background worker (Celery, RQ, or FastAPI BackgroundTasks) or queueing system.
- The database schema is created on startup using SQLAlchemy `Base.metadata.create_all()` in `app/main.py`.

**Optional improvements**

- Add a `POST /businesses` endpoint to insert single records.
- Add unit tests and CI configuration.
- Provide a `docker-compose.yml` to run the API + PostgreSQL for local development.

---

If you'd like, I can also add a small seed script, a `docker-compose.yml`, or convert the synchronous scraper into a background task for non-blocking behavior.