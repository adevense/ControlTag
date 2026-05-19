import customtkinter as ctk
from tkinter import messagebox
from app.config.translations import TEXTS


class SettingsMixin:
    def salvar_cfg_impressao(self):
        try:
            raw = self.view.pages["Config"].get_print_cfg()
            for k, v in raw.items():
                self.print_cfg[k] = float(v.replace(",", "."))
            self.salvar_config()
            self.view.set_status(TEXTS[self.idioma]["msg"][1])
        except (ValueError, AttributeError):
            messagebox.showerror("Erro", "Números inválidos")

    def reset_print_cfg(self):
        defaults = {
            "width": 45.0, "height": 15.0, "margin_x": 2.5,
            "gap": 0.3, "offset_x": 0.0, "offset_y": 0.0
        }
        self.print_cfg = defaults
        self.view.pages["Config"].set_print_cfg(defaults)
        self.salvar_config()

    def mudar_tema(self, tema_nome):
        self.tema_atual = tema_nome
        self.view.apply_theme(tema_nome)
        self.salvar_config()

    def mudar_escala(self, v):
        self.escala_ui = v
        ctk.set_widget_scaling(v)
        self.salvar_config()

    def mudar_idioma(self, novo_lang):
        self.idioma = novo_lang
        self.view.update_texts(TEXTS[self.idioma])
        self.salvar_config()
        self.view.set_status(f"Language: {novo_lang.upper()}")

    def salvar_config(self):
        self.config_service.save_all({
            "last_file": self.excel_path,
            "last_line": self.linha_atual,
            "theme_name": self.tema_atual,
            "language": self.idioma,
            "ui_scale": self.escala_ui,
            "print_config": self.print_cfg,
            "target_printer": self.target_printer,
            "direct_print": self.direct_print_mode,
            "backup_path": self.backup_dir,
        })

    def _texts(self):
        return TEXTS
