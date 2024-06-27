from PySide6.QtWidgets import QApplication
from app import PyClackApp
import sys


def main():
    app = QApplication([])
    window = PyClackApp()
    window.show()
    status = app.exec()
    sys.exit(status)


main()