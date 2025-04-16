import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 👇 asegúrate de que este import sea después del sys.path
from serial_read_port import SerialReaderThread


def test_generate_qr_sheet_returns_image():
    ids = ["123", "456", "789"]
    reader = SerialReaderThread("COM1")  # El puerto no importa para esta prueba
    img = reader.generate_qr_sheet(ids)

    assert img is not None
    assert hasattr(img, "save")  # Comprobamos que sea una imagen de Pillow
