from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import discord
from discord.ext import commands

from helpers import get_items
from cogs.admin import Admin
from cogs.market import Market
from cogs.raids import Raids

# load .env with TOKEN value
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

# reactions form raid embeds.
reaction_list = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8",
        "\U0001F1E9", "\U0001F1EA", "\U0001F1EB", "\U0001F1EC",
        "\U0001F1ED", "\U0001F1EE",  "\U0001F1F0",
        "\U0001F1F1", "\U0001F1F2", "\U0001F1F3", "\U0001F1F4",
        "\U0001F1F5", "\U0001F1F6", "\U0001F1F7", "\U0001F1F8",
        "\U0001F1F9", "\U0001F1FA" ] # J: "\U0001F1EF"

# events
@bot.event
async def on_ready():

    try:
        ## TODO trabalhar no timestamp para atualização da lista
        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(engine)
        
        # Add Cogs
        await bot.add_cog(Admin(bot, getenv("GOD_ID"), Session))
        await bot.add_cog(Raids(bot, getenv("GOD_ID"), Session, reaction_list))
        await bot.add_cog(Market(bot))
        
        # Login message in console
        print(f'Logged in as {bot.user}')

    except Exception as e:
        print(e)
        print("Unable to log in")


if __name__ == '__main__':
    # TODO gunicorn para substituir o nodemon.
    bot.run(getenv("TOKEN"))