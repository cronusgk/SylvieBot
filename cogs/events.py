import discord
import logging
import os

from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "sylvie" in message.content and "hi" in message.content:
            print("Found message to me")
            await message.channel.send(f"HIII HELLOOOOO {message.author}!")
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))