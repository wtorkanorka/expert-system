from PyQt6.QtWidgets import QApplication
import sys
from src.screens.main_window import MainWindow

class EXPSystemApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.show()

    def run(self):
        sys.exit(self.app.exec())
