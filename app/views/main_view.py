import customtkinter as ctk
import os
from app.core.utils import resource_path
from app.config.themes import THEMES
from app.views.components.sidebar import Sidebar
from app.views.pages.gerador_page import GeradorPage
from app.views.pages.tabela_page import TabelaPage
from app.views.pages.fila_page import FilaPage
from app.views.pages.config_page import ConfigPage


class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Control Tag BDGC v1.0")
        self.geometry("1366x900")
        self._set_icon()
        self._build_layout()
        self._bind_keys()

    def _set_icon(self):
        icon_path = resource_path(os.path.join("resources", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self.controller, navigate_callback=self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        container = ctk.CTkFrame(self, corner_radius=0)
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {
            "Gerador": GeradorPage(container, self.controller),
            "Tabela":  TabelaPage(container, self.controller),
            "Fila":    FilaPage(container, self.controller),
            "Config":  ConfigPage(container, self.controller),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def _bind_keys(self):
        self.bind('<Left>',  lambda e: self.controller.anterior())
        self.bind('<Right>', lambda e: self.controller.proximo())
        self.bind('<Return>', lambda e: self.controller.buscar_patrimonio()
                  if self.focus_get() == self.pages["Gerador"].entry_busca else None)

    def show_page(self, name):
        self.pages[name].tkraise()
        self.sidebar.apply_theme(self.controller.get_tema_atual())

    def set_status(self, msg):
        self.sidebar.set_status(msg)
        self.update_idletasks()

    def apply_theme(self, theme_name):
        t = THEMES.get(theme_name, THEMES["Padrão (Azul Tech)"])
        ctk.set_appearance_mode(t["mode"])
        self.sidebar.apply_theme(theme_name)
        self.pages["Gerador"].apply_theme(t)

    def update_texts(self, t):
        self.sidebar.update_texts(t["nav"], t["credits"], t["lbls"][7])
        self.pages["Gerador"].update_texts(t)
        self.pages["Config"].update_texts(t)
