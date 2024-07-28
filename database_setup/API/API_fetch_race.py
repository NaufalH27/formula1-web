import aiohttp 
from tenacity import retry, wait_fixed, stop_after_attempt
from API.API_config import ERGAST_API_BASE_URL

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

SESSION_KEY_CONSTRAINT = {
    "r": "/results", "race": "/results",
    "q": "/qualifying", "qualifying": "/qualifying",
    "i" : "", "info" : ""
}

@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
async def fetch_data_from_url(year, round_number, session_name):
    try:
        url = f"{ERGAST_API_BASE_URL}/{year}/{round_number}{SESSION_KEY_CONSTRAINT[session_name]}.json"
        timeout = aiohttp.ClientTimeout(total=30) 
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        print(f"ERROR: failed retrieving response from {url} error: {e}. Retrying...")
        raise




