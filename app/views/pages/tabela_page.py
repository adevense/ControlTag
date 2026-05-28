import customtkinter as ctk
from tkinter import ttk


class TabelaPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._build()

    def _build(self):
        frame_tree = ctk.CTkFrame(self)
        frame_tree.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Linha", "Patrimônio", "Descrição", "Setor")
        self.tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
        self.tree.column("Linha", width=50)
        self.tree.column("Patrimônio", width=150)
        self.tree.column("Descrição", width=400)
        self.tree.column("Setor", width=200)

        for col in cols:
            self.tree.heading(col, text=col)

        sb = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.controller.selecionar_na_tabela)

        self.btn_refresh = ctk.CTkButton(self, text="Refresh", command=self.controller.carregar_dados_tabela)
        self.btn_refresh.pack(pady=10)

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=row)

    def update_texts(self, t):
        self.btn_refresh.configure(text=t.get("refresh", "Refresh"))
