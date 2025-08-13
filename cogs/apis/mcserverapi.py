import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MinecraftServerAPI:
    def __init__(self, api_key: str, server_ip: str):
        if not api_key or not server_ip:
            raise ValueError("Error: must provide api key and server ip")
        
        self.base_url = f"https://{server_ip}/api/v2"
        self.headers = {"apiKey": api_key}
        self.timeout = 10 
        
    def get_server_info(self, server_id: str) -> dict | None:
        url = f"{self.base_url}/servers/{server_id}"
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                verify=False, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching server info: {e}")
            return None 
        
    def start_server(self, server_id: str):
        url = f"{self.base_url}/servers/{server_id}/execute/action"
        
        payload = {
            "action": 2
        }
        
        try:
            response = requests.post(
                url, 
                headers=self.headers,
                json=payload,
                verify=False,
                timeout=self.timeout
            )
            
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"API request error occurred: {e}")