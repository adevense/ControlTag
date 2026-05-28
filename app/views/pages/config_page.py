import customtkinter as ctk
from app.config.themes import THEMES


DEFAULT_PRINT_CFG = {
    "width": 45.0, "height": 15.0, "margin_x": 2.5,
    "gap": 0.3, "offset_x": 0.0, "offset_y": 0.0
}
PRINT_CFG_KEYS = ["width", "height", "margin_x", "gap", "offset_x", "offset_y"]


class ConfigPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._build()

    def _build(self):
        self.tabview = ctk.CTkTabview(self, width=800, height=600)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        self._build_tab_geral(self.tabview.add("Geral"))
        self._build_tab_visual(self.tabview.add("Aparência"))
        self._build_tab_impressao(self.tabview.add("Impressão"))

    def _build_tab_geral(self, tab):
        self.lbl_conf_lang = ctk.CTkLabel(tab, text="Language", font=("Arial", 14, "bold"))
        self.lbl_conf_lang.pack(pady=(15, 5))
        self.combo_lang = ctk.CTkOptionMenu(tab, values=["pt", "en", "es"], command=self.controller.mudar_idioma)
        self.combo_lang.pack(pady=5)

        self.lbl_conf_file = ctk.CTkLabel(tab, text="File", font=("Arial", 14, "bold"))
        self.lbl_conf_file.pack(pady=(15, 5))
        self.btn_file = ctk.CTkButton(tab, text="Select File", command=self.controller.importar_arquivo)
        self.btn_file.pack(pady=5)

        self.lbl_conf_titulo = ctk.CTkLabel(tab, text="Título da Etiqueta", font=("Arial", 14, "bold"))
        self.lbl_conf_titulo.pack(pady=(15, 5))
        frame_titulo = ctk.CTkFrame(tab, fg_color="transparent")
        frame_titulo.pack(fill="x", padx=20, pady=(0, 5))
        self.entry_titulo = ctk.CTkEntry(frame_titulo, placeholder_text="ControlTag", justify="center", width=200)
        self.entry_titulo.pack(padx=(0, 5))
        self.btn_save_titulo = ctk.CTkButton(frame_titulo, text="Salvar", width=80, command=self.controller.mudar_titulo_etiqueta)
        self.btn_save_titulo.pack(pady=5)

        self.lbl_conf_extra = ctk.CTkLabel(tab, text="Backup", font=("Arial", 14, "bold"))
        self.lbl_conf_extra.pack(pady=(20, 5))

        self.lbl_path_backup_title = ctk.CTkLabel(tab, text="Pasta Atual:", font=("Arial", 10))
        self.lbl_path_backup_title.pack()
        self.lbl_path_backup_val = ctk.CTkLabel(tab, text="", font=("Arial", 10, "italic"), text_color="gray")
        self.lbl_path_backup_val.pack(pady=2)

        frame_bkp = ctk.CTkFrame(tab, fg_color="transparent")
        frame_bkp.pack(pady=10)

        self.btn_change_bkp = ctk.CTkButton(frame_bkp, text="Mudar Pasta", width=140, fg_color="#555", command=self.controller.selecionar_pasta_backup)
        self.btn_change_bkp.grid(row=0, column=0, padx=5, pady=5)
        self.btn_backup = ctk.CTkButton(frame_bkp, text="Fazer Backup", width=140, fg_color="green", command=self.controller.fazer_backup_manual)
        self.btn_backup.grid(row=0, column=1, padx=5, pady=5)
        self.btn_open_folder = ctk.CTkButton(frame_bkp, text="Abrir Pasta", width=140, fg_color="#333", command=self.controller.abrir_pasta_dados)
        self.btn_open_folder.grid(row=1, column=0, padx=5, pady=5)
        self.btn_clear_bkp = ctk.CTkButton(frame_bkp, text="Limpar Backups", width=140, fg_color="#c0392b", hover_color="#922b21", command=self.controller.limpar_backups)
        self.btn_clear_bkp.grid(row=1, column=1, padx=5, pady=5)

    def _build_tab_visual(self, tab):
        self.lbl_conf_theme = ctk.CTkLabel(tab, text="Theme", font=("Arial", 14, "bold"))
        self.lbl_conf_theme.pack(pady=(20, 5))
        self.combo_tema = ctk.CTkOptionMenu(tab, values=list(THEMES.keys()), command=self.controller.mudar_tema)
        self.combo_tema.pack(pady=5)

        self.lbl_conf_scale = ctk.CTkLabel(tab, text="Scale", font=("Arial", 14, "bold"))
        self.lbl_conf_scale.pack(pady=(20, 5))
        self.slider = ctk.CTkSlider(tab, from_=0.8, to=1.4, command=self.controller.mudar_escala)
        self.slider.pack(pady=5)

    def _build_tab_impressao(self, tab):
        frame_hardware = ctk.CTkFrame(tab, fg_color="transparent")
        frame_hardware.pack(fill="x", padx=20, pady=(20, 10))

        self.lbl_sel_print = ctk.CTkLabel(frame_hardware, text="Selecionar Impressora", font=("Arial", 12, "bold"))
        self.lbl_sel_print.pack(anchor="w")

        self.combo_printer = ctk.CTkOptionMenu(frame_hardware, values=[""], command=self.controller.selecionar_impressora)
        self.combo_printer.pack(fill="x", pady=5)

        self.switch_direct = ctk.CTkSwitch(frame_hardware, text="Modo Direto", command=self.controller.toggle_impressao_direta)
        self.switch_direct.pack(pady=10, anchor="w")

        ctk.CTkLabel(tab, text="--------------------------------").pack()
        ctk.CTkLabel(tab, text="Ajuste Dimensional (mm)", text_color="orange").pack(pady=10)

        self.entries_print = {}
        grid_frame = ctk.CTkFrame(tab, fg_color="transparent")
        grid_frame.pack(pady=10)

        for i, k in enumerate(PRINT_CFG_KEYS):
            lbl = ctk.CTkLabel(grid_frame, text=k)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(grid_frame, width=80, justify="center")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_print[k] = (lbl, entry)

        self.btn_save_print = ctk.CTkButton(tab, text="💾 Salvar Config", command=self.controller.salvar_cfg_impressao)
        self.btn_save_print.pack(pady=20)

        self.btn_reset_print = ctk.CTkButton(tab, text="Reset Defaults", fg_color="#444", width=100, command=self.controller.reset_print_cfg)
        self.btn_reset_print.pack()

    # =====================
    # MÉTODOS PÚBLICOS
    # =====================
    def set_language(self, lang):
        self.combo_lang.set(lang)

    def set_theme(self, theme_name):
        self.combo_tema.set(theme_name)

    def set_scale(self, scale):
        self.slider.set(scale)

    def set_titulo_etiqueta(self, titulo):
        self.entry_titulo.delete(0, "end")
        self.entry_titulo.insert(0, titulo)

    def get_titulo_etiqueta(self):
        return self.entry_titulo.get()

    def set_backup_path(self, path):
        self.lbl_path_backup_val.configure(text=path)

    def set_printers(self, printers, selected):
        self.combo_printer.configure(values=printers)
        self.combo_printer.set(selected if selected in printers else "Selecione...")

    def set_direct_mode(self, enabled):
        if enabled:
            self.switch_direct.select()
        else:
            self.switch_direct.deselect()

    def set_print_cfg(self, cfg):
        for k, (_, entry) in self.entries_print.items():
            entry.delete(0, "end")
            entry.insert(0, str(cfg.get(k, "")))

    def get_print_cfg(self):
        result = {}
        for k, (_, entry) in self.entries_print.items():
            result[k] = entry.get()
        return result

    def update_texts(self, t):
        self.tabview._segmented_button.configure(values=t["tabs"])
        self.lbl_conf_lang.configure(text=t["lbls"][0])
        self.lbl_conf_theme.configure(text=t["lbls"][1])
        self.lbl_conf_scale.configure(text=t["lbls"][2])
        self.lbl_conf_file.configure(text=t["lbls"][3])
        self.lbl_conf_extra.configure(text=t["lbls"][4])
        self.lbl_sel_print.configure(text=t["lbls"][5])
        self.switch_direct.configure(text=t["lbls"][6])
        self.lbl_path_backup_title.configure(text=t["lbls"][7])
        self.btn_reset_print.configure(text=t["msg"][6])
        self.btn_change_bkp.configure(text=t["btns"][0])
        self.btn_clear_bkp.configure(text=t["btns"][1])
        self.btn_backup.configure(text=t["btns"][2])
        self.btn_open_folder.configure(text=t["btns"][3])
        for k, txt in zip(PRINT_CFG_KEYS, t["print_cfg"]):
            self.entries_print[k][0].configure(text=txt)
