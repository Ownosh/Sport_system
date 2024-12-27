from PyQt6.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QLineEdit, QComboBox, QDialogButtonBox
)
import mysql.connector
from windows_to_change import get_database_connection

class BaseWindow(QWidget):
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


class GroupWindow(BaseWindow):
    def __init__(self, parent_window):
        column_labels = ["group_id", "name", "trainer_id"]
        super().__init__(parent_window, "Группы", "Список групп", column_labels)

        self.create_group_button = QPushButton("Создать группу")
        self.edit_group_button = QPushButton("Изменить группу")
        self.delete_group_button = QPushButton("Удалить группу")

        self.add_people_button = QPushButton("Добавить людей в группу")
        self.view_people_button = QPushButton("Просмотреть людей в группе")
        self.delete_people_button = QPushButton("Удалить людей из группы")

        group_buttons_layout = QVBoxLayout()
        group_buttons_layout.addWidget(self.create_group_button)
        group_buttons_layout.addWidget(self.edit_group_button)
        group_buttons_layout.addWidget(self.delete_group_button)
        group_buttons_layout.addStretch()

        people_buttons_layout = QHBoxLayout()
        people_buttons_layout.addWidget(self.add_people_button)
        people_buttons_layout.addWidget(self.view_people_button)
        people_buttons_layout.addWidget(self.delete_people_button)

        main_layout = self.layout()
        main_layout.addLayout(group_buttons_layout)
        main_layout.addLayout(people_buttons_layout)

        self.create_group_button.clicked.connect(self.open_create_group_dialog)
        self.edit_group_button.clicked.connect(self.open_edit_group_dialog)
        self.delete_group_button.clicked.connect(self.delete_group)
        self.add_people_button.clicked.connect(self.open_add_people_dialog)
        self.view_people_button.clicked.connect(self.open_view_people_dialog)
        self.delete_people_button.clicked.connect(self.open_delete_people_dialog)

        self.load_data("SELECT group_id, name, trainer_id FROM groups",
                       ["group_id", "name", "trainer_id"])

    def open_create_group_dialog(self):
        dialog = CreateGroupDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.load_data("SELECT group_id, name, trainer_id FROM groups",
                           ["group_id", "name", "trainer_id"])

    def open_edit_group_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для изменения")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = EditGroupDialog(self, group_id)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.load_data("SELECT group_id, name, trainer_id FROM groups",
                           ["group_id", "name", "trainer_id"])

    def delete_group(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для удаления")
            return

        group_id = self.table.item(selected_row, 0).text()

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM groups WHERE group_id = %s", (group_id,))
                connection.commit()
                QMessageBox.information(self, "Успех", "Группа успешно удалена!")
                self.load_data("SELECT group_id, name, trainer_id FROM groups",
                               ["group_id", "name", "trainer_id"])
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении группы: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    def open_add_people_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для добавления людей")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = AddPeopleDialog(self, group_id)
        dialog.exec()

    def open_view_people_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для просмотра людей")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = ViewPeopleDialog(self, group_id)
        dialog.exec()

    def open_delete_people_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для удаления людей")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = DeletePeopleDialog(self, group_id)
        dialog.exec()


class CreateGroupDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Создать группу")

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Название группы:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.desc_label = QLabel("Описание группы:")
        self.desc_input = QLineEdit()
        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.create_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def create_group(self):
        name = self.name_input.text().strip()
        trainer_id = self.desc_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название группы!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO groups (name, trainer_id) VALUES (%s, %s)", (name, trainer_id))
                connection.commit()
                QMessageBox.information(self, "Успех", "Группа успешно создана!")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при создании группы: {e}")
                connection.rollback()
                self.reject()
            finally:
                cursor.close()
                connection.close()


class EditGroupDialog(QDialog):
    def __init__(self, parent, group_id):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle("Изменить группу")

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Название группы:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.desc_label = QLabel("Описание группы:")
        self.desc_input = QLineEdit()
        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_input)

        self.load_group_data()

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.edit_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def load_group_data(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT name, trainer_id FROM groups WHERE group_id = %s", (self.group_id,))
                group = cursor.fetchone()
                if group:
                    self.name_input.setText(group[0])
                    self.desc_input.setText
                    self.desc_input.setText(group[1])
                else:
                    QMessageBox.warning(self, "Ошибка", "Группа не найдена")
                    self.reject()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных группы: {e}")
            finally:
                cursor.close()
                connection.close()

    def edit_group(self):
        name = self.name_input.text().strip()
        trainer_id = self.desc_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название группы!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE groups SET name = %s, trainer_id = %s WHERE group_id = %s", (name, trainer_id, self.group_id))
                connection.commit()
                QMessageBox.information(self, "Успех", "Группа успешно изменена!")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при изменении группы: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()


class AddPeopleDialog(QDialog):
    def __init__(self, parent, group_id):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle("Добавить людей в группу")

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Добавить спортсменов в группу ID: {self.group_id}")
        self.layout.addWidget(self.label)

        self.athlete_combo = QComboBox()
        self.load_athletes()
        self.layout.addWidget(self.athlete_combo)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.add_athlete_to_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def load_athletes(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT sportsman_id, first_name, last_name FROM sportsmen")
                athletes = cursor.fetchall()
                for athlete in athletes:
                    self.athlete_combo.addItem(f"{athlete[1]} {athlete[2]} (ID: {athlete[0]})", athlete[0])
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке спортсменов: {e}")
            finally:
                cursor.close()
                connection.close()

    def add_athlete_to_group(self):
        athlete_id = self.athlete_combo.currentData()
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO sportsman_group (sportsman_id, group_id) VALUES (%s, %s)", (athlete_id, self.group_id))
                connection.commit()
                QMessageBox.information(self, "Успех", "Спортсмен успешно добавлен в группу!")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при добавлении спортсмена в группу: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()


class ViewPeopleDialog(QDialog):
    def __init__(self, parent, group_id):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle("Просмотреть людей в группе")

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.load_people()

        self.setLayout(self.layout)

    def load_people(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT s.sportsman_id, s.first_name, s.last_name
                    FROM sportsmen s
                    JOIN sportsman_group sg ON s.sportsman_id = sg.sportsman_id
                    WHERE sg.group_id = %s
                """, (self.group_id,))
                people = cursor.fetchall()
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["ID Спортсмена", "Имя", "Фамилия"])
                self.table.setRowCount(len(people))
                for row_index, person in enumerate(people):
                    self.table.setItem(row_index, 0, QTableWidgetItem(str(person[0])))
                    self.table.setItem(row_index, 1, QTableWidgetItem(person[1]))
                    self.table.setItem(row_index, 2, QTableWidgetItem(person[2]))
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке людей: {e}")
            finally:
                cursor.close()
                connection.close()


class DeletePeopleDialog(QDialog):
    def __init__(self, parent, group_id):
        super().__init__(parent)
        self.group_id = group_id
        self.setWindowTitle("Удалить людей из группы")

        self.layout = QVBoxLayout()

        self.athlete_combo = QComboBox()
        self.load_athletes()
        self.layout.addWidget(self.athlete_combo)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.delete_athlete_from_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def load_athletes(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "SELECT s.sportsman_id, s.first_name, s.last_name "
                    "FROM sportsmen s JOIN sportsman_group sg ON s.sportsman_id = sg.sportsman_id "
                    "WHERE sg.group_id = %s", (self.group_id,))
                athletes = cursor.fetchall()
                for athlete in athletes:
                    self.athlete_combo.addItem(f"{athlete[1]} {athlete[2]} (ID: {athlete[0]})", athlete[0])
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке спортсменов: {e}")
            finally:
                cursor.close()
                connection.close()

    def delete_athlete_from_group(self):
        athlete_id = self.athlete_combo.currentData()
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM sportsman_group WHERE sportsman_id = %s AND group_id = %s", (athlete_id, self.group_id))
                connection.commit()
                QMessageBox.information(self, "Успех", "Спортсмен успешно удален из группы!")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении спортсмена из группы: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
                