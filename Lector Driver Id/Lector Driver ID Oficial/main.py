from classes import serial_read_port


def main():
    # Listar los puertos seriales disponibles
    ports = serial_read_port.list_serial_ports()

    if not ports:
        print("No hay puertos disponibles.")

    else:
        print("Puertos disponibles:")
        for i, p in enumerate(ports):
            print(f"{i}: {p}")

        seleccion = int(input("Selecciona el número del puerto: "))
        if 0 <= seleccion < len(ports):
            serial_read_port.read_ports(ports[seleccion])
        else:
            print("Selección no válida.")


if __name__ == "__main__":
    # Ejecutar la función principal
    main() 
