"""Centralised configuration loaded once at import time."""

from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.absolute()
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "kraken.sqlite"

# Discord
TOKEN: str = getenv("TOKEN", "")
GOD_ID: str = getenv("GOD_ID", "")
COMMAND_PREFIX: str = getenv("COMMAND_PREFIX", "$")

# Logging
LOG_LEVEL: str = getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = getenv("LOG_FORMAT", "json")  # "json" or "text"

# External APIs
ALBION_DATA_BASE_URL: str = getenv(
    "ALBION_DATA_BASE_URL",
    "https://www.albion-online-data.com/api/v2/stats/prices",
)
ALBION_GAMEINFO_BASE_URL: str = getenv(
    "ALBION_GAMEINFO_BASE_URL",
    "https://gameinfo.albiononline.com/api/gameinfo",
)
ALBION_RENDER_BASE_URL: str = getenv(
    "ALBION_RENDER_BASE_URL",
    "https://render.albiononline.com/v1",
)
ITEMS_DUMP_URL: str = getenv(
    "ITEMS_DUMP_URL",
    "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json",
)

# Healthcheck
HEALTH_PORT: int = int(getenv("HEALTH_PORT", "8080"))
