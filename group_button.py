from PyQt6.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QLineEdit, QComboBox, QDialogButtonBox
)
import mysql.connector
from change_buttons import get_database_connection

class GroupWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Группы")
        self.setGeometry(350, 150, 800, 600)

        # Основной макет
        main_layout = QVBoxLayout()

        # Верхняя панель с заголовком и кнопкой назад
        self.table_label = QLabel("Список групп")
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID Группы", "Название группы", "ID Тренера"])
        for i in range(3):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

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


        # Кнопки управления группами
        self.create_group_button = QPushButton("Создать группу")
        self.edit_group_button = QPushButton("Изменить группу")
        self.delete_group_button = QPushButton("Удалить группу")

        group_buttons_layout = QVBoxLayout()
        group_buttons_layout.addWidget(self.create_group_button)
        group_buttons_layout.addWidget(self.edit_group_button)
        group_buttons_layout.addWidget(self.delete_group_button)
        group_buttons_layout.addStretch()

        # Кнопки управления участниками
        self.add_people_button = QPushButton("Добавить людей в группу")
        self.view_people_button = QPushButton("Просмотреть людей в группе")
        self.delete_people_button = QPushButton("Удалить людей из группы")

        people_buttons_layout = QHBoxLayout()
        people_buttons_layout.addWidget(self.add_people_button)
        people_buttons_layout.addWidget(self.view_people_button)
        people_buttons_layout.addWidget(self.delete_people_button)

        # Макет для основного контента
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.table)
        content_layout.addLayout(group_buttons_layout)

        # Компоновка всех элементов
        main_layout.addLayout(top_layout)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(people_buttons_layout)

        self.setLayout(main_layout)

        # Подключение сигналов к методам
        self.create_group_button.clicked.connect(self.open_create_group_dialog)
        self.edit_group_button.clicked.connect(self.open_edit_group_dialog)
        self.delete_group_button.clicked.connect(self.delete_group)
        self.add_people_button.clicked.connect(self.open_add_people_dialog)
        self.view_people_button.clicked.connect(self.open_view_people_dialog)
        self.delete_people_button.clicked.connect(self.open_delete_people_dialog)

        # Загрузка данных
        self.load_data()

    def go_back(self):
        self.close()
        self.parent_window.show()

    def load_data(self):
        query = """
            SELECT g.group_id, g.name, g.trainer_id
            FROM groups g
        """
        columns = ["group_id", "name", "trainer_id"]
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
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col]) if row[col] is not None else ""))
            # Обновляем заголовок таблицы
            self.table.setHorizontalHeaderLabels(["ID Группы", "Название группы", "ID Тренера"])
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()



    def open_create_group_dialog(self):
        dialog = CreateGroupDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def open_edit_group_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для изменения")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = EditGroupDialog(self, group_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

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
                self.load_data()
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
        self.setGeometry(400, 200, 400, 200)
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

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Название группы:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.trainer_label = QLabel("Выберите тренера:")
        self.trainer_combobox = QComboBox()
        self.load_trainers()  # Загрузка тренеров в выпадающий список
        self.layout.addWidget(self.trainer_label)
        self.layout.addWidget(self.trainer_combobox)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.create_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def load_trainers(self):
    # Загрузка всех тренеров в выпадающий список
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT t.trainer_id, t.last_name 
                    FROM trainers t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE u.active = 1
                """)
                trainers = cursor.fetchall()
                for trainer in trainers:
                    trainer_text = f"{trainer[1]} ID:{trainer[0]}"  # Формат: "Фамилия ID:trainer_id"
                    self.trainer_combobox.addItem(trainer_text, trainer[0])  # Отображаем текст, но храним ID
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке тренеров: {e}")
            finally:
                cursor.close()
                connection.close()


    def create_group(self):
        name = self.name_input.text().strip()
        trainer_id = self.trainer_combobox.currentData()  # Получаем trainer_id из выбранного элемента

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название группы!")
            return
        if not trainer_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера!")
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
        self.setGeometry(400, 200, 400, 200)
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

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Название группы:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.trainer_label = QLabel("Выберите тренера:")
        self.trainer_combobox = QComboBox()
        self.load_trainers()  # Загрузка тренеров в выпадающий список
        self.layout.addWidget(self.trainer_label)
        self.layout.addWidget(self.trainer_combobox)

        self.load_group_data()

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.edit_group)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def load_trainers(self):
    # Загрузка всех тренеров в выпадающий список
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT t.trainer_id, t.last_name 
                    FROM trainers t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE u.active = 1
                """)
                trainers = cursor.fetchall()
                for trainer in trainers:
                    trainer_text = f"{trainer[1]} ID:{trainer[0]}"  # Формат: "Фамилия ID:trainer_id"
                    self.trainer_combobox.addItem(trainer_text, trainer[0])  # Отображаем текст, но храним ID
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке тренеров: {e}")
            finally:
                cursor.close()
                connection.close()


    def load_group_data(self):
        # Загрузка данных для редактирования группы
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT name, trainer_id FROM groups WHERE group_id = %s", (self.group_id,))
                group = cursor.fetchone()
                if group:
                    self.name_input.setText(str(group[0]))  # Устанавливаем название группы
                    
                    trainer_id = group[1]
                    # Устанавливаем тренера в комбобокс
                    for index in range(self.trainer_combobox.count()):
                        if self.trainer_combobox.itemData(index) == trainer_id:
                            self.trainer_combobox.setCurrentIndex(index)
                            break
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
        trainer_id = self.trainer_combobox.currentData()  # Получаем trainer_id из выбранного элемента комбобокса

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название группы!")
            return
        if not trainer_id:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера!")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE groups SET name = %s, trainer_id = %s WHERE group_id = %s",
                               (name, trainer_id, self.group_id))
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
                # Выбираем только активных спортсменов через связь с таблицей users
                cursor.execute("""
                    SELECT s.sportsman_id, s.first_name, s.last_name 
                    FROM sportsmen s
                    JOIN users u ON s.user_id = u.user_id
                    WHERE u.active = 1 
                    ORDER BY s.first_name, s.last_name
                """)
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
        self.setGeometry(400, 200, 335, 400)

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
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении спортсмена из группы: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
                
                


