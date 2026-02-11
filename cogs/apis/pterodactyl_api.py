import requests
import urllib3
import asyncio
from pydactyl import AsyncPterodactylClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PterodactylAPI:
    def __init__(self, panel: str,client_key: str, admin_key: str):
        if not client_key or not admin_key:
            raise ValueError("Error: must provide headers")
        self.panel = panel
        self.client = AsyncPterodactylClient(self.panel, client_key)
        self.admin = AsyncPterodactylClient(self.panel, admin_key)
        self.server_uuids = {}
        
    async def setup(self):
        self.server_uuids = await self.init_server_ids()        
        
    async def init_server_ids(self) -> dict:            
        try:
            servers = await self.client.client.servers.list_servers()
            ids = {}
            for page in servers:
                for server in page:
                        name = server["attributes"]["name"]
                        identifier = server["attributes"]["identifier"]
                        ids[name] = identifier
            
            self.server_uuids = ids
            return ids
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
         
        
    async def get_all_servers(self) -> dict:
        try: 
            servers = {}
            for name in self.server_uuids:
                info = await self.get_server_details(name)
                if info: 
                    servers[name] = info
            return servers
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
        
    async def get_server_details(self, server_id) -> dict:
        try: 
            server = self.server_uuids[server_id]
            details = await self.client.client.servers.get_server(server)
        
            resources = None
            try:
                resources = await self.client.client.servers.get_server_utilization(server)
            except Exception as e:
                if "409" in str(e):
                    resources = {"status": "busy", "message": "Server is installing/busy"}
                else:
                    print(f"Non-409 error fetching stats for {server_id}: {e}")
        
            server_info = {"details" : details, "resources": resources}
            
            return server_info
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
            
        
    async def restart_server(self, server_id) -> None:
        server = self.server_uuids[server_id]
        await self.client.client.servers.send_console_command(server, 'say Server is restarting')
        if(server_id == "Mayview"):
            await asyncio.sleep(10)
            await self.client.client.servers.send_power_action(server, 'stop')
            await asyncio.sleep(5)
            await self.client.client.servers.send_console_command(server, 'stop')
            await asyncio.sleep(3)
            await self.client.client.servers.send_power_action(server, 'start') 
        else:
            await self.client.client.servers.send_power_action(server, 'restart') 
        

        