from f1_entities.f1_entity import *

def load_entities(entities : f1EntitiesStrategy):
    entities.load_entities_to_database()

def load_all_entities():
    load_entities(driverEntities())
    load_entities(constructorEntities())
    load_entities(circuitEntities())
