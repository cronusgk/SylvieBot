import discord
import logging
import os

from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(os.getenv("GUILD_ID")) 

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "sylvie" and "hi" in message.content:
            await message.channel.send(f"HIII HELLOOOOO {message.author}!")
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))