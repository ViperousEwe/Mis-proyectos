import serial
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port: str, baudrate: int = 115200, parent=None):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.keep_reading = True
        self.read_ids = set()
    
    def read_ports(port, baudrate=115200, timeout=1):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                while self.keep_reading is True:
                    try:
                        line = ser.readlines().strip()
                        if not line:
                            continue
                        for toke in line.split("*"):
                            token = token.strip()
                            if token and token not in self.read_ids:
                                self.read_ids.add(token)
                                self.data_received.emit(token)
                    except serial.SerialException as e:
                        self.error_occurred.emit(f"Error de lectura: {e}")
                        break
        except Exception as e:
            self.error_occurred.emit(f"Error de lectura: {e}")

    def stop(self):
        self.keep_reading = False
        self.quit()
        self.wait()
