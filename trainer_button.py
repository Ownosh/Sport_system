from PyQt6.QtWidgets import (QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QDialogButtonBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector
from change_buttons import get_database_connection

class TrainerWindow(QWidget):
    def __init__(self, parent_window: QWidget):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Тренеры")
        self.setGeometry(350, 150, 800, 600)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Верхняя панель
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        self.profile_button = QPushButton("Посмотреть профиль")
        self.profile_button.clicked.connect(self.view_profile)

        self.table_label = QLabel("Список тренеров")
        self.table = QTableWidget()
        column_labels = [ "ID Тренера", "Имя", "Фамилия", "Специализация"]
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

        self.setLayout(main_layout)

    def _resize_table_columns(self, column_labels: list[str]):
        for i in range(len(column_labels)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def go_back(self):
        self.close()
        self.parent_window.show()

    def view_profile(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите тренера для просмотра профиля")
            return

        trainer_id = self.table.item(selected_row, 0).text()
        dialog = ProfileDialog(self, trainer_id)
        dialog.exec()

    def load_data(self):
        query = (
            """SELECT t.trainer_id, t.first_name, t.last_name, t.specialty 
            FROM trainers t
            JOIN users u ON t.user_id = u.user_id  -- Связываем таблицы по user_id
             WHERE u.active = 1"""
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

class ProfileDialog(QDialog):
    def __init__(self, parent, trainer_id):
        super().__init__(parent)
        self.setWindowTitle("Профиль тренера")
        self.setGeometry(400, 200, 700, 300)

        # Фото тренера
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 300)
        self.image_label.setStyleSheet("border: 1px;border-radius: 5px; background-color: #707070;")

        # Информация профиля
        self.profile_label = QLabel()
        self.profile_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #ffffff;
                background-color: #707070;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.profile_label.setWordWrap(True)  # Чтобы длинный текст переносился на следующую строку

        # Кнопка OK
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                font-size: 12px;
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
        self.ok_button.setFixedHeight(40)
        self.ok_button.clicked.connect(self.accept)

        # Компоновка
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(self.profile_label)
        profile_layout.addStretch()
        profile_layout.addWidget(self.ok_button)

        layout = QHBoxLayout()
        layout.addLayout(profile_layout)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

        # Загрузка данных профиля
        self.load_profile_data(trainer_id)

    def load_profile_data(self, trainer_id):
        connection = get_database_connection()
        if not connection:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            self.reject()
            return

        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    trainer_id, user_id, first_name, last_name, patronymic, city, 
                    DATE_FORMAT(birthdate, '%d-%m-%Y') AS formatted_birthdate, 
                    gender, specialty, photo 
                FROM trainers 
                WHERE trainer_id = %s
            """
            cursor.execute(query, (trainer_id,))
            profile = cursor.fetchone()

            if profile:
                # Форматирование профиля
                profile_data = f"""
                    <b>ID тренера:</b> {profile['trainer_id']}<br>
                    <b>ID пользователя:</b> {profile['user_id']}<br>
                    <b>Имя:</b> {profile['first_name']}<br>
                    <b>Фамилия:</b> {profile['last_name']}<br>
                    <b>Отчество:</b> {profile['patronymic']}<br>
                    <b>Город:</b> {profile['city']}<br>
                    <b>Дата рождения:</b> {profile['formatted_birthdate']}<br>
                    <b>Пол:</b> {profile['gender']}<br>
                    <b>Специализация:</b> {profile['specialty']}
                """
                self.profile_label.setText(profile_data)

                # Загрузка фото
                if profile['photo']:
                    pixmap = QPixmap()
                    pixmap.loadFromData(profile['photo'])
                    self.image_label.setPixmap(
                        pixmap.scaled(
                            self.image_label.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                    )
                else:
                    self.image_label.setText("Фото отсутствует")
            else:
                QMessageBox.warning(self, "Ошибка", f"Профиль тренера с ID {trainer_id} не найден.")
                self.reject()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при выполнении запроса: {e}")
        finally:
            cursor.close()
            connection.close()



