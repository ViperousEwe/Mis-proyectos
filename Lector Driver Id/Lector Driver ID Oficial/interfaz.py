import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QMessageBox,
    QTextEdit,
)

from serial_read_port import SerialReaderThread


class SerialReaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector de Serial")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.combo = QComboBox()
        ports = list({p.device for p in serial.tools.list_ports.comports()})
        self.combo.addItems(ports)
        layout.addWidget(QLabel("Selecciona el puerto serial COM:"))
        layout.addWidget(self.combo)

        self.start_button = QPushButton("Iniciar Lectura")
        self.start_button.clicked.connect(self.start_reading)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Detener Lectura")
        self.stop_button.clicked.connect(self.stop_reading)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.text_ids = QTextEdit()
        self.text_ids.setReadOnly(True)
        layout.addWidget(QLabel("IDs leídos:"))
        layout.addWidget(self.text_ids)

        self.lector = None

    def start_reading(self):
        port = self.combo.currentText()
        if not port:
            QMessageBox.warning(self, "Error", "Por favor selecciona un puerto serial.")
            return

        self.reader_thread = SerialReaderThread(port)
        self.reader_thread.data_received.connect(self.show_id)
        self.reader_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        QMessageBox.information(self, "Iniciar Lectura", f"Lectura iniciada en {port}.")

    def show_id(self, read_ids):
        self.text_ids.append(f"{read_ids}")

    def stop_reading(self):
        if self.reader_thread:
            self.reader_thread.stop()

            self.reader_thread = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Detener Lectura", "Lectura detenida.")
