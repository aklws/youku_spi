# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
