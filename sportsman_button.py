from PyQt6.QtWidgets import (QWidget, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QDialog, QInputDialog, QLineEdit, QTextEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector
from change_buttons import get_database_connection

from database_functions import get_trainers

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox
)
from change_buttons import get_database_connection  # Подключение к БД

from characteristics_button import CharacteristicsTrainingWindow, ResultsWindow



class AdminSportsmenWindow(QWidget):
    def __init__(self, parent_window: QWidget):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Спортсмены")
        self.setGeometry(350, 150, 900, 600)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.create_buttons()
        self.create_table()
        self.create_layouts()

    def create_buttons(self):
        self.back_button = self.create_button("Назад", self.go_back)
        self.profile_button = self.create_button("Посмотреть профиль", self.view_profile)
        self.view_progress_button = self.create_button("Посмотреть прогресс", self.view_progress)
        self.add_progress_button = self.create_button("Добавить прогресс", self.add_progress)
        self.view_recommendations_button = self.create_button("Посмотреть рекомендации", self.view_recommendations)
        self.view_injuries_button = self.create_button("Просмотреть травмы", self.open_view_injuries_dialog)
        self.add_injury_button = self.create_button("Добавить травму", self.open_add_injury_dialog)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button

    def create_table(self):
        self.table_label = QLabel("Список спортсменов")
        self.table = QTableWidget()
        column_labels = ["ID Спортсмена", "Имя", "Фамилия", "Тип спорта"]
        self.table.setColumnCount(len(column_labels))
        self.table.setHorizontalHeaderLabels(column_labels)
        self._resize_table_columns(column_labels)

    def create_layouts(self):
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addWidget(self.profile_button)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.back_button)

        self.progress_buttons_layout = QVBoxLayout()
        self.progress_buttons_layout.addWidget(self.view_progress_button)
        self.progress_buttons_layout.addWidget(self.add_progress_button)
        self.progress_buttons_layout.addWidget(self.view_recommendations_button)
        self.progress_buttons_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(self.progress_buttons_layout)

        injury_buttons_layout = QHBoxLayout()
        injury_buttons_layout.addWidget(self.view_injuries_button)
        injury_buttons_layout.addWidget(self.add_injury_button)

        final_layout = QVBoxLayout()
        final_layout.addLayout(top_buttons_layout)
        final_layout.addLayout(main_layout)
        final_layout.addLayout(injury_buttons_layout)

        self.setLayout(final_layout)

    def _resize_table_columns(self, column_labels: list[str]):
        for i in range(len(column_labels)):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def go_back(self):
        self.close()
        self.parent_window.show()

    def view_profile(self):
        self._open_dialog(ProfileDialog, "Выберите спортсмена для просмотра профиля")

    def view_progress(self):
        self._open_window(ResultsWindow, "Выберите спортсмена для просмотра прогресса")

    def add_progress(self):
        self._open_window(CharacteristicsTrainingWindow, "Выберите спортсмена для добавления прогресса")

    def load_data(self):
        query = (
            "SELECT s.sportsman_id, s.first_name, s.last_name, s.typesport "
            "FROM sportsmen s "
            "JOIN users u ON s.user_id = u.user_id "
            "WHERE u.active = 1"
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
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

    def open_add_injury_dialog(self):
        self._open_injury_dialog("Выберите спортсмена для добавления травмы", InjuryDialog)

    def open_view_injuries_dialog(self):
        self._open_injury_dialog("Выберите спортсмена для просмотра травм", ViewInjuriesDialog)

    def _open_injury_dialog(self, error_message: str, dialog_class):
        self._open_dialog(dialog_class, error_message)

    def _open_dialog(self, dialog_class, error_message):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", error_message)
            return
        sportsman_id = self.table.item(selected_row, 0).text()
        dialog = dialog_class(self, sportsman_id)
        dialog.exec()

    def _open_window(self, window_class, error_message):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", error_message)
            return
        sportsman_id = int(self.table.item(selected_row, 0).text())
        window = window_class(sportsman_id, self)
        window.show()
        self.hide()

    def view_recommendations(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для просмотра рекомендаций")
            return

        sportsman_id = int(self.table.item(selected_row, 0).text())
        sportsman_name = self.table.item(selected_row, 1).text()

        recommendations_window = AdminViewRecommendationsWindow(sportsman_id, sportsman_name, self)
        recommendations_window.exec()
                
class TrainerSportsmenWindow(AdminSportsmenWindow):
    def setup_ui(self):
        super().setup_ui()

        # Добавляем кнопку "Добавить рекомендацию" только для тренеров
        self.add_recommendation_button = QPushButton("Добавить рекомендацию")
        self.add_recommendation_button.clicked.connect(self.add_recommendation)
        self.progress_buttons_layout.insertWidget(3, self.add_recommendation_button)  # Вставляем кнопку на нужное место

        # Устанавливаем одинаковый размер для кнопок
        self.add_recommendation_button.setSizePolicy(self.view_progress_button.sizePolicy())

    def add_recommendation(self):
        """Открыть окно добавления рекомендации."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для добавления рекомендации")
            return

        sportsman_id = int(self.table.item(selected_row, 0).text())
        sportsman_name = self.table.item(selected_row, 1).text()  # Предположим, что имя спортсмена находится во втором столбце

        # Получаем список тренеров
        trainers = get_trainers()  # Используем метод для получения списка тренеров
        if not trainers:
            QMessageBox.warning(self, "Ошибка", "Нет доступных тренеров")
            return

        # Создаем список для отображения в диалоговом окне
        trainer_names = [f"{last_name} (ID: {id})" for id, last_name in trainers]

        # Открываем диалоговое окно для выбора тренера
        selected_trainer, ok = QInputDialog.getItem(self, "Выбор тренера", "Выберите тренера:", trainer_names, 0, False)
        if not ok:
            return  # Пользователь отменил выбор

        # Получаем ID и фамилию выбранного тренера
        selected_trainer_index = trainer_names.index(selected_trainer)
        trainer_id, trainer_last_name = trainers[selected_trainer_index]

        # Открываем новое окно для добавления рекомендации
        recommendation_window = RecommendationWindow(sportsman_id, sportsman_name, trainer_id, trainer_last_name, self)
        recommendation_window.exec()
    
    def view_recommendations(self):
        """Открыть окно просмотра рекомендаций."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для просмотра рекомендаций")
            return

        sportsman_id = int(self.table.item(selected_row, 0).text())
        sportsman_name = self.table.item(selected_row, 1).text()  # Предположим, что имя спортсмена находится во втором столбце

        # Открываем новое окно для просмотра рекомендаций
        recommendations_window = ViewRecommendationsWindow(sportsman_id, sportsman_name, self)
        recommendations_window.exec()
        




class ProfileDialog(QDialog):
    def __init__(self, parent, sportsman_id):
        super().__init__(parent)
        self.setWindowTitle("Профиль спортсмена")
        self.setGeometry(400, 200, 700, 300) # Adjusted size for better layout

        # Фото спортсмена
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
        self.profile_label.setWordWrap(True)  # To ensure text wraps when it's long

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
        self.load_profile_data(sportsman_id)

    def load_profile_data(self, sportsman_id):
        connection = get_database_connection()
        if not connection:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            self.reject()
            return

        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    sportsman_id, user_id, first_name, last_name, patronymic, city, 
                    DATE_FORMAT(birthdate, '%d-%m-%Y') AS formatted_birthdate, 
                    gender, typesport, photo 
                FROM sportsmen 
                WHERE sportsman_id = %s
            """
            cursor.execute(query, (sportsman_id,))
            profile = cursor.fetchone()

            if profile:
                # Форматирование профиля
                profile_data = f"""
                    <b>ID спортсмена:</b> {profile['sportsman_id']}<br>
                    <b>ID пользователя:</b> {profile['user_id']}<br>
                    <b>Имя:</b> {profile['first_name']}<br>
                    <b>Фамилия:</b> {profile['last_name']}<br>
                    <b>Отчество:</b> {profile['patronymic']}<br>
                    <b>Город:</b> {profile['city']}<br>
                    <b>Дата рождения:</b> {profile['formatted_birthdate']}<br>
                    <b>Пол:</b> {profile['gender']}<br>
                    <b>Вид спорта:</b> {profile['typesport']}
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
                QMessageBox.warning(self, "Ошибка", f"Профиль спортсмена с ID {sportsman_id} не найден.")
                self.reject()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при выполнении запроса: {e}")
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


class RecommendationWindow(QDialog):
    
    
    """Окно для добавления рекомендации спортсмену."""

    def __init__(self, sportsman_id, sportsman_name, trainer_id, trainer_last_name, parent=None):
        super().__init__(parent)
        self.sportsman_id = sportsman_id
        self.sportsman_name = sportsman_name
        self.trainer_id = trainer_id
        self.trainer_last_name = trainer_last_name
        self.setWindowTitle("Добавление рекомендации")
        self.setGeometry(500, 300, 600, 400)

        layout = QVBoxLayout()

        # Информация о спортсмене и тренере
        layout.addWidget(QLabel(f"Спортсмен: {self.sportsman_name} (ID: {self.sportsman_id})"))
        layout.addWidget(QLabel(f"Тренер: {self.trainer_last_name} (ID: {self.trainer_id})"))

        # Текстовое поле для ввода рекомендации
        self.recommendation_text = QTextEdit()
        self.recommendation_text.setPlaceholderText("Введите рекомендацию здесь...")
        layout.addWidget(self.recommendation_text)

        # Кнопки "Сохранить" и "Назад"
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_recommendation)
        buttons_layout.addWidget(self.save_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def save_recommendation(self):
        """Сохраняет рекомендацию в базу данных."""
        recommendation = self.recommendation_text.toPlainText()
        if not recommendation:
            QMessageBox.warning(self, "Ошибка", "Рекомендация не может быть пустой.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO recommendations (sportsman_id, trainer_id, recommendation_text) VALUES (%s, %s, %s)",
                    (self.sportsman_id, self.trainer_id, recommendation),
                )
                connection.commit()
                QMessageBox.information(self, "Успех", "Рекомендация сохранена.")
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении рекомендации: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
                
class ViewRecommendationsWindow(QDialog):
    """Окно для просмотра рекомендаций спортсмена."""

    def __init__(self, sportsman_id, sportsman_name, parent=None):
        super().__init__(parent)
        self.sportsman_id = sportsman_id
        self.sportsman_name = sportsman_name
        self.setWindowTitle(f"Рекомендации для {self.sportsman_name} (ID: {self.sportsman_id})")
        self.setGeometry(500, 300, 800, 600)

        layout = QVBoxLayout()

        # Таблица рекомендаций
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Рекомендации", "ID Тренера", "Фамилия Тренера", "Рекомендация"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)

        # Полное описание рекомендации
        self.recommendation_text = QTextEdit()
        self.recommendation_text.setReadOnly(True)
        layout.addWidget(self.recommendation_text)

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        self.edit_button = QPushButton("Изменить")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_recommendation)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_recommendation)
        buttons_layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Загружаем данные
        self.load_recommendations()

    def load_recommendations(self):
        """Загружает рекомендации для спортсмена."""
        query = (
            "SELECT r.recommendation_id, r.trainer_id, t.last_name, r.recommendation_text "
            "FROM recommendations r "
            "JOIN trainers t ON r.trainer_id = t.trainer_id "
            "WHERE r.sportsman_id = %s"
        )
        db = get_database_connection()
        if not db:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, (self.sportsman_id,))
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(row["recommendation_id"])))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(row["trainer_id"])))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(row["last_name"])))
                self.table.setItem(row_index, 3, QTableWidgetItem(row["recommendation_text"]))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

    def on_selection_changed(self):
        """Обновляет состояние кнопок при выборе строки в таблице."""
        selected_row = self.table.currentRow()
        if selected_row != -1:
            recommendation_item = self.table.item(selected_row, 3)
            if recommendation_item:
                recommendation_text = recommendation_item.text()
                self.recommendation_text.setText(recommendation_text)
                self.edit_button.setEnabled(True)
                self.delete_button.setEnabled(True)
            else:
                self.recommendation_text.clear()
                self.edit_button.setEnabled(False)
                self.delete_button.setEnabled(False)
        else:
            self.recommendation_text.clear()
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def edit_recommendation(self):
        """Изменение выбранной рекомендации."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите рекомендацию для изменения")
            return

        recommendation_id = self.table.item(selected_row, 0).text()
        recommendation_text = self.table.item(selected_row, 3).text()

        # Открываем диалоговое окно для редактирования
        dialog = EditRecommendationDialog(self, recommendation_id, recommendation_text)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_recommendations()  # Обновляем таблицу после редактирования

    def delete_recommendation(self):
        """Удаление выбранной рекомендации."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите рекомендацию для удаления")
            return

        recommendation_id = self.table.item(selected_row, 0).text()

        # Подтверждение удаления
        confirmation = QMessageBox.question(
            self,
            "Удаление",
            f"Вы уверены, что хотите удалить рекомендацию ID {recommendation_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("DELETE FROM recommendations WHERE recommendation_id = %s", (recommendation_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", f"Рекомендация ID {recommendation_id} удалена.")
                    self.load_recommendations()  # Обновляем таблицу после удаления
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении записи: {e}")
                    connection.rollback()
                finally:
                    cursor.close()
                    connection.close()

