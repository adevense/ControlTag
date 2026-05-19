import os
from tkinter import messagebox
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

try:
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

def enviar_arquivo_para_impressora(filepath, direct_print_mode, target_printer):
    """Envia um arquivo para a impressora configurada ou abre o arquivo."""
    if not HAS_WIN32 or not direct_print_mode:
        os.startfile(filepath)
        return

    if not target_printer or "Erro" in target_printer or "Selecione" in target_printer:
        messagebox.showwarning("Impressora", "Selecione uma impressora válida na aba Config!")
        os.startfile(filepath)
        return

    try:
        win32api.ShellExecute(0, "printto", filepath, f'"{target_printer}"', ".", 0)
    except Exception as e:
        messagebox.showerror("Erro de Impressão", f"Falha ao enviar: {e}\nAbrindo PDF...")
        os.startfile(filepath)

def gerar_pdf_generico(lista_dicts, filepath, print_cfg, renderizar_imagem, enviar_para_impressora):
    """Gera um PDF com códigos de barras e o envia para impressão."""
    try:
        W_mm = print_cfg["width"]
        H_mm = print_cfg["height"]
        Marg_mm = print_cfg["margin_x"]
        Gap_mm = print_cfg["gap"]
        OffX_mm = print_cfg["offset_x"]
        OffY_mm = print_cfg["offset_y"]

        w = W_mm * mm; h = H_mm * mm
        margem = Marg_mm * mm; gap = Gap_mm * mm
        off_x = OffX_mm * mm; off_y = OffY_mm * mm

        larg_total = (margem * 2) + (w * 2) + gap

        c = canvas.Canvas(filepath, pagesize=(larg_total, h))

        for item in lista_dicts:
            img_pil = renderizar_imagem(item['id'])
            img_mem = ImageReader(img_pil)
            pos_x1 = margem + off_x
            pos_y = off_y
            pos_x2 = margem + w + gap + off_x

            c.drawImage(img_mem, pos_x1, pos_y, width=w, height=h)
            c.drawImage(img_mem, pos_x2, pos_y, width=w, height=h)
            c.showPage()

        c.save()
        enviar_para_impressora(filepath)

    except Exception as e:
        messagebox.showerror("Erro PDF", str(e))