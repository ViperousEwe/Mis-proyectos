import sys
import os

from serial_read_port import SerialReaderThread

def test_generate_qr_sheet_returns_image():
    ids = ["123", "456", "789"]
    reader = SerialReaderThread("COM1")
    img = reader.generate_qr_sheet(ids)

    assert img is not None
    assert hasattr(img, "save")