class EditRecommendationDialog(QDialog):
    """Диалоговое окно для редактирования рекомендации."""

    def __init__(self, parent=None, recommendation_id=None, recommendation_text=None):
        super().__init__(parent)
        self.recommendation_id = recommendation_id
        self.setWindowTitle("Редактирование рекомендации")
        self.setGeometry(500, 300, 400, 300)

        layout = QVBoxLayout()

        # Текстовое поле для ввода рекомендации
        self.recommendation_text = QTextEdit(recommendation_text)
        layout.addWidget(self.recommendation_text)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_changes)
        buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def save_changes(self):
        """Сохраняет изменения в базе данных."""
        recommendation_text = self.recommendation_text.toPlainText()
        if not recommendation_text:
            QMessageBox.warning(self, "Ошибка", "Рекомендация не может быть пустой.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE recommendations SET recommendation_text = %s WHERE recommendation_id = %s",
                    (recommendation_text, self.recommendation_id),
                )
                connection.commit()
                QMessageBox.information(self, "Успех", "Изменения сохранены.")
                self.accept()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при сохранении изменений: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

class AdminViewRecommendationsWindow(QDialog):
    """Окно для просмотра рекомендаций спортсмена."""

    def __init__(self, sportsman_id, sportsman_name, parent=None):
        super().__init__(parent)
        self.sportsman_id = sportsman_id
        self.sportsman_name = sportsman_name
        self.setWindowTitle(f"Рекомендации для {self.sportsman_name} (ID: {self.sportsman_id})")
        self.setGeometry(500, 300, 800, 600)

        layout = QVBoxLayout()

        # Таблица рекомендаций
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Рекомендации", "ID Тренера", "Фамилия Тренера", "Рекомендация"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)

        # Полное описание рекомендации
        self.recommendation_text = QTextEdit()
        self.recommendation_text.setReadOnly(True)
        layout.addWidget(self.recommendation_text)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        # Загружаем данные
        self.load_recommendations()

    def load_recommendations(self):
        """Загружает рекомендации для спортсмена."""
        query = (
            "SELECT r.recommendation_id, r.trainer_id, t.last_name, r.recommendation_text "
            "FROM recommendations r "
            "JOIN trainers t ON r.trainer_id = t.trainer_id "
            "WHERE r.sportsman_id = %s"
        )
        db = get_database_connection()
        if not db:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, (self.sportsman_id,))
            rows = cursor.fetchall()
            self.table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(row["recommendation_id"])))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(row["trainer_id"])))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(row["last_name"])))
                self.table.setItem(row_index, 3, QTableWidgetItem(row["recommendation_text"]))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
        finally:
            cursor.close()
            db.close()

    def on_selection_changed(self):
        """Обновляет состояние текста рекомендации при выборе строки в таблице."""
        selected_row = self.table.currentRow()
        if selected_row != -1:
            recommendation_item = self.table.item(selected_row, 3)
            if recommendation_item:
                recommendation_text = recommendation_item.text()
                self.recommendation_text.setText(recommendation_text)
            else:
                self.recommendation_text.clear()
        else:
            self.recommendation_text.clear()