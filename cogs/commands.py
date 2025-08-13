import discord

from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def testing(self, ctx):
        embed = discord.Embed(
            title="test"
        )
        embed.set_footer(text=f'this bot is running on {len(self.bot.guilds)}')
        embed.add_field(name='Version', value='0.1', inline=True)
        embed.add_field(name='Language', value='Python 3.8', inline=True)
        embed.set_author(name='nect', url='https://gist.github.com/bynect', icon_url='http://tiny.cc/nect-user-pic')
        await ctx.send(embed = embed)
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
    