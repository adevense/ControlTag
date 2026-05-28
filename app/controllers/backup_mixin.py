from tkinter import filedialog, messagebox
from app.config.translations import TEXTS


class BackupMixin:
    def abrir_pasta_dados(self):
        self.config_service.open_backup_folder()

    def selecionar_pasta_backup(self):
        path = self.config_service.select_backup_folder(
            filedialog,
            lambda p: self.view.pages["Config"].set_backup_path(p)
        )
        if path:
            self.backup_dir = path
            self.salvar_config()
            messagebox.showinfo("Sucesso", f"Backups agora serão salvos em:\n{path}")

    def limpar_backups(self):
        self.config_service.clear_backups(self.idioma, TEXTS, self.view.set_status)

    def fazer_backup_manual(self):
        self.config_service.manual_backup(self.excel_path)
