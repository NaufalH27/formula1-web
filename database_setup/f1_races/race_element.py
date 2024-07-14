import sys
sys.path.insert(1, "..")
from abc import ABC, abstractmethod
from database_connect import user

class element(ABC):
    @abstractmethod
    def __init__(self, element_data, year, round_number):
        pass

    @abstractmethod
    def insert_element_to_database(self):
        pass

class raceInfoElement(element):
    def __init__(self, element_data, year, round_number):
        self.season_ref = year
        self.round_number = round_number
        self.circuit_ref = get_value(element_data, "Races", 0, "Circuit", "circuitId")
        self.date = get_value(element_data, "Races", 0, "date")
        self.grandPrix_name = get_value(element_data, "Races", 0, "raceName")
        
    def insert_element_to_database(self):
        sql = "INSERT INTO races (season_ref, circuit_ref, race_date, round_number, GrandPrix_name) VALUES (%s, %s, %s, %s, %s)"
        val = (self.season_ref, self.circuit_ref, self.date, self.round_number, self.grandPrix_name)
        user.cursor.execute(sql, val)

class raceParticipantElement(element):
    def __init__(self, element_data, year, round_number):
        self.driver_ref = get_value(element_data, "Driver", "driverId")
        self.constructor_ref = get_value(element_data, "Constructor", "constructorId")
        self.driver_number = get_value(element_data, "number") or "0"
        self.race_ref = str(year) + "-" + str(round_number)
        
    def insert_element_to_database(self):
        sql = "INSERT INTO raceParticipants(race_ref, driver_ref, constructor_ref, driver_number) VALUES(%s, %s, %s, %s)"
        val = (self.race_ref, self.driver_ref, self.constructor_ref, self.driver_number)
        user.cursor.execute(sql, val)

class participantRaceResultElement(element):
    def __init__(self, element_data, year, round_number):
        driver_ref = get_value(element_data, "Driver", "driverId")
        self.position = get_value(element_data, "position")
        self.position_text = get_value(element_data, "positionText")
        self.status_flag = get_value(element_data, "status")
        self.best_lap_time = get_value(element_data, "FastestLap", "Time", "time")
        self.driver_race_time = get_value(element_data, "Time", "time")
        self.points = get_value(element_data, "points")
        self.race_ref = str(year) + "-" + str(round_number)
        self.driver_number = get_value(element_data, "number") or "0"
        self.participant_ref = str(year) + "-" + str(round_number) + "-" + str(get_driver_id(driver_ref))  + "-" +  str(self.driver_number)
        
    def insert_element_to_database(self):
        sql = "INSERT INTO raceResults(participant_ref, position, position_text, status_flag, best_lap_time, driver_race_time, points) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (self.participant_ref, self.position, self.position_text, self.status_flag, self.best_lap_time, self.driver_race_time, self.points)
        user.cursor.execute(sql, val)

class participantQualifyingResultElement(element):
    def __init__(self, element_data, year, round_number):
        driver_ref = get_value(element_data, "Driver", "driverId")
        self.position = get_value(element_data, "position")
        self.q1 = get_value(element_data, "Q1")
        self.q2 = get_value(element_data, "Q2")
        self.q3 = get_value(element_data, "Q3")
        self.driver_number = get_value(element_data, "number") or "0"
        self.participant_ref = str(year) + "-" + str(round_number) + "-" + str(get_driver_id(driver_ref))  + "-" +  str(self.driver_number)

    def insert_element_to_database(self):
        sql = "INSERT INTO qualifyingResults(participant_ref, qualifying_position, Q1, Q2, Q3) VALUES(%s, %s, %s, %s, %s)"
        val = (self.participant_ref, self.position, self.q1, self.q2, self.q3)
        user.cursor.execute(sql, val)

def get_value(json_obj, *keys):
    try:
        value = json_obj
        for key in keys:
            value = value[key]
        return value
    
    except (KeyError, TypeError):
        return None

def get_driver_id(driver_ref):
    sql = "SELECT driver_id FROM drivers WHERE driver_ref = %s"
    user.cursor.execute(sql, (driver_ref,))
    result = user.cursor.fetchone()

    if result is None:
        raise ValueError(f"Driver: {driver_ref} DOES NOT EXIST IN driver table")
    
    return result[0]