from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import mysql.connector
import matplotlib.pyplot as plt

class ReportWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, 780, 580)

        main_layout = QVBoxLayout()

        # Контейнер для фото
        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_label.setFixedSize(360, 300)  # Устанавливаем размер фото
        self.chart_label.setStyleSheet("border: 1px solid gray;")  # Визуализация границ
        main_layout.addWidget(self.chart_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Контейнер для текста
        self.report_text_area = QTextEdit()
        self.report_text_area.setReadOnly(True)
        self.report_text_area.setFixedWidth(400)  # Фиксируем ширину текста
        self.report_text_area.setStyleSheet("border: 1px solid gray;")
        main_layout.addWidget(self.report_text_area, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        self.generate_reports()

    def generate_reports(self):
        connection = mysql.connector.connect(
            host="mysql-ownosh.alwaysdata.net",
            user="ownosh",
            password="S~0U;G~1z(f",
            database="ownosh_sport_system"
        )
        cursor = connection.cursor()

        # Общее количество спортсменов
        cursor.execute("SELECT COUNT(*) FROM sportsmen")
        total_athletes = cursor.fetchone()[0]

        # Количество активных спортсменов
        cursor.execute("SELECT COUNT(*) FROM sportsmen WHERE active=1")
        active_athletes = cursor.fetchone()[0]

        # Количество неактивных спортсменов
        cursor.execute("SELECT COUNT(*) FROM sportsmen WHERE active=0")
        inactive_athletes = cursor.fetchone()[0]

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

        report_text = (
            f"Общее количество спортсменов: {total_athletes}\n"
            f"Постоянные/пришедшие: {active_athletes}\n"
            f"Давно не было/ушли: {inactive_athletes}\n"
            f"Спортсмены, участвовавшие в соревнованиях: {participated_competitions}\n"
            f"Спортсмены, пропустившие соревнования: {absent_competitions}\n"
            f"Спортсмены, присутствовавшие на тренировках: {attended_trainings}\n"
            f"Спортсмены, пропустившие тренировки: {missed_trainings}\n"
        )
        self.report_text_area.setText(report_text)

        labels = ['Постоянники/пришедшие', 'Давно не было/ушли', 'Участвовали в соревнованиях', 'Пропустили соревнования', 'Присутствовали на тренировках', 'Пропустили тренировки']
        values = [active_athletes, inactive_athletes, participated_competitions, absent_competitions, attended_trainings, missed_trainings]

        # Создание диаграммы с высоким разрешением
        plt.figure(figsize=(5, 4), dpi=100)  # DPI увеличен для улучшения качества
        plt.barh(labels, values, color='grey')
        plt.xlabel('Количество')
        plt.title('Отчеты по спортсменам')
        plt.tight_layout()

        plt.savefig('report_chart.png', dpi=200)  # Сохраняем в высоком разрешении

        # Загружаем диаграмму в QLabel
        pixmap = QPixmap('report_chart.png')
        self.chart_label.setPixmap(
            pixmap.scaled(self.chart_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )

        cursor.close()
        connection.close()

