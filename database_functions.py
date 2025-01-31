import mysql.connector
from change_buttons import get_database_connection

def get_sportsmen():
    """Получает список всех спортсменов."""
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute("SELECT sportsman_id, last_name FROM sportsmen")
    sportsmen = cursor.fetchall()
    db.close()
    return sportsmen  # [(1, 'Иван'), (2, 'Петр'), ...]

def get_trainers():
    """Получает список всех тренеров."""
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute("SELECT trainer_id, last_name FROM trainers")  # Предположим, что таблица называется `trainers`
    trainers = cursor.fetchall()
    db.close()
    return trainers  # [(1, 'Иванов'), (2, 'Петров'), ...]

def add_training_result(sportsman_id, training_id, v1, v2):
    """Добавляет результат тренировки спортсмена."""
    db = get_database_connection()
    cursor = db.cursor()
    query = """
    INSERT INTO characteristics_sportsman_trainings (sportsman_id, training_id, v1, v2) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (sportsman_id, training_id, v1, v2))
    db.commit()
    db.close()

def get_training_results(sportsman_id):
    """Получает результаты тренировок спортсмена по его ID."""
    db = get_database_connection()
    cursor = db.cursor(dictionary=True)
    
    query = """
    SELECT id, training_id, v1, v2, progress 
    FROM characteristics_sportsman_trainings 
    WHERE sportsman_id = %s 
    ORDER BY id DESC
    """
    
    cursor.execute(query, (sportsman_id,))
    results = cursor.fetchall()
    db.close()
    return results  # [{'id': 1, 'training_id': 2, 'v1': 10, 'v2': 15, 'progress': 40.0}, ...]


from change_buttons import get_database_connection  # Импортируем вашу функцию для подключения к БД

def get_trainings_for_sportsman(sportsman_id):
    """
    Возвращает список тренировок, на которых был спортсмен.
    :param sportsman_id: ID спортсмена
    :return: Список кортежей (training_id, training_name)
    """
    try:
        # Получаем подключение к базе данных
        conn = get_database_connection()
        cursor = conn.cursor()

        # SQL-запрос для получения тренировок, на которых был спортсмен
        query = """
        SELECT t.training_id, t.name_training
        FROM trainings t
        JOIN training_attendance ta ON t.training_id = ta.training_id
        WHERE ta.athlete_id = %s
        """
        cursor.execute(query, (sportsman_id,))

        # Получаем результат
        trainings = cursor.fetchall()

        # Закрываем соединение
        cursor.close()
        conn.close()

        return trainings  # Возвращаем список кортежей (training_id, training_name)

    except Exception as e:
        print(f"Ошибка при получении тренировок: {e}")
        return []  # В случае ошибки возвращаем пустой список
