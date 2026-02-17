import datetime
import logging
import discord
import os
import asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv
from cogs.apis.pterodactyl_api import PterodactylAPI
from discord import app_commands

load_dotenv()
panel = f'https://{os.getenv("PANEL")}'
client = os.getenv("CLIENT_API")
admin = os.getenv("ADMIN_API")
utc = datetime.timezone.utc
owner_id = os.getenv("DISCORD_ID")

class Pterodactyl(commands.Cog):
    
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.api = PterodactylAPI(panel=panel, client_key=client, admin_key=admin)
    
    async def cog_load(self):
        logging.info(f'Fetching server IDs')
        await self.api.setup()
        await self.start_loops()
        logging.info(f'Fetched {len(self.api.server_uuids)} server IDs')

    async def start_loops(self):
        self.checkServers.start()
        self.restartDaily.start()

    @tasks.loop(hours=1.0)
    async def checkServers(self):
        
        servers = await self.api.get_all_servers()
        channel = self.bot.get_channel(1353220559931965472)
        if len(servers) is None:
            await channel.send("Error retrieving server information from api.")
            return
        
        for name, data in servers.items():
            
            resources = data.get("resources", {})
            state = resources.get("current_state", "offline")
            color = discord.Colour.green() if state == "running" else discord.Colour.red()
            
            embed = discord.Embed(
                title=f"{name}",
                description=f"The server is currently **{state}**.",
                colour=color
            )
            embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
            
            if channel:
                await channel.send(embed=embed)
                await asyncio.sleep(0.5)
    
    @tasks.loop(time=datetime.time(hour=11, minute=00, tzinfo=datetime.timezone.utc))
    async def restartDaily(self):
        servers = await self.api.get_all_servers()
        for name, data in servers.items():
            resources = data.get("resources")
            state = resources.get("current_state", "offline")
            if state == "running":
                await self.api.restart_server(name)
            else:
                continue
    
    @app_commands.command(name="servers", description="Shows all hosted servers")
    async def allServers(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.delete_original_response()
        
        servers = await self.api.get_all_servers()
        channel = self.bot.get_channel(1353220559931965472)
        if len(servers) is None:
            await channel.send("Error retrieving server information from api.")
            return
        
        for name, data in servers.items():
            
            resources = data.get("resources", {})
            state = resources.get("current_state", "offline")
            color = discord.Colour.green() if state == "running" else discord.Colour.red()
            
            embed = discord.Embed(
                title=f"{name}",
                description=f"The server is currently **{state}**.",
                colour=color
            )
            embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
            
            if channel:
                await channel.send(embed=embed)
                await asyncio.sleep(0.5)
    
    @app_commands.command(name="server", description="Shows specified server")
    async def server(self, ctx: commands.Context, server: str):
        await ctx.response.defer()
        
        server = server.capitalize()
        server_info = await self.api.get_server_details(server)
        
        if server_info is None:
            await ctx.followup.send("No server found with that name.")
            return
        
        res = server_info.get("resources", {})
        state = res.get("current_state", "offline")
        
        embed = discord.Embed(
            title=f"{server}",
            description=f"The server is currently **{state}**.",
            colour=discord.Colour.blue()
        )
        embed.set_author(name='cronusgk', url='https://github.com/cronusgk', icon_url='https://tinyurl.com/pterodactylcronus') 
        
        await ctx.followup.send(embed=embed)
        
    """  @commands.Cog.listener()
        async def on_message(self, message: discord.message):
            owner = await self.bot.fetch_user(owner_id)
            embeds = message.embeds
            for embed in embeds:
                curr = embed.to_dict()
                if "The server is currently **offline**." in curr["description"]:
                    await asyncio.sleep(2)
                    await message.reply(f"{owner.mention} {curr["title"]} is down!")  """
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Pterodactyl(bot))
    