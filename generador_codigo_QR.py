import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Datos del código de barras
imei = "353994713145602"
model = "Model: R12L (LA)"
version = "VER: F"

# Ruta donde se guardará la imagen
barcode_filename = "barcode.png"
barcode_path = os.path.join(os.getcwd(), barcode_filename)

# Generar el código de barras en formato CODE128
ean = barcode.get_barcode_class('code128')
barcode_obj = ean(imei, writer=ImageWriter())

# Guardar la imagen del código de barras
barcode_obj.save(barcode_filename)

# Verificar si la imagen se generó correctamente
if os.path.exists(barcode_path):
    print(f"Código de barras generado en: {barcode_path}")

    # Abrir la imagen para agregar texto
    img = Image.open(barcode_path)
    draw = ImageDraw.Draw(img)

    # Cargar una fuente (si Arial no está disponible, usará la predeterminada)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font = ImageFont.load_default()

    # Agregar texto con modelo y versión
    draw.text((10, 10), f"{model}       {version}", fill="black", font=font)

    # Guardar la imagen final con el texto añadido
    final_filename = "barcode_final.png"
    final_path = os.path.join(os.getcwd(), final_filename)
    img.save(final_path)

    print(f"Imagen final con texto guardada en: {final_path}")
else:
    print("Error: No se pudo generar el código de barras.")
