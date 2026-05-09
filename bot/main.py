import logging

import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import health
import log
import settings
from cogs.admin import Admin
from cogs.market import Market
from cogs.raids import Raids
from cogs.profile import Profile
from scheduler import jobs
from telemetry import TelemetryCog

# Bootstrap structured logging before anything else
log.setup()
logger = logging.getLogger("kraken")

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=settings.COMMAND_PREFIX,
    intents=intents,
)


@bot.event
async def on_ready():
    try:
        engine = create_engine(f"sqlite:///{settings.DB_PATH}")
        Session = sessionmaker(engine)

        # Core cogs
        await bot.add_cog(Admin(bot, settings.GOD_ID, Session))
        await bot.add_cog(Raids(bot, settings.GOD_ID, Session))
        await bot.add_cog(Market(bot))
        await bot.add_cog(Profile(bot))

        # Telemetry cog (command_invoked / succeeded / failed)
        await bot.add_cog(TelemetryCog())

        # Health-check HTTP server
        await health.start(bot)

        logger.info("Logged in as %s", bot.user)

    except Exception:
        logger.exception("Unable to start bot")


def failsafe_etl_run():
    jobs.get_items()


if __name__ == "__main__":
    failsafe_etl_run()
    bot.run(settings.TOKEN, log_handler=None)  # logging managed by log.setup()