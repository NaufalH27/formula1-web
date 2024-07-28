import sys
sys.path.insert(1, "..")
from abc import ABC, abstractmethod
from database_connect import DBServer

database = DBServer()

class f1ElementEntities(ABC):
    @abstractmethod
    def __init__(self, element_data):
        pass

    @abstractmethod
    def insert_element_to_database(self):
        pass

class driverElement(f1ElementEntities):
    def __init__(self, element_data):
        self.driver_ref = get_value(element_data, "driverId")
        self.driver_firstname = get_value(element_data, "givenName")
        self.driver_lastname = get_value(element_data, "familyName")
        self.driver_birth_date = get_value(element_data, "dateOfBirth")
        self.driver_nationality = get_value(element_data, "nationality")
        self.driver_url = get_value(element_data, "url")

    def insert_element_to_database(self):
        sql = "INSERT INTO Drivers(driver_ref, driver_firstname, driver_lastname, driver_nationality, driver_birthdate, url) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (self.driver_ref, self.driver_firstname, self.driver_lastname, self.driver_nationality, self.driver_birth_date, self.driver_url)
        database.cursor.execute(sql, val)

class circuitElement(f1ElementEntities):
    def __init__(self, element_data):
        self.circuit_ref = get_value(element_data, "circuitId")
        self.circuit_name = get_value(element_data, "circuitName")
        self.circuit_country = get_value(element_data, "Location", "country")
        self.circuit_location = get_value(element_data, "Location", "locality")
        self.circuit_url = get_value(element_data, "url")

    def insert_element_to_database(self):
        sql = "INSERT INTO Circuits(circuit_name, circuit_ref, circuit_country, circuit_location, url) VALUES(%s, %s, %s, %s, %s)"
        val = (self.circuit_name, self.circuit_ref, self.circuit_country, self.circuit_location, self.circuit_url)
        database.cursor.execute(sql, val)

class constructorElement(f1ElementEntities):
    def __init__(self, element_data):
        self.constructor_ref = get_value(element_data, "constructorId")
        self.constructor_name = get_value(element_data, "name")
        self.constructor_nationality = get_value(element_data, "nationality")
        self.constructor_url = get_value(element_data, "url")

    def insert_element_to_database(self):
        sql = "INSERT INTO Constructors(constructor_ref, constructor_name, constructor_nationality, url) VALUES(%s, %s, %s, %s)"
        val = (self.constructor_ref, self.constructor_name, self.constructor_nationality, self.constructor_url)
        database.cursor.execute(sql, val)


def get_value(json_obj, *keys):
    try:
        value = json_obj
        for key in keys:
            value = value[key]
        return value
    
    except (KeyError, TypeError):
        return None


    