import mysql.connector
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import QDate
import os


def get_database_connection():
    try:
        connection = mysql.connector.connectconnection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as e:
        QMessageBox.critical(None, "Ошибка подключения", f"Ошибка при подключении к базе данных: {e}")
        return None

class CreateUserWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание пользователя")
        self.setGeometry(530, 270, 450, 350)

        # Элементы формы
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.first_name_label = QLabel("Имя:")
        self.last_name_label = QLabel("Фамилия:")
        self.middle_name_label = QLabel("Отчество:")
        self.dob_label = QLabel("Дата рождения (ДД.ММ.ГГГГ):")
        self.city_label = QLabel("Город:")
        self.role_label = QLabel("Должность:")
        self.sport_type_label = QLabel("Тип спорта:")
        self.phone_label = QLabel("Номер телефона:")
        self.email_label = QLabel("Электронная почта:")

        # Поля ввода
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.city_input = QLineEdit()
        self.role_input = QComboBox()
        self.role_input.addItems(["Sportsman", "Trainer"])
        self.sport_type_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Кнопка отправки формы
        self.submit_button = QPushButton("Создать пользователя")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_input, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_input, 1, 1)
        grid_layout.addWidget(self.first_name_label, 2, 0)
        grid_layout.addWidget(self.first_name_input, 2, 1)
        grid_layout.addWidget(self.last_name_label, 3, 0)
        grid_layout.addWidget(self.last_name_input, 3, 1)
        grid_layout.addWidget(self.middle_name_label, 4, 0)
        grid_layout.addWidget(self.middle_name_input, 4, 1)
        grid_layout.addWidget(self.dob_label, 5, 0)
        grid_layout.addWidget(self.dob_input, 5, 1)
        grid_layout.addWidget(self.city_label, 6, 0)
        grid_layout.addWidget(self.city_input, 6, 1)
        grid_layout.addWidget(self.role_label, 7, 0)
        grid_layout.addWidget(self.role_input, 7, 1)
        grid_layout.addWidget(self.sport_type_label, 8, 0)
        grid_layout.addWidget(self.sport_type_input, 8, 1)
        grid_layout.addWidget(self.phone_label, 9, 0)
        grid_layout.addWidget(self.phone_input, 9, 1)
        grid_layout.addWidget(self.email_label, 10, 0)
        grid_layout.addWidget(self.email_input, 10, 1)

        layout.addLayout(grid_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)  # Добавляем кнопку "Назад"

        self.setLayout(layout)

    def submit_form(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        middle_name = self.middle_name_input.text().strip()
        dob = self.dob_input.text().strip()
        city = self.city_input.text().strip()
        role = self.role_input.currentText()
        sport_type = self.sport_type_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not all([username, password, first_name, last_name, dob, city, phone, email]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()

        try:
            # Вставка пользователя
            insert_user_query = """
            INSERT INTO users (username, password, email, phone_number, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_query, (username, password, email, phone, role))
            user_id = cursor.lastrowid  # Получаем ID только что добавленного пользователя

            # Вывод отладочной информации
            print(f"Добавлен пользователь с ID: {user_id}")

            if role == "Sportsman":
                insert_athlete_query = """
                INSERT INTO sportsmen (user_id, first_name, last_name, patronymic, birthdate, city, typesport)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                print(f"Запрос для спортсмена: {insert_athlete_query}, параметры: {user_id}, {first_name}, {last_name}, {middle_name}, {dob}, {city}, {sport_type}")
                cursor.execute(insert_athlete_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type))

            elif role == "Trainer":
                insert_trainer_query = """
                INSERT INTO trainers (user_id, first_name, last_name, patronymic, birthdate, city, specialty)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                print(f"Запрос для тренера: {insert_trainer_query}, параметры: {user_id}, {first_name}, {last_name}, {middle_name}, {dob}, {city}, {sport_type}")
                cursor.execute(insert_trainer_query, (user_id, first_name, last_name, middle_name, dob,city, sport_type))

            db.commit()

            # Передача параметров для загрузки данных
            query = "SELECT user_id, username, password, email, phone_number, role FROM users"
            columns = ["user_id", "username", "password", "email", "phone_number", "role"]
            self.parent_window.load_data(query, columns)

            QMessageBox.information(self, "Успех", "Пользователь успешно создан.")
            self.close()
            self.parent_window.show()

        except mysql.connector.Error as e:
            db.rollback()
            print(f"Ошибка при выполнении запроса: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении пользователя в базу данных: {e}")
        finally:
            cursor.close()
            db.close()

    def go_back(self):
        """Обработчик для кнопки 'Назад'."""
        self.close()  # Закрыть текущее окно
        self.parent_window.show()  # Показать родительское окно

class CreateGroupWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание группы")
        self.setGeometry(530, 270, 450, 350)

        # Элементы формы
        self.group_name_label = QLabel("Название группы:")
        self.coach_id_label = QLabel("ID тренера:")

        # Поля ввода
        self.coach_id_input = QLineEdit()
        self.coach_id_input.setReadOnly(True)  # ID тренера будет заполняться автоматически
        self.group_name_input = QLineEdit()

        # Выпадающий список для выбора тренера
        self.coach_input = QComboBox()
        self.coach_input.currentIndexChanged.connect(self.update_coach_id)

        # Кнопка отправки формы
        self.submit_button = QPushButton("Создать группу")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.group_name_label, 0, 0)
        grid_layout.addWidget(self.group_name_input, 0, 1)
        grid_layout.addWidget(self.coach_id_label, 1, 0)
        grid_layout.addWidget(self.coach_id_input, 1, 1)
        grid_layout.addWidget(QLabel("Тренер:"), 2, 0)
        grid_layout.addWidget(self.coach_input, 2, 1)

        layout.addLayout(grid_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)  # Добавляем кнопку "Назад"

        self.setLayout(layout)

        self.load_coaches()

    def load_coaches(self):
        """Загружает список тренеров из базы данных в комбобокс"""
        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()

        try:
            select_coaches_query = "SELECT trainer_id, first_name, last_name FROM trainers"
            cursor.execute(select_coaches_query)

            coaches = cursor.fetchall()
            for coach in coaches:
                full_name = f"{coach[1]} {coach[2]}"  # Показать только имя и фамилию тренера
                self.coach_input.addItem(full_name, coach[0])  # ID тренера будет храниться в данных элемента

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке списка тренеров: {e}")

        finally:
            cursor.close()
            db.close()

    def update_coach_id(self):
        """Обновляет ID тренера при выборе тренера из списка"""
        selected_coach_id = self.coach_input.currentData()  # Получаем ID тренера из комбобокса
        self.coach_id_input.setText(str(selected_coach_id))  # Отображаем ID тренера в поле

    def submit_form(self):
        group_name = self.group_name_input.text().strip()
        coach_id = self.coach_id_input.text().strip()

        if not all([group_name, coach_id]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()

        try:
            insert_group_query = """
            INSERT INTO groups (name, trainer_id)
            VALUES (%s, %s)
            """
            cursor.execute(insert_group_query, (group_name, coach_id))
            group_id = cursor.lastrowid  # Получаем ID только что добавленной группы

            db.commit()

            QMessageBox.information(self, "Успех", "Группа успешно создана.")
            self.close()

            # Передаем нужный SQL-запрос и список столбцов для родительского окна
            query = "SELECT group_id, trainer_id, name FROM groups"
            columns = ["group_id", "trainer_id", "name"]  # Столбцы для отображения
            self.parent_window.load_data(query, columns)  # Вызываем метод load_data с нужными параметрами
            self.parent_window.show()

        except mysql.connector.Error as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении группы в базу данных: {e}")

        finally:
            cursor.close()
            db.close()

    def go_back(self):
        """Обработчик для кнопки 'Назад'."""
        self.close()  # Закрыть текущее окно
        self.parent_window.show()  # Показать родительское окно

class CreateRewardWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание Награды")
        self.setGeometry(530, 270, 450, 350)

        # Элементы формы
        self.sportsman_label = QLabel("Спортсмен:")
        self.competition_label = QLabel("Соревнование:")
        self.reward_date_label = QLabel("Дата награды (ДД.ММ.ГГГГ):")
        self.reward_description_label = QLabel("Описание награды:")

        # Поля ввода
        self.sportsman_input = QComboBox()  # Предполагается, что список спортсменов будет загружен в этот выпадающий список
        self.competition_input = QComboBox()  # То же самое для соревнований
        self.reward_date_input = QLineEdit()  # Ввод даты награды
        self.reward_description_input = QLineEdit()  # Описание награды

        # Кнопка отправки формы
        self.submit_button = QPushButton("Создать награду")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.sportsman_label, 0, 0)
        grid_layout.addWidget(self.sportsman_input, 0, 1)
        grid_layout.addWidget(self.competition_label, 1, 0)
        grid_layout.addWidget(self.competition_input, 1, 1)
        grid_layout.addWidget(self.reward_date_label, 2, 0)
        grid_layout.addWidget(self.reward_date_input, 2, 1)
        grid_layout.addWidget(self.reward_description_label, 3, 0)
        grid_layout.addWidget(self.reward_description_input, 3, 1)

        layout.addLayout(grid_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)  # Добавляем кнопку "Назад"

        self.setLayout(layout)

        # Загрузить спортсменов и соревнования
        self.load_sportsmen()
        self.load_competitions()

    def load_sportsmen(self):
        """Загружает список спортсменов в выпадающий список."""
        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE role = 'Sportsman'")

        sportsmen = cursor.fetchall()
        for sportsman in sportsmen:
            self.sportsman_input.addItem(sportsman[1], sportsman[0])  # Добавляем имя спортсмена и его ID

        cursor.close()
        db.close()

    def load_competitions(self):
        """Загружает список соревнований в выпадающий список."""
        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()
        cursor.execute("SELECT competition_id, name FROM competitions")

        competitions = cursor.fetchall()
        for competition in competitions:
            self.competition_input.addItem(competition[1], competition[0])  # Добавляем название соревнования и его ID

        cursor.close()
        db.close()

    def submit_form(self):
        sportsman_id = self.sportsman_input.currentData()  # Получаем ID выбранного спортсмена
        competition_id = self.competition_input.currentData()  # Получаем ID выбранного соревнования
        reward_date = self.reward_date_input.text().strip()
        reward_description = self.reward_description_input.text().strip()

        if not all([sportsman_id, competition_id, reward_date, reward_description]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверим, существует ли спортсмен в таблице sportsmen
        db = get_database_connection()  # Здесь мы вызываем глобальную функцию
        cursor = db.cursor()

        cursor.execute("SELECT 1 FROM sportsmen WHERE sportsman_id = %s", (sportsman_id,))
        if cursor.fetchone() is None:
            QMessageBox.warning(self, "Ошибка", "Указанный спортсмен не найден в базе данных.")
            cursor.close()
            db.close()
            return

        # Проверим, существует ли соревнование в таблице competitions
        cursor.execute("SELECT 1 FROM competitions WHERE competition_id = %s", (competition_id,))
        if cursor.fetchone() is None:
            QMessageBox.warning(self, "Ошибка", "Указанное соревнование не найдено в базе данных.")
            cursor.close()
            db.close()
            return

        # Преобразуем дату в нужный формат (ДД.ММ.ГГГГ -> ГГГГ-ММ-ДД)
        try:
            reward_date = QDate.fromString(reward_date, "dd.MM.yyyy").toString("yyyy-MM-dd")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            return

        try:
            # Вставка награды
            insert_reward_query = """
            INSERT INTO rewards (sportsman_id, competition_id, reward_date, reward_description)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_reward_query, (sportsman_id, competition_id, reward_date, reward_description))
            db.commit()

            QMessageBox.information(self, "Успех", "Награда успешно добавлена.")
            self.close()  # Закрыть текущее окно

            # Передаем нужный SQL-запрос и список столбцов для родительского окна
            query = "SELECT * FROM rewards"  # Пример SQL-запроса
            columns = ["reward_id", "sportsman_id", "competition_id", "reward_date", "reward_description"]  # Пример столбцов
            self.parent_window.load_data(query, columns)  # Передаем параметры для обновления данных

            self.parent_window.show()  # Показать родительское окно

        except mysql.connector.Error as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении награды в базу данных: {e}")
        finally:
            cursor.close()
            db.close()

    def go_back(self):
        """Обработчик для кнопки 'Назад'."""
        self.close()  # Закрыть текущее окно
        self.parent_window.show()  # Показать родительское окно

