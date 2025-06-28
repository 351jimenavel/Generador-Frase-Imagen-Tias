from PIL import Image, ImageDraw, ImageFont
import io
import base64

def generar_imagen(frase, imagen_base_path):
    img = Image.open(imagen_base_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    fuente = ImageFont.truetype("arial.ttf", 30)
    w, h = draw.textsize(frase, font=fuente)
    ancho, alto = img.size
    draw.text(((ancho - w) / 2, alto - 50), frase, font=fuente, fill="white")

    # Guardar imagen resultante
    ruta_salida = "static/resultado.png"
    img.save(ruta_salida)

    return ruta_salida
