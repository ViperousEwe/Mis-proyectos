import serial
import os
import serial.tools.list_ports
import tempfile
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QMessageBox,
    QTextEdit,
    QApplication,
)

from serial_read_port import SerialReaderThread


class SerialReaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector de Serial")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a label and combo box for selecting the serial port
        self.combo = QComboBox()
        ports = list({p.device for p in serial.tools.list_ports.comports()})
        self.combo.addItems(ports)
        layout.addWidget(QLabel("Selecciona el puerto serial COM:"))
        layout.addWidget(self.combo)

        # Create buttons for starting and stopping the reading process
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

        self.boton_import_qr = QPushButton("Generar QR")
        self.boton_import_qr.clicked.connect(self.print_qr)
        layout.addWidget(self.boton_import_qr)

        self.lector = None

    def start_reading(self):
        port = self.combo.currentText()
        if not port:
            QMessageBox.warning(self, "Error", "Por favor selecciona un puerto serial.")
            return

        self.reader_thread = SerialReaderThread(port)
        self.reader_thread.data_received.connect(self.show_id)
        self.reader_thread.error_occurred.connect(self.show_error)
        self.reader_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        QMessageBox.information(self, "Iniciar Lectura", f"Lectura iniciada en {port}.")

    def show_id(self, read_ids):
        self.text_ids.append(f"{read_ids}")

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)
        self.stop_reading()
        QApplication.quit()

    def stop_reading(self):
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Detener Lectura", "Lectura detenida.")

    def print_qr(self):
        if not self.text_ids.toPlainText():
            QMessageBox.warning(self, "Error", "No hay IDs leídos para generar QR.")
            return

        # filt ing out empty lines and duplicates
        # and converting to a list
        read_ids = list(
            set(filter(None, self.text_ids.toPlainText().strip().splitlines()))
        )

        page = SerialReaderThread.generate_qr_sheet(self.reader_thread, read_ids)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            ruta_temporal = tmp.name
            page.save(ruta_temporal)

        os.startfile(ruta_temporal, "print")