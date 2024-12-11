import sys
from bd_connect import get_database_connection
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Window")

# Окно для спортсмена
class AthleteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Athlete Window")

# Окно для тренера
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
        username = self.username_input.text()
        password = self.password_input.text()

    # Запрос на получение пароля и роли
        query = "SELECT password, role FROM users WHERE username = %s"
        params = (username,)
        result = self.db.execute_query(query, params)

        if result:  # Если пользователь найден
            stored_password, role = result  # Получаем пароль и роль из результата запроса

            if stored_password == password:  # Сравниваем пароли
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                self.close()

            # Открытие соответствующего окна в зависимости от роли
                if role == "admin":
                    AdminWindow()
                elif role == "sportsman":
                    AthleteWindow()
                elif role == "trainer":
                    CoachWindow()
                else:
                    QMessageBox.warning(self, "Ошибка", "Неизвестная роль пользователя!")
                    return
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя!")

def closeEvent(self, event):
    self.db.close()  # Закрытие соединения с базой данных
    event.accept()



def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()  
    sys.exit(app.exec_())  


if __name__ == "__main__":
    main()
