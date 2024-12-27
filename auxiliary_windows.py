from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QHeaderView, QMessageBox, QTableWidgetItem
import mysql.connector
import os
from windows_to_change import CreateGroupWindow, CreateUserWindow,CreateRewardWindow, CreateTrainingWindow, CreateCompetitionWindow, DeleteTrainingWindow, DeleteCompetitionWindow, DeleteUserWindow, DeleteAwardWindow


def get_database_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        QMessageBox.critical(None, "Ошибка подключения", f"Ошибка при подключении к базе данных: {e}")
        return None

class BaseWindow(QWidget):
    def __init__(self, parent_window, title, table_label, column_labels, button_labels):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(title)
        self.setGeometry(350, 150, 800, 600)

        main_layout = QVBoxLayout()

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        self.table_label = QLabel(table_label)
        self.table = QTableWidget()
        self.table.setColumnCount(len(column_labels))
        self.table.setHorizontalHeaderLabels(column_labels)
        for i in range(len(column_labels)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self.add_button = QPushButton(button_labels['add'])
        self.edit_button = QPushButton(button_labels['edit'])
        self.delete_button = QPushButton(button_labels['delete'])

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.table)
        content_layout.addLayout(buttons_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def go_back(self):
        self.close()
        self.parent_window.show()

    def load_data(self, query, columns):
        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                for col_index, col in enumerate(columns):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col])))
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

class AwardWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["reward_id","sportsman_id", "competition_id", "data", "reward_description"]
        super().__init__(parent_window, "Журнал наград", "Список наград", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_award)
        self.delete_button.clicked.connect(self.delete_award)
        self.load_data("SELECT reward_id, sportsman_id, competition_id, reward_date, reward_description FROM rewards", 
                       ["reward_id","sportsman_id", "competition_id", "reward_date", "reward_description"])

    def add_award(self): 
        self.create_award_window = CreateRewardWindow(self)
        self.create_award_window.show()
        self.hide()
        
    def delete_award(self): 
        self.create_award_window = DeleteAwardWindow(self)
        self.create_award_window.show()
        self.hide()
        
class UserWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID", "Логин", "Пароль", "Роль", "Телефон", "Email"]
        super().__init__(parent_window, "Журнал пользователей", "Список пользователей", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.load_data("SELECT user_id, username, password, role, phone_number, email FROM users", 
                       ["user_id", "username", "password", "role", "phone_number", "email"])

    def add_user(self):
        self.create_user_window = CreateUserWindow(self)
        self.create_user_window.show()
        self.hide()
        
    def delete_user(self):
        self.create_user_window = DeleteUserWindow(self)
        self.create_user_window.show()
        self.hide()

class TrainingWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["training_id", "group_id", "date", "location"]
        super().__init__(parent_window, "Журнал тренировок", "Тренировки", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_training)
        self.delete_button.clicked.connect(self.delete_training)
        self.load_data("SELECT training_id, group_id, date, location FROM trainings", 
               ["training_id", "group_id", "date", "location"])
        
    def add_training(self): 
        self.create_user_window = CreateTrainingWindow(self)
        self.create_user_window.show()
        self.hide()
        
    def delete_training(self): 
        self.create_user_window = DeleteTrainingWindow(self)
        self.create_user_window.show()
        self.hide()
        
class CompetitionWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["competition_id", "name", "date", "location"]
        super().__init__(parent_window, "Журнал соревнований", "Соревнования", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_competition)
        self.delete_button.clicked.connect(self.delete_competition)
        self.load_data("SELECT competition_id, name, date, location FROM competitions", 
               ["competition_id", "name", "date", "location"])
        
    def add_competition(self):  
        self.create_user_window = CreateCompetitionWindow(self)
        self.create_user_window.show()
        self.hide()
        
    def delete_competition(self):  
        self.create_user_window = DeleteCompetitionWindow(self)
        self.create_user_window.show()
        self.hide()

class GroupWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["group_id", "trainer_id", "name"]
        super().__init__(parent_window, "Группы", "Списпок групп", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_group)
        self.load_data("SELECT group_id, trainer_id, name FROM groups", 
                       ["group_id", "trainer_id", "name"])
        
    def add_group(self):
        self.create_user_window = CreateGroupWindow(self)
        self.create_user_window.show()
        self.hide()

class SportsmenWindow(BaseWindow):
     def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["sportsman_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "gender","city", "typesport"]
        super().__init__(parent_window, "Спортсмены", "Списпок спортсменов", column_labels, button_labels)
        self.load_data("SELECT sportsman_id, user_id, first_name, last_name, patronymic, birthdate, gender, city, typesport FROM sportsmen", 
                       ["sportsman_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "gender","city", "typesport"])

class TrainerWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["trainer_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "specialty"]
        super().__init__(parent_window, "Тренера", "Списпок тренеров", column_labels, button_labels)
        self.load_data("SELECT trainer_id, user_id, first_name, last_name, patronymic, birthdate, specialty FROM trainers", 
                       ["trainer_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "specialty"])
        
class ProfileWindow(QWidget):
    def __init__(self, parent_window, username=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Профиль")
        self.setGeometry(350, 150, 400, 300)
        self.username = username
        print(self.username)

        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.role_label = QLabel("Роль: ")
        self.username_label = QLabel("Логин: ")
        self.password_label = QLabel("Пароль: ")

        layout.addWidget(self.role_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.password_label)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_profile_data(self):
        connection = get_database_connection()
        if connection and self.username:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT role, password FROM users WHERE username = %s", (self.username,))
                user = cursor.fetchone()
                if user:
                    role, password = user
                    self.role_label.setText(f"Роль: {role}")
                    self.username_label.setText(f"Логин: {self.username}")
                    self.password_label.setText(f"Пароль: {password}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def go_back(self):
        self.close()  
        self.parent_window.show()  

