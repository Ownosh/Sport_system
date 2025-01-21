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
        column_labels = ["ID Тренера", "Имя", "Фамилия", "Отчество", "Дата Рождения", "Специализация"]
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
            "SELECT trainer_id, first_name, last_name, patronymic, birthdate, specialty FROM trainers"
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
        self.setGeometry(400, 200, 400, 400)

        self.image_label = QLabel()
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.layout = QHBoxLayout()
        self.profile_layout = QVBoxLayout()
        self.profile_label = QLabel(f"Профиль тренера с ID: {trainer_id}")
        self.profile_layout.addWidget(self.profile_label)

        self.load_profile_data(trainer_id)

        self.profile_layout.addStretch()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)

        self.profile_layout.addWidget(self.button_box)
        self.layout.addLayout(self.profile_layout)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    def load_profile_data(self, trainer_id):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT first_name, last_name, patronymic, birthdate, specialty, photo FROM trainers WHERE trainer_id = %s", (trainer_id,))
                profile = cursor.fetchone()
                if profile:
                    profile_data = f"""
                    <b>Имя:</b> {profile[0]}<br>
                    <b>Фамилия:</b> {profile[1]}<br>
                    <b>Отчество:</b> {profile[2]}<br>
                    <b>Дата рождения:</b> {profile[3]}<br>
                    <b>Специализация:</b> {profile[4]}
                    """
                    self.profile_label.setText(profile_data)
                    if profile[5]:
                        pixmap = QPixmap()
                        pixmap.loadFromData(profile[5])
                        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    QMessageBox.warning(self, "Ошибка", "Профиль тренера не найден")
                    self.reject()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке профиля тренера: {e}")
            finally:
                cursor.close()
                connection.close()
