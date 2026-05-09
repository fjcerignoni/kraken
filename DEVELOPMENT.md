# Development Guide

## Project Status

**Current Version:** 0.1.0 (Phase 0 complete)  
**Python:** ≥3.10  
**Status:** Foundation layer implemented and Docker-validated

---

## Quick Start

```bash
# Setup environment
uv sync

# Run locally
uv run python bot/main.py

# Build and deploy
./build.sh

# Healthcheck
curl http://localhost:8080/health
```

---

## What's Implemented (Phase 0 ✅)

### Core Infrastructure
- ✅ `bot/settings.py` — Centralized config from environment variables
- ✅ `bot/log.py` — Structured JSON logging with correlation IDs
- ✅ `bot/telemetry.py` — Automatic command telemetry (invoked/succeeded/failed)
- ✅ `bot/health.py` — Async HTTP health-check endpoint on port 8080

### Integration
- ✅ `bot/main.py` — Rewired to use settings, logging, telemetry, health
- ✅ All cogs (`admin.py`, `market.py`, `profile.py`, `raids.py`) — Migrated to logger
- ✅ `bot/helpers.py` — 10× print(e) replaced with logger.exception()

### Deployment
- ✅ `pyproject.toml` + `uv.lock` — Dependency management via uv
- ✅ `Dockerfile` — Multi-stage, Python 3.12-slim, uv sync
- ✅ `bot/scheduler/Dockerfile` — Same pattern
- ✅ `build.sh` — Deploy helper with versioned tags (0.1.0)

### Documentation
- ✅ `MODERNIZACAO_BOT_BLUEPRINT.md` — Strategic roadmap (90 days)
- ✅ This file — Developer reference

---

## Architecture Overview

```
kraken/
├── bot/
│   ├── main.py                 # Entry point + cog loader
│   ├── settings.py             # Config from .env
│   ├── log.py                  # Structured logging (JSON)
│   ├── telemetry.py            # Command event tracking
│   ├── health.py               # GET /health async server
│   ├── helpers.py              # API calls (Albion, Discord)
│   ├── data_models.py          # Pydantic models
│   ├── db/
│   │   ├── kraken.sqlite       # Local DB (to migrate to PG)
│   │   ├── kraken_schema.sql
│   │   └── raid_templates/     # JSON per-guild
│   ├── cogs/
│   │   ├── admin.py
│   │   ├── market.py
│   │   ├── profile.py
│   │   └── raids.py
│   └── scheduler/
│       ├── jobs.py
│       ├── scheduler.py
│       ├── Dockerfile
│       └── supervisord.conf
├── pyproject.toml              # uv project definition
├── uv.lock                     # Locked dependency tree
├── Dockerfile                  # Main bot image
├── build.sh                    # Deploy script
├── DEVELOPMENT.md              # ← You are here
├── MODERNIZACAO_BOT_BLUEPRINT.md
└── README.md
```

---

## Running Locally

### Environment Setup
```bash
# Create .env with:
TOKEN=your_discord_bot_token
GOD_ID=your_discord_user_id
COMMAND_PREFIX=$
LOG_LEVEL=INFO
LOG_FORMAT=json
HEALTH_PORT=8080
```

### Commands
```bash
# Sync dependencies
uv sync

# Run bot
uv run python bot/main.py

# Run specific module
uv run python -c "import bot.settings; print(bot.settings.DB_PATH)"

# Interactive Python in project context
uv run python
```

---

## Docker & Deployment

### Build
```bash
# Main bot image
docker build -t kraken-bot:phase0 .

# Scheduler image
docker build -t kraken-scheduler:phase0 -f bot/scheduler/Dockerfile .

# Using deploy script
./build.sh  # Builds 0.1.0 and runs it
```

### Deploy Script (`build.sh`)
- Builds image tag `kraken-image:0.1.0`
- Creates persistent DB volume `kraken-db`
- Mounts DB at `/opt/kraken/bot/db`
- Publishes healthcheck port `8080:8080`
- Auto-restarts on crash

### Validate
```bash
# Smoke test (all imports)
docker run --rm kraken-bot:phase0 python -c \
  "import sys; sys.path.insert(0, '/opt/kraken/bot'); \
  import settings, log, health, telemetry, helpers; \
  from cogs.admin import Admin; from cogs.market import Market; \
  from cogs.raids import Raids; from cogs.profile import Profile; \
  log.setup(); print('ALL IMPORTS OK')"

# Healthcheck
curl http://localhost:8080/health

# Should output:
# {"status":"ok","user":"Kraken#1234"}
```

