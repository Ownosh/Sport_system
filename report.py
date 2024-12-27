from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem, QFrame, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import mysql.connector

class ReportWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, 780, 580)

        layout = QVBoxLayout()

        # Отображение текстового отчета
        self.report_text_area = QTextEdit()
        self.report_text_area.setReadOnly(True)
        layout.addWidget(self.report_text_area)

        # Отображение диаграммы
        self.chart_label = QLabel()
        layout.addWidget(self.chart_label)

        self.setLayout(layout)
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
            f"Активных спортсменов: {active_athletes}\n"
            f"Неактивных спортсменов: {inactive_athletes}\n"
            f"Спортсмены, участвовавшие в соревнованиях: {participated_competitions}\n"
            f"Спортсмены, пропустившие соревнования: {absent_competitions}\n"
            f"Спортсмены, присутствовавшие на тренировках: {attended_trainings}\n"
            f"Спортсмены, пропустившие тренировки: {missed_trainings}\n"
        )
        self.report_text_area.setText(report_text)

        # Построение диаграммы
        labels = ['Активные', 'Неактивные', 'Участвовали в соревнованиях', 'Пропустили соревнования', 'Присутствовали на тренировках', 'Пропустили тренировки']
        values = [active_athletes, inactive_athletes, participated_competitions, absent_competitions, attended_trainings, missed_trainings]

        plt.figure(figsize=(8, 6))
        plt.barh(labels, values, color='skyblue')
        plt.xlabel('Количество')
        plt.title('Отчеты по спортсменам')
        plt.tight_layout()

        # Сохранение диаграммы во временный файл
        plt.savefig('report_chart.png')

        # Отображение диаграммы
        pixmap = QPixmap('report_chart.png')
        self.chart_label.setPixmap(pixmap.scaled(self.chart_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

        cursor.close()
        connection.close()
