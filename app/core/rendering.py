import pdf417gen
from PIL import Image, ImageDraw, ImageFont


APP_NAME = "ControlTag"


def renderizar_imagem(valor, titulo=None):
    """Gera uma imagem PIL com título, código de barras PDF417 e identificador."""
    if titulo is None:
        titulo = APP_NAME
    largura, altura = 900, 300
    valor = str(valor) if valor is not None else ""
    if not valor:
        return Image.new("RGB", (largura, altura), "white")

    encoded = None
    for cols in (3, 4, 6, 8):
        try:
            encoded = pdf417gen.encode(valor, columns=cols)
            break
        except Exception:
            encoded = None

    if encoded is None:
        return Image.new("RGB", (largura, altura), "white")

    barcode = pdf417gen.render_image(encoded, scale=5, ratio=3, padding=1)
    barcode = barcode.resize((700, 140), Image.Resampling.LANCZOS)

    etiqueta = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(etiqueta)

    try:
        font = ImageFont.truetype("arial.ttf", 55)
        font_p = ImageFont.truetype("arial.ttf", 45)
    except Exception:
        font = font_p = ImageFont.load_default()

    bbox_titulo = draw.textbbox((0, 0), titulo, font=font)
    draw.text(((largura - bbox_titulo[2]) // 2, 15), titulo, fill="black", font=font)

    etiqueta.paste(barcode, ((largura - 700) // 2, 80))

    bbox_valor = draw.textbbox((0, 0), valor, font=font_p)
    draw.text(((largura - bbox_valor[2]) // 2, 235), valor, fill="black", font=font_p)

    return etiqueta
