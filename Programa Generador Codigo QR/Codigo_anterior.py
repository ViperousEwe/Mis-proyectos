#Generar los codigos QR
#Realizar el Menu y diseño visual
#Generar los CP con un comentario junto al codigo QR
#Generar todos los codigos en una misma pagina (limitar un maximo de pagina por cantidad de QR)
#Poder con un boton selecionar la carpeta que desean
#Agregar que cree una carpeta y agregue los QR ahi
#Agregar una ventana previsualizacion y se imprima la hoja

import os
import qrcode
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageDraw, ImageTk

ancho_hoja = 2480
alto_hoja = 3508
tamaño_qr = 300
espacio = 50
x,y = 100,100

hoja = Image.new("RGB",(ancho_hoja,alto_hoja),"white")
draw = ImageDraw.Draw(hoja)
 
def mesage_box ():
    mensaje = messagebox.showinfo("Mensaje importante", "Se exporto correctamente los codigos QR.")
    
def mesage_box1 ():
    mensaje = messagebox.showinfo("Mensaje importante", "No selecionaste ningun archivo.")
    
def mesage_box2 ():
    mensaje = messagebox.showinfo("Mensaje importante", "Error al leer el archivo.")
    
def mesage_box3 ():
    mensaje = messagebox.showinfo("Mensaje importante", "La carpeta ya existe.")
    
def generador_codigo_QR():
    file_path = filedialog.askopenfilename(title="Seleciona un archivo") #Permite al usuario selecionar la carpeta a abrir.        
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.readlines() #Obtener las lineas del archivo
                
                for index, line in enumerate(file_content):
                    line = line.strip()
                    
                    qr = qrcode.QRCode( #Crear el codigo QR y ajustar el tamaño
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=2,
                        border=1,
                    )

                    qr.add_data(line) #Agregar la data al codigo QR
                    qr.make(fit=True)

                    qr_image = qr.make_image(fill="black", back_color="white")
                    filename= f"{line}.png"
                    
                    carpeta_codigos_qr = "Codigos QR Generados"
                    if not os.path.exists(carpeta_codigos_qr):
                        os.makedirs(carpeta_codigos_qr)
                    
                    else:
                        mesage_box3
                    ruta_codigos_qr = os.path.join(carpeta_codigos_qr,f"{filename}")
                    qr_image.save(ruta_codigos_qr)
                    
            mesage_box()
                    
        except Exception as e:
            mesage_box2()                    
    else:
        mesage_box1()

root = tk.Tk() #Crea una ventana tkinter
root.title("Generador de Codigos QR.")
root.geometry("400x300")

etiqueta = tk.Label(root, text="""Bienvenido al programa generador de codigo QR. \n
                    \n favor selecionar el blod de notas""",font=("Arial",12))
etiqueta.pack(pady=10)

boton = tk.Button(root, text="Importar blod de notas",command= generador_codigo_QR)
boton.pack(pady=10)

root.mainloop()