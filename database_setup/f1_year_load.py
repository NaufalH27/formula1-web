from database_connect import user

def load_year(year):
    user.cursor.execute("INSERT INTO Seasons (season_year) VALUES (%s)", (year,))