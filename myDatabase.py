import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, database_host, database_user, database_name, database_password):
        print("Connecting to database...")
        try:
            self.database = mysql.connector.connect(
            host=database_host,
            user=database_user,
            database=database_name,
            passwd=database_password
            )
            self.cursor = self.database.cursor()
            print("Database Connected :3")
        except Error as e:
            print(f"Failed to connect :c Error : {e}")
        

    def get_cursor(self):
        return self.cursor
    
    def commit(self):
        return self.database.commit()
    
    def close_connection(self):
        self.cursor.close()
        self.database.close()

f1_database = Database("localhost","root", "f1", {insert password here})
f1db_cursor = f1_database.get_cursor()
