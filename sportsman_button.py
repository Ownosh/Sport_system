from PyQt6.QtWidgets import (QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QDialog, QDialogButtonBox, QLineEdit, QTextEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector
from change_buttons import get_database_connection

class SportsmenWindow(QWidget):
    def __init__(self, parent_window: QWidget):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Спортсмены")
        self.setGeometry(350, 150, 800, 600)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Верхняя панель
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        self.profile_button = QPushButton("Посмотреть профиль")
        self.profile_button.clicked.connect(self.view_profile)

        self.table_label = QLabel("Список спортсменов")
        self.table = QTableWidget()
        column_labels = [
            "ID Спортсмена", "Фамилия", 
            "Дата Рождения", "Пол", "Тип спорта"
        ]
        self.table.setColumnCount(len(column_labels))
        self.table.setHorizontalHeaderLabels(column_labels)
        self._resize_table_columns(column_labels)
        
                

        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #505050; /* Цвет фона таблицы */
                font-size: 12px;           /* Размер шрифта */
                border: 1px solid #d0d0d0; /* Граница таблицы */
                color: #ffffff;            /* Цвет текста */
            }
            QTableWidget::item {
                font-size: 12px; 
            }
            QHeaderView::section {
                font-size: 12px; 
                background-color: #707070; /* Цвет фона для заголовков */
                padding: 5px;
                color: #ffffff;            /* Цвет текста заголовков */
            }
            QTableWidget::item:selected {
                background-color: #808080; /* Цвет выделенного элемента */
            }
        """)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        top_layout.addWidget(self.profile_button)
        top_layout.addWidget(self.back_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        # Кнопки травм
        self.view_injuries_button = QPushButton("Просмотреть травмы и болезни")
        self.add_injury_button = QPushButton("Добавить травму или болезнь")

        injury_buttons_layout = QHBoxLayout()
        injury_buttons_layout.addWidget(self.view_injuries_button)
        injury_buttons_layout.addWidget(self.add_injury_button)

        main_layout.addLayout(injury_buttons_layout)
        self.setLayout(main_layout)

        # Подключение кнопок
        self.view_injuries_button.clicked.connect(self.open_view_injuries_dialog)
        self.add_injury_button.clicked.connect(self.open_add_injury_dialog)

    def _resize_table_columns(self, column_labels: list[str]):
        for i in range(len(column_labels)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

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

    def load_data(self):
        query = (
            "SELECT sportsman_id, last_name, "
            "birthdate, gender, typesport FROM sportsmen"
        )
        db = get_database_connection()
        if not db:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                for col_index, col in enumerate(row.keys()):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col])))
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

    def open_add_injury_dialog(self):
        self._open_injury_dialog("Выберите спортсмена для добавления травмы или болезни", InjuryDialog)

    def open_view_injuries_dialog(self):
        self._open_injury_dialog("Выберите спортсмена для просмотра травм и болезней", ViewInjuriesDialog)

    def _open_injury_dialog(self, error_message: str, dialog_class):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", error_message)
            return

        sportsman_id = self.table.item(selected_row, 0).text()
        dialog = dialog_class(self, sportsman_id)
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
    def __init__(self, parent, sportsman_id=None, injury_id=None):
        super().__init__(parent)
        self.sportsman_id = sportsman_id
        self.injury_id = injury_id  # Новый параметр для injury_id

        self.setWindowTitle("Добавление записи о травме или болезни")
        self.setGeometry(500, 300, 500, 400)

        self._initialize_ui()

        if self.injury_id:
            self.load_injury_details()

    def _initialize_ui(self):
        """Создаёт UI элементы."""
        self.layout = QVBoxLayout()

        self.participant_label = QLabel("Участник:")
        self.participant_input = QLineEdit(self.sportsman_id or "")
        self.participant_input.setReadOnly(True)

        self.period_label = QLabel("Период освобождения:")
        self.period_input = QLineEdit()

        self.description_label = QLabel("Описание:")
        self.description_input = QTextEdit()  # Многострочное текстовое поле

        # Добавление элементов в основной макет
        for widget in [
            self.participant_label, self.participant_input,
            self.period_label, self.period_input,
            self.description_label, self.description_input
        ]:
            self.layout.addWidget(widget)

        # Кнопки управления
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_injury)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.reject)

        # Макет для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.back_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # Стили
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

    def load_injury_details(self):
        """Загружает детали травмы для редактирования."""
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT period, injury_description FROM injuries WHERE injury_id = %s", (self.injury_id,))
                injury = cursor.fetchone()

                if injury:
                    self.period_input.setText(injury[0])
                    self.description_input.setPlainText(injury[1])
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных: {e}")
            finally:
                cursor.close()
                connection.close()

    def save_injury(self):
        """Сохраняет данные о травме, либо обновляет запись если injury_id существует."""
        participant = self.participant_input.text().strip()
        period = self.period_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not period or not description:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                if self.injury_id:
                    # Обновление существующей записи
                    query = "UPDATE injuries SET period = %s, injury_description = %s WHERE injury_id = %s"
                    cursor.execute(query, (period, description, self.injury_id))
                    QMessageBox.information(self, "Успех", "Запись успешно обновлена!")
                else:
                    # Добавление новой записи
                    query = "INSERT INTO injuries (sportsman_id, period, injury_description) VALUES (%s, %s, %s)"
                    cursor.execute(query, (participant, period, description))
                    QMessageBox.information(self, "Успех", "Запись успешно добавлена!")

                connection.commit()
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении записи: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Нет соединения с базой данных")




from PyQt6.QtCore import Qt

class ViewInjuriesDialog(QDialog):
    def __init__(self, parent, sportsman_id):
        super().__init__(parent)
        self.setWindowTitle("Травмы и болезни спортсмена")
        self.setGeometry(500, 300, 500, 400)

        self.sportsman_id = sportsman_id

        self.layout = QVBoxLayout()

        # Создание таблицы для отображения травм
        self.injuries_table = QTableWidget()
        self.injuries_table.setColumnCount(3)
        self.injuries_table.setHorizontalHeaderLabels(["Период освобождения", "Описание", "ID"])
        self.injuries_table.hideColumn(2)  # Скрываем столбец с ID

        # Включаем перенос текста в ячейках
        self.injuries_table.setWordWrap(True)

        self.layout.addWidget(self.injuries_table)
        self.load_injuries()

        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.reject)

        # Лэйаут для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # Подключение обработчиков событий
        self.edit_button.clicked.connect(self.edit_injury)
        self.delete_button.clicked.connect(self.delete_injury)

        # Отключаем кнопки при отсутствии выбранной строки
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Обработчик изменения выбора строки в таблице
        self.injuries_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
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

                    # Используем многострочный текст для "Описание"
                    description_item = QTableWidgetItem(injury[1])
                    description_item.setTextAlignment(Qt.AlignmentFlag.AlignTop)  # Для PyQt6 нужно использовать AlignmentFlag
                    self.injuries_table.setItem(row_index, 1, description_item)

                    self.injuries_table.setItem(row_index, 2, QTableWidgetItem(str(injury[2])))

                # Автоматическое изменение размера столбцов под их содержимое
                self.injuries_table.resizeColumnsToContents()
                
                # Устанавливаем ширину столбцов
                self.injuries_table.setColumnWidth(0, 170)  # Ширина для столбца "Период освобождения"
                self.injuries_table.setColumnWidth(1, 295)  # Ширина для столбца "Описание"
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных записей: {e}")
            finally:
                cursor.close()
                connection.close()

    def on_selection_changed(self):
        """ Обновление состояния кнопок в зависимости от выбора строки в таблице """
        selected_row = self.injuries_table.currentRow()
        self.edit_button.setEnabled(selected_row != -1)
        self.delete_button.setEnabled(selected_row != -1)

    def edit_injury(self):
        """ Редактирование выбранной травмы """
        selected_row = self.injuries_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")
            return

        injury_id = self.injuries_table.item(selected_row, 2).text()
        dialog = InjuryDialog(self, self.sportsman_id, injury_id=int(injury_id))
        dialog.exec()
        
        # После изменения данных обновим таблицу
        self.load_injuries()

    def delete_injury(self):
        """ Удаление выбранной травмы """
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







