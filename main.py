import discord
import logging
import os 
from dotenv import load_dotenv
from discord.ext import commands, tasks
from os import listdir

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
GUILD_ID = os.getenv("GUILD_ID")

COGS = [
    "cogs.events",
    "cogs.commands",
    "cogs.minecraft"
]

bot = commands.Bot(command_prefix='!', description=description, intents=discord.Intents.all())

if __name__ == '__main__':
    if not DISCORD_TOKEN:
        logging.critical("DISCORD_TOKEN not found in environment.")
        exit(1)
    

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    for cog in COGS:
        await bot.load_extension(cog)
        
    try:
        guild = discord.Object(GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        logging.info(f"{len(synced)} commands loaded!")
        
    except Exception as e:
        logging.critical(f"Error syncing commands: {e}")
    
    
bot.run(DISCORD_TOKEN)
