import qrcode
from PIL import Image, ImageDraw, ImageFont

try:
    with open('ejemplo.txt', 'r') as fichero:
        lineas = fichero.readlines()

        if not lineas:
            print("⚠️ El archivo está vacío.")
            exit()

        for linea in lineas:
            # Divide la línea en dos partes: CP y comentario
            datos = linea.strip().split(maxsplit=1)
            if len(datos) == 2:
                codigo = datos[0]  # IMEI o CP
                comentario_usuario = datos[1]  # Comentario ingresado por el usuario
            else:
                codigo = datos[0]
                comentario_usuario = "Sin comentario"

            # Generar QR
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=2
            )

            qr.add_data(codigo)
            qr.make(fit=True)

            img_qr = qr.make_image(fill="black", back_color="white").convert("RGB")

            # Ajuste de imagen
            ancho_qr, alto_qr = img_qr.size
            ancho_total = ancho_qr + 250  # Espacio extra para el texto al lado
            alto_total = max(alto_qr, 100)

            img_final = Image.new("RGB", (ancho_total, alto_total), "white")
            draw = ImageDraw.Draw(img_final)

            # Agregar QR
            y_paste = max(0, (alto_total - alto_qr) // 2)
            img_final.paste(img_qr, (0, y_paste))

            # Agregar texto al lado del QR
            x_texto = ancho_qr + 20
            y_texto = (alto_total // 3)

            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()

            draw.text((x_texto, y_texto), f"CP: {codigo}", fill="black", font=font)
            draw.text((x_texto, y_texto + 30), f"{comentario_usuario}", fill="black", font=font)

            # Guardar imagen con QR + CP + Comentario
            img_final.save(f"QR_{codigo}.png")
            print(f"✅ Imagen generada: QR_{codigo}.png")

except FileNotFoundError:
    print("❌ El archivo no fue encontrado.")
