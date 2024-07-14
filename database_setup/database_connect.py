import mysql.connector
from mysql.connector import errorcode, Error
import re

class userDB:
    def __init__(self, database_host, database_user, user_password):
        print("Connecting to database...")
        
        try:
            self.database_host = database_host
            self.database_user = database_user
            self.user_password = user_password
            self.database = mysql.connector.connect(
            host = self.database_host,
            user = self.database_user,
            passwd = self.user_password
            )
            self.cursor = self.database.cursor()
            print("Database Connected :3")

        except Error as e:
            print(f"Failed to connect :c Error : {e}")
    
    def create_and_connect_to_database(self, database_name):
        self.database_name = database_name

        if self.cursor is None:
            print("No connection to the server. Cannot create or connect to database.")
            raise
        
        try:
            print(f"trying to onnect to {database_name}")
            self.database = mysql.connector.connect(
            host = self.database_host,
            user = self.database_user,
            database = database_name,
            passwd = self.user_password
            )
            self.cursor = self.database.cursor()
            print(f"Database {database_name} connected :3")
            
        except mysql.connector.Error as err:
                print(err.msg)
                raise
        
    def commit(self):
        return self.database.commit()
    
    def close_connection(self):
        self.cursor.close()
        self.database.close()
    
    def drop_database(self):
        self.cursor(f"DROP DATABASE {self.database_name}")




#connect to your server here
user = userDB({your host},{your username}, {your password})