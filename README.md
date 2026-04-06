# Coilcast

> **Note:** This project is under active development and is not production-ready yet.

Coilcast is an in-progress self-hosted music streaming server that targets compatibility with the Subsonic REST API (`1.16.1`).

The project scans a local music library, extracts metadata, stores it in a database, and serves Subsonic-compatible endpoints for browsing and streaming tracks.

## Current Status

Implemented today:

- FastAPI-based HTTP service
- Subsonic-compatible routing under `/rest`
- Library scan and metadata sync from filesystem
- Streaming endpoint for indexed tracks
- Database backends:
  - `SQLITE` (default)
  - `POSTGRESQL`

Supported audio extensions in the current scanner:

- `.flac`
- `.mp3`
- `.ogg`
- `.wav`

## Tech Stack

- Python `3.14`
- FastAPI + Uvicorn
- SQLAlchemy (async)
- `aiosqlite` and `asyncpg`
- Mutagen for audio metadata
- Docker

## Project Structure

- `src/main.py`: application entrypoint and startup endpoints
- `src/presentation/api/subsonic/routers`: Subsonic endpoints
- `src/application/services`: library scanner + sync logic
- `src/infrastructure/database`: DB engine, models, sessions
- `music/`: local library mount point for development

## Configuration

Copy example environment file and adjust values:

```bash
cp env.example .env
```

Main variables:

```env
ADMIN_LOGIN=admin
ADMIN_PASS=changeme
MUSIC_FOLDER=./music
HTTP_PORT=8080
DEBUG_MODE=False

DB_TYPE=SQLITE          # SQLITE or POSTGRESQL
DB_NAME=coilcast

# Required only for POSTGRESQL
DB_USER=coilcast
DB_PASS=coilcast
DB_HOST=postgres
DB_PORT=5432
```

## Run Locally

### 1. Create environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure database mode

#### Option A: SQLite (default)

In `.env`:

```env
DB_TYPE=SQLITE
DB_NAME=coilcast
```

This creates/uses `coilcast.db` in the project root.

#### Option B: PostgreSQL

In `.env`:

```env
DB_TYPE=POSTGRESQL
DB_NAME=coilcast
DB_USER=coilcast
DB_PASS=coilcast
DB_HOST=127.0.0.1
DB_PORT=5432
```

Make sure PostgreSQL is running and credentials are valid.

### 3. Start the app

```bash
python src/main.py
```

Service will listen on `http://0.0.0.0:${HTTP_PORT}` (default `8080`).

### 4. Initialize schema and perform first library sync

After startup, call:

```bash
curl -X POST "http://127.0.0.1:8080/setup_database"
```

This creates DB tables and runs an initial metadata sync from `MUSIC_FOLDER`.

## Run with Docker (SQLite)

`docker-compose.yaml` tuned for SQLite:

```
services:
  coilcast:
    image: coilcast:latest
    build: .
    container_name: coilcast-app
    ports: 
      - "${HTTP_PORT}:8080"
    environment:
      # Coilcast application settings
      ADMIN_LOGIN: "${ADMIN_LOGIN}"
      ADMIN_PASS: "${ADMIN_PASS}"
      MUSIC_FOLDER: "${MUSIC_FOLDER}"
      DEBUG_MODE: "${DEBUG_MODE}"
      HTTP_PORT: "${HTTP_PORT}"
      # Database settings
      DB_TYPE: "${DB_TYPE}"
      DB_NAME: "${DB_NAME}"
    volumes:
      - ./music:/app/music
      - ./coilcast.db:/app/coilcast.db
    restart: unless-stopped
```

1. Prepare `.env` with SQLite values (`DB_TYPE=SQLITE`).
2. Ensure your local `music/` directory contains audio files.
3. Start services:

```bash
docker compose up --build -d
```

Mounted volumes in this mode:

- `./music -> /app/music`
- `./coilcast.db -> /app/coilcast.db`

Initialize DB and scan library:

```bash
curl -X POST "http://127.0.0.1:${HTTP_PORT}/setup_database"
```

## Run with Docker (PostgreSQL)

`docker-compose.yaml` tuned for PostgreSQL:

```
services:
  coilcast:
    image: coilcast:latest
    build: .
    container_name: coilcast-app
    ports: "${HTTP_PORT}:8080"
    environment:
      # Coilcast application settings
      ADMIN_LOGIN: "${ADMIN_LOGIN}"
      ADMIN_PASS: "${ADMIN_PASS}"
      MUSIC_FOLDER: "${MUSIC_FOLDER}"
      DEBUG_MODE: "${DEBUG_MODE}"
      HTTP_PORT: "${HTTP_PORT}"
      # Database settings
      DB_TYPE: "${DB_TYPE}"
      DB_NAME: "${DB_NAME}"
      DB_USER: "${DB_USER}"
      DB_PASS: "${DB_PASS}"
      DB_HOST: "${DB_HOST}"
      DB_PORT: "${DB_PORT}"
    volumes:
      - ./music:/app/coilcast/music
    networks:
      - coilcast
    restart: unless-stopped

  postgres:
    image: postgres:latest
    container_name: coilcast-db
    environment:
      POSTGRES_USER: "${DB_USER}"
      POSTGRES_PASSWORD: "${DB_PASS}"
      POSTGRES_DB: "${DB_NAME}"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - coilcast
    restart: unless-stopped
    
networks:
  coilcast:
    driver: bridge

volumes:
  postgres-data:
```

### Example compose pattern (recommended)

Use a stack with two services (`coilcast` + `postgres`) and set:

```env
DB_TYPE=POSTGRESQL
DB_NAME=coilcast
DB_USER=coilcast
DB_PASS=coilcast
DB_HOST=postgres
DB_PORT=5432
```

Then:

```bash
docker compose up --build -d
curl -X POST "http://127.0.0.1:${HTTP_PORT}/setup_database"
```

## Makefile Shortcuts

Available helper targets:

- `make python-venv` - create virtual environment and install deps
- `make run` - run app locally
- `make docker` - build image
- `make up` - build + run compose stack
- `make logs` - follow logs
- `make stop` - stop containers
- `make down` - tear down stack

## Subsonic Compatibility Notes

Base API prefix:

- `/rest`

Examples:

- `/rest/ping`
- `/rest/getLicense`
- `/rest/getArtists`
- `/rest/getArtist`
- `/rest/getAlbum`
- `/rest/getSong`
- `/rest/getMusicFolders`
- `/rest/getMusicDirectory`
- `/rest/stream`
- `/rest/startScan`
- `/rest/getScanStatus`

Auth supports Subsonic query parameters:

- username: `u`
- client + version: `c`, `v`
- either legacy password `p` (including `enc:` style) or token auth `t` + `s`

## TODO (Short)

- Expand Subsonic API coverage (playlists, search, user-facing library actions, richer metadata endpoints).
- Improve API behavior parity and compatibility testing against real Subsonic clients.
- Implement robust `.cue` parsing for split-image albums with correct virtual track mapping.
- Add migration workflow, test coverage, and CI checks.
