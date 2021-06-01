from PyQt5.QtWidgets import QApplication
from src.gui import ElevatorsWindow

import sys


def application():
    app = QApplication(sys.argv)

    window = ElevatorsWindow(
        floors=15,
        elevators=5,
    )
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
