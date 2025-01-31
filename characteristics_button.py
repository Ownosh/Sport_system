
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QLineEdit, QMessageBox,QGridLayout
)
from database_functions import  add_training_result, get_training_results, get_trainings_for_sportsman

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox, QHeaderView
)
from database_functions import get_training_results
from change_buttons import get_database_connection  # Подключение к БД
import mysql.connector






class CharacteristicsTrainingWindow(QWidget):
    """Окно для добавления результатов тренировок спортсмена."""
    
    def __init__(self, sportsman_id: int, parent_window: QWidget):
        super().__init__()
        self.sportsman_id = sportsman_id
        self.parent_window = parent_window
        self.setWindowTitle(f"Добавление результатов для спортсмена ID: {sportsman_id}")
        self.setGeometry(400, 200, 600, 300)

        layout = QVBoxLayout()

        # Убрали отображение ID спортсмена

        # Выбор тренировки
        self.training_select = QComboBox()
        self.load_trainings()
        layout.addWidget(self.training_select)

        # Поля для ввода V1 и V2
        self.v1_input = QLineEdit()
        self.v1_input.setPlaceholderText("Введите V1")
        self.v1_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.v1_input)

        self.v2_input = QLineEdit()
        self.v2_input.setPlaceholderText("Введите V2")
        self.v2_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.v2_input)

        # Кнопки "Сохранить результат" и "Назад"
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить результат")
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setStyleSheet("""
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
        buttons_layout.addWidget(self.save_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("""
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
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_trainings(self):
        """Загружает список тренировок в выпадающий список только для текущего спортсмена."""
        trainings = get_trainings_for_sportsman(self.sportsman_id)  # Получаем тренировки для конкретного спортсмена
        self.training_select.clear()  # Очищаем выпадающий список перед добавлением новых элементов
        for training in trainings:
            # training[0] - ID тренировки, training[1] - название тренировки
            self.training_select.addItem(f"{training[1]} (ID: {training[0]})", training[0])

    def save_result(self):
        """Сохраняет результат тренировки в базу данных."""
        training_id = self.training_select.currentData()
        v1 = self.v1_input.text()
        v2 = self.v2_input.text()

        if not v1 or not v2:
            QMessageBox.warning(self, "Ошибка", "Введите значения V1 и V2")
            return

        try:
            v1, v2 = float(v1), float(v2)
            add_training_result(self.sportsman_id, training_id, v1, v2)
            QMessageBox.information(self, "Успех", "Результат добавлен!")
            self.go_back()  # Закрываем окно после успешного сохранения
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "V1 и V2 должны быть числами!")

    def go_back(self):
        """Возвращает пользователя в окно со спортсменами."""
        self.close()
        if self.parent_window:
            self.parent_window.show()








from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QHBoxLayout, QMessageBox, QDialog, QLineEdit
)
from PyQt6.QtCore import Qt
import mysql.connector