---

## Logging & Observability

### Structured Log Format (JSON)
```json
{
  "ts": "2026-05-09T15:07:56",
  "level": "INFO",
  "logger": "kraken.admin",
  "msg": "command_invoked",
  "cid": "a1b2c3d4e5f6",
  "guild_id": 123456789,
  "user_id": 987654321,
  "command": "price",
  "duration_ms": 45,
  "status": "succeeded"
}
```

### Environment Variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `LOG_LEVEL` | INFO | DEBUG, INFO, WARNING, ERROR |
| `LOG_FORMAT` | json | json or text |
| `HEALTH_PORT` | 8080 | Healthcheck server port |

---

## Known Issues

### Locale Error (Non-blocking)
**Symptom:**  
```
locale.Error: unsupported locale setting
```

**Cause:**  
Local dev machine doesn't have `pt_BR.UTF-8` installed. Affects `bot/cogs/market.py` and `bot/cogs/profile.py` when run outside Docker.

**Status:**  
✅ Not a regression. Works fine in Docker (locales installed in image).

**Workaround:**  
- Use Docker for testing
- Or install locale on host: `sudo locale-gen pt_BR.UTF-8`

---

## Next Steps (Phase 1)

**Target:** Migrate to slash commands + improve UX

**Priority 1 (Week 1-2):**
- [ ] Migrate `/price` command to slash command with autocomplete
- [ ] Add `/setup` onboarding command
- [ ] Log telemetry events to dashboard

**Priority 2 (Week 3-4):**
- [ ] Migrate `/organize_raid` to modal-based flow
- [ ] Add retry logic + backoff to external API calls
- [ ] Implement rate limiting per guild

**Success Metric:**
- Command success rate > 99%
- P95 latency < 500ms

See [MODERNIZACAO_BOT_BLUEPRINT.md](MODERNIZACAO_BOT_BLUEPRINT.md) for full 90-day roadmap.

---

## Testing

### Unit Tests
```bash
# Not yet implemented
# Recommended: pytest + fixtures for Discord.py
```

### Integration Tests
```bash
# Smoke test (imports)
uv run python -c "import bot.main"

# In Docker
docker run --rm kraken-bot:phase0 python -c "import bot.main; print('OK')"
```

### Manual Testing
1. Invite bot to test server
2. Run command: `$price item_name`
3. Check logs via healthcheck + `/health` endpoint
4. Verify JSON logs in stdout

---

## File Reference

| File | Purpose | Last Modified |
|------|---------|----------------|
| `bot/settings.py` | Config loader | Phase 0 |
| `bot/log.py` | JSON logging + correlation ID | Phase 0 |
| `bot/telemetry.py` | Command telemetry events | Phase 0 |
| `bot/health.py` | HTTP healthcheck server | Phase 0 |
| `bot/main.py` | Bot entry point + cog loader | Phase 0 |
| `bot/helpers.py` | API helpers (Albion, Discord) | Phase 0 |
| `pyproject.toml` | uv project config | Phase 0 |
| `Dockerfile` | Main bot image | Phase 0 |
| `build.sh` | Deploy helper | Phase 0 |

---

## Troubleshooting

### Import Error: `No module named 'settings'`
**Solution:** Run with `uv run python` or ensure `bot/` is in PYTHONPATH

### Docker Build Fails: `locales not found`
**Cause:** Base image changed. Current: `python:3.12-slim` includes locales package.

### Healthcheck Returns 503
**Cause:** Bot not ready yet (starting). Wait a few seconds and retry.

---

## Team Handoff Notes

### For Next Developer
- Phase 0 is **complete** ✅
- Treat version `0.1.0` as stable baseline
- Start with Phase 1 (slash commands)
- Use this guide to onboard, then update as you progress
- Keep MODERNIZACAO_BOT_BLUEPRINT.md as source of truth for product decisions

### Environment Assumptions
- Python 3.10+ (3.12 in Docker)
- Discord.py 2.x with prefix commands (legacy, being modernized)
- SQLite locally (migrate to PostgreSQL in Phase 2)
- Docker for production deployment

---

## Resources

- **Discord.py Docs:** https://discordpy.readthedocs.io/
- **App Commands Guide:** https://discordpy.readthedocs.io/en/latest/interactions/slash_commands.html
- **Albion Online APIs:** Used in `bot/helpers.py`
- **uv Package Manager:** https://docs.astral.sh/uv/

---

*Last updated: 2026-05-09*
