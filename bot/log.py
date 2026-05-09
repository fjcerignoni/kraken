"""Structured logging with optional correlation id."""

import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar

import settings

# Per-request correlation id
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def new_correlation_id() -> str:
    cid = uuid.uuid4().hex[:12]
    correlation_id.set(cid)
    return cid


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        cid = correlation_id.get("")
        if cid:
            payload["cid"] = cid
        if record.exc_info and record.exc_info[1]:
            payload["exc"] = self.formatException(record.exc_info)
        # Merge extra fields injected via `logger.info("...", extra={...})`
        for key in ("guild_id", "user_id", "command", "duration_ms", "status"):
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        return json.dumps(payload, ensure_ascii=False)


class _TextFormatter(logging.Formatter):
    fmt = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        cid = correlation_id.get("")
        if cid:
            record.msg = f"[{cid}] {record.msg}"
        return super().format(record)


def setup() -> None:
    """Call once at startup to configure the root logger."""
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL.upper())

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_FORMAT == "json":
        handler.setFormatter(_JsonFormatter())
    else:
        handler.setFormatter(_TextFormatter(_TextFormatter.fmt))

    root.handlers.clear()
    root.addHandler(handler)

    # Silence noisy third-party loggers
    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)
    logging.getLogger("discord.client").setLevel(logging.WARNING)
