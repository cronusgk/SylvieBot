import discord
import os
import asyncio
import json

from discord.ext import commands
from cogs.apis.mcserverapi import MinecraftServerAPI

api_key = os.getenv("MC_WRAPPER_API")
server_ip = os.getenv("MINECRAFT_SERVER")
server_id = os.getenv("SERVER_ID")

class Minecraft(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.api_service = MinecraftServerAPI(api_key=api_key, server_ip=server_ip)

    @commands.command(name="server")
    async def server(self, ctx):
        
        server_data = await asyncio.to_thread(self.api_service.get_server_info, server_id)
        
        if server_data is None:
            await ctx.send("Error retrieving server information from api.")
            return
        
        server_status = {
            0: "Offline",
            1: "Online"
        }
        
        embed = discord.Embed(
            title="MC Eternal 2 Server Status",
            description=f"The server is currently **{server_status.get(server_data.get("status"), "Unknown")}**."
        )
        embed.set_footer(text=f"Running on version {server_data.get('version', 'N/A')}")
        embed.add_field(name='Server IP', value=server_ip, inline=True)
        embed.add_field(name='Online Players', value=server_data.get("players", 0), inline=True)
        embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='http://tiny.cc/cro-eternal-server')
        
        await ctx.send(embed = embed)
        
    @commands.command(name="startserver")
    async def startserver(self, ctx):
        start = await asyncio.to_thread(self.api_service.start_server, server_id)
        
        await ctx.send("Starting minecraft server!")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Minecraft(bot))
    