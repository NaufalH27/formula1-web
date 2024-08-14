import requests
import logging

ERGAST_API_BASE_URL = "https://ergast.com/api/f1"

SESSION_KEY_CONSTRAINT = {
    "r": "/results", "race": "/results",
    "q": "/qualifying", "qualifying": "/qualifying",
    "i" : "", "info" : "",
    "s" : "/sprint", "sprint" : "/sprint"
}

def fetch(year, round_number, session_name):
    try:
        url = f"{ERGAST_API_BASE_URL}/{year}/{round_number}{SESSION_KEY_CONSTRAINT[session_name]}.json"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logging.error(f"failed retrieving response from {url} error: {e}.")
        raise

