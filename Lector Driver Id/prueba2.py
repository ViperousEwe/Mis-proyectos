import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QPushButton, QMessageBox, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal

# Hilo de lectura serial mejorado
class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, port: str, baudrate: int = 115200, parent=None):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.keep_reading = True
        self.read_ids = set()

    def run(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                while self.keep_reading:
                    try:
                        line = ser.readline().decode("utf-8", errors="ignore").strip()
                        if not line:
                            continue
                        # Se asume que los IDs vienen separados por "*"
                        for token in line.split('*'):
                            token = token.strip()
                            if token and token not in self.read_ids:
                                self.read_ids.add(token)
                                self.data_received.emit(token)
                    except serial.SerialException as e:
                        self.error_occurred.emit(f"Error de lectura: {e}")
                        break
        except Exception as e:
            self.error_occurred.emit(f"Error al abrir el puerto: {e}")

    def stop(self):
        self.keep_reading = False
        self.wait()

# Interfaz principal de la aplicación
class SerialReaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector de IDs desde Puerto Serial")
        self.resize(400, 300)
        self.reader_thread = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Selector de puertos disponibles
        layout.addWidget(QLabel("Selecciona un puerto COM:"))
        self.port_combo = QComboBox()
        self.refresh_ports()
        layout.addWidget(self.port_combo)

        # Botón para iniciar la lectura
        self.start_btn = QPushButton("Iniciar Lectura")
        self.start_btn.clicked.connect(self.start_reading)
        layout.addWidget(self.start_btn)

        # Botón para detener la lectura
        self.stop_btn = QPushButton("Detener Lectura")
        self.stop_btn.clicked.connect(self.stop_reading)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)

        # Área de texto para mostrar los IDs leídos
        layout.addWidget(QLabel("IDs leídos:"))
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

    def refresh_ports(self):
        # Actualiza la lista de puertos disponibles
        ports = sorted({port.device for port in serial.tools.list_ports.comports()})
        self.port_combo.clear()
        self.port_combo.addItems(ports)

    def start_reading(self):
        port = self.port_combo.currentText()
        if not port:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un puerto COM")
            return

        self.reader_thread = SerialReaderThread(port)
        self.reader_thread.data_received.connect(self.update_text_area)
        self.reader_thread.error_occurred.connect(self.handle_error)
        self.reader_thread.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        QMessageBox.information(self, "Puerto Abierto", f"El puerto {port} ha sido abierto para la lectura.")

    def update_text_area(self, id_value):
        self.text_area.append(id_value)

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.stop_reading()

    def stop_reading(self):
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        QMessageBox.information(self, "Lectura detenida", "La lectura del puerto ha sido detenida.")

    def closeEvent(self, event):
        # Asegura que el hilo se detenga al cerrar la aplicación
        if self.reader_thread:
            self.reader_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = SerialReaderApp()
    main_win.show()
    sys.exit(app.exec())
