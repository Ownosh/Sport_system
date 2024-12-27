from PyQt6.QtWidgets import QWidget,QLineEdit,QGridLayout, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QHeaderView, QMessageBox, QTableWidgetItem
import mysql.connector
import os
from windows_to_change import CreateGroupWindow, CreateUserWindow,CreateRewardWindow

# Database connection function
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

# Base window class for all other windows
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

# Specific windows for various types (Awards, Users, etc.)
class AwardWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["reward_id","sportsman_id", "competition_id", "data", "reward_description"]
        super().__init__(parent_window, "Журнал наград", "Список наград", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_award)
        self.load_data("SELECT reward_id, sportsman_id, competition_id, reward_date, reward_description FROM rewards", 
                       ["reward_id","sportsman_id", "competition_id", "reward_date", "reward_description"])

    def add_award(self): 
        self.create_award_window = CreateRewardWindow(self)
        self.create_award_window.show()
        self.hide()
        
class UserWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID", "Логин", "Пароль", "Роль", "Телефон", "Email"]
        super().__init__(parent_window, "Журнал пользователей", "Список пользователей", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_user)
        self.load_data("SELECT user_id, username, password, role, phone_number, email FROM users", 
                       ["user_id", "username", "password", "role", "phone_number", "email"])

    def add_user(self):
        self.create_user_window = CreateUserWindow(self)
        self.create_user_window.show()
        self.hide()

class TrainingWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["training_id", "group_id", "date", "location"]
        super().__init__(parent_window, "Журнал тренировок", "Тренировки", column_labels, button_labels)
        self.load_data("SELECT training_id, group_id, date, location FROM trainings", 
               ["training_id", "group_id", "date", "location"])
        


class CompetitionWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["competition_id", "name", "date", "location"]
        super().__init__(parent_window, "Журнал соревнований", "Соревнования", column_labels, button_labels)
        self.load_data("SELECT competition_id, name, date, location FROM competitions", 
               ["competition_id", "name", "date", "location"])

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
    pass
