import mysql.connector
from PyQt6.QtWidgets import QWidget,QApplication, QVBoxLayout,QCheckBox,QTableWidgetItem, QDateTimeEdit,QTableWidget,QHeaderView,QHBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import QDate
import sys
import os
from PyQt6.QtCore import QDateTime


def get_database_connection(): 
    try:
        connection = mysql.connector.connect( 
                    host=os.getenv("DB_HOST"), 
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"), 
                    database=os.getenv("DB_NAME") 
        ) 
        return connection 
    except mysql.connector.Error as e: QMessageBox.critical(None, "Ошибка подключения", f"Ошибка при подключении к базе данных: {e}")

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

class CreateTrainingWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание тренировки")
        self.setGeometry(530, 270, 450, 350)
        
        self.setup_ui()
        self.load_data_from_db()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        self.name_label = QLabel("Название тренировки:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        form_layout.addWidget(self.datetime_label)
        form_layout.addWidget(self.datetime_input)

        self.coach_label = QLabel("Тренер:")
        self.coach_input = QComboBox()
        form_layout.addWidget(self.coach_label)
        form_layout.addWidget(self.coach_input)

        self.group_label = QLabel("Группа:")
        self.group_input = QComboBox()
        self.group_input.currentIndexChanged.connect(self.load_athletes)
        form_layout.addWidget(self.group_label)
        form_layout.addWidget(self.group_input)

        self.location_label = QLabel("Местоположение:")
        self.location_input = QLineEdit()
        self.location_input.setText(self.get_default_location())  
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить тренировку")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.back_button)
        form_layout.addLayout(buttons_layout)

        main_layout.addLayout(form_layout)

        self.athletes_table = QTableWidget()
        self.athletes_table.setRowCount(0)  
        self.athletes_table.setColumnCount(2)
        self.athletes_table.setHorizontalHeaderLabels(["Спортсмен", "Присутствует"])
        self.athletes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.athletes_table)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_training)
        self.back_button.clicked.connect(self.go_back)

    def get_default_location(self):
        return "Спортзал 1" 

    def load_data_from_db(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT trainer_id, last_name FROM trainers")
                trainers = cursor.fetchall()
                self.coach_input.addItems([f"{row[1]}" for row in trainers])

                cursor.execute("SELECT group_id, name FROM groups")
                groups = cursor.fetchall()
                self.group_input.addItems([f"{row[1]}" for row in groups])

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_athletes(self):
        group_name = self.group_input.currentText()
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT group_id FROM groups WHERE name = %s", (group_name,))
                group = cursor.fetchone()
                if group:
                    group_id = group[0]
                    cursor.execute("""
                        SELECT s.sportsman_id, s.last_name 
                        FROM sportsmen s 
                        JOIN sportsman_group sg ON s.sportsman_id = sg.sportsman_id 
                        WHERE sg.group_id = %s
                    """, (group_id,))
                    sportsmen = cursor.fetchall()
                    self.athletes_table.setRowCount(len(sportsmen))
                    for row, athlete in enumerate(sportsmen):
                        name_item = QTableWidgetItem(athlete[1])
                        presence_checkbox = QCheckBox()
                        self.athletes_table.setItem(row, 0, name_item)
                        self.athletes_table.setCellWidget(row, 1, presence_checkbox)
                else:
                    QMessageBox.warning(self, "Внимание", "Группа не найдена в базе данных.")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def add_training(self):
        training_name = self.name_input.text()
        training_datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        coach_name = self.coach_input.currentText()
        group_name = self.group_input.currentText()
        location = self.location_input.text()
        
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT trainer_id FROM trainers WHERE last_name = %s", (coach_name,))
                trainer = cursor.fetchone()
                if trainer:
                    trainer_id = trainer[0]
                    
                    cursor.execute("SELECT group_id FROM groups WHERE name = %s", (group_name,))
                    group = cursor.fetchone()
                    if group:
                        group_id = group[0]
                        
                        cursor.execute("""
                            INSERT INTO trainings (name, date, trainer, group_id, location)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (training_name, training_datetime, trainer_id, group_id, location))
                        training_id = cursor.lastrowid

                        presence_data = []
                        for row in range(self.athletes_table.rowCount()):
                            athlete_name = self.athletes_table.item(row, 0).text()
                            is_present = self.athletes_table.cellWidget(row, 1).isChecked()
                            cursor.execute("""
                                SELECT sportsman_id FROM sportsmen WHERE last_name = %s
                            """, (athlete_name,))
                            athlete = cursor.fetchone()
                            if athlete:
                                athlete_id = athlete[0]
                                presence_data.append((training_id, athlete_id, is_present))
                        
                        for training_id, athlete_id, is_present in presence_data:
                            cursor.execute("""
                                INSERT INTO training_attendance (training_id, athlete_id, is_present)
                                VALUES (%s, %s, %s)
                            """, (training_id, athlete_id, is_present))
                        
                        connection.commit()
                        QMessageBox.information(self, "Успех", "Тренировка успешно добавлена!")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Группа не найдена в базе данных.")
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренер не найден в базе данных.")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при добавлении тренировки: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close() 
        self.parent_window.show()  
        
class CreateCompetitionWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание соревнования")
        self.setGeometry(350, 150, 800, 400)
        
        self.setup_ui()
        self.load_data_from_db()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        # Левая часть с формой
        form_layout = QVBoxLayout()

        # Поле для названия соревнования
        self.name_label = QLabel("Название соревнования:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        # Поле для даты и времени соревнования
        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        form_layout.addWidget(self.datetime_label)
        form_layout.addWidget(self.datetime_input)

        # Поле для выбора тренера
        self.coach_label = QLabel("Тренер:")
        self.coach_input = QComboBox()
        form_layout.addWidget(self.coach_label)
        form_layout.addWidget(self.coach_input)

        # Поле для местоположения соревнования
        self.location_label = QLabel("Местоположение:")
        self.location_input = QLineEdit()
        self.location_input.setText(self.get_default_location())  # Устанавливаем значение по умолчанию
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        # Кнопки "Добавить соревнование" и "Назад"
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить соревнование")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.back_button)
        form_layout.addLayout(buttons_layout)

        main_layout.addLayout(form_layout)

        # Правая часть с таблицей
        self.athletes_table = QTableWidget()
        self.athletes_table.setRowCount(0)  # Изначально количество строк 0
        self.athletes_table.setColumnCount(2)
        self.athletes_table.setHorizontalHeaderLabels(["Спортсмен", "Отметить участников"])
        self.athletes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.athletes_table)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_competition)
        self.back_button.clicked.connect(self.go_back)

    def get_default_location(self):
        # Получаем местоположение по умолчанию. Здесь можно добавить логику для определения местоположения.
        return "Стадион 1"  # Пример

    def load_data_from_db(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Загружаем тренеров
                cursor.execute("SELECT trainer_id, last_name FROM trainers")
                trainers = cursor.fetchall()
                self.coach_input.addItems([f"{row[1]}" for row in trainers])

                # Загружаем всех спортсменов
                cursor.execute("SELECT sportsman_id, last_name FROM sportsmen")
                sportsmen = cursor.fetchall()
                self.athletes_table.setRowCount(len(sportsmen))
                for row, athlete in enumerate(sportsmen):
                    name_item = QTableWidgetItem(athlete[1])
                    presence_checkbox = QCheckBox()
                    self.athletes_table.setItem(row, 0, name_item)
                    self.athletes_table.setCellWidget(row, 1, presence_checkbox)

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def add_competition(self):
        competition_name = self.name_input.text()
        competition_datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        coach_name = self.coach_input.currentText()
        location = self.location_input.text()
        
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Получение идентификатора тренера
                cursor.execute("SELECT trainer_id FROM trainers WHERE last_name = %s", (coach_name,))
                trainer = cursor.fetchone()
                if trainer:
                    trainer_id = trainer[0]
                    
                    cursor.execute("""
                        INSERT INTO competitions (name, date, trainer, location)
                        VALUES (%s, %s, %s, %s)
                    """, (competition_name, competition_datetime, trainer_id, location))
                    competition_id = cursor.lastrowid

                    presence_data = []
                    for row in range(self.athletes_table.rowCount()):
                        athlete_name = self.athletes_table.item(row, 0).text()
                        is_present = self.athletes_table.cellWidget(row, 1).isChecked()
                        cursor.execute("""
                            SELECT sportsman_id FROM sportsmen WHERE last_name = %s
                        """, (athlete_name,))
                        athlete = cursor.fetchone()
                        if athlete:
                            athlete_id = athlete[0]
                            presence_data.append((competition_id, athlete_id, is_present))
                    
                    for competition_id, athlete_id, is_present in presence_data:
                        cursor.execute("""
                            INSERT INTO competition_attendance (competition_id, athlete_id, is_present)
                            VALUES (%s, %s, %s)
                        """, (competition_id, athlete_id, is_present))
                    
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Соревнование успешно добавлено!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренер не найден в базе данных.")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при добавлении соревнования: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close() 
        self.parent_window.show()  

class DeleteTrainingWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Удаление тренировки")
        self.setGeometry(350, 150, 400, 200)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_label = QLabel("ID тренировки:")
        self.id_input = QLineEdit()
        self.delete_button = QPushButton("Удалить тренировку")
        self.back_button = QPushButton("Назад")

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_training)
        self.back_button.clicked.connect(self.go_back)

    def delete_training(self):
        training_id = self.id_input.text().strip()

        if not training_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID тренировки!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка наличия тренировки в базе данных
                cursor.execute("SELECT training_id FROM trainings WHERE training_id = %s", (training_id,))
                training = cursor.fetchone()
                print(f"ID тренировки: {training_id}, Результат запроса: {training}")

                if training:
                    # Удаление записи из таблицы training_attendance, связанной с тренировкой
                    cursor.execute("DELETE FROM training_attendance WHERE training_id = %s", (training_id,))

                    # Удаление записи из таблицы trainings
                    cursor.execute("DELETE FROM trainings WHERE training_id = %s", (training_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Тренировка успешно удалена!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Такой тренировки нет!")
            except Exception as e:
                print(f"Ошибка: {e}")
                QMessageBox.warning(self, "Ошибка", "Такой тренировки нет!")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

         
class DeleteCompetitionWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Удаление соревнования")
        self.setGeometry(350, 150, 400, 200)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_label = QLabel("ID соревнования:")
        self.id_input = QLineEdit()
        self.delete_button = QPushButton("Удалить соревнование")
        self.back_button = QPushButton("Назад")

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_competition)
        self.back_button.clicked.connect(self.go_back)

    def delete_competition(self):
        competition_id = self.id_input.text().strip()

        if not competition_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID соревнования!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Удаление записи из таблицы competition_attendance, связанной с соревнованием
                cursor.execute("DELETE FROM competition_attendance WHERE competition_id = %s", (competition_id,))

                # Удаление записи из таблицы competitions
                cursor.execute("DELETE FROM competitions WHERE competition_id = %s", (competition_id,))
                connection.commit()
                QMessageBox.information(self, "Успех", "Соревнование успешно удалено!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении соревнования: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()
            
            
class DeleteCompetitionWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Удаление соревнования")
        self.setGeometry(350, 150, 400, 200)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_label = QLabel("ID соревнования:")
        self.id_input = QLineEdit()
        self.delete_button = QPushButton("Удалить соревнование")
        self.back_button = QPushButton("Назад")

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_competition)
        self.back_button.clicked.connect(self.go_back)

    def delete_competition(self):
        competition_id = self.id_input.text().strip()

        if not competition_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID соревнования!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка наличия соревнования в базе данных
                cursor.execute("SELECT competition_id FROM competitions WHERE competition_id = %s", (competition_id,))
                competition = cursor.fetchone()
                print(f"ID соревнования: {competition_id}, Результат запроса: {competition}")

                if competition:
                    # Удаление записи из таблицы competition_attendance, связанной с соревнованием
                    cursor.execute("DELETE FROM competition_attendance WHERE competition_id = %s", (competition_id,))

                    # Удаление записи из таблицы competitions
                    cursor.execute("DELETE FROM competitions WHERE competition_id = %s", (competition_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Соревнование успешно удалено!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Такого соревнования нет!")
            except Exception as e:
                print(f"Ошибка: {e}")
                QMessageBox.warning(self, "Ошибка", "Такого соревнования нет!")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()




class DeleteUserWindow(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Удаление пользователя")
        self.setGeometry(350, 150, 400, 200)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_label = QLabel("ID пользователя:")
        self.id_input = QLineEdit()
        self.delete_button = QPushButton("Удалить пользователя")
        self.back_button = QPushButton("Назад")

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_user)
        self.back_button.clicked.connect(self.go_back)

    def delete_user(self):
        user_id = self.id_input.text().strip()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID пользователя!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка наличия пользователя в базе данных
                cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                if user:
                    # Удаление пользователя из таблицы users
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Пользователь успешно удален!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Такого пользователя нет!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении пользователя: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

class DeleteAwardWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Удаление награды")
        self.setGeometry(350, 150, 400, 200)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_label = QLabel("ID награды:")
        self.id_input = QLineEdit()
        self.delete_button = QPushButton("Удалить награду")
        self.back_button = QPushButton("Назад")

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete_award)
        self.back_button.clicked.connect(self.go_back)

    def delete_award(self):
        award_id = self.id_input.text().strip()

        if not award_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID награды!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка наличия награды в базе данных
                cursor.execute("SELECT reward_id FROM rewards WHERE reward_id = %s", (award_id,))
                award = cursor.fetchone()

                if award:
                    # Удаление награды из таблицы awards
                    cursor.execute("DELETE FROM rewards WHERE reward_id = %s", (award_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Награда успешно удалена!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Такой награды нет!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", "Такой награды нет!")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()






