import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget,QSpacerItem, QLabel,QSizePolicy, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout,QTabWidget, QMessageBox, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt,QTimer
from main_buttons import (
    AwardWindow, UserWindow, TrainingWindow, CompetitionWindow, 
    ProfileWindow, GroupWindowForTrainers, GroupMembersWindow
)
from group_button import GroupWindow
from sportsman_button import SportsmenWindow
from trainer_button import TrainerWindow
from report_button import ReportWindow
from change_buttons import get_database_connection
import mysql.connector

class AdminWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Окно Администратора")
        self.setGeometry(350, 150, 800, 600)

        self.current_username = username
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Рабочая область
        self.workspace = QFrame()
        self.workspace.setFrameShape(QFrame.Shape.StyledPanel)
        self.workspace.setLayout(QVBoxLayout())

        # Верхняя навигация
        top_nav_layout = QHBoxLayout()
        self.profile_button = self.create_button("Профиль", self.open_profile_)
        self.competition_button = self.create_button("Журнал соревнований", self.open_competition_)
        self.training_button = self.create_button("Журнал тренировок", self.open_training_)
        self.user_button = self.create_button("Журнал пользователей", self.open_user_)
        self.award_button = self.create_button("Журнал наград", self.open_award_)

        top_nav_layout.addWidget(self.profile_button)
        top_nav_layout.addWidget(self.competition_button)
        top_nav_layout.addWidget(self.training_button)
        top_nav_layout.addWidget(self.user_button)
        top_nav_layout.addWidget(self.award_button)

        # Боковая навигация
        side_nav_layout = QVBoxLayout()
        self.nav_buttons = {
            "Группы": self.open_group_,
            "Спортсмены": self.open_sportsmen_,
            "Тренера": self.open_trainer_,
            "Общий отчет": self.display_report
        }

        for label, handler in self.nav_buttons.items():
            side_nav_layout.addWidget(self.create_button(label, handler))

        side_nav_layout.addStretch()
        self.exit_button = self.create_button("Выход", self.close)
        side_nav_layout.addWidget(self.exit_button)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.workspace)
        content_layout.addLayout(side_nav_layout)

        main_layout.addLayout(top_nav_layout)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.handle_button_click(button, handler))
        return button

    def handle_button_click(self, button, handler):
        if not button.isEnabled():
            return
        button.setEnabled(False)
        QTimer.singleShot(7000, lambda: button.setEnabled(True))  # Блокируем кнопку на 10 секунд
        handler()

    def open_window(self, window_class, *args, **kwargs):
        self.hide()
        window = window_class(self, *args, **kwargs)
        window.show()
        return window

    def display_report(self):
        self.clear_workspace()
        report_window = ReportWindow(self.workspace)
        self.workspace.layout().addWidget(report_window)

    def clear_workspace(self):
        layout = self.workspace.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if widget := child.widget():
                    widget.setParent(None)

    def open_group_(self):
        self.open_window(GroupWindow)

    def open_sportsmen_(self):
        self.open_window(SportsmenWindow)

    def open_trainer_(self):
        self.open_window(TrainerWindow)

    def open_award_(self):
        self.open_window(AwardWindow)

    def open_training_(self):
        self.open_window(TrainingWindow)

    def open_competition_(self):
        self.open_window(CompetitionWindow)

    def open_user_(self):
        self.open_window(UserWindow)

    def open_profile_(self):
        self.clear_workspace()
        profile_widget = ProfileWindow(username=self.current_username)
        self.workspace.layout().addWidget(profile_widget)



class AthleteWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(350, 150, 800, 600)

        top_nav_layout = QHBoxLayout()
        self.current_username = username
        print(self.current_username)

        self.report_button = QPushButton("Отчет")
        self.group_button = QPushButton("Группы")
        self.profile_button = QPushButton("Профиль")
        
        self.profile_button.clicked.connect(self.open_profile_)
        self.group_button.clicked.connect(self.open_group)
        
        top_nav_layout.addWidget(self.report_button)
        top_nav_layout.addWidget(self.group_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        top_nav_layout.addSpacerItem(spacer)
        top_nav_layout.addWidget(self.profile_button)

        self.tabs = QTabWidget()
        self.progress_tab = QWidget()
        self.awards_tab = QWidget()
        self.injuries_tab = QWidget()
        self.recommendations_tab = QWidget()
        self.dopmaterial_tab = QWidget()
        self.competition_tab = QWidget()
        self.training_tab = QWidget()

        self.tabs.addTab(self.progress_tab, "Прогресс")
        self.tabs.addTab(self.awards_tab, "Награды")
        self.tabs.addTab(self.injuries_tab, "Травмы/Болезни")
        self.tabs.addTab(self.recommendations_tab, "Рекомендации")
        self.tabs.addTab(self.dopmaterial_tab, "Дополнительные материалы")
        self.tabs.addTab(self.competition_tab, "Соревнования")
        self.tabs.addTab(self.training_tab, "Тренировки")

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

        self.report_button.clicked.connect(self.open_report)
        self.exit_button.clicked.connect(self.close_application)

        self.load_athlete_info()

    def load_athlete_info(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT first_name, last_name, birthdate, gender, city, typesport, photo FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s)", (self.current_username,))
                athlete_info = cursor.fetchone()
                if athlete_info:
                    info_layout = QHBoxLayout()

                    # Добавление фотографии справа
                    right_layout = QVBoxLayout()
                    photo_label = QLabel()
                    if athlete_info[6]:
                        pixmap = QPixmap()
                        pixmap.loadFromData(athlete_info[6])
                        photo_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
                    else:
                        photo_label.setText("Фото отсутствует")
                    right_layout.addWidget(photo_label)

                    left_layout = QVBoxLayout()
                    left_layout.addWidget(QLabel(f"Имя: {athlete_info[0]}"))
                    left_layout.addWidget(QLabel(f"Фамилия: {athlete_info[1]}"))
                    left_layout.addWidget(QLabel(f"Дата рождения: {athlete_info[2]}"))
                    left_layout.addWidget(QLabel(f"Пол: {athlete_info[3]}"))
                    left_layout.addWidget(QLabel(f"Город: {athlete_info[4]}"))
                    left_layout.addWidget(QLabel(f"Вид спорта: {athlete_info[5]}"))

                    info_layout.addLayout(left_layout)
                    info_layout.addLayout(right_layout)
                    self.progress_tab.setLayout(info_layout)

                    self.load_injury_history()
                    self.load_recommendations()
                    self.load_dopmaterials()
                    self.load_competitions()
                    self.load_trainings()
                    self.load_awards()

                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить информацию о спортсмене")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных спортсмена: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_injury_history(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT period, injury_description FROM injuries WHERE sportsman_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))", (self.current_username,))
                injuries = cursor.fetchall()
                injury_layout = QVBoxLayout()
                for injury in injuries:
                    injury_widget = QWidget()
                    injury_layout_inner = QVBoxLayout(injury_widget)
                    injury_layout_inner.addWidget(QLabel(f"Период: {injury[0]}"))
                    injury_layout_inner.addWidget(QLabel(f"Описание: {injury[1]}"))
                    injury_widget.setLayout(injury_layout_inner)
                    injury_layout.addWidget(injury_widget)
                self.injuries_tab.setLayout(injury_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке истории травм: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_recommendations(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT recommendation_id FROM recommendations WHERE sportsman_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))", (self.current_username,))
                recommendations = cursor.fetchall()
                recommendations_layout = QVBoxLayout()
                for recommendation in recommendations:
                    recommendations_layout.addWidget(QLabel(recommendation[0]))
                self.recommendations_tab.setLayout(recommendations_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке рекомендаций: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_dopmaterials(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT material FROM dopmaterials WHERE sportsman_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))", (self.current_username,))
                materials = cursor.fetchall()
                materials_layout = QVBoxLayout()
                for material in materials:
                    materials_layout.addWidget(QLabel(material[0]))
                self.dopmaterial_tab.setLayout(materials_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке дополнительных материалов: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_competitions(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT c.name, c.date
                    FROM competition_attendance ca
                    JOIN competitions c ON ca.competition_id = c.competition_id
                    WHERE ca.athlete_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))
                """, (self.current_username,))
                competitions = cursor.fetchall()
                competitions_layout = QVBoxLayout()
                for competition in competitions:
                    competitions_layout.addWidget(QLabel(f"Название: {competition[0]}, Дата: {competition[1]}"))
                self.competition_tab.setLayout(competitions_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке соревнований: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_trainings(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT t.name, t.date
                    FROM training_attendance ta
                    JOIN trainings t ON ta.training_id = t.training_id
                    WHERE ta.athlete_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))
                """, (self.current_username,))
                trainings = cursor.fetchall()
                trainings_layout = QVBoxLayout()
                for training in trainings:
                    trainings_layout.addWidget(QLabel(f"Название: {training[0]}, Дата: {training[1]}"))
                self.training_tab.setLayout(trainings_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке тренировок: {e}")
            finally:
                cursor.close()
                connection.close()

    def load_awards(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT reward_id, reward_date, reward_description FROM rewards WHERE sportsman_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))", (self.current_username,))
                awards = cursor.fetchall()
                awards_layout = QVBoxLayout()
                for award in awards:
                    award_widget = QWidget()
                    award_layout_inner = QVBoxLayout(award_widget)
                    award_layout_inner.addWidget(QLabel(f"Название: {award[0]}"))
                    award_layout_inner.addWidget(QLabel(f"Дата: {award[1]}"))
                    award_layout_inner.addWidget(QLabel(f"Описание: {award[2]}"))
                    award_widget.setLayout(award_layout_inner)
                    awards_layout.addWidget(award_widget)
                self.awards_tab.setLayout(awards_layout)
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке наград: {e}")
            finally:
                cursor.close()
                connection.close()


    def open_group(self):
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT g.group_id, g.name
                    FROM sportsman_group sg
                    JOIN groups g ON sg.group_id = g.group_id
                    WHERE sg.sportsman_id = (SELECT sportsman_id FROM sportsmen WHERE user_id = (SELECT user_id FROM users WHERE username = %s))
                """, (self.current_username,))
                group = cursor.fetchone()
                if group:
                    self.group_window = GroupMembersWindow(self, group[0])
                    self.group_window.show()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить информацию о группе")
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных группы: {e}")
            finally:
                cursor.close()
                connection.close()

    def open_profile_(self):
        self.hide()
        self.profile_window = ProfileWindow(self, username=self.current_username)
        self.profile_window.show()

    def open_report(self):
        pass

    def close_application(self):
        self.close()
        

class CoachWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(350, 150, 800, 600)

        self.current_username = username
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Рабочая область
        self.workspace = QFrame()
        self.workspace.setFrameShape(QFrame.Shape.StyledPanel)
        self.workspace.setLayout(QVBoxLayout())

        # Верхняя навигация
        top_nav_layout = QHBoxLayout()
        self.profile_button = self.create_button("Профиль", self.open_profile_)
        self.competition_button = self.create_button("Журнал соревнований", self.open_competition_)
        self.training_button = self.create_button("Журнал тренировок", self.open_training_)
        self.award_button = self.create_button("Журнал наград", self.open_award_)

        top_nav_layout.addWidget(self.profile_button)
        top_nav_layout.addWidget(self.competition_button)
        top_nav_layout.addWidget(self.training_button)
        top_nav_layout.addWidget(self.award_button)

        # Боковая навигация
        side_nav_layout = QVBoxLayout()
        self.nav_buttons = {
            "Группы": self.open_group_,
            "Спортсмены": self.open_sportsmen_,
            "Тренера": self.open_trainer_,
            "Отчеты": self.display_report
        }

        for label, handler in self.nav_buttons.items():
            side_nav_layout.addWidget(self.create_button(label, handler))

        side_nav_layout.addStretch()  
        self.exit_button = self.create_button("Выход", self.close)
        side_nav_layout.addWidget(self.exit_button)

        # Организация главного макета
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.workspace)
        content_layout.addLayout(side_nav_layout)

        main_layout.addLayout(top_nav_layout)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        return button

    def open_window(self, window_class, *args, **kwargs):
        self.hide()
        window = window_class(self, *args, **kwargs)
        window.show()
        return window

    def display_report(self):
        self.clear_workspace()
        report_window = ReportWindow(self.workspace)
        self.workspace.layout().addWidget(report_window)

    def clear_workspace(self):
        layout = self.workspace.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if widget := child.widget():
                    widget.setParent(None)

    def open_group_(self):
        self.open_window(GroupWindowForTrainers)

    def open_sportsmen_(self):
        self.open_window(SportsmenWindow)

    def open_trainer_(self):
        self.open_window(TrainerWindow)

    def open_award_(self):
        self.open_window(AwardWindow)

    def open_training_(self):
        self.open_window(TrainingWindow)

    def open_competition_(self):
        self.open_window(CompetitionWindow)

    def open_profile_(self):
        self.clear_workspace()
        profile_widget = ProfileWindow(username=self.current_username)
        self.workspace.layout().addWidget(profile_widget)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(530, 270, 350, 250)

        # UI элементы
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Вход")
        self.exit_button = QPushButton("Выход")

        # Основной макет
        main_layout = QVBoxLayout()

        # Сетка для полей ввода
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)
        grid_layout.addWidget(self.username_input, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_input, 1, 1)
        main_layout.addLayout(grid_layout)

        # Кнопки
        main_layout.addWidget(self.login_button)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.exit_button)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Подключение событий
        self.login_button.clicked.connect(self.check_user_credentials)
        self.exit_button.clicked.connect(self.close)

        # Подключение к базе данных
        self.db = get_database_connection()

    def check_user_credentials(self):
        """Проверяет учетные данные пользователя в базе данных."""
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
                if stored_password == password:
                    QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                    self.open_role_window(role, username)
                else:
                    QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")

    def open_role_window(self, role, username):
        """Открывает окно в зависимости от роли пользователя."""
        self.close()
        if role == "admin":
            self.admin_window = AdminWindow(username)
            self.admin_window.show()
        elif role == "sportsman":
            self.athlete_window = SportsmenWindow(username)
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
