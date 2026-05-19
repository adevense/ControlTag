import customtkinter as ctk
from PIL import Image
import os
from app.core.utils import resource_path
from app.config.themes import THEMES


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, controller, navigate_callback):
        super().__init__(parent, width=280, corner_radius=0)
        self.controller = controller
        self.navigate = navigate_callback
        self.grid_rowconfigure(6, weight=1)
        self._build()

    def _build(self):
        self._build_logo()

        self.lbl_version = ctk.CTkLabel(self, text="v1.0", font=("Arial", 12))
        self.lbl_version.pack(pady=(0, 30))

        self.btn_nav = {
            "Gerador": self._nav_btn("...", "Gerador"),
            "Tabela":  self._nav_btn("...", "Tabela"),
            "Fila":    self._nav_btn("...", "Fila"),
            "Config":  self._nav_btn("...", "Config"),
        }

        ctk.CTkFrame(self, height=1, fg_color="gray").pack(side="bottom", fill="x", padx=20, pady=5)
        self.lbl_credits = ctk.CTkLabel(self, text="Dev. Inácio Ribeiro Azevedo", font=("Arial", 10), text_color="gray")
        self.lbl_credits.pack(side="bottom", pady=(0, 15))

        self.status_bar = ctk.CTkLabel(self, text="System Ready", font=("Arial", 11, "italic"), text_color="gray")
        self.status_bar.pack(side="bottom", pady=(5, 10))

    def _build_logo(self):
        img_path = resource_path(os.path.join("resources", "logo.png"))
        if os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                self.logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(160, 160))
                self.lbl_logo = ctk.CTkLabel(self, text="", image=self.logo_image)
                self.lbl_logo.pack(pady=(40, 5))
                return
            except Exception:
                pass
        self.lbl_logo = ctk.CTkLabel(self, text="CONTROL\nTAG BDGC", font=("Impact", 32))
        self.lbl_logo.pack(pady=(40, 5))

    def _nav_btn(self, text, page_name):
        btn = ctk.CTkButton(
            self, text=text, height=50, corner_radius=8,
            fg_color="transparent", anchor="w", font=("Arial", 15, "bold"),
            command=lambda: self.navigate(page_name)
        )
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def set_status(self, msg):
        self.status_bar.configure(text=msg)

    def apply_theme(self, theme_name):
        t = THEMES.get(theme_name, THEMES["Padrão (Azul Tech)"])
        self.configure(fg_color=t["sidebar"])
        if isinstance(self.lbl_logo, ctk.CTkLabel) and not hasattr(self, 'logo_image'):
            self.lbl_logo.configure(text_color=t["primary"])
        for btn in self.btn_nav.values():
            btn.configure(text_color=t.get("text_menu", "white"))

    def update_texts(self, nav_texts, credits_text, current_path_text):
        pages = ["Gerador", "Tabela", "Fila", "Config"]
        for page, text in zip(pages, nav_texts):
            self.btn_nav[page].configure(text=text)
        self.lbl_credits.configure(text=credits_text)
        self.lbl_path_backup_title_text = current_path_text
