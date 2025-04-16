import sys
from PyQt6.QtWidgets import QApplication
from interfaz import SerialReaderApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialReaderApp()
    window.show()
    sys.exit(app.exec())
