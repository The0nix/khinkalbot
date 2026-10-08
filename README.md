To run: 

```
uv run khinkalbot start
```

For admin console:

```
uv run khinkalbot admin
```

## Docker

Copy `.env.example` to `.env` and fill it in (plain `KEY=value` lines, no `export`), then:

```
docker compose run --rm bot init   # first run only: creates the database
docker compose up -d --build
```

The database is stored in `./data/users_data.db`. To keep an existing database, move it there before starting.

The admin console is optional:

```
docker compose --profile admin up -d
```

## Configuration

Env variables to set:
- `BOT_TOKEN`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_SECRET_KEY`
- `ADMIN_PORT`
