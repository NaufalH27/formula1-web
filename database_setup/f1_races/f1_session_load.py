import sys
sys.path.insert(1, "..")
import asyncio
from API.API_fetch_race import *
from f1_races.race_data import *

async def fetch_race_data(year):
    max_round = MAX_ROUND[year]
    race_results_data = []
    qualifying_results_data = []
    f1_round_list = []

    for round_number in range(1,max_round+1):
        awaited_race_data = fetch_data_from_url(year, round_number, "race")
        awaited_qualifying_data = fetch_data_from_url(year, round_number, "qualifying")
        race_results_data.append(awaited_race_data)
        qualifying_results_data.append(awaited_qualifying_data)
    race_list = await asyncio.gather(*race_results_data)
    qualifying_data_list = await asyncio.gather(*qualifying_results_data)

    for i in range(len(race_list)):
        f1_round_list.append(f1round(year,i+1, race_list[i], qualifying_data_list[i]))
    return f1_round_list
    
def load_data(data : f1RaceData):
    data.load_data_to_database()

class f1season:
    def __init__(self, year):
        self.year = year
        self.round_list = asyncio.run(fetch_race_data(year))
        
    def insert_to_database(self):
        for round in self.round_list:
            load_data(raceInfo(round))
            load_data(raceParticipant(round))
            load_data(participantRaceResult(round))

            if round.get_qualifying_result_element_data() is not None:
                load_data(participantQualifyingResult(round))
            
        print(f"LOG : season {self.year} has been loaded total races = {round.get_round_number()}")



