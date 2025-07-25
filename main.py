import discord
import logging
import os
from dotenv import load_dotenv
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

COGS = [
    "cogs.events"
]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    for cog in COGS:
        await bot.load_extension(cog)
    await bot.tree.sync()
    
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logging.critical("DISCORD_TOKEN not found in environment.")
        exit(1)
    
    bot.run(DISCORD_TOKEN)
    
    
