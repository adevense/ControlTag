import os
import shutil
from datetime import datetime
from tkinter import messagebox

def abrir_pasta_dados(backup_dir):
    if os.path.exists(backup_dir):
        os.startfile(backup_dir)
    else:
        messagebox.showerror("Erro", "Pasta não encontrada")

def selecionar_pasta_backup(current_dir, filedialog, update_callback=None):
    path = filedialog.askdirectory(title="Selecione onde salvar os backups", initialdir=current_dir)
    if path:
        if update_callback:
            update_callback(path)
        return path
    return None

def limpar_backups(backup_dir, idioma, TEXTS, status_msg=None):
    resp = messagebox.askyesno("Limpar Backups", f"Tem certeza que deseja apagar TODOS os arquivos .xlsx da pasta:\n\n{backup_dir}\n\nIsso não pode ser desfeito.")
    if resp:
        try:
            count = 0
            for filename in os.listdir(backup_dir):
                if filename.endswith(".xlsx") or filename.startswith("Backup_"):
                    filepath = os.path.join(backup_dir, filename)
                    os.remove(filepath)
                    count += 1
            if status_msg:
                status_msg(TEXTS[idioma]["msg"][8])
            messagebox.showinfo("Limpeza", f"{count} arquivos foram removidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def fazer_backup_manual(excel_path, backup_dir):
    if excel_path and os.path.exists(excel_path):
        if not os.path.exists(backup_dir): os.makedirs(backup_dir)
        nome_arq = f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        dst = os.path.join(backup_dir, nome_arq)
        try:
            shutil.copy2(excel_path, dst)
            messagebox.showinfo("Backup", f"Backup salvo com sucesso em:\n{dst}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar backup: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo Excel carregado para fazer backup.")
