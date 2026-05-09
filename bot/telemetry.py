"""Lightweight command telemetry via discord.py listeners.

Emits structured log events:
  command_invoked  – when any prefix or app command starts
  command_succeeded – when it finishes without error
  command_failed   – when it raises
"""

import logging
import time

from discord.ext import commands

import log

logger = logging.getLogger("kraken.telemetry")

# Store invocation start times keyed by (message_id or interaction_id)
_start_times: dict[int, float] = {}


def _ctx_key(ctx: commands.Context) -> int:
    return ctx.message.id


def _extra(ctx: commands.Context, **kwargs) -> dict:
    return {
        "guild_id": getattr(ctx.guild, "id", None),
        "user_id": ctx.author.id,
        "command": ctx.command.qualified_name if ctx.command else "unknown",
        **kwargs,
    }


class TelemetryCog(commands.Cog):
    """Attach to the bot to get automatic command telemetry."""

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        log.new_correlation_id()
        _start_times[_ctx_key(ctx)] = time.monotonic()
        logger.info(
            "command_invoked",
            extra=_extra(ctx, status="invoked"),
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        elapsed = _elapsed(ctx)
        logger.info(
            "command_succeeded",
            extra=_extra(ctx, status="succeeded", duration_ms=elapsed),
        )

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        elapsed = _elapsed(ctx)
        logger.error(
            "command_failed",
            extra=_extra(ctx, status="failed", duration_ms=elapsed),
            exc_info=error,
        )


def _elapsed(ctx: commands.Context) -> int:
    start = _start_times.pop(_ctx_key(ctx), None)
    if start is None:
        return -1
    return int((time.monotonic() - start) * 1000)
