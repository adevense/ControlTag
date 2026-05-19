import os
from app.core import backup
from app.core.config import carregar_config, salvar_config, DEFAULT_BACKUP_DIR

class ConfigService:
    def __init__(self):
        self.config = carregar_config()
        self.backup_dir = self.config.get("backup_path", DEFAULT_BACKUP_DIR)
        if not os.path.exists(self.backup_dir):
            try:
                os.makedirs(self.backup_dir)
            except Exception:
                self.backup_dir = DEFAULT_BACKUP_DIR

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        salvar_config(self.config)

    def save_all(self, data: dict):
        self.config.update(data)
        salvar_config(self.config)

    def get_backup_dir(self):
        return self.backup_dir

    def set_backup_dir(self, path):
        self.backup_dir = path
        self.set_config("backup_path", path)

    def manual_backup(self, excel_path):
        backup.fazer_backup_manual(excel_path, self.backup_dir)

    def clear_backups(self, idioma, TEXTS, status_callback):
        backup.limpar_backups(self.backup_dir, idioma, TEXTS, status_callback)

    def open_backup_folder(self):
        backup.abrir_pasta_dados(self.backup_dir)

    def select_backup_folder(self, filedialog, callback):
        path = backup.selecionar_pasta_backup(self.backup_dir, filedialog, callback)
        if path:
            self.set_backup_dir(path)
        return path