class ResultsWindow(QWidget):
    """Окно для просмотра результатов тренировок спортсмена."""

    def __init__(self, sportsman_id: int, parent_window: QWidget):
        super().__init__()
        self.sportsman_id = sportsman_id
        self.parent_window = parent_window
        self.setWindowTitle(f"Результаты тренировок (Спортсмена ID: {sportsman_id})")
        self.setGeometry(450, 250, 700, 450)

        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Тренировка", "V1", "V2", "Прогресс (%)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #505050;
                font-size: 12px;
                border: 1px solid #d0d0d0;
                color: #ffffff;
            }
            QHeaderView::section {
                font-size: 12px; 
                background-color: #707070;
                padding: 5px;
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #808080;
            }
        """)

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        self.edit_button = QPushButton("Изменить")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_result)
        buttons_layout.addWidget(self.edit_button)
        self.edit_button.setStyleSheet("""
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

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_result)
        buttons_layout.addWidget(self.delete_button)
        self.delete_button.setStyleSheet("""
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

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        buttons_layout.addWidget(self.back_button)
        self.back_button.setStyleSheet("""
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

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Загружаем данные
        self.load_results()

    def load_results(self):
        """Загружает результаты тренировок для спортсмена."""
        results = get_training_results(self.sportsman_id)  # Предположим, что эта функция возвращает список результатов

        if not results:
            QMessageBox.information(self, "Информация", "Результатов для этого спортсмена нет.")
            return

        self.table.setRowCount(len(results))
        for row_index, row in enumerate(results):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(row["training_id"])))  # Используем name_training
            self.table.setItem(row_index, 2, QTableWidgetItem(str(row["v1"])))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(row["v2"])))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(row["progress"])))

    def on_selection_changed(self):
        """Обновляет состояние кнопок при выборе строки в таблице."""
        selected_row = self.table.currentRow()
        self.edit_button.setEnabled(selected_row != -1)
        self.delete_button.setEnabled(selected_row != -1)

    def edit_result(self):
        """Изменение выбранного результата тренировки."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите результат для изменения")
            return

        result_id = self.table.item(selected_row, 0).text()
        training_id = self.table.item(selected_row, 1).text()  # Получаем ID тренировки
        training_name = self.table.item(selected_row, 1).text()  # Получаем имя тренировки
        v1 = self.table.item(selected_row, 2).text()
        v2 = self.table.item(selected_row, 3).text()

        print(f"Передача training_id: {training_id}")  # Отладочный вывод

        # Открываем диалоговое окно для редактирования
        dialog = EditResultDialog(self, result_id, training_id, v1, v2, self.sportsman_id)  # Передаем training_id и sportsman_id
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_results()  # Обновляем таблицу после редактирования

    def delete_result(self):
        """Удаление выбранного результата тренировки."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите результат для удаления")
            return

        result_id = self.table.item(selected_row, 0).text()

        # Подтверждение удаления
        confirmation = QMessageBox.question(
            self,
            "Удаление",
            f"Вы уверены, что хотите удалить результат ID {result_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("DELETE FROM characteristics_sportsman_trainings WHERE id = %s", (result_id,))
                    connection.commit()
                    QMessageBox.information(self, "Успех", f"Результат ID {result_id} удален.")
                    self.load_results()  # Обновляем таблицу после удаления
                except mysql.connector.Error as e:
                    QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении записи: {e}")
                    connection.rollback()
                finally:
                    cursor.close()
                    connection.close()

    def go_back(self):
        """Закрыть окно и вернуться в SportsmenWindow."""
        self.close()
        self.parent_window.show()


class EditResultDialog(QDialog):
    """Диалоговое окно для редактирования результата тренировки."""

    def __init__(self, parent=None, result_id=None, training_id=None, v1=None, v2=None, sportsman_id=None):
        super().__init__(parent)
        self.result_id = result_id
        self.sportsman_id = sportsman_id
        self.training_id = int(training_id) if training_id else None  # Преобразуем training_id в int
        self.setWindowTitle("Редактирование результата")
        self.setGeometry(500, 300, 400, 200)

        layout = QVBoxLayout()

        # Выпадающий список для выбора тренировки
        self.training_combo = QComboBox()
        layout.addWidget(QLabel("Тренировка:"))
        layout.addWidget(self.training_combo)

        # Поля для ввода V1 и V2
        self.v1_input = QLineEdit(str(v1))  # Преобразуем v1 в строку
        self.v1_input.setPlaceholderText("Введите V1")
        layout.addWidget(self.v1_input)

        self.v2_input = QLineEdit(str(v2))  # Преобразуем v2 в строку
        self.v2_input.setPlaceholderText("Введите V2")
        layout.addWidget(self.v2_input)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_changes)
        buttons_layout.addWidget(self.save_button)
        self.save_button.setStyleSheet("""
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

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        self.cancel_button.setStyleSheet("""
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

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Теперь загружаем тренировки, когда `QComboBox` уже добавлен в интерфейс
        self.load_trainings()

    def load_trainings(self):
        """Загружает список тренировок в выпадающий список только для текущего спортсмена."""
        trainings = get_trainings_for_sportsman(self.sportsman_id)  # Получаем тренировки

        print(f"Загруженные тренировки: {trainings}")  # Отладочный вывод

        self.training_combo.clear()  # Очищаем список перед обновлением
        selected_index = 0  # По умолчанию первая тренировка

        for index, training in enumerate(trainings):
            training_id, training_name = training[0], training[1]
            print(f"Добавление тренировки: {training_name} (ID: {training_id})")  # Отладочный вывод
            self.training_combo.addItem(f"{training_name} (ID: {training_id})", training_id)

            # Если ID тренировки совпадает с переданным, выбираем её
            if self.training_id and self.training_id == training_id:
                selected_index = index

        # Устанавливаем выбранную тренировку
        if self.training_combo.count() > 0:
            print(f"Установка текущей тренировки на индекс: {selected_index}")  # Отладочный вывод
            self.training_combo.setCurrentIndex(selected_index)

    def save_changes(self):
        """Сохраняет изменения в базе данных."""
        v1 = self.v1_input.text()
        v2 = self.v2_input.text()
        training_id = self.training_combo.currentData()

        if not v1 or not v2:
            QMessageBox.warning(self, "Ошибка", "Поля V1 и V2 не могут быть пустыми.")
            return

        try:
            v1 = float(v1)
            v2 = float(v2)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "V1 и V2 должны быть числами.")
            return

        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE characteristics_sportsman_trainings SET training_id = %s, v1 = %s, v2 = %s WHERE id = %s",
                    (training_id, v1, v2, self.result_id),
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