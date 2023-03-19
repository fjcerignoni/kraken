from os import getenv
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cogs.admin import Admin
from cogs.market import Market
from cogs.raids import Raids
from cogs.profile import Profile
from helpers import get_items
from scheduler import jobs

# load .env 
load_dotenv()
current_path = current_path = Path(__file__).parent.absolute()
db_path = current_path / 'db' / 'kraken.sqlite'

# discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# client = discord.Client(intents=intents)
bot = commands.Bot(
    command_prefix='$',
    intents=intents
)

# events
@bot.event
async def on_ready():

    try:
        ## TODO trabalhar no timestamp para atualização da lista
        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(engine)
        
        # Add Cogs
        await bot.add_cog(Admin(bot, getenv("GOD_ID"), Session))
        await bot.add_cog(Raids(bot, getenv("GOD_ID"), Session))
        await bot.add_cog(Market(bot))
        await bot.add_cog(Profile(bot))

        # Login message in console
        print(f'Logged in as {bot.user}')

    except Exception as e:
        print(e)
        print("Unable to log in")


def failsafe_etl_run():    
    jobs.get_items()


if __name__ == '__main__':
    # TODO gunicorn para substituir o nodemon.

    failsafe_etl_run()

    bot.run(getenv("TOKEN"))