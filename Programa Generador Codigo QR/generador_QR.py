import sys
import tempfile
import qrcode
import os
from PIL import Image, ImageDraw, ImageTk, ImageFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
)


class miventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador Código QR")
        self.setFixedSize(300, 300)  # Ajustamos el tamaño de la ventana
        self.generador_qr()

    def generador_qr(self):
        self.etiqueta_comentario = QLabel("Comentario:")
        self.campo_comentario = QLineEdit()
        self.campo_comentario.setPlaceholderText("Escribe tu comentario aquí")

        self.boton_importar_documento = QPushButton("Importar bloc de notas")
        self.boton_importar_documento.clicked.connect(self.generador_codigo_QR)

        layout_principal = QVBoxLayout()

        layout_comentario = QHBoxLayout()
        layout_comentario.addWidget(self.etiqueta_comentario)
        layout_comentario.addWidget(self.campo_comentario)

        layout_principal.addLayout(layout_comentario)
        layout_principal.addWidget(self.boton_importar_documento)

        self.setLayout(layout_principal)

    def generador_codigo_QR(self, checked=False):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Seleciona un archivo",
            "",
            "Archivos de texto (*txt);;Todos los archivos(*)",
        )
        if file_path:
            ancho_hoja = 2480
            alto_hoja = 3508
            tamaño_qr = 140
            espacio = 30  # Espacio entre el QR y el texto
            margen_x = 100
            margen_y = 100
            espacio_entre_textos = 10

            hoja = Image.new("RGB", (ancho_hoja, alto_hoja), "white")
            draw = ImageDraw.Draw(hoja)
            fuente = ImageFont.truetype("arial.ttf", 40)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.readlines()

                comentario = (
                    self.campo_comentario.text().strip().upper()
                )  # Obtener el comentario

                x, y = margen_x, margen_y

                for index, line in enumerate(file_content):
                    line = line.strip()
                    qr = qrcode.make(line)
                    qr = qr.resize((tamaño_qr, tamaño_qr))
                    hoja.paste(qr, (x, y))

                    pos_x_texto = x + tamaño_qr + espacio
                    pos_y_texto = y + (tamaño_qr // 4)

                    draw.text(
                        (pos_x_texto, pos_y_texto), line, font=fuente, fill="black"
                    )

                    pos_y_comentario = pos_y_texto + 40 + espacio_entre_textos
                    draw.text(
                        (pos_x_texto, pos_y_comentario),
                        comentario,
                        font=fuente,
                        fill="Black",
                    )

                    # Pasar a la siguiente fila
                    y += tamaño_qr + espacio

                    if (
                        y + tamaño_qr > alto_hoja - 100
                    ):  # Si llegamos al final de la hoja, nueva columna
                        y = margen_y
                        x += tamaño_qr + 400  # Avanzamos en X para la nueva columna
            except:
                QMessageBox.warning(
                    self, "Error", "Favor selecionar un archivo de texto."
                )

            # Guardar la imagen temporalmente y abrirla para imprimir
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                ruta_temporal = tmp.name
                hoja.save(ruta_temporal)

            os.startfile(ruta_temporal, "print")

        else:
            QMessageBox.warning(self, "Error", "Favor, eligir el blod de notas.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = miventana()
    ventana.show()
    sys.exit(app.exec())
