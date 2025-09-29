import discord
import os
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from cogs.apis.pterodactylApi import PterodactylAPI
from discord import app_commands

load_dotenv()
panel = os.getenv("PANEL")
api_key = os.getenv("PTERODACTYL_API")

headers = {
  'Authorization': f'Bearer {api_key}',
  'Accept': 'Application/vnd.pterodactyl.v1+json',
  'Content-Type': 'application/json'
}

class Pterodactyl(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.api = PterodactylAPI(api_key=api_key, headers=headers, panel=panel)
    
    @app_commands.command(name="servers", description="Shows all hosted servers")
    async def allServers(self, ctx):
        
        servers = await asyncio.to_thread(self.api.get_all_servers)
        
        if len(servers) is None:
            await ctx.send("Error retrieving server information from api.")
            return
        
        embeds = []
        for server, info in servers.items():
            embed = discord.Embed(
                title=f"{server}",
                description=f"The server is currently **{info.get("attributes").get("status")}**.",
                colour=discord.Colour.green()
            )
            embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
            embeds.append(embed)
        await ctx.response.send_message(embed=embeds[0])
        embeds.remove(embeds[0])
        for embed in embeds:
            await ctx.followup.send(embed=embed)
    
    @app_commands.command(name="server", description="Shows specified server")
    async def server(self, ctx, server: str):
        
        server_info = await asyncio.to_thread(self.api.get_server, server)
        
        if server_info is None:
            await ctx.response.send_message("No server found with that name.")
            return
        
        embed = discord.Embed(
            title=f"{server}",
            description=f"The server is currently **{server_info.get("attributes").get("status")}**.",
            colour=discord.Colour.green()
        )
        embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
        
        await ctx.response.send_message(embed=embed)
        
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Pterodactyl(bot))
    