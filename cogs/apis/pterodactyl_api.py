import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PterodactylAPI:
    def __init__(self, api_key: str, headers: str, panel):
        if not api_key or not headers:
            raise ValueError("Error: must provide api key and headers")
        self.api_key = api_key
        self.panel = panel
        self.headers = headers
        
    def get_all_servers(self) -> dict:
        url = f"https://{self.panel}/api/client"
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
            )
            response.raise_for_status()
            
            servers = {}
            data = response.json()
            
            server_info = data.get("data")
            for server in server_info:
                server_id = server["attributes"]["uuid"]
                servers[server["attributes"]["name"]] = self.get_server(server_id)
            
            return servers
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    def get_server(self, server_id) -> dict:

        url = f"https://{self.panel}/api/client/servers/{server_id}/resources"
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
            )
            response.raise_for_status()
            
            data = response.json()
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    