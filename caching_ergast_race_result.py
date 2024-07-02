import json
import asyncio
import aiohttp 
import time
from retrying import retry
import os
from tenacity import retry, wait_fixed, stop_after_attempt


# Constants
DIRECTORY = "path/to/dir"  
API_BASE_URL = "https://ergast.com/api/f1"
DEFAULT_LIMIT = 1000
DEFAULT_OFFSET = 0
URL_SUFFIX = {
    "info": "",
    "race": "/results",
    "qualifying": "/qualifying",
    "sprint": "/sprint"
    }
MAX_ROUND = {
    1950: 7, 1951: 8, 1952: 8, 1953: 9, 1954: 9, 1955: 7, 1956: 8, 1957: 8, 1958: 11, 1959: 9,
    1960: 10, 1961: 8, 1962: 9, 1963: 10, 1964: 10, 1965: 10, 1966: 9, 1967: 11, 1968: 12, 1969: 11,
    1970: 13, 1971: 11, 1972: 12, 1973: 15, 1974: 15, 1975: 14, 1976: 16, 1977: 17, 1978: 16, 1979: 15,
    1980: 14, 1981: 15, 1982: 16, 1983: 15, 1984: 16, 1985: 16, 1986: 16, 1987: 16, 1988: 16, 1989: 16,
    1990: 16, 1991: 16, 1992: 16, 1993: 16, 1994: 16, 1995: 17, 1996: 16, 1997: 17, 1998: 16, 1999: 16,
    2000: 17, 2001: 17, 2002: 17, 2003: 16, 2004: 18, 2005: 19, 2006: 18, 2007: 17, 2008: 18, 2009: 17,
    2010: 19, 2011: 19, 2012: 20, 2013: 19, 2014: 19, 2015: 19, 2016: 21, 2017: 20, 2018: 21, 2019: 21,
    2020: 17, 2021: 22, 2022: 22, 2023: 22, 2024: 24, 2025: 24
}



def get_metadata_url_suffix(metadata_type):
    try:
        return URL_SUFFIX[metadata_type]
    except KeyError:
        raise ValueError(f"ERROR: Invalid metadata type : {metadata_type}")
    

def construct_race_result_url(year, round_number, session_type):
    session_type = get_metadata_url_suffix(session_type)
    url = f"{API_BASE_URL}/{year}/{round_number}{session_type}.json"
    return url


@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
async def fetch_data_from_url(url):
    try:
        timeout = aiohttp.ClientTimeout(total=30)  # Set a total timeout of 30 seconds
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                print(f"LOG: Successfully retrieved url: {url}")
                return await response.json()
    except Exception as e:
        print(f"ERROR: failed retrieving response from {url} error: {e}. Retrying...")
        raise


def save_result(result_data, dir_path, session_name):
    race_info = result_data['MRData']['RaceTable']
    season_year = race_info['season']
    round_number = race_info['round']

    session_path = os.path.join(dir_path, season_year, round_number)
    os.makedirs(session_path, exist_ok=True)
    filename = session_name
    file_path = os.path.join(session_path, filename)

    with open(file_path, 'w') as file:
        json.dump(result_data, file, indent=4)
    
    print(f"LOG: sucessfylly cached : {file_path} ")


def cache_result(json_data, dir_path, session_name):
    try:
        save_result(json_data, dir_path, session_name)
    except IOError as e:
        print(f"ERROR: Failed to caching file. reason:{e}")


def is_race_data_valid(json_data):
    return bool(json_data['MRData']['RaceTable']['Races'])

def result_log(result_data, session_name):
    for result in result_data:
        try:
            curr_json_data = result['MRData']['RaceTable']
            season = curr_json_data['season']
            round_number = curr_json_data['round']
            raceName = curr_json_data['Races'][0]['raceName']

            print(f"LOG : {session_name}, {raceName} : {season} season, race number {round_number} has been LOADED with status: VALID")
        except IndexError:
            print(f"LOG :  {session_name} year: {season}. race number {round_number} is INVALID, WARNING: WILL BE NOT SAFED IN CACHE")


async def load_session(year,session_name):
    max_round = MAX_ROUND[year]
    tasks = []
    for round_number in range(1,max_round+1):
        curr_url = construct_race_result_url(year, round_number, session_name)
        awaited_requests = fetch_data_from_url(curr_url)
        tasks.append(awaited_requests)
        
    fetched_results = await asyncio.gather(*tasks)
    return fetched_results

if __name__ == '__main__':
    session_list = ["race", "qualifying"]

    for year in range(2002,1949, -1):

        for session in session_list:
            races = asyncio.run(load_session(year,session))
            result_log(races, session)

            for race_result in races:
                if is_race_data_valid(race_result):
                    cache_result(race_result)
                
            
        

