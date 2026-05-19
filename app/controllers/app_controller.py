import os
import customtkinter as ctk
from app.config.translations import TEXTS
from app.config.themes import THEMES
from app.controllers.navigation_mixin import NavigationMixin
from app.controllers.excel_mixin import ExcelMixin
from app.controllers.queue_mixin import QueueMixin
from app.controllers.printer_mixin import PrinterMixin
from app.controllers.backup_mixin import BackupMixin
from app.controllers.settings_mixin import SettingsMixin


class AppController(NavigationMixin, ExcelMixin, QueueMixin, PrinterMixin, BackupMixin, SettingsMixin):
    def __init__(self, config_service, queue_service):
        self.config_service = config_service
        self.queue_service = queue_service
        self.view = None

        config = config_service.config
        self.excel_path = config.get("last_file")
        self.linha_atual = config.get("last_line", 2)
        self.backup_dir = config_service.get_backup_dir()
        saved_theme = config.get("theme_name", "Padrão (Azul Tech)")
        self.tema_atual = saved_theme if saved_theme in THEMES else "Padrão (Azul Tech)"
        self.idioma = config.get("language", "pt")
        if self.idioma not in TEXTS:
            self.idioma = "pt"
        self.escala_ui = config.get("ui_scale", 1.0)
        self.print_cfg = config.get("print_config", {
            "width": 45.0, "height": 15.0, "margin_x": 2.5,
            "gap": 0.3, "offset_x": 0.0, "offset_y": 0.0
        })
        self.target_printer = config.get("target_printer", "")
        self.direct_print_mode = config.get("direct_print", False)

        self.wb = None
        self.ws = None
        self.dado = None

        ctk.set_widget_scaling(self.escala_ui)

    def set_view(self, view):
        self.view = view
        self._initialize_view()

    def _initialize_view(self):
        config_page = self.view.pages["Config"]
        config_page.set_language(self.idioma)
        config_page.set_theme(self.tema_atual)
        config_page.set_scale(self.escala_ui)
        config_page.set_backup_path(self.backup_dir)
        config_page.set_print_cfg(self.print_cfg)
        config_page.set_direct_mode(self.direct_print_mode)
        config_page.set_printers(self._listar_impressoras(), self.target_printer)

        if self.excel_path and os.path.exists(self.excel_path):
            self._abrir_planilha()
        else:
            self.view.set_status("Aguardando arquivo...")

        self.view.show_page("Gerador")
        self.view.apply_theme(self.tema_atual)
        self.view.update_texts(TEXTS[self.idioma])

    def get_tema_atual(self):
        return self.tema_atual