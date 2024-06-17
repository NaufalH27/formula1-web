import fastf1
import pandas as pd
import mysql.connector
import os

# Database connection
database = mysql.connector.connect(
    host="localhost",
    user="root",
    database="f1",
    passwd="-"
)
cursor = database.cursor()

# FastF1 cache settings
fastf1.Cache.enable_cache("C:\\DataEngProject\\f1cache")
fastf1.Cache.offline_mode("enabled")


def parse_race_stats(race_table):
    parsed_race_table = race_table[['FirstName', 'LastName', 'Position', 'Points', 'Status', 'Time']].copy()
    parsed_race_table['Position'] = parsed_race_table['Position'].astype(int)
    parsed_race_table['Points'] = parsed_race_table['Points'].astype(int)
    parsed_race_table['Time'] = parsed_race_table['Time'].astype(str).str.replace('0 days ', '', regex=False)
    return parsed_race_table

def check_data_integrity(table):
    driver_exist_count = 0
    number_of_drivers_from_API = len(table)
    
    for row in range(number_of_drivers_from_API):
        curr_first_name = table.iloc[row, 0]
        curr_last_name = table.iloc[row, 1]
        query = 'SELECT EXISTS(SELECT 1 FROM drivers WHERE driver_firstname = %s AND driver_lastname = %s)'
        cursor.execute(query, (curr_first_name, curr_last_name))
        exists = cursor.fetchone()[0]
        
        if exists:
            driver_exist_count += 1
        else:
            print(f"MISSING :{curr_first_name} {curr_last_name} does not exist")

    return driver_exist_count == number_of_drivers_from_API

for year in range(2020, 2024):
    race_index = 1
    race_integrated_count = 0
    
    while True:
        try:
            session = fastf1.get_session(year, race_index, "R")
            session.load()
            result_table = session.results
            parsed_result = parse_race_stats(result_table)
            is_data_integrated = check_data_integrity(parsed_result)
            os.system("cls")
            
            if is_data_integrated:
                print(f"Year: {year}: Race number {race_index} integrated")
                race_integrated_count += 1
            
            race_index += 1
        
        except ValueError:
            race_index -= 1
            print("Year has been loaded")
            break
    
    os.system("cls")
    
    if race_integrated_count == race_index:
        print(f"{year} integrated")
    else:
        print(f"{year} not fully integrated")

