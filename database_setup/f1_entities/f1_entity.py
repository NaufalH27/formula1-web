import sys
sys.path.insert(1, "..")
from abc import ABC, abstractmethod
from f1_entities.f1_entities_element import driverElement, constructorElement, circuitElement
from API.API_fetch_entities import get_data_from_api

class f1EntitiesStrategy(ABC):
    @abstractmethod
    def __init__ (self):
        pass

    @abstractmethod
    def load_entities_to_database(self):
        pass

class driverEntities(f1EntitiesStrategy):
    def __init__ (self):
        self.driver_list = get_data_from_api("Driver")
    
    def load_entities_to_database(self):
        for driver in self.driver_list:
            driverElement(driver).insert_element_to_database()
        print("LOG: All drivers has been loaded")
    
class constructorEntities(f1EntitiesStrategy):
    def __init__ (self):
        self.constructor_list = get_data_from_api("Constructor")
    
    def load_entities_to_database(self):
        for constructor in self.constructor_list:
            constructorElement(constructor).insert_element_to_database()
        print("LOG: All constructor has been loaded")

class circuitEntities(f1EntitiesStrategy):
    def __init__ (self):
        self.circuit_list = get_data_from_api("Circuit")
    
    def load_entities_to_database(self):
        for circuit in self.circuit_list:
            circuitElement(circuit).insert_element_to_database()
        print("LOG: All circuit has been loaded")

