import tkinter as tk
import customtkinter as ctk


class GeradorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._build()


    def _force_focus_search_entry(self, event):
        widget = self.focus_get()
        if not isinstance(widget, (ctk.CTkEntry, tk.Entry)):
            self.entry_busca.focus_set()

    def _build(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self._build_preview_panel()
        self._build_controls_panel()

    def _build_preview_panel(self):
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.lbl_preview_title = ctk.CTkLabel(left, text="Preview", font=("Arial", 12, "bold"))
        self.lbl_preview_title.pack(anchor="w")

        preview_frame = ctk.CTkFrame(left, fg_color="white", height=250)
        preview_frame.pack(fill="x", pady=5)
        preview_frame.pack_propagate(False)
        self.img_label = tk.Label(preview_frame, bg="white")
        self.img_label.pack(expand=True, fill="both")

        card = ctk.CTkFrame(left)
        card.pack(fill="both", expand=True, pady=20)

        self.lbl_desc_title = ctk.CTkLabel(card, text="Description", font=("Arial", 16, "bold"))
        self.lbl_desc_title.pack(pady=10)
        self.lbl_desc = ctk.CTkLabel(card, text="--", font=("Arial", 20), wraplength=500)
        self.lbl_desc.pack(pady=5)

        nav = ctk.CTkFrame(card, fg_color="transparent")
        nav.pack(side="bottom", pady=30)

        self.btn_ant = ctk.CTkButton(nav, text="<", width=120, height=45, command=self.controller.anterior)
        self.btn_ant.pack(side="left", padx=15)

        self.entry_id = ctk.CTkEntry(nav, width=200, height=45, font=("Arial", 22, "bold"), justify="center")
        self.entry_id.pack(side="left", padx=10)

        self.btn_prox = ctk.CTkButton(nav, text=">", width=120, height=45, command=self.controller.proximo)
        self.btn_prox.pack(side="left", padx=15)

        self.btn_save = ctk.CTkButton(nav, text="Save", width=80, fg_color="#555", command=self.controller.salvar_edicao)
        self.btn_save.pack(side="bottom", pady=5)

    def _build_controls_panel(self):
        right = ctk.CTkFrame(self)
        right.grid(row=0, column=1, sticky="nsew")

        self.lbl_controls_title = ctk.CTkLabel(right, text="Controls", font=("Arial", 18, "bold"))
        self.lbl_controls_title.pack(pady=20)

        self.entry_busca = ctk.CTkEntry(right, placeholder_text="...")
        self.entry_busca.pack(fill="x", padx=20, pady=(0, 5))
        self.entry_busca.bind('<Return>', lambda e: self.controller.buscar_patrimonio())

        self.btn_buscar = ctk.CTkButton(right, text="Search", command=self.controller.buscar_patrimonio)
        self.btn_buscar.pack(fill="x", padx=20, pady=(0, 30))

        self.btn_add = ctk.CTkButton(right, text="Add Queue", height=50, command=self.controller.add_fila)
        self.btn_add.pack(fill="x", padx=20, pady=10)

        self.btn_pdf_unico = ctk.CTkButton(right, text="PDF Single", fg_color="#444", command=self.controller.exportar_pdf_unico)
        self.btn_pdf_unico.pack(fill="x", padx=20, pady=10)

        ctk.CTkFrame(right, height=2, fg_color="gray").pack(fill="x", padx=20, pady=20)

        self.lbl_batch_title = ctk.CTkLabel(right, text="Batch", font=("Arial", 14))
        self.lbl_batch_title.pack()

        self.batch_start = ctk.CTkEntry(right, justify="center")
        self.batch_start.pack(pady=5)

        self.batch_end = ctk.CTkEntry(right, justify="center")
        self.batch_end.pack(pady=5)

        self.btn_lote = ctk.CTkButton(right, text="Batch", fg_color="#c0392b", command=self.controller.gerar_lote_intervalo)
        self.btn_lote.pack(fill="x", padx=20, pady=10)

    def focus_search_entry(self):
        self.entry_busca.focus_set()

    def apply_theme(self, theme):
        for btn in [self.btn_ant, self.btn_prox, self.btn_buscar, self.btn_add, self.btn_lote]:
            btn.configure(fg_color=theme["primary"], hover_color=theme.get("hover", theme["primary"]))

    def update_texts(self, t):
        self.lbl_preview_title.configure(text=t["ui"][0])
        self.lbl_desc_title.configure(text=t["ui"][1])
        self.lbl_controls_title.configure(text=t["ui"][2])
        self.btn_ant.configure(text=t["ui"][3])
        self.btn_prox.configure(text=t["ui"][4])
        self.btn_save.configure(text=t["ui"][5])
        self.entry_busca.configure(placeholder_text=t["actions"][0])
        self.btn_buscar.configure(text=t["actions"][1])
        self.btn_add.configure(text=t["actions"][2])
        self.btn_pdf_unico.configure(text=t["actions"][3])
        self.batch_start.configure(placeholder_text=t["actions"][4])
        self.batch_end.configure(placeholder_text=t["actions"][5])
        self.btn_lote.configure(text=t["actions"][6])
