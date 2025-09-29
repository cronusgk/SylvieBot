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
            i = 0
            for server in server_info:
                server_name = server["attributes"]["name"]
                servers[server_name] = server_info[i]
                i += 1
            
            return servers
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    def get_server(self, external_id) -> dict:
        url = f"https://{self.panel}/api/application/servers/external/{external_id}"
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
        
    