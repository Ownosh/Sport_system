import mysql.connector
from PyQt6.QtWidgets import QWidget,QDialog,QFormLayout,QFileDialog,QTextEdit, QDateEdit, QHBoxLayout, QVBoxLayout,QCheckBox,QTableWidgetItem, QDateTimeEdit,QTableWidget,QHeaderView,QHBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import os
from PyQt6.QtCore import QDateTime,QDate
from PyQt6.QtGui import QPixmap
from datetime import datetime, date 




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
        self.setGeometry(350, 150, 800, 400)

        # Элементы формы
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.first_name_label = QLabel("Имя:")
        self.last_name_label = QLabel("Фамилия:")
        self.middle_name_label = QLabel("Отчество:")
        self.dob_label = QLabel("Дата рождения (ДД.ММ.ГГГГ):")
        self.city_label = QLabel("Город:")
        self.gender_label = QLabel("Пол:")  # Добавленное поле "Пол"
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
        self.gender_input = QComboBox()  # Комбобокс для выбора пола
        self.gender_input.addItems(["male", "female"])  # Доступные опции
        self.role_input = QComboBox()
        self.role_input.addItems(["Sportsman", "Trainer"])  # Исключаем "Admin"
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
        layout = QHBoxLayout()
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
        grid_layout.addWidget(self.gender_label, 7, 0)  # Позиция для выбора пола
        grid_layout.addWidget(self.gender_input, 7, 1)  # Позиция для выбора пола
        grid_layout.addWidget(self.role_label, 8, 0)
        grid_layout.addWidget(self.role_input, 8, 1)
        grid_layout.addWidget(self.sport_type_label, 9, 0)
        grid_layout.addWidget(self.sport_type_input, 9, 1)
        grid_layout.addWidget(self.phone_label, 10, 0)
        grid_layout.addWidget(self.phone_input, 10, 1)
        grid_layout.addWidget(self.email_label, 11, 0)
        grid_layout.addWidget(self.email_input, 11, 1)

        form_layout.addLayout(grid_layout)
        form_layout.addWidget(self.submit_button)
        form_layout.addWidget(self.back_button)

        photo_layout = QVBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(400, 300)
        self.photo_label.setStyleSheet("")

        self.add_photo_button = QPushButton("Добавить фото")
        self.add_photo_button.clicked.connect(self.add_photo)

        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.add_photo_button)
        photo_layout.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(photo_layout)

        self.setLayout(layout)

    def add_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(pixmap.scaled(self.photo_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.photo_file = file_name

    def submit_form(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        middle_name = self.middle_name_input.text().strip()
        dob = self.dob_input.text().strip()
        city = self.city_input.text().strip()
        gender = self.gender_input.currentText()  # Получаем выбранный пол
        role = self.role_input.currentText()
        sport_type = self.sport_type_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not all([username, password, first_name, last_name, city, phone, email]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Преобразование даты для спортсмена и тренера в формат ГГГГ-ММ-ДД
        if dob:
            try:
                dob = datetime.strptime(dob, "%d.%m.%Y").strftime("%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Некорректный формат даты (используйте ДД.ММ.ГГГГ).")
                return
        else:
            dob = "0000-00-00"  # Если дата не указана, сохраняем в виде "0000-00-00"

        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor()

        try:
            insert_user_query = """
            INSERT INTO users (username, password, email, phone_number, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_query, (username, password, email, phone, role))
            user_id = cursor.lastrowid

            # Добавляем в зависимости от роли
            if role == "Sportsman":
                insert_sportsman_query = """
                INSERT INTO sportsmen (user_id, first_name, last_name, patronymic, birthdate, city, typesport, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sportsman_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type, gender))
            elif role == "Trainer":
                insert_trainer_query = """
                INSERT INTO trainers (user_id, first_name, last_name, patronymic, birthdate, city, specialty)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_trainer_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type))

            # Если была добавлена фотография
            if hasattr(self, 'photo_file'):
                with open(self.photo_file, "rb") as file:
                    photo_data = file.read()
                cursor.execute("UPDATE users SET photo = %s WHERE user_id = %s", (photo_data, user_id))

            db.commit()
            QMessageBox.information(self, "Успех", "Пользователь успешно создан.")
            self.close()
            self.parent_window.load_data("SELECT user_id, username, password, role, phone_number, email FROM users", ["user_id", "username", "password", "role", "phone_number", "email"])
            self.parent_window.show()

        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления пользователя: {e}")
        finally:
            cursor.close()
            db.close()

    def go_back(self):
        self.close()
        self.parent_window.show()

class CreateRewardWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание Награды")
        self.setGeometry(500, 300, 500, 400)  # Обновленный размер и позиция окна

        # Применяем стилизацию
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                font-size: 14px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Минимальная высота для многострочного поля */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

        # Элементы формы
        self.sportsman_id_label = QLabel("ID Спортсмена:")
        self.competition_id_label = QLabel("ID Соревнования:")
        self.reward_date_label = QLabel("Дата награды (ДД.ММ.ГГГГ):")
        self.reward_description_label = QLabel("Описание награды:")

        # Поля ввода
        self.sportsman_id_input = QLineEdit()
        self.competition_id_input = QLineEdit()
        self.reward_date_input = QLineEdit()

        # Многострочное текстовое поле для описания награды
        self.reward_description_input = QTextEdit()  # Используем QTextEdit для многострочного ввода

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

        # Горизонтальный layout для кнопок "Назад" и "Создать награду"
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.submit_button)

        layout.addLayout(button_layout)  # Добавляем горизонтальный layout с кнопками в основной layout

        self.setLayout(layout)

    def submit_form(self):
        sportsman_id = self.sportsman_id_input.text().strip()
        competition_id = self.competition_id_input.text().strip()
        reward_date = self.reward_date_input.text().strip()
        reward_description = self.reward_description_input.toPlainText().strip()  # Получаем текст из QTextEdit

        if not all([sportsman_id, competition_id, reward_date, reward_description]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Преобразуем дату в формат ГГГГ-ММ-ДД
        try:
            reward_date = QDate.fromString(reward_date, "dd.MM.yyyy").toString("yyyy-MM-dd")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            return

        db = get_database_connection()  # Убедитесь, что эта функция определена
        cursor = db.cursor()
        try:
            # Проверка существования спортсмена и соревнования
            cursor.execute("SELECT 1 FROM sportsmen WHERE sportsman_id = %s", (sportsman_id,))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "Ошибка", "Указанный спортсмен не найден.")
                return

            cursor.execute("SELECT 1 FROM competitions WHERE competition_id = %s", (competition_id,))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "Ошибка", "Указанное соревнование не найдено.")
                return

            # Вставка награды (не указываем reward_id, если он автоинкрементный)
            cursor.execute(
                "INSERT INTO rewards (sportsman_id, competition_id, reward_date, reward_description) "
                "VALUES (%s, %s, %s, %s)",
                (sportsman_id, competition_id, reward_date, reward_description)
            )
            db.commit()
            self.parent_window.load_data(
                "SELECT reward_id, reward_date, reward_description FROM rewards",
                ["reward_id", "reward_date", "reward_description"]
            )
            QMessageBox.information(self, "Успех", "Награда успешно добавлена.")
            self.close() 
            self.parent_window.show()

        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении награды: {e}")
        finally:
            cursor.close()
            db.close()

    def go_back(self):
        self.close()
        self.parent_window.show()


class CreateTrainingWindow(QDialog):
    def __init__(self, parent_window, config=None, user_role=None):
        super().__init__()
        self.parent_window = parent_window
        self.config = config  # Новый параметр конфигурации
        self.user_role = user_role  # Новый параметр роли пользователя
        self.setWindowTitle("Создание тренировки")
        self.setGeometry(350, 150, 800, 400)  # Размер окна

        # Добавление стилизации
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Минимальная высота для многострочного поля */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

        self.setup_ui()
        self.load_data_from_db()

    def setup_ui(self):
        main_layout = QHBoxLayout()  # Основной горизонтальный layout

        form_layout = QVBoxLayout()

        # Название тренировки
        self.name_label = QLabel("Название тренировки:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        # Дата и время тренировки
        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        form_layout.addWidget(self.datetime_label)
        form_layout.addWidget(self.datetime_input)

        # Тренер
        self.coach_label = QLabel("Тренер:")
        self.coach_input = QComboBox()
        form_layout.addWidget(self.coach_label)
        form_layout.addWidget(self.coach_input)

        # Группа
        self.group_label = QLabel("Группа:")
        self.group_input = QComboBox()
        self.group_input.currentIndexChanged.connect(self.load_athletes_for_selected_group)
        form_layout.addWidget(self.group_label)
        form_layout.addWidget(self.group_input)

        # Местоположение
        self.location_label = QLabel("Место проведения:")
        self.location_input = QLineEdit()
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить тренировку")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.back_button)
        form_layout.addLayout(buttons_layout)

        main_layout.addLayout(form_layout)  # Левый блок (форма)

        # Таблица спортсменов (правый блок)
        self.athletes_table = QTableWidget()
        self.athletes_table.setRowCount(0)
        self.athletes_table.setColumnCount(2)
        self.athletes_table.setHorizontalHeaderLabels(["Спортсмен", "Присутствует"])
        self.athletes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.athletes_table)  # Добавляем таблицу спортсменов справа

        # Устанавливаем layout в окно
        self.setLayout(main_layout)

        # Подключаем кнопки к методам
        self.add_button.clicked.connect(self.add_training)
        self.back_button.clicked.connect(self.go_back)

    def load_data_from_db(self):
        """Загрузка данных из базы данных."""
        connection = get_database_connection()  # Используем вашу функцию для подключения
        if connection:
            cursor = connection.cursor()
            try:
                # Загрузка групп
                cursor.execute("SELECT group_id, name FROM groups")
                groups = cursor.fetchall()
                self.group_input.addItems([group[1] for group in groups])

                # Загрузка тренеров, которые активны (active = 1)
                cursor.execute("""
                    SELECT t.trainer_id, t.last_name
                    FROM trainers t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE u.active = 1
                """)
                trainers = cursor.fetchall()
                for trainer in trainers:
                    self.coach_input.addItem(f"{trainer[1]} (ID: {trainer[0]})", trainer[0])  # Добавляем ID тренера

            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_athletes_for_selected_group(self):
        """Загрузка спортсменов для выбранной группы."""
        group_name = self.group_input.currentText()
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Получаем id выбранной группы
                cursor.execute("SELECT group_id FROM groups WHERE name = %s", (group_name,))
                group_id = cursor.fetchone()
                if group_id:
                    # Загрузка спортсменов в выбранной группе, которые активны (active = 1)
                    cursor.execute("""
                        SELECT s.sportsman_id, s.last_name
                        FROM sportsmen s
                        JOIN sportsman_group sg ON s.sportsman_id = sg.sportsman_id
                        JOIN users u ON s.user_id = u.user_id
                        WHERE sg.group_id = %s AND u.active = 1
                    """, (group_id[0],))
                    sportsmen = cursor.fetchall()
                    self.athletes_table.setRowCount(len(sportsmen))
                    for row, athlete in enumerate(sportsmen):
                        name_item = QTableWidgetItem(athlete[1])
                        presence_checkbox = QCheckBox()
                        self.athletes_table.setItem(row, 0, name_item)
                        self.athletes_table.setCellWidget(row, 1, presence_checkbox)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке спортсменов: {e}")
            finally:
                cursor.close()
                connection.close()

    def add_training(self):
        """Добавление тренировки в базу данных."""
        training_name = self.name_input.text().strip()
        training_datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        group_name = self.group_input.currentText()
        coach_name_with_id = self.coach_input.currentText()
        location = self.location_input.text().strip()

        # Проверка на заполненность полей
        if not training_name or not group_name or not coach_name_with_id or not location:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        # Извлечение ID тренера из строки
        coach_id = self.coach_input.currentData()

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Получение group_id
                cursor.execute("SELECT group_id FROM groups WHERE name = %s", (group_name,))
                group = cursor.fetchone()
                if not group:
                    QMessageBox.warning(self, "Ошибка", "Выбранная группа не найдена.")
                    return
                group_id = group[0]

                # Добавление тренировки
                cursor.execute("""INSERT INTO trainings (name_training, date, trainer, group_id, location)
                                  VALUES (%s, %s, %s, %s, %s)""",
                               (training_name, training_datetime, coach_id, group_id, location))
                connection.commit()

                # Получение training_id последней добавленной тренировки
                cursor.execute("SELECT LAST_INSERT_ID()")
                training_id = cursor.fetchone()[0]

                # Сохранение данных о присутствующих
                presence_data = []
                for row in range(self.athletes_table.rowCount()):
                    athlete_name = self.athletes_table.item(row, 0).text()
                    is_present = self.athletes_table.cellWidget(row, 1).isChecked()
                    cursor.execute("SELECT sportsman_id FROM sportsmen WHERE last_name = %s", (athlete_name,))
                    athlete = cursor.fetchone()
                    if athlete:
                        athlete_id = athlete[0]
                        presence_data.append((training_id, athlete_id, is_present))

                for training_id, athlete_id, is_present in presence_data:
                    cursor.execute("""INSERT INTO training_attendance (training_id, athlete_id, is_present)
                                      VALUES (%s, %s, %s)""", (training_id, athlete_id, is_present))

                connection.commit()

                # Закрытие текущего окна и обновление родительского окна с новым списком тренировок
                self.parent_window.refresh_training_list()  # Используем новый метод родительского класса
                self.close()
                self.parent_window.show()# Закрываем окно создания тренировки
                QMessageBox.information(self, "Успех", "Тренировка успешно добавлена!")
                
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при добавлении тренировки: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        """Возврат к родительскому окну."""
        self.close()
        self.parent_window.show()





class CreateCompetitionWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание соревнования")
        self.setGeometry(350, 150, 800, 400)

        # Установка стилей
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Минимальная высота для многострочного поля */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

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
        return "Стадион 1"  # Пример

    def load_data_from_db(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Загружаем активных тренеров
                cursor.execute("""
                    SELECT t.trainer_id, t.last_name 
                    FROM trainers t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE u.active = 1
                """)
                trainers = cursor.fetchall()
                self.coach_input.addItems([f"{row[1]} (ID: {row[0]})" for row in trainers])

                # Загружаем активных спортсменов
                cursor.execute("""
                    SELECT s.sportsman_id, s.last_name 
                    FROM sportsmen s
                    JOIN users u ON s.user_id = u.user_id
                    WHERE u.active = 1
                """)
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
        coach_data = self.coach_input.currentText()
        coach_id = coach_data.split("(ID: ")[1].strip(")")
        location = self.location_input.text()

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO competitions (name, date, trainer, location)
                    VALUES (%s, %s, %s, %s)
                """, (competition_name, competition_datetime, coach_id, location))
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
                self.parent_window.load_data("SELECT * FROM competitions", ["competition_id", "name", "date", "trainer", "location"])
                self.close()
                self.parent_window.show()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при добавлении соревнования: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        self.parent_window.show()
         
class EditTrainingWindow(QDialog):
    def __init__(self, parent_window, training_id):
        super().__init__()
        self.parent_window = parent_window
        self.training_id = training_id
        self.setWindowTitle("Редактирование тренировки")
        self.setGeometry(350, 150, 800, 400)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        # Название тренировки
        self.name_label = QLabel("Название тренировки:")
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        # Дата и время тренировки
        self.datetime_label = QLabel("Дата и время:")
        self.datetime_input = QDateTimeEdit()
        form_layout.addWidget(self.datetime_label)
        form_layout.addWidget(self.datetime_input)

        # Тренер
        self.coach_label = QLabel("Тренер:")
        self.coach_input = QComboBox()
        form_layout.addWidget(self.coach_label)
        form_layout.addWidget(self.coach_input)

        # Группа
        self.group_label = QLabel("Группа:")
        self.group_input = QComboBox()
        self.group_input.currentIndexChanged.connect(self.load_athletes)
        form_layout.addWidget(self.group_label)
        form_layout.addWidget(self.group_input)

        # Местоположение
        self.location_label = QLabel("Местоположение:")
        self.location_input = QLineEdit()
        form_layout.addWidget(self.location_label)
        form_layout.addWidget(self.location_input)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить изменения")
        self.back_button = QPushButton("Назад")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.back_button)
        form_layout.addLayout(buttons_layout)

        main_layout.addLayout(form_layout)

        # Таблица спортсменов
        self.athletes_table = QTableWidget()
        self.athletes_table.setRowCount(0)
        self.athletes_table.setColumnCount(2)
        self.athletes_table.setHorizontalHeaderLabels(["Спортсмен", "Присутствует"])
        self.athletes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        main_layout.addWidget(self.athletes_table)

        self.setLayout(main_layout)

        # Подключение кнопок
        self.save_button.clicked.connect(self.save_training)
        self.back_button.clicked.connect(self.go_back)

    def load_data(self):
        """Загрузка данных о тренировке и заполняет поля."""
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Загрузка данных тренировки
                cursor.execute("SELECT name_training, date, trainer, group_id, location FROM trainings WHERE training_id = %s", (self.training_id,))
                training = cursor.fetchone()
                if training:
                    self.name_input.setText(training[0])
                    self.datetime_input.setDateTime(QDateTime.fromString(training[1].strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd HH:mm:ss"))
                    self.location_input.setText(training[4])

                    # Загрузка активных тренеров
                    cursor.execute("""
                        SELECT t.trainer_id, t.last_name
                        FROM trainers t
                        JOIN users u ON t.user_id = u.user_id
                        WHERE u.active = 1
                    """)
                    trainers = cursor.fetchall()
                    for trainer in trainers:
                        self.coach_input.addItem(trainer[1], trainer[0])
                    index = self.coach_input.findData(training[2])
                    if index != -1:
                        self.coach_input.setCurrentIndex(index)

                    # Загрузка групп
                    cursor.execute("SELECT group_id, name FROM groups")
                    groups = cursor.fetchall()
                    for group in groups:
                        self.group_input.addItem(group[1], group[0])
                    index = self.group_input.findData(training[3])
                    if index != -1:
                        self.group_input.setCurrentIndex(index)

                    # Загрузка спортсменов
                    self.load_athletes()
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренировка не найдена")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных тренировки: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_athletes(self):
        """Загрузка спортсменов для выбранной группы, исключая неактивных."""
        group_id = self.group_input.currentData()
        if not group_id:
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Загрузка спортсменов из выбранной группы, которые активны
                cursor.execute("""
                    SELECT s.sportsman_id, s.last_name, ta.is_present
                    FROM sportsmen s
                    JOIN sportsman_group sg ON s.sportsman_id = sg.sportsman_id
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN training_attendance ta ON s.sportsman_id = ta.athlete_id AND ta.training_id = %s
                    WHERE sg.group_id = %s AND u.active = 1
                """, (self.training_id, group_id))
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

    def save_training(self):
        """Сохранение изменений тренировки в базе данных."""
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
                # Обновление информации о тренировке
                cursor.execute("""
                    UPDATE trainings SET name_training = %s, date = %s, trainer = %s, group_id = %s, location = %s
                    WHERE training_id = %s
                """, (training_name, training_datetime, coach_id, group_id, location, self.training_id))

                # Удаление старых данных о присутствующих
                cursor.execute("DELETE FROM training_attendance WHERE training_id = %s", (self.training_id,))

                # Сохранение новых данных о присутствующих
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

                # Подтверждение изменений
                connection.commit()
                self.parent_window.load_data("SELECT * FROM trainings", ["training_id", "name_training", "date","location", "trainer", "group_id"])
                QMessageBox.information(self, "Успех", "Тренировка успешно сохранена!")
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении изменений: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        """Закрыть текущее окно и вернуться в родительское окно."""
        self.close()

class EditCompetitionWindow(QDialog):
    def __init__(self, parent_window, competition_id):
        super().__init__()
        self.parent_window = parent_window
        self.competition_id = competition_id
        self.setWindowTitle("Редактирование соревнования")
        self.setGeometry(350, 150, 800, 400)
        
        self.setModal(True)

        self.setup_ui()
        self.load_data()
        self.apply_styles()

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

                    cursor.execute("""
                        SELECT t.trainer_id, t.last_name 
                        FROM trainers t
                        JOIN users u ON t.user_id = u.user_id
                        WHERE u.active = 1
                    """)
                    trainers = cursor.fetchall()
                    for trainer in trainers:
                        # Добавляем фамилию и ID тренера в QComboBox
                        self.coach_input.addItem(f"{trainer[1]} (ID: {trainer[0]})", trainer[0])
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
                    JOIN users u ON s.user_id = u.user_id
                    LEFT JOIN competition_attendance ca ON s.sportsman_id = ca.athlete_id AND ca.competition_id = %s
                    WHERE u.active = 1
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
                self.parent_window.load_data("SELECT competition_id, name, DATE_FORMAT(date, '%H:%i-%d-%m-%Y') as formatted_date, trainer, location FROM competitions", 
               ["competition_id", "name", "formatted_date", "trainer", "location"])
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

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Минимальная высота для многострочного поля */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        
class EditUserWindow(QWidget):
    def __init__(self, parent_window, user_id):
        super().__init__()
        self.parent_window = parent_window
        self.user_id = user_id
        self.setWindowTitle("Изменение пользователя")
        self.setGeometry(350, 150, 800, 400)

        # Применение стилей
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Minimum height for multi-line text field */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)
        
        self.setModal(True)

        # Элементы формы
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.first_name_label = QLabel("Имя:")
        self.last_name_label = QLabel("Фамилия:")
        self.middle_name_label = QLabel("Отчество:")
        self.dob_label = QLabel("Дата рождения (ДД.ММ.ГГГГ):")
        self.city_label = QLabel("Город:")
        self.sport_type_label = QLabel("Тип спорта:")
        self.phone_label = QLabel("Номер телефона:")
        self.email_label = QLabel("Электронная почта:")
        self.gender_label = QLabel("Пол:")
        self.active_label = QLabel("Активен:")

        # Поля ввода
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.city_input = QLineEdit()
        self.sport_type_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Пол выбора пола
        self.gender_input = QComboBox()
        self.gender_input.addItems(["male", "female"])

        # Чекбокс для активности
        self.active_checkbox = QCheckBox()
        self.active_checkbox.setChecked(True)  # По умолчанию активен

        # Кнопка отправки формы
        self.submit_button = QPushButton("Сохранить изменения")
        self.submit_button.clicked.connect(self.submit_form)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Размещение элементов на форме
        layout = QHBoxLayout()
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
        grid_layout.addWidget(self.gender_label, 7, 0)
        grid_layout.addWidget(self.gender_input, 7, 1)
        grid_layout.addWidget(self.sport_type_label, 8, 0)
        grid_layout.addWidget(self.sport_type_input, 8, 1)
        grid_layout.addWidget(self.phone_label, 9, 0)
        grid_layout.addWidget(self.phone_input, 9, 1)
        grid_layout.addWidget(self.email_label, 10, 0)
        grid_layout.addWidget(self.email_input, 10, 1)
        grid_layout.addWidget(self.active_label, 11, 0)
        grid_layout.addWidget(self.active_checkbox, 11, 1)

        form_layout.addLayout(grid_layout)
        form_layout.addWidget(self.submit_button)
        form_layout.addWidget(self.back_button)

        photo_layout = QVBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(400, 300)
        self.photo_label.setStyleSheet("border: 1px solid black;")

        self.add_photo_button = QPushButton("Изменить фото")
        self.add_photo_button.clicked.connect(self.add_photo)

        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.add_photo_button)
        photo_layout.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(photo_layout)

        self.setLayout(layout)

        # Загружаем данные пользователя
        self.load_user_data()

    def load_user_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT username, password, email, phone_number, role, active
                    FROM users
                    WHERE user_id = %s
                """, (self.user_id,))
                user_data = cursor.fetchone()

                if user_data:
                    # Заполняем основные поля
                    self.username_input.setText(user_data[0])
                    self.password_input.setText(user_data[1])
                    self.email_input.setText(user_data[2])
                    self.phone_input.setText(user_data[3])

                    # Устанавливаем активность
                    self.active_checkbox.setChecked(bool(user_data[5]))

                    # Загружаем фото
                    if user_data[4].lower() == "sportsman":
                        cursor.execute("""
                            SELECT photo
                            FROM sportsmen
                            WHERE user_id = %s
                        """, (self.user_id,))
                    elif user_data[4].lower() == "trainer":
                        cursor.execute("""
                            SELECT photo
                            FROM trainers
                            WHERE user_id = %s
                        """, (self.user_id,))

                    photo_data = cursor.fetchone()
                    if photo_data and photo_data[0]:
                        photo = QPixmap()
                        photo.loadFromData(photo_data[0])
                        self.photo_label.setPixmap(photo.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))

                    # Загружаем дополнительные данные в зависимости от роли
                    if user_data[4].lower() == "sportsman":
                        cursor.execute("""
                            SELECT first_name, last_name, patronymic, birthdate, city, typesport, gender
                            FROM sportsmen
                            WHERE user_id = %s
                        """, (self.user_id,))
                        sportsman_data = cursor.fetchone()
                        if sportsman_data:
                            self.first_name_input.setText(sportsman_data[0])
                            self.last_name_input.setText(sportsman_data[1])
                            self.middle_name_input.setText(sportsman_data[2] if sportsman_data[2] else "")
                            dob = sportsman_data[3]

                            # Преобразуем дату рождения в нужный формат
                            if isinstance(dob, datetime):
                                # Если dob - это объект datetime, форматируем его
                                dob = dob.strftime("%d.%m.%Y")
                            elif isinstance(dob, str):
                                # Если dob - строка, проверяем и преобразуем
                                try:
                                    dob = datetime.strptime(dob, "%Y-%m-%d").strftime("%d.%m.%Y")
                                except ValueError:
                                    dob = None
                            elif isinstance(dob, date):
                                # Если dob - это объект datetime.date, преобразуем его в строку
                                dob = dob.strftime("%d.%m.%Y")
                            self.dob_input.setText(dob if dob else "")

                            self.city_input.setText(sportsman_data[4] if sportsman_data[4] else "")
                            self.sport_type_input.setText(sportsman_data[5] if sportsman_data[5] else "")
                            self.gender_input.setCurrentText(sportsman_data[6] if sportsman_data[6] else "male")
                    else:
                        cursor.execute("""
                            SELECT first_name, last_name, patronymic, birthdate, city, specialty
                            FROM trainers
                            WHERE user_id = %s
                        """, (self.user_id,))
                        trainer_data = cursor.fetchone()
                        if trainer_data:
                            self.first_name_input.setText(trainer_data[0])
                            self.last_name_input.setText(trainer_data[1])
                            self.middle_name_input.setText(trainer_data[2] if trainer_data[2] else "")
                            dob = trainer_data[3]

                            # Преобразуем дату рождения в нужный формат
                            if isinstance(dob, datetime):
                                # Если dob - это объект datetime, форматируем его
                                dob = dob.strftime("%d.%m.%Y")
                            elif isinstance(dob, str):
                                # Если dob - строка, проверяем и преобразуем
                                try:
                                    dob = datetime.strptime(dob, "%Y-%m-%d").strftime("%d.%m.%Y")
                                except ValueError:
                                    dob = None
                            elif isinstance(dob, date):
                                # Если dob - это объект datetime.date, преобразуем его в строку
                                dob = dob.strftime("%d.%m.%Y")
                            self.dob_input.setText(dob if dob else "")

                            self.city_input.setText(trainer_data[4] if trainer_data[4] else "")
                            self.sport_type_input.setText(trainer_data[5] if trainer_data[5] else "")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные пользователя.")
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
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        middle_name = self.middle_name_input.text().strip()
        dob = self.dob_input.text().strip()
        city = self.city_input.text().strip()
        sport_type = self.sport_type_input.text().strip()
        gender = self.gender_input.currentText()
        active = 1 if self.active_checkbox.isChecked() else 0  # Получаем значение активности

        if not all([username, password, email, phone, first_name, last_name]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return

        try:
            if dob:
                # Преобразуем из формата "день.месяц.год" в "год-месяц-день"
                dob = datetime.strptime(dob, "%d.%m.%Y").strftime("%Y-%m-%d")
            else:
                dob = None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный формат даты (используйте ДД.ММ.ГГГГ).")
            return

        connection = get_database_connection()
        if not connection:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET username = %s, password = %s, email = %s, phone_number = %s, active = %s
                WHERE user_id = %s
            """, (username, password, email, phone, active, self.user_id))

            cursor.execute("SELECT role FROM users WHERE user_id = %s", (self.user_id,))
            role = cursor.fetchone()[0].lower()

            if role == "sportsman":
                cursor.execute("""
                    UPDATE sportsmen
                    SET first_name = %s, last_name = %s, patronymic = %s, birthdate = %s, city = %s, typesport = %s, gender = %s
                    WHERE user_id = %s
                """, (first_name, last_name, middle_name, dob if dob else None, city, sport_type, gender, self.user_id))

                if hasattr(self, 'photo_file'):
                    with open(self.photo_file, "rb") as file:
                        photo_data = file.read()
                    cursor.execute("UPDATE sportsmen SET photo = %s WHERE user_id = %s", (photo_data, self.user_id))

            elif role == "trainer":
                cursor.execute("""
                    UPDATE trainers
                    SET first_name = %s, last_name = %s, patronymic = %s, birthdate = %s, city = %s, specialty = %s
                    WHERE user_id = %s
                """, (first_name, last_name, middle_name, dob if dob else None, city, sport_type, self.user_id))

                if hasattr(self, 'photo_file'):
                    with open(self.photo_file, "rb") as file:
                        photo_data = file.read()
                    cursor.execute("UPDATE trainers SET photo = %s WHERE user_id = %s", (photo_data, self.user_id))

            connection.commit()
            QMessageBox.information(self, "Успех", "Данные пользователя успешно обновлены.")
            self.close()
            self.parent_window.show()
        except mysql.connector.Error as e:
            connection.rollback()
            print(f"Ошибка при выполнении запроса: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных пользователя: {e}")
        finally:
            cursor.close()
            connection.close()


    def add_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
            self.photo_file = file_name

    def go_back(self):
        self.close()
        self.parent_window.show()

