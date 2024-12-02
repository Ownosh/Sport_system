import sys
from bd_connect import get_database_connection
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")  # Заголовок нового окна
        self.setGeometry(800, 300, 400, 350)  # Размер нового окна

        # Пример приветствия на главном окне
        self.welcome_label = QLabel("Добро пожаловать!", self)
        self.welcome_label.setGeometry(100, 100, 800, 800)

        # Кнопка для выхода
        self.exit_button = QPushButton("Выход", self)
        self.exit_button.setGeometry(150, 220, 100, 30)
        self.exit_button.clicked.connect(self.close)

    def closeEvent(self, event):
        event.accept()  # Закрытие окна


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Window")  
        self.setGeometry(800, 300, 400, 350) 

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

        query = "SELECT password FROM users WHERE username = %s"
        params = (username,)
        result = self.db.execute_query(query, params)

        if result:  
            stored_password = result[0][0]  
            if stored_password == password:  
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                self.close()

                self.main_window = MainWindow()
                self.main_window.show()

            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя!")

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
