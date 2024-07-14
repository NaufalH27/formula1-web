from abc import ABC, abstractmethod
from f1_races.round_class import *
from f1_races.race_element import *

class f1RaceData(ABC):
    @abstractmethod
    def __init__ (self,  round :f1round):
        pass
    
    @abstractmethod
    def load_data_to_database(self):
        pass

class raceInfo(f1RaceData):
    def __init__(self, round:f1round):
        self.data = round.get_race_info_data()
        self.year = round.get_year()
        self.round_number = round.get_round_number()
    
    def load_data_to_database(self):
        raceInfoElement(self.data, self.year, self.round_number).insert_element_to_database()        

class raceParticipant(f1RaceData):
    def __init__(self, round:f1round):
        self.data = round.get_participant_data()
        self.year = round.get_year()
        self.round_number = round.get_round_number()
    
    def load_data_to_database(self):
        for element in self.data:
            raceParticipantElement(element, self.year, self.round_number).insert_element_to_database()
        
class participantRaceResult(f1RaceData):
    def __init__(self, round:f1round):
        self.data = round.get_race_result_element_data()
        self.year = round.get_year()
        self.round_number = round.get_round_number()
    
    def load_data_to_database(self):
        for element in self.data:
            participantRaceResultElement(element, self.year, self.round_number).insert_element_to_database()
            
class participantQualifyingResult(f1RaceData):
    def __init__(self, round:f1round):
        self.data = round.get_qualifying_result_element_data()
        self.year = round.get_year()
        self.round_number = round.get_round_number()
    
    def load_data_to_database(self):
        for element in self.data:
            participantQualifyingResultElement(element, self.year, self.round_number).insert_element_to_database()