class EditRewardWindow(QDialog):
    def __init__(self, parent_window, reward_id):
        super().__init__()
        self.parent_window = parent_window
        self.reward_id = reward_id  # ID награды передается при создании окна

        self.setWindowTitle("Редактирование награды")
        self.setGeometry(350, 150, 800, 400)
        
        self.setModal(True)

        self.setup_ui()
        self.load_reward_data()  # Загружаем данные сразу при открытии окна

    def setup_ui(self):
        # Применяем стилизацию
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
                padding: 5px;
            }
            QTextEdit {
                min-height: 80px; /* Минимальная высота для многострочного поля */
            }
            QPushButton {
                background-color: #707070;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

        layout = QVBoxLayout()

        # Поля для редактирования награды
        self.competition_id_label = QLabel("ID соревнования:")
        self.competition_id_input = QLineEdit()

        self.athlete_id_label = QLabel("ID спортсмена:")
        self.athlete_id_input = QLineEdit()

        self.reward_date_label = QLabel("Дата награды (гггг-мм-дд):")
        self.reward_date_input = QLineEdit()

        self.description_label = QLabel("Описание награды:")
        self.description_input = QTextEdit()

        form_layout = QGridLayout()
        form_layout.addWidget(self.competition_id_label, 0, 0)
        form_layout.addWidget(self.competition_id_input, 0, 1)
        form_layout.addWidget(self.athlete_id_label, 1, 0)
        form_layout.addWidget(self.athlete_id_input, 1, 1)
        form_layout.addWidget(self.reward_date_label, 2, 0)
        form_layout.addWidget(self.reward_date_input, 2, 1)
        form_layout.addWidget(self.description_label, 3, 0)
        form_layout.addWidget(self.description_input, 3, 1)

        layout.addLayout(form_layout)

        # Кнопки управления
        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_reward)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_reward_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Загружаем данные награды по её ID
                cursor.execute(
                    "SELECT competition_id, sportsman_id, reward_date, reward_description FROM rewards WHERE reward_id = %s",
                    (self.reward_id,)
                )
                reward_data = cursor.fetchone()
                if reward_data:
                    self.competition_id_input.setText(str(reward_data[0]))
                    self.athlete_id_input.setText(str(reward_data[1]))  # Используем спортсмен_id
                    self.reward_date_input.setText(reward_data[2].strftime("%Y-%m-%d"))
                    self.description_input.setPlainText(reward_data[3])
                else:
                    QMessageBox.warning(self, "Ошибка", "Награда не найдена.")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def save_reward(self):
        competition_id = self.competition_id_input.text().strip()
        athlete_id = self.athlete_id_input.text().strip()
        reward_date = self.reward_date_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not all([competition_id, athlete_id, reward_date, description]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка присутствия спортсмена на соревновании
                cursor.execute(
                    """
                    SELECT is_present FROM competition_attendance
                    WHERE competition_id = %s AND athlete_id = %s
                    """,
                    (competition_id, athlete_id)
                )
                attendance = cursor.fetchone()

                if not attendance or attendance[0] == 0:
                    QMessageBox.warning(
                        self, "Ошибка",
                        "Спортсмен не был на этом соревновании. Награду нельзя добавить."
                    )
                    return

                # Обновление награды
                cursor.execute(
                    """
                    UPDATE rewards
                    SET competition_id = %s, sportsman_id = %s, reward_date = %s, reward_description = %s
                    WHERE reward_id = %s
                    """,
                    (competition_id, athlete_id, reward_date, description, self.reward_id)
                )
                connection.commit()
                QMessageBox.information(self, "Успех", "Награда успешно обновлена.")
                self.close()

                # Передаем необходимые аргументы в load_data
                self.parent_window.load_data(
                    "SELECT reward_id, reward_date, reward_description FROM rewards",
                    ["reward_id", "reward_date", "reward_description"]
                )
            except mysql.connector.Error as e:
                connection.rollback()
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении: {e}")
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()
        self.parent_window.show()





