import os
import qrcode
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tempfile
from PIL import Image,ImageDraw, ImageTk, ImageFont

#mensajes de avisos
def mesage_box ():
    mensaje = messagebox.showinfo("Mensaje importante", "Se imprimio correctamente, favor revisar la impresora.")
    
def mesage_box1 ():
    mensaje = messagebox.showinfo("Mensaje importante", "No selecionaste ningun archivo.")
    
def mesage_box2 ():
    mensaje = messagebox.showinfo("Mensaje importante", "Error al leer el archivo.")
   
def generador_codigo_QR():
    file_path = filedialog.askopenfilename(title="Seleciona un archivo") #Permite al usuario selecionar la carpeta a abrir.        
    if file_path:

        ancho_hoja = 2480
        alto_hoja = 3508
        tamaño_qr = 200
        espacio = 200
        x, y = 100, 100
        hoja = Image.new("RGB",(ancho_hoja,alto_hoja),"white")
        draw = ImageDraw.Draw(hoja)
        fuente = ImageFont.truetype("arial.ttf", 40)
  
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.readlines() #Obtener las lineas del archivo
                
                for index, line in enumerate(file_content):
                    line = line.strip()
                
                    qr = qrcode.make(line)
                    qr = qr.resize((tamaño_qr,tamaño_qr))
                    
                    hoja.paste(qr,(x, y))
                    
                    bbox = draw.textbbox((0,0), line, font=fuente)
                    ancho_texto = bbox[2] - bbox[0]
                    
                    pos_x_texto = x + (tamaño_qr - ancho_texto) / 2
                    pos_y_texto = y + tamaño_qr + 10
                    
                    draw.text((pos_x_texto,pos_y_texto), line, font=fuente, fill="black")
                    
                    x += tamaño_qr + espacio
                    
                    if x + tamaño_qr > ancho_hoja - 100:
                        x = 100
                        y += tamaño_qr + espacio
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    ruta_temporal = tmp.name
                    hoja.save(ruta_temporal)
                    
                    os.startfile(ruta_temporal, "print")
                    
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