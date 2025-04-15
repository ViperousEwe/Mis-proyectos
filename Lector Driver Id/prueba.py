import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QPushButton, QMessageBox, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal


# Hilo que lee desde el puerto serial sin bloquear la interfaz
class LectorSerial(QThread):
    nuevo_id = pyqtSignal(str)

    def __init__(self, puerto):
        super().__init__()
        self.puerto = puerto
        self.ids_leidos = set()
        self.lectura_activa = True

    def run(self):
        try:
            with serial.Serial(self.puerto, 115200, timeout=1) as ser:
                while self.lectura_activa:
                    linea = ser.readline().decode("utf-8", errors="ignore").strip()
                    for id_raw in linea.split("*"):
                        id_limpio = id_raw.strip()
                        if id_limpio and id_limpio not in self.ids_leidos:
                            self.ids_leidos.add(id_limpio)
                            self.nuevo_id.emit(id_limpio)
        except Exception as e:
            self.nuevo_id.emit(f"Error: {e}")

    def detener(self):
        self.lectura_activa = False
        self.quit()
        self.wait()


# Interfaz principal
class SerialPortSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector de IDs por Puerto Serial")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.combo = QComboBox()
        puertos = list({p.device for p in serial.tools.list_ports.comports()})
        self.combo.addItems(puertos)
        layout.addWidget(QLabel("Selecciona un puerto COM:"))
        layout.addWidget(self.combo)

        self.boton_iniciar = QPushButton("Iniciar lectura")
        self.boton_iniciar.clicked.connect(self.abrir_puerto)
        layout.addWidget(self.boton_iniciar)

        self.boton_detener = QPushButton("Detener lectura")
        self.boton_detener.clicked.connect(self.detener_lectura)
        self.boton_detener.setEnabled(False)
        layout.addWidget(self.boton_detener)

        self.texto_ids = QTextEdit()
        self.texto_ids.setReadOnly(True)
        layout.addWidget(QLabel("IDs leídos:"))
        layout.addWidget(self.texto_ids)

        self.lector = None

    def abrir_puerto(self):
        puerto = self.combo.currentText()
        if not puerto:
            QMessageBox.warning(self, "Error", "Selecciona un puerto COM")
            return

        self.lector = LectorSerial(puerto)
        self.lector.nuevo_id.connect(self.mostrar_id)
        self.lector.start()

        self.boton_iniciar.setEnabled(False)
        self.boton_detener.setEnabled(True)
        QMessageBox.information(self, "Puerto abierto", f"El puerto {puerto} ha sido abierto")

    def mostrar_id(self, id_leido):
        self.texto_ids.append(f"{id_leido}")

    def detener_lectura(self):
        if self.lector:
            self.lector.detener()
            
            self.lector = None
        self.boton_iniciar.setEnabled(True)
        self.boton_detener.setEnabled(False)
        QMessageBox.information(self, "Lectura detenida", "La lectura del puerto ha sido detenida.")


# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SerialPortSelector()
    ventana.show()
    sys.exit(app.exec())
