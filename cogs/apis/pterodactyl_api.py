import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PterodactylAPI:
    def __init__(self, client_headers: str, panel: str, admin_headers: str):
        if not client_headers or not admin_headers:
            raise ValueError("Error: must provide headers")
        self.panel = panel
        self.client = client_headers
        self.admin = admin_headers
        self.server_uuids = self.init_server_ids()
        
    def init_server_ids(self) -> dict:
        url = f"https://{self.panel}/api/client"
        try:
            params = {
                'include': 'user,node',
                'per_page': 25,
            }
            response = requests.get(
                url, 
                headers=self.client, 
                params=params
            )
            response.raise_for_status()
            
            servers = {}
            data = response.json()
            
            server_info = data.get("data")
            for server in server_info:
                servers[server["attributes"]["name"]] = server["attributes"]["uuid"]
            
            return servers
        
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    def get_all_servers(self) -> dict:
        url = f"https://{self.panel}/api/client"
        try:
            params = {
                'include': 'user,node',
                'per_page': 25,
            }
            response = requests.get(
                url, 
                headers=self.client, 
                params=params
            )
            response.raise_for_status()
            
            servers = {}
            data = response.json()
            
            server_info = data.get("data")
            for server in server_info:
                server_id = server["attributes"]["name"]
                servers[server_id] = self.get_server_details(server_id)
            
            return servers
        
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    def get_server_details(self, server_id) -> dict:

        details = f"https://{self.panel}/api/client/servers/{self.server_uuids[server_id]}"
        resources = f"https://{self.panel}/api/client/servers/{self.server_uuids[server_id]}/resources"
        server = {"details" : "", "resources": ""}
        
        try:
            details_response = requests.get(
                details, 
                headers=self.client, 
            )
            details_response.raise_for_status()
            
            resources_response = requests.get(
                resources, 
                headers=self.client, 
            )
            resources_response.raise_for_status()
            
            server["details"] = details_response.json().get("attributes")
            server["resources"] = resources_response.json().get("attributes")
            
            return server
            
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    