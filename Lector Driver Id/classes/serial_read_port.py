import serial
import serial.tools.list_ports
import time
import qrcode

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]


def read_ports(port, baudrate=115200, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            time.sleep(2)  # Espera a que el puerto se estabilice
            print(
                f"Puerto abierto: {port}. Esperando datos... \n Presione Ctrl+C para salir."
            )
            while True:
                if ser.in_waiting:
                    line = ser.readline().decode("utf-8", errors="ignore").split("*").strip()
                    if line:
                        print("ID leido:", line)
    except serial.SerialException as e:
        print(f"Error al abrir el puerto: {e}")
    except KeyboardInterrupt:
        print("Lectura interrumpida por el usuario.")

def create_qr_code():
    
