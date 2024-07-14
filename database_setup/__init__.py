import f1_year_load
from database_connect import user
from f1_entities import f1_entities_load
from f1_races.f1_session_load import f1season
from mysql.connector import Error
     
if __name__ == "__main__":
  try:
    user.create_and_connect_to_database("test")
    f1_entities_load.load_all_entities()

    for year in range(1950, 2025):
        f1_year_load.load_year(year)
        curr_season = f1season(year)
        curr_season.insert_to_database()
        user.commit()

  except IndexError as e:
    user.commit()
    print("LOG ALL DATA HAS BEEN LOADED")
  
  except Error as e:
     print(e)
        
  
        

        