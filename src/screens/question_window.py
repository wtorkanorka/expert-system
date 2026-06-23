from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox, QButtonGroup
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt

class QuestionWindow(QWidget):
    def __init__(self, questions, result_callback):
        super().__init__()
        self.setWindowTitle('Опрос')
        self.setFixedSize(800, 600)
        self.questions = questions
        self.result_callback = result_callback
        self.current_question_index = 0
        self.answers = {}
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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.display_question()

    def display_question(self):
        # Очищаем layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]

            progress_label = QLabel(f'Вопрос {self.current_question_index + 1} из {len(self.questions)}')
            progress_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
            self.layout.addWidget(progress_label)

            question_label = QLabel(question_data['question'])
            question_label.setStyleSheet("font-size: 20px; color: white;")
            self.layout.addWidget(question_label)

            self.button_group = QButtonGroup(self)
            self.option_buttons = []  # Список для хранения кнопок и соответствующих опций

            for option in question_data['options']:
                option_text = option['text']
                radio_button = QRadioButton(option_text)
                radio_button.setStyleSheet("font-size: 18px; color: white;")
                self.button_group.addButton(radio_button)
                self.layout.addWidget(radio_button)
                self.option_buttons.append((radio_button, option))  # Сохраняем пару (кнопка, опция)

            self.next_button = QPushButton('Далее')
            self.next_button.setFixedSize(100, 40)
            self.next_button.clicked.connect(self.next_question)
            self.layout.addWidget(self.next_button)
        else:
            # Опрос завершён
            self.result_callback(self.answers)
            self.close()

    def next_question(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            # Находим выбранную опцию
            selected_option = None
            for radio_button, option in self.option_buttons:
                if radio_button == selected_button:
                    selected_option = option
                    break

            if selected_option:
                answer_text = selected_option['text']
                question_key = self.questions[self.current_question_index]['question']
                self.answers[question_key] = answer_text
                self.current_question_index += 1
                self.display_question()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Произошла ошибка при обработке вашего выбора.')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите вариант ответа.')