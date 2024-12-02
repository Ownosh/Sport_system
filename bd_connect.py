import mysql.connector
from mysql.connector import Error

# Конфигурация для подключения к базе данных
DATABASE_CONFIG = {
    'host': 'sql7.freesqldatabase.com',
    'database': 'sql7748562',
    'user': 'sql7748562',
    'password': 'rUe9qv5eU3'
}

class MySQLDatabase:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Подключение к базе данных"""
        try:
            # Используем конфигурацию из DATABASE_CONFIG
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            if self.connection.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('MySQL connection closed')

    def execute_query(self, query, params=None):
        """
        Выполняет запрос и возвращает результат
        :param query: SQL-запрос
        :param params: Параметры для подстановки в запрос
        :return: Результат запроса или None
        """
        if not self.connection or not self.connection.is_connected():
            print("Connection is not established. Call connect() first.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()  # Возвращаем все строки результата
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

# Функция для получения уже подключенного экземпляра базы
def get_database_connection():
    db = MySQLDatabase()
    db.connect()  # автоматически подключаемся
    return db
