import math  # Importar el modulo matematicos
import pandas as pd  # Importar pandas para expotar a Excel


# Funcion para validar entradas numericas
def validar_entrada(prompt):
    while True:
        try:
            valor = float(input(prompt))  # Intenta convertir a float
            return valor  # Retorna el valor si es valido
        except ValueError:
            print("Error: Por favor, ingrese un numero valido.")


def logitud_Vara_Combustible(longitud_vara, L):
    # Logitud Vara
    longitud_vara = longitud_vara - 20
    longitud_vara_tabla = longitud_vara / 29
    longitud_vara_tabla_litro_tanque = L / longitud_vara

    return longitud_vara_tabla, longitud_vara_tabla_litro_tanque


def Imprimir_Excel(longitud_vara_tabla, longitud_vara_tabla_litro_tanque):

    # Crear el contenido del archivo .ttd
    contenido_ttd = []
    # Metadatos inicaicles
    contenido_ttd.append(":163325177")
    contenido_ttd.append("$0 ")
    contenido_ttd.append("&0 ")

    # Genera filas de 0 a 30
    for i in range(30):
        mm = i * longitud_vara_tabla
        l = mm * longitud_vara_tabla_litro_tanque
        # Formatear las filas como en el archivo original
        contenido_ttd.append(f"{mm:.1f} {l:.1f}")

    # Expotar el DataFrame a un archivo .ttd
    nombre_archivo = "tabla_calibracion.ttd"
    with open(nombre_archivo, "w") as file:
        file.write("\r\n".join(contenido_ttd))

    print(f"\nLa tabla ha sido exportada exitosamente a '{nombre_archivo}'")


def Calcular_Tanque_Cuadrado():

    # Solicitar dimensiones del tanque usando la funcion
    largo = validar_entrada("Ingrese el largo del tanque en cm:")
    ancho = validar_entrada("Ingrese el ancho (A) del tanque en cm:")
    altura = validar_entrada("Ingrese la altura (B) del tanque en cm:")
    longitud_vara = validar_entrada("Ingrese la logitud de la vara en mm:")

    # Conversion dimesiones del tanque a Metros
    largo = largo / 100
    ancho = ancho / 100
    altura = altura / 100

    # Conversion de las dimesiones en metros litros
    M = largo * ancho * altura
    L = M * 1000

    longitud_vara_tabla, longitud_vara_tabla_litro_tanque = logitud_Vara_Combustible(
        longitud_vara, L
    )

    Imprimir_Excel(longitud_vara_tabla, longitud_vara_tabla_litro_tanque)


def Calcular_Tanque_Cilindrico():

    # Solicitar dimensiones del tanque usando la funcion
    largo = validar_entrada("Ingrese el largo del tanque en cm:")
    Diametro = validar_entrada("Ingrese el Diametro (D) del tanque en cm:")
    longitud_vara = validar_entrada("Ingrese la logitud de la vara en mm: ")

    Radio = Diametro / 2  # Diametro del cilindrico

    # Conversion dimesiones del tanque a Metros
    largo = largo / 100
    Diametro = Diametro / 100
    Radio = Radio / 100

    # Conversion de las dimesiones en metros a galones y galones a litros
    M = math.pi * (Radio**2) * largo
    L = M * 1000

    longitud_vara_tabla, longitud_vara_tabla_litro_tanque = logitud_Vara_Combustible(
        longitud_vara, L
    )

    Imprimir_Excel(longitud_vara_tabla, longitud_vara_tabla_litro_tanque)


def Calcular_Tanque_Ovalado():
    # Solicitar dimensiones del tanque usando la funcion
    largo = validar_entrada("Ingrese el largo del tanque en cm:")
    Ancho = validar_entrada("Ingrese el ancho (A) del tanque en cm:")
    Altura = validar_entrada("Ingrese la altura (B) de la vara en mm: ")
    longitud_vara = validar_entrada("Ingrese la logitud de la vara en mm: ")

    # Conversion dimesiones del tanque a Metros
    largo = largo / 100
    Ancho = Ancho / 100
    Altura = Altura / 100

    Relacion = Relacion = ((Ancho / 2) + (Altura / 2)) / 2
    # Realacion A&B del Ovalado

    # Conversion de las dimesiones en metros a galones y galones a litros
    M = math.pi * (Relacion**2) * largo
    L = M * 1000

    longitud_vara_tabla, longitud_vara_tabla_litro_tanque = logitud_Vara_Combustible(
        longitud_vara, L
    )

    Imprimir_Excel(longitud_vara_tabla, longitud_vara_tabla_litro_tanque)


# Menu
def mostrar_menu():
    print("\n--- Menu Principal ---")
    print("1. Calcular Tanque Cuadrado")
    print("2. Calcular Tanque Cilindrico")
    print("3. Calcular Tanque Ovalado")
    print("4. Salir")


# Programa principal
while True:
    mostrar_menu()
    opcion = input("Elige una opcion (1-4): ")

    if opcion == "1":
        Calcular_Tanque_Cuadrado()
    elif opcion == "2":
        Calcular_Tanque_Cilindrico()
    elif opcion == "3":
        Calcular_Tanque_Ovalado()
    elif opcion == "4":
        print("Gracias por usar el programa! Adios.")
        break
    else:
        print("Opcion no valida. Por favor, elige una opcion entre 1 y 4.")
