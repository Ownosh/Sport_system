import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from datetime import datetime
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

# Класс формы для создания пользователя
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
            insert_user_query = """
            INSERT INTO users (username, password, email, phone_number, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_query, (username, password, email, phone, role))

            user_id = cursor.lastrowid

            if role == "Спортсмен":
                insert_athlete_query = """
                INSERT INTO sportsmen (user_id, first_name, last_name, patronymic, birthdate, city, typesport)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_athlete_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type))
            elif role == "Тренер":
                insert_trainer_query = """
                INSERT INTO trainers (user_id, first_name, last_name, middle_name, dob, city, sport_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_trainer_query, (user_id, first_name, last_name, middle_name, dob, city, sport_type))

            db.commit()

            QMessageBox.information(self, "Успех", "Пользователь успешно создан.")
            self.close()
            self.parent_window.load_data() 
            self.parent_window.show()

        except mysql.connector.Error as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении пользователя в базу данных: {e}")

        finally:
            cursor.close()
            db.close()
       
    


