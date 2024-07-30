import sys
sys.path.insert(1, "..")
import asyncio
from API.API_fetch_race import MAX_ROUND
from f1_races.round_class import f1round
from f1_races.race_data import f1RaceData, raceInfo, raceParticipant, participantRaceResult, participantQualifyingResult, participantSprintResult
from database_connect import DBServer

database = DBServer()

class f1season:
    def __init__(self, year):
        self.year = year
        self.round_list = asyncio.run(fetch_race_data(year))
        
    def insert_to_database(self):
        for round in self.round_list:
            load_data(raceInfo(round))
            load_data(raceParticipant(round))
            
            if round.get_race_result_element_data() is not None:
                load_data(participantRaceResult(round))
            if round.get_qualifying_result_element_data() is not None:
                load_data(participantQualifyingResult(round))
            if round.get_sprint_element_data() is not None:
                load_data(participantSprintResult(round))

            database.commit()
            print(f"LOG : season {self.year} round {round.get_round_number()} has been loaded")
        print(f"LOG : season {self.year} SUCCESSFULLY loaded total races = {round.get_round_number()}")

async def fetch_race_data(year):
    max_round = MAX_ROUND[year]
    round_list = []

    for round_number in range(1,max_round+1):
        round_list.append(f1round(year, round_number))
        
    fetched_round_list = await asyncio.gather(*(round.fetch_data() for round in round_list))

    return round_list
    
def load_data(data : f1RaceData):
    data.load_data_to_database()





