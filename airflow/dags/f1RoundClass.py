from airflow.dags.helper.jsonHelper import get_value
from extractDataFromAPI import fetch

class f1Round:
    def __init__(self, year, round_number):
        self.year = year
        self.round_number = round_number
        self.race_info = None
        self.race_data = None
        self.qualifying_data = None
        self.sprint_data = None
    
    def fetch_race_info_data(self):
        self.race_info = fetch(self.year, self.round_number, "info")["MRData"]["RaceTable"]

    def fetch_race_result_data(self):
        self.race_data = fetch(self.year, self.round_number, "race")["MRData"]["RaceTable"]
        
    def fetch_qualifying_race_data(self):
        self.qualifying_data = fetch(self.year, self.round_number, "qualifying")["MRData"]["RaceTable"]

    def fetch_sprint_race_data(self):
          self.sprint_data = fetch(self.year, self.round_number, "sprint")["MRData"]["RaceTable"]

    def get_race_info_data(self):
        return self.race_info
    
    def get_participant_data(self):
        qualifying_results = get_value(self.qualifying_data,"Races", 0, "QualifyingResults") or []
        sprint_results = get_value(self.sprint_data, "Races", 0, "SprintResults") or []
        race_results =  get_value(self.race_data,"Races", 0, "Results") or []
        participant_list = qualifying_results + sprint_results + race_results
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
    
    def get_sprint_element_data(self):
        return get_value(self.sprint_data, "Races", 0, "SprintResults")

    def get_year(self):
        return self.year

    def get_round_number(self):
        return self.round_number
    
