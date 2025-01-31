from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
        plt.title('Отчет')
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




from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from change_buttons import get_database_connection

class AthleteReportWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, 780, 580)

        main_layout = QVBoxLayout()

        self.athlete_selector = QComboBox()
        self.load_athletes()
        main_layout.addWidget(self.athlete_selector, alignment=Qt.AlignmentFlag.AlignCenter)

        self.generate_button = QPushButton("Сгенерировать отчет")
        self.generate_button.clicked.connect(self.generate_athlete_report)
        main_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_label.setFixedSize(400, 300)
        self.chart_label.setStyleSheet("border: 1px solid #d0d0d0; background-color: #505050;")
        main_layout.addWidget(self.chart_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.report_text_area = QTextEdit()
        self.report_text_area.setReadOnly(True)
        self.report_text_area.setFixedWidth(400)
        self.report_text_area.setStyleSheet("""
            font-size: 14px;
            padding: 2px;
            background-color: #505050;
            border: 1px solid #d0d0d0;
        """
        )
        main_layout.addWidget(self.report_text_area, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def load_athletes(self):
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT sportsman_id, last_name FROM sportsmen")
        athletes = cursor.fetchall()
        cursor.close()
        connection.close()
        for athlete in athletes:
            self.athlete_selector.addItem(f"{athlete[1]} ({athlete[0]})", athlete[0])

    def generate_athlete_report(self):
        athlete_id = self.athlete_selector.currentData()
        if not athlete_id:
            return

        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT progress FROM characteristics_sportsman_trainings
            WHERE sportsman_id = %s
        """, (athlete_id,))
        progress = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT injury_description, period FROM injuries
            WHERE sportsman_id = %s
        """, (athlete_id,))
        injuries = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) FROM training_attendance
            WHERE athlete_id = %s AND is_present = 1
        """, (athlete_id,))
        attended_trainings = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM training_attendance
            WHERE athlete_id = %s AND is_present = 0
        """, (athlete_id,))
        missed_trainings = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM competition_attendance
            WHERE athlete_id = %s AND is_present = 1
        """, (athlete_id,))
        attended_competitions = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM competition_attendance
            WHERE athlete_id = %s AND is_present = 0
        """, (athlete_id,))
        missed_competitions = cursor.fetchone()[0]

        injury_text = "\n".join([f"{i[0]} ({i[1]})" for i in injuries]) or "Нет данных"
        report_text = (
            f"Прогресс: {', '.join(map(str, progress))}\n"
            f"Травмы и болезни: {injury_text}\n"
            f"Посещено тренировок: {attended_trainings}\n"
            f"Пропущено тренировок: {missed_trainings}\n"
            f"Посещено соревнований: {attended_competitions}\n"
            f"Пропущено соревнований: {missed_competitions}\n"
        )
        self.report_text_area.setText(report_text)

        labels = ['Прогресс', 'Посещенные тренировки', 'Пропущенные тренировки',
                  'Посещенные соревнования', 'Пропущенные соревнования']
        values = [sum(progress) if progress else 0, attended_trainings, missed_trainings,
                  attended_competitions, missed_competitions]

        plt.figure(figsize=(5, 4), dpi=100)
        plt.barh(labels, values, color='grey')
        plt.xlabel('Количество')
        plt.title('Отчет спортсмена')
        plt.tight_layout()
        plt.savefig('athlete_report_chart.png', dpi=200)

        pixmap = QPixmap('athlete_report_chart.png')
        self.chart_label.setPixmap(
            pixmap.scaled(
                self.chart_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        cursor.close()
        connection.close()



