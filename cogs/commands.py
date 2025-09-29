import os
import discord

from discord.ext import commands
from discord import app_commands

GUILD_ID = os.getenv("GUILD_ID")
DISCORD_ID = os.getenv("DISCORD_ID")

class Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
    