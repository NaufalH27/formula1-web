from database_connect import DBServer
from f1_entities import f1_entities_load
from f1_races.f1_session_load import f1season
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

database = DBServer()

# Connect your server right here
#IMPORTANT NOTES: please configure your .env file first or replace the .env parameter below to your database server
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password= os.getenv('DB_PASSWORD') 
database_name = os.getenv('DB') 

if __name__ == "__main__":
  current_year = datetime.now().year
  database.set_server(host, user, password)

  #connect your database in your database from your server right here to become a place to the f1 data
  #IMPORTANT Note: PLEASE RUN THE database_schema.sql FIRST IN YOUR DATABASE SERVER!!!!!!!!!!!!!!!!!!!
  database.connect_to_database(database_name)

  # this function below for loading the participant or entities data to database
  # consisting: Driver, Constructor, and Circuits
  f1_entities_load.load_all_entities()

#load race data each year
  for year in range(1950, current_year + 1):
      curr_season = f1season(year)
      curr_season.insert_to_database()

  print("LOG : ALL DATA SUCCESSFULLY LOADED TO DATABASE")   
  database.close_connection()  


        
  
        

        