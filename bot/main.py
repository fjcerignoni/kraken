import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from market import Market

# load .env with TOKEN value
load_dotenv()
currentPath = os.path.dirname(os.path.realpath(__file__))

# discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# client = discord.Client(intents=intents)
bot = commands.Bot(
    command_prefix='$',
    intents=intents
)

# events
@bot.event
async def on_ready():
    # Login message in console
    print(f'Logged in as {bot.user}')

    # Add Cogs
    await bot.add_cog(Market(bot))

    # guild = bot.get_guild(1022920500919410709)
    # memberList = guild.members

    # print(guild)
    # for member in memberList:
    #     m = await guild.fetch_member(member.id)
    #     print(m.nick)

if __name__ == '__main__':
    bot.run(os.getenv("TOKEN"))