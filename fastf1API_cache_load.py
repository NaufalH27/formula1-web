import fastf1

fastf1.Cache.enable_cache("\\my\\cache\\dir")

def load_session_cache(session_year):
    j = 1
    while True:
        try:
            session = fastf1.get_session(session_year,j , "race")
            session.load()
            j += 1
        except ValueError:
            print("year has been loaded")
            break



for year in range(2020,2023):
    load_session_cache(year)
    
    
        

    
