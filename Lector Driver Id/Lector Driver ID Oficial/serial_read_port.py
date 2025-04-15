import serial
from PyQt6.QtCore import QThread, pyqtSignal


class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.read_ids = set()
        self.keep_reading = True

    def read_ports(self):
        try:
            with serial.Serial(self.port, 115200, timeout=1) as ser:
                while self.keep_reading:
                    line = ser.readline().decode("utf-8", errors="ignore").strip()
                    for id_raw in line.split("*"):
                        id_clean = id_raw.strip()
                        if id_clean and id_clean not in self.read_ids:
                            self.read_ids.add(id_clean)
                            self.data_received.emit(id_clean)
        except Exception as e:
            self.data_received.emit(f"Error de lectura: {e}")

    def stop(self):
        self.keep_reading = False
        self.quit()
        self.wait()
