from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import mysql.connector
import matplotlib.pyplot as plt
from change_buttons import get_database_connection  # Импортируем функцию подключения

class ReportWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, 780, 580)

        main_layout = QVBoxLayout()

        # Контейнер для фото
        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_label.setFixedSize(400, 300)  # Устанавливаем размер фото
        self.chart_label.setStyleSheet("border: 1px solid #d0d0d0; background-color: #505050;")  # Визуализация границ
        main_layout.addWidget(self.chart_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Контейнер для текста
        self.report_text_area = QTextEdit()
        self.report_text_area.setReadOnly(True)
        self.report_text_area.setFixedWidth(400)  # Фиксируем ширину текста
        self.report_text_area.setStyleSheet(""" 
            font-size: 14px;
            padding: 2px;
            background-color: #505050;  /* Светло-серый фон */
            border: 1px solid #d0d0d0;  /* Легкая граница */
        """)
        main_layout.addWidget(self.report_text_area, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        self.generate_reports()

    def generate_reports(self):
        connection = get_database_connection()  # Используем уже существующее подключение
        cursor = connection.cursor()

        # Общее количество спортсменов и тренеров
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='sportsman'")
        total_athletes = cursor.fetchone()[0]

        # Количество активных спортсменов (проверяем активность через users и роль)
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN sportsmen ON users.user_id = sportsmen.user_id
            WHERE users.active = 1 AND users.role = 'sportsman'
        """)
        active_athletes = cursor.fetchone()[0]

        # Количество неактивных спортсменов
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN sportsmen ON users.user_id = sportsmen.user_id
            WHERE users.active = 0 AND users.role = 'sportsman'
        """)
        inactive_athletes = cursor.fetchone()[0]

        # Количество активных тренеров (проверяем активность через users и роль)
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN trainers ON users.user_id = trainers.user_id
            WHERE users.active = 1 AND users.role = 'trainer'
        """)
        active_trainers = cursor.fetchone()[0]

        # Количество неактивных тренеров
        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            JOIN trainers ON users.user_id = trainers.user_id
            WHERE users.active = 0 AND users.role = 'trainer'
        """)
        inactive_trainers = cursor.fetchone()[0]

        # Количество спортсменов, которые участвовали в соревнованиях
        cursor.execute("""
            SELECT COUNT(DISTINCT athlete_id)
            FROM competition_attendance
            WHERE is_present=1
        """)
        participated_competitions = cursor.fetchone()[0]

        # Количество спортсменов, которые пропустили соревнования
        cursor.execute("""
            SELECT COUNT(DISTINCT athlete_id)
            FROM competition_attendance
            WHERE is_present=0
        """)
        absent_competitions = cursor.fetchone()[0]

        # Количество спортсменов, которые присутствовали на тренировках
        cursor.execute("""
            SELECT COUNT(DISTINCT athlete_id)
            FROM training_attendance
            WHERE is_present=1
        """)
        attended_trainings = cursor.fetchone()[0]

        # Количество спортсменов, которые пропустили тренировки
        cursor.execute("""
            SELECT COUNT(DISTINCT athlete_id)
            FROM training_attendance
            WHERE is_present=0
        """)
        missed_trainings = cursor.fetchone()[0]

        # Формируем текст отчета
        report_text = (
            f"Общее количество спортсменов: {total_athletes}\n"
            f"Постоянные/пришедшие спортсмены: {active_athletes}\n"
            f"Давно не было/ушедшие спортсмены: {inactive_athletes}\n"
            f"Активные тренеры: {active_trainers}\n"
            f"Неактивные тренеры: {inactive_trainers}\n"
            f"Спортсмены, участвовавшие в соревнованиях: {participated_competitions}\n"
            f"Спортсмены, пропустившие соревнования: {absent_competitions}\n"
            f"Спортсмены, присутствовавшие на тренировках: {attended_trainings}\n"
            f"Спортсмены, пропустившие тренировки: {missed_trainings}\n"
        )
        self.report_text_area.setText(report_text)

        labels = [
            'Постоянники/пришедшие спортсмены', 'Давно не было/ушли спортсмены',
            'Активные тренеры', 'Неактивные тренеры',
            'Участвовали в соревнованиях', 'Пропустили соревнования',
            'Присутствовали на тренировках', 'Пропустили тренировки'
        ]
        values = [
            active_athletes, inactive_athletes, active_trainers, inactive_trainers,
            participated_competitions, absent_competitions, attended_trainings, missed_trainings
        ]

        # Создание диаграммы с высоким разрешением
        plt.figure(figsize=(5, 4), dpi=100)  # DPI увеличен для улучшения качества
        plt.barh(labels, values, color='grey')
        plt.xlabel('Количество')
        plt.title('Отчет по спортсменам и тренерам')
        plt.tight_layout()

        plt.savefig('report_chart.png', dpi=200)  # Сохраняем в высоком разрешении

        # Загружаем диаграмму в QLabel
        pixmap = QPixmap('report_chart.png')
        self.chart_label.setPixmap(
            pixmap.scaled(
                self.chart_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        cursor.close()
        connection.close()


