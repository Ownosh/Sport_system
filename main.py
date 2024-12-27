import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QTabWidget, QFrame,QSpacerItem, QSizePolicy)
from auxiliary_windows import AwardWindow, UserWindow, TrainingWindow, CompetitionWindow, ProfileWindow, TrainerWindow
import mysql.connector
from PyQt6.QtWidgets import QLabel
from group import GroupWindow
from spwin import SportsmenWindow
from windows_to_change import get_database_connection

class AdminWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Admin Window")
        self.setGeometry(350, 150, 800, 600)

        main_layout = QVBoxLayout()
        self.current_username = username

        self.profile_button = QPushButton("Профиль")
        self.competition_button = QPushButton("Журнал соревнований")
        self.training_button = QPushButton("Журнал тренировок")
        self.user_button = QPushButton("Журнал пользователей")
        self.award_button = QPushButton("Журнал наград")
        self.profile_button.clicked.connect(self.open_profile_)

        top_nav_layout = QHBoxLayout()
        top_nav_layout.addWidget(self.profile_button)
        top_nav_layout.addWidget(self.competition_button)
        top_nav_layout.addWidget(self.training_button)
        top_nav_layout.addWidget(self.user_button)
        top_nav_layout.addWidget(self.award_button)

        self.workspace = QFrame()
        self.workspace.setFrameShape(QFrame.Shape.StyledPanel)


        self.report_text_area = QTextEdit(self.workspace)
        self.report_text_area.setReadOnly(True)
        self.report_text_area.setGeometry(10, 10, 580, 580)
        self.chart_label = QLabel(self.workspace)
        self.chart_label.setGeometry(600, 10, 180, 180)

        self.groups_button = QPushButton("Группы")
        self.sportsmen_button = QPushButton("Спортсмены")
        self.trainers_button = QPushButton("Тренера")
        self.reports_button = QPushButton("Отчеты")
        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

        side_nav_layout = QVBoxLayout()
        side_nav_layout.addWidget(self.groups_button)
        side_nav_layout.addWidget(self.sportsmen_button)
        side_nav_layout.addWidget(self.trainers_button)
        side_nav_layout.addWidget(self.reports_button)
        side_nav_layout.addStretch()
        side_nav_layout.addWidget(self.exit_button)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.workspace)
        content_layout.addLayout(side_nav_layout)

        main_layout.addLayout(top_nav_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.trainers_button.clicked.connect(self.open_trainer_)
        self.sportsmen_button.clicked.connect(self.open_sportsmen_)
        self.groups_button.clicked.connect(self.open_group_)
        self.award_button.clicked.connect(self.open_award_)
        self.training_button.clicked.connect(self.open_training_)
        self.competition_button.clicked.connect(self.open_competition_)
        self.user_button.clicked.connect(self.open_user_)
        self.reports_button.clicked.connect(self.generate_reports)
        

    def open_profile_(self):
        self.hide()
        self.profile_window = ProfileWindow(self, username=self.current_username)
        self.profile_window.show()
        
    def open_sportsmen_(self):
        self.sportsmen_window = SportsmenWindow(self)
        self.sportsmen_window.show()
        self.hide()
        
    def open_trainer_(self):
        self.hide()
        self.profile_window = TrainerWindow(self)
        self.profile_window.show()
        
    def open_group_(self):
        self.group_window = GroupWindow(self)
        self.group_window.show()
        self.hide()
        
    def open_award_(self):
        self.hide()
        self.award_window = AwardWindow(self)
        self.award_window.show()

    def open_training_(self):
        self.hide()
        self.training_window = TrainingWindow(self)  
        self.training_window.show()

    def open_competition_(self):
        self.hide()
        self.competition_window = CompetitionWindow(self)
        self.competition_window.show()

    def open_user_(self):
        self.hide()
        self.user_window = UserWindow(self)
        self.user_window.show()
    
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


class AthleteWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Athlete Window")
        self.setGeometry(350, 150, 800, 600)

        top_nav_layout = QHBoxLayout()
        self.current_username = username
        print(self.current_username)

        self.competition_button = QPushButton("Соревнования")
        self.training_button = QPushButton("Тренировка")
        self.report_button = QPushButton("Отчет")
        self.profile_button = QPushButton("Профиль")
        self.profile_button.clicked.connect(self.open_profile_)
        
        top_nav_layout.addWidget(self.competition_button)
        top_nav_layout.addWidget(self.training_button)
        top_nav_layout.addWidget(self.report_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        top_nav_layout.addSpacerItem(spacer)
        top_nav_layout.addWidget(self.profile_button)

        self.tabs = QTabWidget()
        self.progress_tab = QWidget()
        self.awards_tab = QWidget()
        self.injuries_tab = QWidget()
        self.recommendations_tab = QWidget()
        self.dopmaterial_tab = QWidget()

        self.tabs.addTab(self.progress_tab, "Прогресс")
        self.tabs.addTab(self.awards_tab, "Награды")
        self.tabs.addTab(self.injuries_tab, "Травмы/Болезни")
        self.tabs.addTab(self.recommendations_tab, "Рекомендации")
        self.tabs.addTab(self.dopmaterial_tab, "Дополнительные материалы")

        bottom_layout = QHBoxLayout()
        exit_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.exit_button = QPushButton("Выход")
        bottom_layout.addSpacerItem(exit_spacer)
        bottom_layout.addWidget(self.exit_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_nav_layout)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.competition_button.clicked.connect(self.open_competition)
        self.training_button.clicked.connect(self.open_training)
        self.report_button.clicked.connect(self.open_report)
        self.exit_button.clicked.connect(self.close_application)

    def open_competition(self):
        self.hide()
        self.competition_window = CompetitionWindow(self)
        self.competition_window.show()

    def open_training(self):
        self.hide()
        self.training_window = TrainingWindow(self)  
        self.training_window.show()

    def open_report(self):
        pass

    def open_profile_(self):
        self.hide()
        self.profile_window = ProfileWindow(self, username=self.current_username)
        self.profile_window.show()
        
    def close_application(self):
        self.close()

class CoachWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Coach Window")
        self.setGeometry(350, 150, 800, 600)

        # Главный лэйаут
        main_layout = QVBoxLayout()
        self.current_username1 = username
        print(self.current_username1)

        top_layout = QHBoxLayout()
        self.profile_button = QPushButton("Профиль")
        self.competition_button = QPushButton("Журнал соревнований")
        self.training_button = QPushButton("Журнал тренировок")
        self.award_button = QPushButton("Журнал наград")
        self.profile_button.clicked.connect(self.open_profile_)

        top_layout.addWidget(self.profile_button)
        top_layout.addWidget(self.competition_button)
        top_layout.addWidget(self.training_button)
        top_layout.addWidget(self.award_button)

        # Центральная часть с вкладками
        self.tabs = QTabWidget()
        self.profile_tab = QWidget()
        self.competition_tab = QWidget()
        self.training_tab = QWidget()
        self.award_tab = QWidget()
        
        self.tabs.addTab(self.profile_tab, "Профиль")
        self.tabs.addTab(self.competition_tab, "Журнал соревнований")
        self.tabs.addTab(self.training_tab, "Журнал тренировок")
        self.tabs.addTab(self.award_tab, "Журнал наград")


        side_nav_layout = QVBoxLayout()
        
        self.groups_button = QPushButton("Группы")
        self.sportsmen_button = QPushButton("Спортсмены")
        self.trainers_button = QPushButton("Тренера")
        self.reports_button = QPushButton("Отчеты")
        self.exit_button = QPushButton("Выход")
        
        side_nav_layout.addWidget(self.groups_button)
        side_nav_layout.addWidget(self.sportsmen_button)
        side_nav_layout.addWidget(self.trainers_button)
        side_nav_layout.addWidget(self.reports_button)
        side_nav_layout.addStretch()
        side_nav_layout.addWidget(self.exit_button)

        # Создаем центральную панель
        self.workspace = QFrame()
        self.workspace.setFrameShape(QFrame.Shape.StyledPanel)
        
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.workspace)
        content_layout.addLayout(side_nav_layout)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.trainers_button.clicked.connect(self.open_trainer_)
        self.sportsmen_button.clicked.connect(self.open_sportsmen_)
        self.groups_button.clicked.connect(self.open_group_)
        self.competition_button.clicked.connect(self.open_competition)
        self.training_button.clicked.connect(self.open_training)
        self.award_button.clicked.connect(self.open_award)

        self.exit_button.clicked.connect(self.exit_application)
        
        
    def open_profile_(self):
        self.hide()
        self.profile_window = ProfileWindow(self, username=self.current_username1)
        self.profile_window.show()
        
    def open_sportsmen_(self):
        self.hide()
        self.profile_window = SportsmenWindow(self)
        self.profile_window.show()
        
    def open_trainer_(self):
        self.hide()
        self.profile_window = TrainerWindow(self)
        self.profile_window.show()
        
    def open_group_(self):
        self.hide()
        self.profile_window = GroupWindow(self)
        self.profile_window.show()
        
    def open_profile_window(self):
        self.hide()
        self.profile_window = ProfileWindow(self)
        self.profile_window.show()

    def open_competition(self):
        self.hide()
        self.competition__window = CompetitionWindow(self)
        self.competition__window.show()

    def open_training(self):
        self.hide()
        self.training__window = TrainingWindow(self)
        self.training__window.show()

    def open_award(self):
        self.hide()
        self.award__window = AwardWindow(self)
        self.award__window.show()

    def exit_application(self):
        self.close()  

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.setGeometry(530, 270, 450, 350)

        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Вход")
        self.exit_button = QPushButton("Выход")
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_input, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_input, 1, 1)

        main_layout.addLayout(grid_layout)

        main_layout.addWidget(self.login_button)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.exit_button)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.login_button.clicked.connect(self.check_user_credentials)
        self.exit_button.clicked.connect(self.close)

        self.db = get_database_connection()

    def check_user_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя и пароль!")
            return

        try:
            cursor = self.db.cursor()
            query = "SELECT password, role FROM users WHERE username = %s"
            params = (username,)
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                stored_password, role = result

                if stored_password == password.strip():
                    QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                    self.open_role_window(role, username)
                else:
                    QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")

    def open_role_window(self, role, username):
        self.close()
        if role == "admin":
            self.admin_window = AdminWindow(username)
            self.admin_window.show()
        elif role == "sportsman":
            self.athlete_window = AthleteWindow(username)
            self.athlete_window.show()
        elif role == "trainer":
            self.coach_window = CoachWindow(username)
            self.coach_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неизвестная роль пользователя!")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LoginWindow()
    window.show()  
    sys.exit(app.exec())  

if __name__ == "__main__":
    main()
