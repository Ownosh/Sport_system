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

        self.setWindowTitle("Login Window")  # Заголовок окна
        self.setGeometry(800, 300, 400, 350)  # Размеры окна (400x350)

        # Создаем элементы интерфейса
        self.username_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрыть символы пароля
        self.login_button = QPushButton("Вход")
        self.exit_button = QPushButton("Выход")

        # Основной лейаут
        main_layout = QVBoxLayout()

        # Сетка для логина и пароля
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.username_label, 0, 0)  # Логин (надпись)
        grid_layout.addWidget(self.username_input, 0, 1)  # Поле ввода для логина
        grid_layout.addWidget(self.password_label, 1, 0)  # Пароль (надпись)
        grid_layout.addWidget(self.password_input, 1, 1)  # Поле ввода для пароля

        # Добавляем сетку в основной лейаут
        main_layout.addLayout(grid_layout)

        # Добавляем кнопку "Вход"
        main_layout.addWidget(self.login_button)

        # Лейаут для кнопки "Выход" (в правом нижнем углу)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()  # Заполняет пространство слева
        bottom_layout.addWidget(self.exit_button)

        # Добавляем нижний лейаут в основной
        main_layout.addLayout(bottom_layout)

        # Устанавливаем основной лейаут
        self.setLayout(main_layout)

        # Обработчики кнопок
        self.login_button.clicked.connect(self.check_user_credentials)
        self.exit_button.clicked.connect(self.close)  # Закрыть окно

        # Подключение к базе данных
        self.db = get_database_connection()

    def check_user_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Запрос к базе данных
        query = "SELECT password FROM users WHERE username = %s"
        params = (username,)
        result = self.db.execute_query(query, params)

        if result:  # Если пользователь найден
            stored_password = result[0][0]  # Получаем хранимый пароль
            if stored_password == password:  # Если пароли совпадают
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")

                # Закрываем окно логина
                self.close()

                # Открываем основное окно
                self.main_window = MainWindow()
                self.main_window.show()

            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя!")

    def closeEvent(self, event):
        self.db.close()  # Закрываем соединение с БД
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем главный цикл приложения


if __name__ == "__main__":
    main()
