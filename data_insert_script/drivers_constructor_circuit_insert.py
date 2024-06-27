import requests
import json
from database_connect_module import f1_database

# Constants
API_BASE_URL = "https://ergast.com/api/f1"
DEFAULT_LIMIT = 1000
DEFAULT_OFFSET = 0

def get_metadata_url_suffix(metadata):
    metadata_type = {
        "drivers": "/drivers",
        "circuits": "/circuits",
        "constructors": "/constructors",
    }
    try:
        return metadata_type[metadata]
    except KeyError:
        raise ValueError("Invalid metadata type")


def fetch_metadata(metadata_type):
    metadata_suffix = get_metadata_url_suffix(metadata_type)
    url = f"{API_BASE_URL}{metadata_suffix}.json?limit={DEFAULT_LIMIT}&offset={DEFAULT_OFFSET}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        print(f"successfully retrieve metadata: {metadata_type}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {metadata_type} metadata: {e}")



def driver_data_extraction(driver_data):
    total_drivers = int(driver_data["MRData"]["total"])
    driver_list = driver_data["MRData"]["DriverTable"]["Drivers"]

    for driver_index in range(total_drivers):
        driver = driver_list[driver_index]
        driver_ref = driver["driverId"]
        driver_firstname = driver["givenName"]
        driver_lastname = driver["familyName"]
        driver_birth_date = driver["dateOfBirth"]
        driver_nationality = driver["nationality"]
        driver_url = driver["url"]


        sql = "INSERT INTO Drivers(driver_ref, driver_firstname, driver_lastname, driver_nationality, driver_birthdate, url) VALUES(%s, %s, %s, %s, %s, %s)"
        value = (driver_ref, driver_firstname, driver_lastname, driver_nationality, driver_birth_date, driver_url)
        cursor = f1_database.get_cursor()
        cursor.execute(sql,value)

        print(f"successfully insert: {driver_ref} {driver_firstname} {driver_lastname} {driver_birth_date} {driver_nationality} {driver_url}")
        

def circuit_data_extraction(circuit_data):
    total_circuit = int(circuit_data["MRData"]["total"])
    circuit_list = circuit_data["MRData"]["CircuitTable"]["Circuits"]

    for circuit_index in range(total_circuit):
        circuit = circuit_list[circuit_index]

        circuit_ref = circuit["circuitId"]
        circuit_name = circuit["circuitName"]
        circuit_country = circuit["Location"]["country"]
        circuit_location = circuit["Location"]["locality"]
        circuit_url = circuit["url"]


        sql = "INSERT INTO circuits(circuit_name, circuit_ref, circuit_country, circuit_location, url) VALUES(%s, %s, %s, %s, %s)"
        value = (circuit_name, circuit_ref, circuit_country, circuit_location, circuit_url)
        cursor = f1_database.get_cursor()
        cursor.execute(sql,value)

        print(f"successfully insert: {circuit_ref} {circuit_name} {circuit_country} { circuit_location} {circuit_url}")


def constructor_data_extraction(constructor_data):
    total_constructor = int(constructor_data["MRData"]["total"])
    constructor_list = constructor_data["MRData"]["ConstructorTable"]["Constructors"]

    for constructor_index in range(total_constructor):
        constructor = constructor_list[constructor_index]

        constructor_ref = constructor["constructorId"]
        constructor_name = constructor["name"]
        constructor_nationality = constructor["nationality"]
        constructor_url = constructor["url"]


        sql = "INSERT INTO Constructors(constructor_ref, constructor_name, constructor_nationality, url) VALUES(%s, %s, %s, %s)"
        value = (constructor_ref, constructor_name, constructor_nationality, constructor_url)
        cursor = f1_database.get_cursor()
        cursor.execute(sql,value)

        print(f"successfully insert: {constructor_ref} {constructor_name} {constructor_nationality} {constructor_url}")

if __name__ == "__main__":
    driver_data = fetch_metadata("drivers")
    constructor_data = fetch_metadata("constructors")
    circuit_data = fetch_metadata("circuits")

    driver_data_extraction(driver_data)
    constructor_data_extraction(constructor_data)
    circuit_data_extraction(circuit_data)
    
    f1_database.commit()
    

    
