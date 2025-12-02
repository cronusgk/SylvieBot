import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()
panel = os.getenv("PANEL")
api_key = os.getenv("PTERODACTYL_API")

headers = {
  'Authorization': f'Bearer {api_key}',
  'Accept': 'Application/vnd.pterodactyl.v1+json',
  'Content-Type': 'application/json'
}

external_id = "Mayview"
url = f"https://{panel}/api/client/"
try:
    response = requests.get(
        url, 
        headers=headers, 
    )
    response.raise_for_status()
    
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API Error fetching server info: {e}")
    


pretty_json = json.dumps(data, indent=4)
print(pretty_json)
