from extractDataFromAPI import fetch

def initializeRound():
    year = None
    round_number = None

# Define tasks
def fetch_race_info():
    race_info = fetch(year, round_number, "info")["MRData"]["RaceTable"]

def fetch_race_result():
    race_data = fetch(year, round_number, "race")["MRData"]["RaceTable"]

def fetch_qualifying_data():
     qualifying_data = fetch(year, round_number, "qualifying")["MRData"]["RaceTable"]

def fetch_sprint_data():
    sprint_data = fetch(year, round_number, "sprint")["MRData"]["RaceTable"]