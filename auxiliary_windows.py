from PyQt6.QtWidgets import QWidget,QDialog, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QHeaderView, QMessageBox, QTableWidgetItem
import mysql.connector
from windows_to_change import (
    CreateUserWindow,CreateRewardWindow, CreateTrainingWindow,get_database_connection, EditTrainingWindow, EditCompetitionWindow,EditUserWindow,SelectAwardWindow,
    CreateCompetitionWindow, DeleteTrainingWindow, DeleteCompetitionWindow, DeleteUserWindow, DeleteAwardWindow)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from PyQt6.QtWidgets import QSizePolicy


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

class BaseWindow2(QWidget):
    def __init__(self, parent_window, title, table_label, column_labels):
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

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

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
        column_labels = ["reward_id", "data", "reward_description"]
        super().__init__(parent_window, "Журнал наград", "Список наград", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_award)
        self.edit_button.clicked.connect(self.edit_award)
        self.delete_button.clicked.connect(self.delete_award)
        
    def load_awards(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT award_, award_date, description FROM awards WHERE sportsman_id = %s", (self.sportsman_id,))
                awards = cursor.fetchall()
                self.table.setRowCount(len(awards))
                for row, award in enumerate(awards):
                    self.table.setItem(row, 0, QTableWidgetItem(award[0]))
                    award_date = award[1].strftime("%Y-%m-%d") if award[1] else "Дата отсутствует"
                    self.table.setItem(row, 1, QTableWidgetItem(award_date))
                    self.table.setItem(row, 2, QTableWidgetItem(award[2]))
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке наград: {e}")
            finally:
                cursor.close()
                connection.close()



    def add_award(self): 
        self.create_award_window = CreateRewardWindow(self)
        self.create_award_window.show()
        self.hide()
        
    def edit_award(self): 
        self.create_award_window = SelectAwardWindow(self)
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
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.load_data("SELECT user_id, username, password, role, phone_number, email FROM users", 
                       ["user_id", "username", "password", "role", "phone_number", "email"])

    def add_user(self):
        self.create_user_window = CreateUserWindow(self)
        self.create_user_window.show()
        self.hide()
        
    def edit_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return

        user_id = self.table.item(selected_row, 0).text()
        self.edit_user_window = EditUserWindow(self, user_id)
        self.edit_user_window.show()

        
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
        self.edit_button.clicked.connect(self.edit_training)
        self.delete_button.clicked.connect(self.delete_training)
        self.load_data("SELECT training_id, group_id, date, location FROM trainings", 
               ["training_id", "group_id", "date", "location"])
        
    def add_training(self): 
        self.create_user_window = CreateTrainingWindow(self)
        self.create_user_window.show()
        self.hide()
        
    def edit_training(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренировку для редактирования")
            return

        training_id = self.table.item(selected_row, 0).text()
        self.create_user_window = EditTrainingWindow(self, training_id)
        self.create_user_window.show()
        
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
        self.edit_button.clicked.connect(self.edit_competition)
        self.delete_button.clicked.connect(self.delete_competition)
        self.load_data("SELECT competition_id, name, date, location FROM competitions", 
               ["competition_id", "name", "date", "location"])
        
    def add_competition(self):  
        self.create_user_window = CreateCompetitionWindow(self)
        self.create_user_window.show()
        self.hide()
    
    def edit_competition(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите соревнование для редактирования")
            return

        competition_id = self.table.item(selected_row, 0).text()
        self.edit_competition_window = EditCompetitionWindow(self, competition_id)
        self.edit_competition_window.show()

        
    def delete_competition(self):  
        self.create_user_window = DeleteCompetitionWindow(self)
        self.create_user_window.show()
        self.hide()

class TrainerWindow(BaseWindow2):
    def __init__(self, parent_window):
        column_labels = ["trainer_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "specialty"]
        super().__init__(parent_window, "Тренера", "Списпок тренеров", column_labels)
        
        self.load_data("SELECT trainer_id, user_id, first_name, last_name, patronymic, birthdate, specialty FROM trainers", 
                       ["trainer_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "specialty"])
        
        

class GroupWindowForTrainers(BaseWindow2):
    def __init__(self, parent_window):
        column_labels = ["group_id", "trainer_id", "name"]
        super().__init__(parent_window, "Группы", "Список групп", column_labels)
        
        self.load_data("SELECT group_id, trainer_id, name FROM groups", 
                       ["group_id", "trainer_id", "name"])

        # Добавляем кнопку для просмотра участников группы
        self.view_members_button = QPushButton("Просмотреть участников")
        self.view_members_button.clicked.connect(self.view_members)
        self.layout().addWidget(self.view_members_button)

    def view_members(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для просмотра участников")
            return

        group_id = self.table.item(selected_row, 0).text()
        self.members_window = GroupMembersWindow(self, group_id)
        self.members_window.show()

class GroupMembersWindow(QDialog):
    def __init__(self, parent_window, group_id):
        super().__init__()
        self.parent_window=parent_window
        self.group_id = group_id
        self.setWindowTitle("Участники группы")
        self.setGeometry(530, 270, 600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.load_members()

    def load_members(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT gm.sportsman_id, s.first_name, s.last_name 
                FROM sportsman_group gm
                JOIN sportsmen s ON gm.sportsman_id = s.sportsman_id
                WHERE gm.group_id = %s
                """
                cursor.execute(query, (self.group_id,))
                members = cursor.fetchall()
                self.table.setRowCount(len(members))
                for row, member in enumerate(members):
                    self.table.setItem(row, 0, QTableWidgetItem(str(member[0])))
                    self.table.setItem(row, 1, QTableWidgetItem(member[1]))
                    self.table.setItem(row, 2, QTableWidgetItem(member[2]))
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке участников группы: {e}")
            finally:
                cursor.close()
                connection.close()


class ProfileWindow(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        # Основной вертикальный макет
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Фото пользователя
        self.photo_label = QLabel("Фото отсутствует")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setFixedSize(400, 300)  # Фиксированный размер для фото
        self.photo_label.setStyleSheet("border: 1px solid #d0d0d0; background-color: #505050; ")  # Граница для визуализации
        layout.addWidget(self.photo_label)

        # Контейнер для данных с серым фоном
        data_container = QWidget()
        data_container_layout = QVBoxLayout(data_container)
        data_container_layout.setContentsMargins(10, 10, 10, 10)  # Отступы внутри контейнера
        data_container_layout.setSpacing(5)  # Расстояние между метками
        data_container.setStyleSheet("""
            background-color: #505050;  /* Светло-серый фон */
            border: 1px solid #d0d0d0;  /* Легкая граница */
        """)

        # Метки данных
        self.role_label = QLabel("Роль: ")
        self.username_label = QLabel("Логин: ")
        self.password_label = QLabel("Пароль: ")

        for label in (self.role_label, self.username_label, self.password_label):
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Выравнивание текста слева
            label.setStyleSheet("font-size: 14px; padding: 2px;")  # Увеличенный шрифт и отступы
            data_container_layout.addWidget(label)

        layout.addWidget(data_container)  # Добавляем контейнер в основной макет
        layout.setSpacing(15)  # Разделяем фото и данные

        self.setLayout(layout)

    def load_profile_data(self):
        connection = get_database_connection()
        if connection and self.username:
            cursor = connection.cursor()
            try:
                # Получение данных пользователя
                cursor.execute("SELECT role, password, photo FROM users WHERE username = %s", (self.username,))
                user = cursor.fetchone()
                if user:
                    role, password, photo = user
                    self.role_label.setText(f"Роль: {role}")
                    self.username_label.setText(f"Логин: {self.username}")
                    self.password_label.setText(f"Пароль: {password}")

                    # Загрузка фото пользователя
                    if photo:
                        pixmap = QPixmap()
                        pixmap.loadFromData(photo)  # Загрузка изображения из BLOB
                        pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        self.photo_label.setPixmap(pixmap)
                    else:
                        self.photo_label.setText("Фото отсутствует")
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()





