from PyQt6.QtWidgets import QWidget,QDialog, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QHeaderView, QMessageBox, QTableWidgetItem
import mysql.connector
from change_buttons import (
    CreateUserWindow,CreateRewardWindow, CreateTrainingWindow,get_database_connection, EditTrainingWindow, EditCompetitionWindow,EditUserWindow,EditRewardWindow,
    CreateCompetitionWindow)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap



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

        # Кнопки с текстом
        self.add_button = QPushButton(button_labels['add'])
        self.edit_button = QPushButton(button_labels['edit'])
        self.delete_button = QPushButton(button_labels['delete'])

        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #505050; /* Цвет фона таблицы */
                font-size: 12px;           /* Размер шрифта */
                border: 1px solid #d0d0d0; /* Граница таблицы */
            }
            QTableWidget::item {
                font-size: 12px; 
                padding: 5px;
            }
            QHeaderView::section {
                font-size: 12px; 
                background-color: #707070;
                padding: 5px;
            }
        """)


        # Макет кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()

        # Макет верхней части
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        # Макет контента
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.table)
        content_layout.addLayout(buttons_layout)

        # Основной макет
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

        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #505050; /* Цвет фона таблицы */
                font-size: 12px;           /* Размер шрифта */
                border: 1px solid #d0d0d0; /* Граница таблицы */
            }
            QTableWidget::item {
                font-size: 12px; 
                padding: 5px;
            }
            QHeaderView::section {
                font-size: 12px; 
                background-color: #707070; /* Цвет фона для заголовков */
                padding: 5px;
            }
        """)

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
        # Инициализируем с нужными параметрами
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID Награды", "ID Соревнования", "ID спортсмена", "Дата", "Описание награды"]
        super().__init__(parent_window, "Журнал наград", "Список наград", column_labels, button_labels)

        # Подключаем кнопки к методам
        self.add_button.clicked.connect(self.add_award)
        self.edit_button.clicked.connect(self.edit_award)
        self.delete_button.clicked.connect(self.delete_award)

        # Загружаем данные о наградах
        self.load_data("SELECT reward_id, competition_id, sportsman_id, reward_date, reward_description FROM rewards", 
                       ["reward_id", "competition_id", "sportsman_id", "reward_date", "reward_description"])

    def add_award(self):
        # Открыть окно для добавления награды
        self.create_award_window = CreateRewardWindow(self)
        self.create_award_window.show()
        self.hide()

    def edit_award(self):
        # Получаем выбранную строку в таблице
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите награду для редактирования")
            return

        # Получаем ID награды из выбранной строки
        reward_id = self.table.item(selected_row, 0).text()

        # Открываем окно редактирования с передачей reward_id
        self.edit_reward_window = EditRewardWindow(self, reward_id)
        self.edit_reward_window.show()

    def delete_award(self):
        # Получаем выбранную строку в таблице
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите награду для удаления")
            return

        # Получаем ID награды из выбранной строки
        reward_id = self.table.item(selected_row, 0).text()

        # Запрос на удаление награды
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка, существует ли награда в базе
                cursor.execute("SELECT reward_id FROM rewards WHERE reward_id = %s", (reward_id,))
                reward = cursor.fetchone()

                if reward:
                    # Удаление награды
                    cursor.execute("DELETE FROM rewards WHERE reward_id = %s", (reward_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Награда успешно удалена!")

                    # Обновляем данные на экране
                    self.load_data("SELECT reward_id, reward_date, reward_description FROM rewards", 
                                   ["reward_id", "reward_date", "reward_description"])
                else:
                    QMessageBox.warning(self, "Ошибка", "Такой награды нет!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении награды: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()



        
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
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        user_id = self.table.item(selected_row, 0).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя с ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    # Определяем, спортсмен или тренер
                    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
                    role_result = cursor.fetchone()
                    if not role_result:
                        QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
                        return

                    role = role_result[0]

                    if role == "sportsman":
                        # Получаем ID спортсмена
                        cursor.execute("SELECT sportsman_id FROM sportsmen WHERE user_id = %s", (user_id,))
                        sportsman_result = cursor.fetchone()
                        if sportsman_result:
                            sportsman_id = sportsman_result[0]

                            # Удаляем зависимости для спортсмена
                            cursor.execute("DELETE FROM training_attendance WHERE athlete_id = %s", (sportsman_id,))
                            cursor.execute("DELETE FROM sportsman_group WHERE sportsman_id = %s", (sportsman_id,))
                            cursor.execute("DELETE FROM recommendations WHERE sportsman_id = %s", (sportsman_id,))
                            cursor.execute("DELETE FROM rewards WHERE sportsman_id = %s", (sportsman_id,))
                            
                            # Удаляем запись из таблицы sportsmen
                            cursor.execute("DELETE FROM sportsmen WHERE sportsman_id = %s", (sportsman_id,))

                    elif role == "trainer":
                        # Получаем ID тренера
                        cursor.execute("SELECT trainer_id FROM trainers WHERE user_id = %s", (user_id,))
                        trainer_result = cursor.fetchone()
                        if trainer_result:
                            trainer_id = trainer_result[0]

                            # Удаляем зависимости для тренера
                            cursor.execute("DELETE FROM groups WHERE trainer_id = %s", (trainer_id,))
                            cursor.execute("DELETE FROM trainings WHERE trainer = %s", (trainer_id,))
                            cursor.execute("DELETE FROM recommendations WHERE trainer_id = %s", (trainer_id,))
                            cursor.execute("DELETE FROM competitions WHERE trainer = %s", (trainer_id,))
                            
                            # Удаляем запись из таблицы trainers
                            cursor.execute("DELETE FROM trainers WHERE trainer_id = %s", (trainer_id,))

                    # Удаляем пользователя из таблицы users
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    connection.commit()

                    QMessageBox.information(self, "Успех", "Пользователь успешно удален!")
                    self.load_data(
                        "SELECT user_id, username, password, role, phone_number, email FROM users",
                        ["user_id", "username", "password", "role", "phone_number", "email"],
                    )
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении пользователя: {e}")
                    connection.rollback()
                finally:
                    cursor.close()
                    connection.close()



class TrainingWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID Тренировки", "Название тренировки", "Название группы", "Дата", "Место проведения"]
        super().__init__(parent_window, "Журнал тренировок", "Тренировки", column_labels, button_labels)

        self.add_button.clicked.connect(self.add_training)
        self.edit_button.clicked.connect(self.edit_training)
        self.delete_button.clicked.connect(self.delete_training)

        # Загружаем данные
        self.refresh_training_list()

    def refresh_training_list(self):
        """Обновление списка тренировок."""
        query = """
            SELECT t.training_id, t.name_training, g.name, 
                   DATE_FORMAT(t.date, '%H:%i-%d-%m-%Y') as formatted_date, t.location 
            FROM trainings t
            JOIN groups g ON t.group_id = g.group_id
        """
        self.load_data(query, ["training_id", "name_training", "name", "formatted_date", "location"])

    def add_training(self):
        """Открытие окна добавления тренировки."""
        self.create_user_window = CreateTrainingWindow(self)
        self.hide()
        self.create_user_window.show()
        self.create_user_window.finished.connect(self.refresh_training_list)

    def edit_training(self):
        """Открытие окна редактирования тренировки."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренировку для редактирования")
            return

        training_id = self.table.item(selected_row, 0).text()
        self.create_user_window = EditTrainingWindow(self, training_id)
        self.create_user_window.show()

    def delete_training(self):
        """Удаление выбранной тренировки."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренировку для удаления")
            return

        training_id = self.table.item(selected_row, 0).text()

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT training_id FROM trainings WHERE training_id = %s", (training_id,))
                if not cursor.fetchone():
                    QMessageBox.warning(self, "Ошибка", "Такой тренировки нет!")
                    return

                cursor.execute("DELETE FROM training_attendance WHERE training_id = %s", (training_id,))
                cursor.execute("DELETE FROM trainings WHERE training_id = %s", (training_id,))
                connection.commit()
                QMessageBox.information(self, "Успех", "Тренировка успешно удалена!")
                self.refresh_training_list()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении тренировки: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        
        
class CompetitionWindow(BaseWindow):
    def __init__(self, parent_window):
        button_labels = {'add': "Добавить", 'edit': "Изменить", 'delete': "Удалить"}
        column_labels = ["ID Соревнования", "Название", "Дата", "ID Тренера", "Место проведения"]
        super().__init__(parent_window, "Журнал соревнований", "Соревнования", column_labels, button_labels)
        self.add_button.clicked.connect(self.add_competition)
        self.edit_button.clicked.connect(self.edit_competition)
        self.delete_button.clicked.connect(self.delete_competition)
        self.load_data("SELECT competition_id, name, DATE_FORMAT(date, '%H:%i-%d-%m-%Y') as formatted_date, trainer, location FROM competitions", 
               ["competition_id", "name", "formatted_date", "trainer", "location"])
        
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
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите соревнование для удаления")
            return

        competition_id = self.table.item(selected_row, 0).text()

        # Запрос на удаление соревнования
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Проверка, существует ли соревнование в базе
                cursor.execute("SELECT competition_id FROM competitions WHERE competition_id = %s", (competition_id,))
                competition = cursor.fetchone()

                if competition:
                    # Удаление соревнования
                    cursor.execute("DELETE FROM competitions WHERE competition_id = %s", (competition_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", "Соревнование успешно удалено!")

                    # Обновляем данные на экране
                    self.load_data("SELECT competition_id, name, DATE_FORMAT(date, '%H:%i-%d-%m-%Y') as formatted_date, trainer, location FROM competitions", 
                                   ["competition_id", "name", "formatted_date", "trainer", "location"])
                else:
                    QMessageBox.warning(self, "Ошибка", "Такого соревнования нет!")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении соревнования: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        

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
        self.table.setHorizontalHeaderLabels(["ID Пользователя", "Имя", "Фамилия"])
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
                
        





