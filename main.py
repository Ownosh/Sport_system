import sys
from bd_connect import get_database_connection
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Window")

class AthleteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Athlete Window")

class CoachWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coach Window")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Window")  
        self.setGeometry(800, 300, 450, 350) 

        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  
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
            query = "SELECT password, role FROM users WHERE username = %s"
            params = (username,)
            result = self.db.execute_query(query, params)

            if result:
                stored_password, role = result[0]

                print(f"Stored password: '{stored_password}', Input password: '{password}'")

                if stored_password == password.strip():
                    QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                    self.open_role_window(role)
                else:
                    QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")


    def open_role_window(self, role):
        self.close()
        if role == "admin":
            self.admin_window = AdminWindow()
            self.admin_window.show()
        elif role == "sportsman":
            self.athlete_window = AthleteWindow()
            self.athlete_window.show()
        elif role == "trainer":
            self.coach_window = CoachWindow()
            self.coach_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неизвестная роль пользователя!")

def closeEvent(self, event):
        self.db.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()  
    sys.exit(app.exec_())  


if __name__ == "__main__":
    main()
