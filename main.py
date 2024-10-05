## python libraries
import sys

## GUI library
from PySide6.QtWidgets import QApplication

## local
from main_window import MainWindow

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())
   