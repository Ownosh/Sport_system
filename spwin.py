from PyQt6.QtWidgets import (QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QDialog, QDialogButtonBox, QLineEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector
from windows_to_change import get_database_connection

class BaseWindow2(QWidget):
    def __init__(self, parent_window, title, table_label, column_labels):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(title)
        self.setGeometry(350, 150, 1000, 600)

        main_layout = QVBoxLayout()

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        self.profile_button = QPushButton("Посмотреть профиль")
        self.profile_button.clicked.connect(self.view_profile)

        self.table_label = QLabel(table_label)
        self.table = QTableWidget()
        self.table.setColumnCount(len(column_labels))
        self.table.setHorizontalHeaderLabels(column_labels)
        for i in range(len(column_labels)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.profile_button)
        top_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def go_back(self):
        self.close()
        self.parent_window.show()

    def view_profile(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для просмотра профиля")
            return

        sportsman_id = self.table.item(selected_row, 0).text()
        dialog = ProfileDialog(self, sportsman_id)
        dialog.exec()

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

class SportsmenWindow(BaseWindow2):
    def __init__(self, parent_window):
        column_labels = ["sportsman_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "gender", "city", "typesport"]
        super().__init__(parent_window, "Спортсмены", "Список спортсменов", column_labels)
        
        self.load_data("SELECT sportsman_id, user_id, first_name, last_name, patronymic, birthdate, gender, city, typesport FROM sportsmen", 
                       ["sportsman_id", "user_id", "first_name", "last_name", "patronymic", "birthdate", "gender", "city", "typesport"])

        self.view_injuries_button = QPushButton("Просмотреть травмы и болезни")
        self.add_injury_button = QPushButton("Добавить травму или болезнь")

        injury_buttons_layout = QHBoxLayout()
        injury_buttons_layout.addWidget(self.view_injuries_button)
        injury_buttons_layout.addWidget(self.add_injury_button)

        self.layout().addLayout(injury_buttons_layout)

        self.view_injuries_button.clicked.connect(self.open_view_injuries_dialog)
        self.add_injury_button.clicked.connect(self.open_add_injury_dialog)

    def open_add_injury_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для добавления травмы или болезни")
            return

        sportsman_id = self.table.item(selected_row, 0).text()
        dialog = InjuryDialog(self, None, sportsman_id)
        dialog.exec()

    def open_view_injuries_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для просмотра травм и болезней")
            return

        sportsman_id = self.table.item(selected_row, 0).text()
        dialog = ViewInjuriesDialog(self, sportsman_id)
        dialog.exec()

class ProfileDialog(QDialog):
    def __init__(self, parent, sportsman_id):
        super().__init__(parent)
        self.setWindowTitle("Профиль спортсмена")
        self.setGeometry(400, 200, 400, 400)

        self.image_label = QLabel()
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.layout = QHBoxLayout()
        self.profile_layout = QVBoxLayout()
        self.profile_label = QLabel(f"Профиль спортсмена с ID: {sportsman_id}")
        self.profile_layout.addWidget(self.profile_label)

        self.load_profile_data(sportsman_id)

        self.profile_layout.addStretch()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        
        self.profile_layout.addWidget(self.button_box)
        self.layout.addLayout(self.profile_layout)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    def load_profile_data(self, sportsman_id):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT first_name, last_name, patronymic, birthdate, gender, city, typesport, photo FROM sportsmen WHERE sportsman_id = %s", (sportsman_id,))
                profile = cursor.fetchone()
                if profile:
                    profile_data = f"""
                    <b>Имя:</b> {profile[0]}<br>
                    <b>Фамилия:</b> {profile[1]}<br>
                    <b>Отчество:</b> {profile[2]}<br>
                    <b>Дата рождения:</b> {profile[3]}<br>
                    <b>Пол:</b> {profile[4]}<br>
                    <b>Город:</b> {profile[5]}<br>
                    <b>Вид спорта:</b> {profile[6]}
                    """
                    self.profile_label.setText(profile_data)
                    if profile[7]:
                        pixmap = QPixmap()
                        pixmap.loadFromData(profile[7])
                        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    QMessageBox.warning(self, "Ошибка", "Профиль спортсмена не найден")
                    self.reject()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке профиля спортсмена: {e}")
            finally:
                cursor.close()
                connection.close()

class InjuryDialog(QDialog):
    def __init__(self, parent, injury_id, sportsman_id):
        super().__init__(parent)
        self.setWindowTitle("Запись о травме или болезни")

        self.layout = QVBoxLayout()

        self.participant_label = QLabel("Участник:")
        self.participant_input = QLineEdit()
        self.participant_input.setText(sportsman_id)
        self.participant_input.setReadOnly(True)  # Поле только для чтения
        self.period_label = QLabel("Период освобождения:")
        self.period_input = QLineEdit()
        self.description_label = QLabel("Описание:")
        self.description_input = QLineEdit()

        self.layout.addWidget(self.participant_input)
        self.layout.addWidget(self.period_label)
        self.layout.addWidget(self.period_input)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(lambda: self.save_injury(injury_id))

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.back_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        if injury_id is not None:
            self.load_injury_data(injury_id)

    def load_injury_data(self, injury_id):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT sportsman_id, period, injury_description FROM injuries WHERE injury_id = %s", (injury_id,))
                injury = cursor.fetchone()
                if injury:
                    self.participant_input.setText(str(injury[0]))
                    self.period_input.setText(str(injury[1]))
                    self.description_input.setText(injury[2])
                else:
                    QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных записи: {e}")
            finally:
                cursor.close()
                connection.close()

    def save_injury(self, injury_id):
        participant = self.participant_input.text().strip()
        period = self.period_input.text().strip()
        description = self.description_input.text().strip()

        if not participant or not period or not description:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                if injury_id is None:
                    cursor.execute("INSERT INTO injuries (sportsman_id, period, injury_description) VALUES (%s, %s, %s)", 
                                   (participant, period, description))
                else:
                    cursor.execute("UPDATE injuries SET sportsman_id = %s, period = %s, injury_description = %s WHERE injury_id = %s",
                                   (participant, period, description, injury_id))
                connection.commit()
                QMessageBox.information(self, "Успех", "Запись успешно сохранена!")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении записи: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

class ViewInjuriesDialog(QDialog):
    def __init__(self, parent, sportsman_id):
        super().__init__(parent)
        self.setWindowTitle("Травмы и болезни спортсмена")

        self.sportsman_id = sportsman_id

        self.layout = QVBoxLayout()

        self.injuries_table = QTableWidget()
        self.injuries_table.setColumnCount(3)
        self.injuries_table.setHorizontalHeaderLabels(["Период освобождения", "Описание", "ID"])
        self.injuries_table.hideColumn(2)  # Скрываем столбец с ID

        self.layout.addWidget(self.injuries_table)
        self.load_injuries()

        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.edit_button.clicked.connect(self.edit_injury)
        self.delete_button.clicked.connect(self.delete_injury)

    def load_injuries(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT period, injury_description, injury_id FROM injuries WHERE sportsman_id = %s", (self.sportsman_id,))
                injuries = cursor.fetchall()
                self.injuries_table.setRowCount(len(injuries))
                for row_index, injury in enumerate(injuries):
                    self.injuries_table.setItem(row_index, 0, QTableWidgetItem(injury[0]))
                    self.injuries_table.setItem(row_index, 1, QTableWidgetItem(injury[1]))
                    self.injuries_table.setItem(row_index, 2, QTableWidgetItem(str(injury[2])))
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных записей: {e}")
            finally:
                cursor.close()
                connection.close()

    def edit_injury(self):
        selected_row = self.injuries_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")
            return

        injury_id = self.injuries_table.item(selected_row, 2).text()
        dialog = InjuryDialog(self, injury_id, self.sportsman_id)
        dialog.exec()
        self.load_injuries()

    def delete_injury(self):
        selected_row = self.injuries_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        injury_id = self.injuries_table.item(selected_row, 2).text()

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM injuries WHERE injury_id = %s", (injury_id,))
                connection.commit()
                QMessageBox.information(self, "Успех", "Запись успешно удалена!")
                self.load_injuries()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении записи: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()