class GroupWindowForTrainers(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Группы тренера")
        self.setGeometry(350, 150, 800, 600)

        # Основной макет
        main_layout = QVBoxLayout()

        # Верхняя панель с заголовком
        self.table_label = QLabel("Список групп тренера")

        # Таблица групп
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Добавляем 3-й столбец (ID Тренера)
        self.table.setHorizontalHeaderLabels(["ID Группы", "Название группы", "ID Тренера"])
        for i in range(3):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #505050;
                font-size: 12px;
                border: 1px solid #d0d0d0;
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

        # Кнопки справа
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        self.view_people_button = QPushButton("Просмотреть участников")
        self.view_people_button.clicked.connect(self.open_view_people_dialog)

        # Размещение кнопок справа
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.view_people_button)
        button_layout.addStretch()

        # Основной контентный макет (таблица слева, кнопки справа)
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.table)
        content_layout.addLayout(button_layout)

        # Компоновка элементов
        main_layout.addWidget(self.table_label)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Загрузка данных
        self.load_data()

    def go_back(self):
        self.close()
        self.parent_window.show()

    def load_data(self):
        query = """
            SELECT group_id, name, trainer_id
            FROM groups
        """
        db = get_database_connection()
        if not db:
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(row["group_id"])))
                self.table.setItem(row_index, 1, QTableWidgetItem(row["name"]))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(row["trainer_id"])))
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

    def open_view_people_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для просмотра участников")
            return

        group_id = self.table.item(selected_row, 0).text()
        dialog = ViewPeopleDialog(self, group_id)
        dialog.exec()
