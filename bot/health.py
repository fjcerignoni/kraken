"""Minimal async HTTP health-check server.

Runs alongside the bot on HEALTH_PORT (default 8080).
GET /health  -> 200 {"status": "ok"}  when the bot is connected
GET /health  -> 503 {"status": "not_ready"} otherwise
"""

import asyncio
import json
import logging
from http import HTTPStatus

import discord

import settings

logger = logging.getLogger("kraken.health")


async def start(bot: discord.Client) -> None:
    """Start the health-check server in the background."""

    async def _handle(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            await reader.readuntil(b"\r\n\r\n")
        except asyncio.IncompleteReadError:
            pass

        if bot.is_ready() and not bot.is_closed():
            status = HTTPStatus.OK
            body = {"status": "ok", "user": str(bot.user)}
        else:
            status = HTTPStatus.SERVICE_UNAVAILABLE
            body = {"status": "not_ready"}

        payload = json.dumps(body).encode()
        writer.write(
            f"HTTP/1.1 {status.value} {status.phrase}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(payload)}\r\n"
            f"\r\n".encode()
            + payload
        )
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(_handle, "0.0.0.0", settings.HEALTH_PORT)
    logger.info("health-check listening on :%s", settings.HEALTH_PORT)
    asyncio.ensure_future(server.serve_forever())
