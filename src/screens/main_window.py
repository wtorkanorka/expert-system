from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt
from src.screens.question_window import QuestionWindow
from data.knowledge_base import KnowledgeBase
from src.inference_engine import InferenceEngine
from src.screens.result_window import ResultWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Экспертная система по выбору языка программирования')
        self.setFixedSize(800, 600)
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb)
        self.init_ui()

    def init_ui(self):
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.background_label = QLabel(self.container)
        self.background_label.setGeometry(0, 0, 800, 600)
        self.movie = QMovie('assets/backgound.gif')
        self.movie.setScaledSize(self.size())
        self.background_label.setMovie(self.movie)
        self.movie.start()
        self.content_widget = QWidget(self.container)
        self.content_widget.setGeometry(0, 0, 800, 600)
        self.content_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.start_button = QPushButton('Начать опрос', self.content_widget)
        self.start_button.setFixedSize(200, 50)
        self.start_button.move(300, 275) 
        self.start_button.clicked.connect(self.start_survey)

    def start_survey(self):
        self.question_window = QuestionWindow(self.kb.get_questions(), self.show_result)
        self.question_window.show()
        self.hide()

    def show_result(self, answers):
        detailed_results = self.engine.infer(answers)
        self.result_window = ResultWindow(detailed_results, self.restart_survey)
        self.result_window.show()
        self.question_window.close()

    def restart_survey(self):
        self.start_survey()
