import serial
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtCore import QThread, pyqtSignal


class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.read_ids = set()
        self.keep_reading = True

    def run(self):
        self.read_ports()

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
            self.error_occurred.emit(f"Error al leer el puerto: {str(e)}")

    def generate_qr_sheet(self, read_ids):

        page_width = 2480
        page_height = 3508
        qr_size = 140
        spacing = 30  # Space between the QR and the text
        margin_x = 100
        margin_y = 100
        text_spacing = 10

        page = Image.new("RGB", (page_width, page_height), "white")
        draw = ImageDraw.Draw(page)
        font = ImageFont.truetype("arial.ttf", 40)

        x, y = margin_x, margin_y

        for index, line in enumerate(read_ids):
            qr = qrcode.make(line)
            qr = qr.resize((qr_size, qr_size))
            page.paste(qr, (x, y))

            # Pasar a la siguiente fila
            y += qr_size + text_spacing

            if (
                y + qr_size > page_height - 100
            ):  # Si llegamos al final de la hoja, nueva columna
                y = margin_y
                x += qr_size + 400  # Avanzamos en X para la nueva columna
        return page

    def stop(self):
        self.keep_reading = False
        self.quit()
        self.wait()
