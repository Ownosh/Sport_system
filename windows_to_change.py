import mysql.connector
from PyQt6.QtWidgets import QWidget,QDialog,QFileDialog,QTextEdit, QVBoxLayout,QCheckBox,QTableWidgetItem, QDateTimeEdit,QTableWidget,QHeaderView,QHBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import os
from PyQt6.QtCore import QDateTime,QDate
from PyQt6.QtGui import QPixmap



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
        self.setGeometry(530, 270, 600, 400)  # Увеличиваем размеры окна

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
        layout = QHBoxLayout()  # Используем горизонтальный макет

        # Сетка для формы слева
        form_layout = QVBoxLayout()

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

        form_layout.addLayout(grid_layout)
        form_layout.addWidget(self.submit_button)
        form_layout.addWidget(self.back_button)  # Добавляем кнопку "Назад"

        # Панель для фото справа
        photo_layout = QVBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("border: 1px solid black;")

        self.add_photo_button = QPushButton("Добавить фото")
        self.add_photo_button.clicked.connect(self.add_photo)

        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.add_photo_button)
        photo_layout.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(photo_layout)

        self.setLayout(layout)

    def add_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.xpm *.jpg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(pixmap.scaled(self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.photo_file = file_name  # Сохраняем имя файла для последующего использования
 # Сохраняем имя файла для последующего использования

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

                # Добавление фото спортсмена
                if hasattr(self, 'photo_file'):
                    with open(self.photo_file, "rb") as file:
                        binary_data = file.read()
                    cursor.execute("UPDATE sportsmen SET photo = %s WHERE user_id = %s", (binary_data, user_id))

            elif role == "Trainer":
                insert_trainer_query = """
                INSERT INTO trainers (user_id, first_name, last_name, patronymic, birthdate, city, specialty)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                print(f"Запрос для тренера: {insert_trainer_query}, параметры: {user_id}, {first_name}, {last_name}, {middle_name}, {dob}, {city}, {sport_type}")
                cursor.execute(insert_trainer_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type))

                # Добавление фото тренера
                if hasattr(self, 'photo_file'):
                    with open(self.photo_file, "rb") as file:
                        binary_data = file.read()
                    cursor.execute("UPDATE trainers SET photo = %s WHERE user_id = %s", (binary_data, user_id))

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

class CreateRewardWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание Награды")
        self.setGeometry(530, 270, 450, 250)

        # Элементы формы
        self.sportsman_id_label = QLabel("ID Спортсмена:")
        self.competition_id_label = QLabel("ID Соревнования:")
        self.reward_date_label = QLabel("Дата награды (ДД.ММ.ГГГГ):")
        self.reward_description_label = QLabel("Описание награды:")

        # Поля ввода
        self.sportsman_id_input = QLineEdit()  # Ввод ID спортсмена
        self.competition_id_input = QLineEdit()  # Ввод ID соревнования
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
        grid_layout.addWidget(self.sportsman_id_label, 0, 0)
        grid_layout.addWidget(self.sportsman_id_input, 0, 1)
        grid_layout.addWidget(self.competition_id_label, 1, 0)
        grid_layout.addWidget(self.competition_id_input, 1, 1)
        grid_layout.addWidget(self.reward_date_label, 2, 0)
        grid_layout.addWidget(self.reward_date_input, 2, 1)
        grid_layout.addWidget(self.reward_description_label, 3, 0)
        grid_layout.addWidget(self.reward_description_input, 3, 1)

        layout.addLayout(grid_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def submit_form(self):
        sportsman_id = self.sportsman_id_input.text().strip()  # Получаем ID спортсмена
        competition_id = self.competition_id_input.text().strip()  # Получаем ID соревнования
        reward_date = self.reward_date_input.text().strip()
        reward_description = self.reward_description_input.text().strip()

        if not all([sportsman_id, competition_id, reward_date, reward_description]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Преобразуем дату в нужный формат (ДД.ММ.ГГГГ -> ГГГГ-ММ-ДД)
        try:
            reward_date = QDate.fromString(reward_date, "dd.MM.yyyy").toString("yyyy-MM-dd")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            return

        db = get_database_connection()
        cursor = db.cursor()
        try:
            # Проверим, существует ли спортсмен в таблице sportsmen
            cursor.execute("SELECT 1 FROM sportsmen WHERE sportsman_id = %s", (sportsman_id,))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "Ошибка", "Указанный спортсмен не найден в базе данных.")
                return

            # Проверим, существует ли соревнование в таблице competitions
            cursor.execute("SELECT 1 FROM competitions WHERE competition_id = %s", (competition_id,))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "Ошибка", "Указанное соревнование не найдено в базе данных.")
                return

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
                        # Обновляем таблицу с тренировками, указывая правильные аргументы для load_data
                        self.parent_window.load_data("SELECT training_id, name, date, trainer, group_id, location FROM trainings", 
                                                     ["training_id", "name", "date", "trainer", "group_id", "location"])  
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
                    self.parent_window.load_data("SELECT * FROM competitions", ["competition_id", "name", "date", "trainer", "location"])  # Обновляем таблицу с соревнованиями
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

class EditTrainingWindow(QDialog):
    def __init__(self, parent_window, training_id):
        super().__init__()
        self.parent_window=parent_window
        self.training_id = training_id
        self.setWindowTitle("Редактирование тренировки")
        self.setGeometry(530, 270, 450, 350)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        self.name_label = QLabel("Название тренировки:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit()
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
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить изменения")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.save_button)
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

        self.save_button.clicked.connect(self.save_training)
        self.back_button.clicked.connect(self.go_back)



    def load_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT name, date, trainer, group_id, location FROM trainings WHERE training_id = %s", (self.training_id,))
                training = cursor.fetchone()
                if training:
                    self.name_input.setText(training[0])
                    self.datetime_input.setDateTime(QDateTime.fromString(training[1].strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd HH:mm:ss"))
                    self.location_input.setText(training[4])

                    cursor.execute("SELECT trainer_id, last_name FROM trainers")
                    trainers = cursor.fetchall()
                    for trainer in trainers:
                        self.coach_input.addItem(trainer[1], trainer[0])
                    index = self.coach_input.findData(training[2])
                    if index != -1:
                        self.coach_input.setCurrentIndex(index)

                    cursor.execute("SELECT group_id, name FROM groups")
                    groups = cursor.fetchall()
                    for group in groups:
                        self.group_input.addItem(group[1], group[0])
                    index = self.group_input.findData(training[3])
                    if index != -1:
                        self.group_input.setCurrentIndex(index)

                    self.load_athletes()
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренировка не найдена")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных тренировки: {e}")
            finally:
                cursor.close()
                connection.close()



    def load_athletes(self):
        group_id = self.group_input.currentData()
        if not group_id:
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT s.sportsman_id, s.last_name, ta.is_present
                    FROM sportsmen s
                    LEFT JOIN training_attendance ta ON s.sportsman_id = ta.athlete_id AND ta.training_id = %s
                    WHERE s.sportsman_id IN (SELECT sportsman_id FROM sportsman_group WHERE group_id = %s)
                """, (self.training_id, group_id))
                sportsmen = cursor.fetchall()
                self.athletes_table.setRowCount(len(sportsmen))
                for row, athlete in enumerate(sportsmen):
                    name_item = QTableWidgetItem(athlete[1])
                    presence_checkbox = QCheckBox()
                    presence_checkbox.setChecked(athlete[2])
                    self.athletes_table.setItem(row, 0, name_item)
                    self.athletes_table.setCellWidget(row, 1, presence_checkbox)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных спортсменов: {e}")
            finally:
                cursor.close()
                connection.close()

    def save_training(self):
        training_name = self.name_input.text()
        training_datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        coach_id = self.coach_input.currentData()
        group_id = self.group_input.currentData()
        location = self.location_input.text()
        
        if not training_name or not training_datetime or not coach_id or not group_id or not location:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    UPDATE trainings SET name = %s, date = %s, trainer = %s, group_id = %s, location = %s
                    WHERE training_id = %s
                """, (training_name, training_datetime, coach_id, group_id, location, self.training_id))

                cursor.execute("DELETE FROM training_attendance WHERE training_id = %s", (self.training_id,))
                
                presence_data = []
                for row in range(self.athletes_table.rowCount()):
                    athlete_name = self.athletes_table.item(row, 0).text()
                    is_present = self.athletes_table.cellWidget(row, 1).isChecked()
                    cursor.execute("SELECT sportsman_id FROM sportsmen WHERE last_name = %s", (athlete_name,))
                    athlete = cursor.fetchone()
                    if athlete:
                        athlete_id = athlete[0]
                        presence_data.append((self.training_id, athlete_id, is_present))
                
                for training_id, athlete_id, is_present in presence_data:
                    cursor.execute("""
                        INSERT INTO training_attendance (training_id, athlete_id, is_present)
                        VALUES (%s, %s, %s)
                    """, (training_id, athlete_id, is_present))
                
                connection.commit()
                self.parent_window.load_data("SELECT * FROM trainings", ["training_id", "name", "date","location", "trainer", "group_id"])
                QMessageBox.information(self, "Успех", "Тренировка успешно сохранена!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении изменений: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()


    def go_back(self):
        self.close()

class EditCompetitionWindow(QDialog):
    def __init__(self, parent_window, competition_id):
        super().__init__()
        self.parent_window=parent_window
        self.competition_id = competition_id
        self.setWindowTitle("Редактирование соревнования")
        self.setGeometry(350, 150, 800, 400)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        self.name_label = QLabel("Название соревнования:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit()
        form_layout.addWidget(self.datetime_label)
        form_layout.addWidget(self.datetime_input)

        self.coach_label = QLabel("Тренер:")
        self.coach_input = QComboBox()
        form_layout.addWidget(self.coach_label)
        form_layout.addWidget(self.coach_input)

        self.location_label = QLabel("Местоположение:")
        self.location_input = QLineEdit()
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить изменения")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.save_button)
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

        self.save_button.clicked.connect(self.save_competition)
        self.back_button.clicked.connect(self.go_back)

    def load_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT name, date, trainer, location FROM competitions WHERE competition_id = %s", (self.competition_id,))
                competition = cursor.fetchone()
                if competition:
                    self.name_input.setText(competition[0])
                    self.datetime_input.setDateTime(QDateTime.fromString(competition[1].strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd HH:mm:ss"))
                    self.location_input.setText(competition[3])

                    cursor.execute("SELECT trainer_id, last_name FROM trainers")
                    trainers = cursor.fetchall()
                    for trainer in trainers:
                        self.coach_input.addItem(trainer[1], trainer[0])
                    index = self.coach_input.findData(competition[2])
                    if index != -1:
                        self.coach_input.setCurrentIndex(index)

                    self.load_athletes()
                else:
                    QMessageBox.warning(self, "Ошибка", "Соревнование не найдено")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных соревнования: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_athletes(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT s.sportsman_id, s.last_name, ca.is_present
                    FROM sportsmen s
                    LEFT JOIN competition_attendance ca ON s.sportsman_id = ca.athlete_id AND ca.competition_id = %s
                """, (self.competition_id,))
                sportsmen = cursor.fetchall()
                self.athletes_table.setRowCount(len(sportsmen))
                for row, athlete in enumerate(sportsmen):
                    name_item = QTableWidgetItem(athlete[1])
                    presence_checkbox = QCheckBox()
                    presence_checkbox.setChecked(bool(athlete[2]))  # Преобразование в bool
                    self.athletes_table.setItem(row, 0, name_item)
                    self.athletes_table.setCellWidget(row, 1, presence_checkbox)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных спортсменов: {e}")
            finally:
                cursor.close()
                connection.close()


    def save_competition(self):
        competition_name = self.name_input.text()
        competition_datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        coach_id = self.coach_input.currentData()
        location = self.location_input.text()

        if not competition_name or not competition_datetime or not coach_id or not location:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    UPDATE competitions SET name = %s, date = %s, trainer = %s, location = %s
                    WHERE competition_id = %s
                """, (competition_name, competition_datetime, coach_id, location, self.competition_id))

                cursor.execute("DELETE FROM competition_attendance WHERE competition_id = %s", (self.competition_id,))
                
                presence_data = []
                for row in range(self.athletes_table.rowCount()):
                    athlete_name = self.athletes_table.item(row, 0).text()
                    is_present = self.athletes_table.cellWidget(row, 1).isChecked()
                    cursor.execute("SELECT sportsman_id FROM sportsmen WHERE last_name = %s", (athlete_name,))
                    athlete = cursor.fetchone()
                    if athlete:
                        athlete_id = athlete[0]
                        presence_data.append((self.competition_id, athlete_id, is_present))
                
                for competition_id, athlete_id, is_present in presence_data:
                    cursor.execute("""
                        INSERT INTO competition_attendance (competition_id, athlete_id, is_present)
                        VALUES (%s, %s, %s)
                    """, (competition_id, athlete_id, is_present))
                
                connection.commit()
                self.parent_window.load_data("SELECT * FROM competitions", ["competition_id", "name", "date", "location", "trainer"])
                QMessageBox.information(self, "Успех", "Соревнование успешно сохранено!")
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении изменений: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()


class EditUserWindow(QWidget):
    def __init__(self, parent_window, user_id):
        super().__init__()
        self.parent_window = parent_window
        self.user_id = user_id
        self.setWindowTitle("Изменение пользователя")
        self.setGeometry(530, 270, 600, 400)  # Увеличиваем размеры окна

        # Элементы формы
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.email_label = QLabel("Электронная почта:")
        self.phone_label = QLabel("Номер телефона:")
        self.role_label = QLabel("Должность:")

        # Поля ввода
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.role_input = QComboBox()
        self.role_input.addItems(["Sportsman", "Trainer", "Admin"])

        # Кнопка отправки формы
        self.submit_button = QPushButton("Сохранить изменения")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.addWidget(self.username_label, 0, 0)
        form_layout.addWidget(self.username_input, 0, 1)
        form_layout.addWidget(self.password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)
        form_layout.addWidget(self.email_label, 2, 0)
        form_layout.addWidget(self.email_input, 2, 1)
        form_layout.addWidget(self.phone_label, 3, 0)
        form_layout.addWidget(self.phone_input, 3, 1)
        form_layout.addWidget(self.role_label, 4, 0)
        form_layout.addWidget(self.role_input, 4, 1)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)  # Добавляем кнопку "Назад"

        self.setLayout(layout)

        # Загружаем данные пользователя
        self.load_user_data()

    def load_user_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                print(f"Загрузка данных для пользователя с ID: {self.user_id}")
                # Получение данных из таблицы users
                cursor.execute("SELECT username, password, email, phone_number, role FROM users WHERE user_id = %s", (self.user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    print(f"Данные из таблицы users: {user_data}")
                    self.username_input.setText(user_data[0])
                    self.password_input.setText(user_data[1])
                    self.email_input.setText(user_data[2])
                    self.phone_input.setText(user_data[3])
                    index = self.role_input.findText(user_data[4].capitalize())
                    if index != -1:
                        self.role_input.setCurrentIndex(index)
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные пользователя")
            except mysql.connector.Error as e:
                print(f"Ошибка при загрузке данных пользователя: {e}")
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных пользователя: {e}")
            finally:
                cursor.close()
                connection.close()

    def submit_form(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        role = self.role_input.currentText()

        if not all([username, password, email, phone]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()

        try:
            # Обновление данных пользователя
            update_user_query = """
            UPDATE users SET username = %s, password = %s, email = %s, phone_number = %s, role = %s
            WHERE user_id = %s
            """
            cursor.execute(update_user_query, (username, password, email, phone, role, self.user_id))
            db.commit()

            # Передача параметров для загрузки данных
            query = "SELECT user_id, username, password, email, phone_number, role FROM users"
            columns = ["user_id", "username", "password", "email", "phone_number", "role"]
            self.parent_window.load_data(query, columns)

            QMessageBox.information(self, "Успех", "Данные пользователя успешно обновлены.")
            self.close()
            self.parent_window.show()

        except mysql.connector.Error as e:
            db.rollback()
            print(f"Ошибка при выполнении запроса: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных пользователя в базе данных: {e}")
        finally:
            cursor.close()
            db.close()

    def go_back(self):
        self.close()  # Закрыть текущее окно
        self.parent_window.show()  # Показать родительское окно


class AwardDetailWindow(QWidget):
    def __init__(self, parent_window, award_id):
        super().__init__()
        self.parent_window = parent_window
        self.award_id = award_id
        self.setWindowTitle("Изменение награды")
        self.setGeometry(530, 270, 600, 400)

        # Элементы формы
        self.award_name_label = QLabel("Название награды:")
        self.award_date_label = QLabel("Дата награды:")
        self.description_label = QLabel("Описание:")

        # Поля ввода
        self.award_name_input = QLineEdit()
        self.award_date_input = QLineEdit()
        self.description_input = QTextEdit()

        # Кнопка отправки формы
        self.submit_button = QPushButton("Сохранить изменения")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.addWidget(self.award_name_label, 0, 0)
        form_layout.addWidget(self.award_name_input, 0, 1)
        form_layout.addWidget(self.award_date_label, 1, 0)
        form_layout.addWidget(self.award_date_input, 1, 1)
        form_layout.addWidget(self.description_label, 2, 0)
        form_layout.addWidget(self.description_input, 2, 1, 4, 1)  # Увеличиваем высоту текстового поля

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        # Загружаем данные награды
        self.load_award_data()

    def load_award_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT reward_id, reward_date, reward_description FROM rewards WHERE reward_id = %s", (self.award_id,))
                award_data = cursor.fetchone()
                if award_data:
                    self.award_name_input.setText(str(award_data[0]))
                    self.award_date_input.setText(award_data[1].strftime("%Y-%m-%d"))  # Преобразуем дату в строку
                    self.description_input.setPlainText(award_data[2])
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные награды")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных награды: {e}")
            finally:
                cursor.close()
                connection.close()

    def submit_form(self):
        award_name = self.award_name_input.text().strip()
        award_date = self.award_date_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not all([award_name, award_date, description]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE rewards SET reward_id = %s, reward_date = %s, reward_description = %s WHERE reward_id = %s", (award_name, award_date, description, self.award_id))
                connection.commit()

                QMessageBox.information(self, "Успех", "Данные награды успешно обновлены.")
                self.close()
                self.parent_window.load_awards()  # Обновляем данные наград в родительском окне
                self.parent_window.show()

            except mysql.connector.Error as e:
                connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных награды: {e}")
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        """Обработчик для кнопки 'Назад'."""
        self.close()
        self.parent_window.show()  # Показать родительское окно

class SelectAwardWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Выберите награду для изменения")
        self.setGeometry(530, 270, 450, 150)

        # Элементы формы
        self.award_name_label = QLabel("ID награды:")
        self.award_name_input = QLineEdit()

        # Кнопка подтверждения
        self.submit_button = QPushButton("Изменить награду")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QVBoxLayout()

        form_layout = QGridLayout()
        form_layout.addWidget(self.award_name_label, 0, 0)
        form_layout.addWidget(self.award_name_input, 0, 1)
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def submit_form(self):
        award_id = self.award_name_input.text().strip()

        if not award_id:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите ID награды.")
            return

        # Проверка существования награды
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT 1 FROM rewards WHERE reward_id = %s", (award_id,))
                if cursor.fetchone() is None:
                    QMessageBox.warning(self, "Ошибка", "Указанная награда не найдена.")
                    return
                self.edit_award_window = AwardDetailWindow(self, award_id) 
                self.edit_award_window.show() 
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при проверке награды: {e}")
            finally:
                cursor.close()
                connection.close()
            

    def go_back(self):
        """Обработчик для кнопки 'Назад'."""
        self.close()
        self.parent_window.show()

    def load_awards(self):
        """Этот метод нужен для вызова из AwardDetailWindow"""
        self.parent_window.load_awards()

