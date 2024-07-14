import requests
from API.API_config import ERGAST_API_BASE_URL

def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {url} reason: {e}")

def get_data_from_api(data_type):
    valid_key = ["Driver", "Constructor", "Circuit"]
    if data_type not in valid_key:
        raise KeyError(f"data type: {data_type} is not valid")
    
    url = f"{ERGAST_API_BASE_URL}/{data_type}s.json?limit=1000&offset=0"
    json_data = fetch_data_from_url(url)
    return json_data["MRData"][f"{data_type}Table"][f"{data_type}s"]
