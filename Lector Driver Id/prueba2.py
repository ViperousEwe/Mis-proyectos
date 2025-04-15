import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox
)

class SerialPortSelector(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lector Dallas")
        self.resize(300, 150)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Etiqueta
        self.label = QLabel("Selecciona un puerto COM:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems([p.device for p in serial.tools.list_ports.comports()])
        layout.addWidget(QLabel("Puerto:"))
        layout.addWidget(self.combo)
        
        self.boton = QPushButton("Abrir puerto")
        self.boton.clicked.connect(self.abrir_puerto)
        layout.addWidget(self.boton)

        self.lector = None

    ids_leidos = set()
    
    def abrir_puerto(self):
        puerto = self.combo.currentText()
        if not puerto:
            QMessageBox.warning(self, "Error", "Selecciona un puerto COM")
            return
        
        self.lector = serial.Serial(puerto)
        self.lector.nuevo_id.connect(self.mostrar_id)
        self.lector.start()
        self.boton.setEnabled(False)
        QMessageBox.information(self, "Puerto abierto", f"El puerto {puerto} ha sido abierto")
        
    def mostrar_id(self,id_leido):
        print("ID leido:", id_leido)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SerialPortSelector()
    ventana.show()
    sys.exit(app.exec())
