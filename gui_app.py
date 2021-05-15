from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


def application():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle("Лифты")
    window.setGeometry(300, 250, 600, 500)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
