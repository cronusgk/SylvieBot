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
GUILD_ID = os.getenv("GUILD_ID")
DISCORD_ID = os.getenv("DISCORD_ID")


COGS = [
    "cogs.events",
    "cogs.commands",
    "cogs.pterodactyl"
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
    
@bot.command(name="sync") 
async def sync(self):
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s).")

@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context):
    for cog in COGS:
        await bot.reload_extension(cog)
        embed = discord.Embed(title='Reload', description=f'{cog} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)
    embed = discord.Embed(title='Reload', description=f'all cogs successfully reloaded', color=0xf000c8)
    await ctx.send (embed=embed)
    
bot.run(DISCORD_TOKEN)
