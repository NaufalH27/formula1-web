import sys
sys.path.insert(1, "..")
from abc import ABC, abstractmethod
from database_connect import DBServer

database = DBServer()

class element(ABC):
    @abstractmethod
    def __init__(self, element_data, year, round_number):
        pass

    @abstractmethod
    def insert_element_to_database(self):
        pass

class raceInfoElement(element):
    def __init__(self, element_data, year, round_number):
        self.season_year = year
        self.round_number = round_number
        self.circuit_ref = get_value(element_data, "Races", 0, "Circuit", "circuitId")
        self.date = get_value(element_data, "Races", 0, "date")
        self.grandPrix_name = get_value(element_data, "Races", 0, "raceName")
        self.circuit_id = fetch_id_from_database("SELECT circuit_id FROM Circuits WHERE circuit_ref = %s", (self.circuit_ref,))
        
    def insert_element_to_database(self):
        sql = "INSERT INTO races (season_year, circuit_id, race_date, round_number, GrandPrix_name) VALUES (%s, %s, %s, %s, %s)"
        val = (self.season_year, self.circuit_id, self.date, self.round_number, self.grandPrix_name)
        database.cursor.execute(sql, val)

class raceParticipantElement(element):
    def __init__(self, element_data, year, round_number):
        self.driver_ref = get_value(element_data, "Driver", "driverId")
        self.constructor_ref = get_value(element_data, "Constructor", "constructorId")
        self.driver_number = get_value(element_data, "number") or "0"
        self.driver_id = fetch_id_from_database("SELECT driver_id FROM Drivers WHERE driver_ref = %s", (self.driver_ref,))
        self.constructor_id = fetch_id_from_database("SELECT constructor_id FROM Constructors WHERE constructor_ref = %s", (self.constructor_ref,))
        self.race_id = fetch_id_from_database("SELECT race_id FROM Races WHERE season_year = %s AND round_number = %s", (year, round_number))

        
    def insert_element_to_database(self):
        sql = "INSERT INTO raceParticipants(race_id, driver_id, constructor_id, driver_number) VALUES(%s, %s, %s, %s)"
        val = (self.race_id, self.driver_id, self.constructor_id, self.driver_number)
        database.cursor.execute(sql, val)

class participantRaceResultElement(element):
    def __init__(self, element_data, year, round_number):
        self.position = get_value(element_data, "position")
        self.position_text = get_value(element_data, "positionText")
        self.status_flag = get_value(element_data, "status")
        self.best_lap_time = get_value(element_data, "FastestLap", "Time", "time")
        self.driver_race_time = get_value(element_data, "Time", "time")
        self.points = get_value(element_data, "points")
        self.driver_number = get_value(element_data, "number") or "0"
        self.driver_ref = get_value(element_data, "Driver", "driverId")
        self.constructor_ref = get_value(element_data, "Constructor", "constructorId")
        self.race_id = fetch_id_from_database("SELECT race_id FROM Races WHERE season_year = %s AND round_number = %s", (year, round_number))
        self.driver_id = fetch_id_from_database("SELECT driver_id FROM Drivers WHERE driver_ref = %s", (self.driver_ref,))
        self.constructor_id = fetch_id_from_database("SELECT constructor_id FROM Constructors WHERE constructor_ref = %s", (self.constructor_ref,))
        self.participant_id = fetch_id_from_database("SELECT participant_id FROM RaceParticipants WHERE race_id = %s AND driver_id = %s AND driver_number = %s", (self.race_id, self.driver_id, self.driver_number,))
        
    def insert_element_to_database(self):
        sql = "INSERT INTO raceResults(participant_id, position, position_text, status_flag, best_lap_time, driver_race_time, points) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (self.participant_id, self.position, self.position_text, self.status_flag, self.best_lap_time, self.driver_race_time, self.points)
        database.cursor.execute(sql, val)

class participantQualifyingResultElement(element):
    def __init__(self, element_data, year, round_number):
        self.position = get_value(element_data, "position")
        self.q1 = get_value(element_data, "Q1")
        self.q2 = get_value(element_data, "Q2")
        self.q3 = get_value(element_data, "Q3")
        self.driver_number = get_value(element_data, "number") or "0"
        self.driver_ref = get_value(element_data, "Driver", "driverId")
        self.constructor_ref = get_value(element_data, "Constructor", "constructorId")
        self.race_id = fetch_id_from_database("SELECT race_id FROM Races WHERE season_year = %s AND round_number = %s", (year, round_number))
        self.driver_id = fetch_id_from_database("SELECT driver_id FROM Drivers WHERE driver_ref = %s", (self.driver_ref,))
        self.constructor_id = fetch_id_from_database("SELECT constructor_id FROM Constructors WHERE constructor_ref = %s", (self.constructor_ref,))
        self.participant_id = fetch_id_from_database("SELECT participant_id FROM RaceParticipants WHERE race_id = %s AND driver_id = %s AND driver_number = %s", (self.race_id, self.driver_id, self.driver_number,))

    def insert_element_to_database(self):
        sql = "INSERT INTO qualifyingResults(participant_id, qualifying_position, Q1, Q2, Q3) VALUES(%s, %s, %s, %s, %s)"
        val = (self.participant_id, self.position, self.q1, self.q2, self.q3)
        database.cursor.execute(sql, val)

def get_value(json_obj, *keys):
    try:
        value = json_obj
        for key in keys:
            value = value[key]
        return value
    
    except (KeyError, TypeError):
        return None

def fetch_id_from_database(query, params):
    database.cursor.execute(query, params)
    result = database.cursor.fetchone()
    return result[0] if result else None

