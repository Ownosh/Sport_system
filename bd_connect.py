from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

class MySQLDatabase:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            if self.connection.is_connected():
                print('Подключен к базе данных MySQL')
        except Error as e:
            print(f"Ошибка при подключении к MySQL: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Соединение с MySQL закрыто')

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established. Call connect() first.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()  
        except Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


def get_database_connection():
    db = MySQLDatabase()
    db.connect()  
    return db
