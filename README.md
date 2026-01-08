# Tic Tac Toe (Flask)

This repo contains a small Flask application and a `docker-compose` setup to run the app together with MySQL.

Prerequisites
- Docker (with Compose)
- `.env` present in project root with `MYSQL_*` values (example provided in repo)

Build & run (detached)
```bash
docker compose up --build -d
```

Follow logs (web)
```bash
docker compose logs -f web
```

Stop and remove containers + volumes
```bash
docker compose down -v
```

Notes
- The web service binds to port `8000` (http://localhost:8000).
- Compose will read `MYSQL_DB`, `MYSQL_USER`, and `MYSQL_PASSWORD` from the `.env` file in the project root.
- If you need an interactive shell inside the running web container:
```bash
docker compose exec web /bin/sh
```
- If you prefer to run without Compose, build the image then run it and ensure it can reach a MySQL instance.
