from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt

class ResultWindow(QWidget):
    def __init__(self, recommendations, restart_callback):
        super().__init__()
        self.setWindowTitle('Результат')
        self.setFixedSize(800, 600)
        self.recommendations = recommendations
        self.restart_callback = restart_callback
        self.init_ui()

    def init_ui(self):
        # Создаем основной контейнер
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 800, 600)

        # Создаем слой для фона
        self.background_label = QLabel(self.container)
        self.background_label.setGeometry(0, 0, 800, 600)

        # Загружаем ваш GIF из корневого каталога
        self.movie = QMovie('backgound.gif')
        self.movie.setScaledSize(self.size())
        self.background_label.setMovie(self.movie)
        self.movie.start()

        # Создаем слой для контента
        self.content_widget = QWidget(self.container)
        self.content_widget.setGeometry(0, 0, 800, 600)
        self.content_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Устанавливаем layout для контента
        self.layout = QVBoxLayout(self.content_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Отображаем результат
        result_label = QLabel('Рекомендуемые языки программирования:')
        result_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        self.layout.addWidget(result_label)

        for rec in self.recommendations:
            lang_label = QLabel(f"{rec['language']} - {rec['score']}% соответствия")
            lang_label.setStyleSheet("font-size: 20px; font-weight: bold; color: yellow;")
            self.layout.addWidget(lang_label)

        # Кнопка для перезапуска
        restart_button = QPushButton('Пройти опрос заново')
        restart_button.setFixedSize(200, 50)
        restart_button.clicked.connect(self.restart)
        self.layout.addWidget(restart_button)

    def restart(self):
        self.restart_callback()
        self.close()