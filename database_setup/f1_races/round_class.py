import sys
sys.path.insert(1, "..")
from API.API_fetch_race import fetch_data_from_url

class f1round:
    def __init__(self, year, round_number):
        self.year = year
        self.round_number = round_number
        self.race_info = None
        self.race_data = None
        self.qualifying_data = None

    async def fetch_data(self):
        awaited_race_info = await fetch_data_from_url(self.year, self.round_number, "info")
        awaited_race_data = await fetch_data_from_url(self.year, self.round_number, "race")
        awaited_qualifying_data = await fetch_data_from_url(self.year, self.round_number, "qualifying")
        
        self.race_info = awaited_race_info["MRData"]["RaceTable"]
        self.race_data = awaited_race_data["MRData"]["RaceTable"]
        self.qualifying_data = awaited_qualifying_data["MRData"]["RaceTable"]

    def get_race_info_data(self):
        return self.race_info
    
    def get_participant_data(self):
        qualifying_results = get_value(self.qualifying_data,"Races", 0, "QualifyingResults") or []
        race_results =  get_value(self.race_data,"Races", 0, "Results") or []
        participant_list = qualifying_results + race_results
        processed_participant = []
        unique_participant = set()

        for element in participant_list:
            driver_ref = get_value(element, "Driver", "driverId")
            driver_number = get_value(element, "number") or "0"

            if (driver_ref, driver_number) not in unique_participant:
                unique_participant.add((driver_ref, driver_number))
                processed_participant.append(element)
            else:
                continue
        return processed_participant

    def get_race_result_element_data(self):
        return get_value(self.race_data, "Races", 0, "Results")

    def get_qualifying_result_element_data(self):
        return get_value(self.qualifying_data, "Races", 0, "QualifyingResults")

    def get_year(self):
        return self.year

    def get_round_number(self):
        return self.round_number
    
def get_value(json_obj, *keys):
    try:
        value = json_obj
        for key in keys:
            value = value[key]
        return value
    
    except (KeyError, TypeError,IndexError):
        return None