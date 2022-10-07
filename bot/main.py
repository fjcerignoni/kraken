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

# events
@bot.event
async def on_ready():
    # Login message in console

    try:
            ## TODO trabalhar no timestamp para atualização da lista
        item_list = await get_items()
        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(engine)
        
        # Add Cogs
        await bot.add_cog(Admin(bot, Session))
        await bot.add_cog(Market(bot, item_list))

        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(e)
        print("Unable to log in")

if __name__ == '__main__':
    bot.run(getenv("TOKEN"))