import pprint
import discord
import os
import asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv
from cogs.apis.pterodactyl_api import PterodactylAPI
from discord import app_commands

load_dotenv()
panel = os.getenv("PANEL")
client = os.getenv("CLIENT_API")
admin = os.getenv("ADMIN_API")

client_headers = {
  'Authorization': f'Bearer {client}',
  'Accept': 'Application/vnd.pterodactyl.v1+json',
  'Content-Type': 'application/json'
}

admin_headers = {
  'Authorization': f'Bearer {admin}',
  'Accept': 'Application/vnd.pterodactyl.v1+json'
}

class Pterodactyl(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.api = PterodactylAPI(client_headers=client_headers, admin_headers=admin_headers, panel=panel)
    
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
                description=f"The server is currently **{info.get("resources").get("current_state")}**.",
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
        
        server_info = await asyncio.to_thread(self.api.get_server_details, server)
        
        if server_info is None:
            await ctx.response.send_message("No server found with that name.")
            return
        
        embed = discord.Embed(
            title=f"{server}",
            description=f"The server is currently **{server_info.get("resources").get("current_state")}**.",
            colour=discord.Colour.green()
        )
        embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
        
        await ctx.response.send_message(embed=embed)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        owner = message.guild.owner
        embeds = message.embeds
        for embed in embeds:
            curr = embed.to_dict()
            if "The server is currently **offline**." in curr["description"]:
                await message.reply(f"{owner.mention} {curr["title"]} is down!") 
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Pterodactyl(bot))
    