from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QHeaderView, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
import mysql.connector
import os

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
        self.setGeometry(800, 300, 600, 400)

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
        self.edit_button.clicked.connect(self.edit_award)
        self.delete_button.clicked.connect(self.delete_award)
        self.load_data("SELECT reward_id, sportsman_id, competition_id, reward_date, reward_description FROM rewards", 
                       ["reward_id","sportsman_id", "competition_id", "reward_date", "reward_description"])

    def add_award(self): QMessageBox.information(self, "Добавить награду", "Открывается окно добавления награды.")
    def edit_award(self): QMessageBox.information(self, "Изменить награду", "Открывается окно редактирования награды.")
    def delete_award(self): QMessageBox.information(self, "Удалить награду", "Запрос на удаление награды.")

class UserWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID", "Логин", "Пароль", "Роль", "Телефон", "Email"]
        super().__init__(parent_window, "Журнал пользователей", "Список пользователей", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_user)
        self.load_data("SELECT user_id, username, password, role, phone_number, email FROM users", 
                       ["user_id", "username", "password", "role", "phone_number", "email"])

    def add_user(self):
        from windows_to_change import CreateUserWindow
        self.create_user_window = CreateUserWindow(self)
        self.create_user_window.show()
        self.hide()

class TrainingWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["Тренировки"]
        super().__init__(parent_window, "Журнал тренировок", "Тренировки", column_labels, button_labels)

class CompetitionWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["Соревнования"]
        super().__init__(parent_window, "Журнал соревнований", "Соревнования", column_labels, button_labels)

class GroupWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["Группы"]
        super().__init__(parent_window, "Группы", "Список групп", column_labels, button_labels)

class SportsmenWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["Спортсмены"]
        super().__init__(parent_window, "Спортсмены", "Список спортсменов", column_labels, button_labels)

class TrainerWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["Тренеры"]
        super().__init__(parent_window, "Тренеры", "Список тренеров", column_labels, button_labels)

# Profile window to show admin details
class ProfileWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Профиль администратора")
        self.setGeometry(800, 300, 400, 300)

        main_layout = QVBoxLayout()

        self.username_label = QLabel("Логин: admin")
        self.role_label = QLabel("Роль: Администратор")
        self.logout_button = QPushButton("Вернуться обратно")
        self.logout_button.clicked.connect(self.logout)

        main_layout.addWidget(self.username_label)
        main_layout.addWidget(self.role_label)
        main_layout.addWidget(self.logout_button)

        self.setLayout(main_layout)

    def logout(self):
        self.close()
        self.parent_window.show()


