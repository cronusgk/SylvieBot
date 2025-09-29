import discord
import os
import asyncio

from discord.ext import commands
from cogs.apis.pterodactyl_api import MinecraftServerAPI

api_key = os.getenv("MC_WRAPPER_API")
server_ip = os.getenv("MINECRAFT_SERVER")
server_id = os.getenv("SERVER_ID")
public_ip = os.getenv("PUBLIC_IP")

class Minecraft(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.api = MinecraftServerAPI(api_key=api_key, server_ip=server_ip, public_ip=public_ip)

    @commands.command(name="server")
    async def server(self, ctx):
        
        server_data = await asyncio.to_thread(self.api_service.get_server_info, server_id)
        server_version = await asyncio.to_thread(self.api_service.get_server_version)
        
        if server_data is None:
            await ctx.send("Error retrieving server information from api.")
            return
        
        server_status = {
            0: "Offline",
            1: "Online"
        }
        
        embed = discord.Embed(
            title=f"{server_data.get("name", "Minecraft Server")}",
            description=f"The server is currently **{server_status.get(server_data.get("status"), "Unknown")}**.",
            colour=discord.Colour.green()
        )
        embed.set_footer(text=f"Running on version {server_version}")
        embed.add_field(name='Server IP', value=public_ip, inline=True)
        embed.add_field(name='Online Players', value=server_data.get("players", 0), inline=True)
        embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='http://tiny.cc/cro-eternal-server')
        
        await ctx.send(embed = embed)
        
    @commands.command(name="startserver")
    async def startserver(self, ctx):
        start = await asyncio.to_thread(self.api_service.start_server, server_id)
        
        await ctx.send("Starting minecraft server!")
        
    @commands.command(name="restartserver")
    async def restartserver(self, ctx):
        start = await asyncio.to_thread(self.api_service.restart_server, server_id)
        
        await ctx.send("Restarting minecraft server!")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Minecraft(bot))
    