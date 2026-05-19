import customtkinter as ctk


class FilaPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._build()

    def _build(self):
        self.lbl_queue_count = ctk.CTkLabel(self, text="0", font=("Arial", 20))
        self.lbl_queue_count.pack(pady=20)

        self.lista_fila = ctk.CTkTextbox(self, width=700, height=400, font=("Consolas", 14))
        self.lista_fila.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.btn_clear = ctk.CTkButton(btn_frame, text="Clear", fg_color="red", command=self.controller.limpar_fila)
        self.btn_clear.pack(side="left", padx=10)

        self.btn_print_queue = ctk.CTkButton(btn_frame, text="Print Queue", width=200, command=self.controller.gerar_pdf_fila)
        self.btn_print_queue.pack(side="left", padx=10)

    def add_item(self, text):
        self.lista_fila.insert("end", f"▶ {text}\n")

    def clear_list(self):
        self.lista_fila.delete("1.0", "end")

    def set_count(self, count):
        self.lbl_queue_count.configure(text=str(count))

    def update_texts(self, t):
        self.btn_clear.configure(text=t.get("clear", "Clear"))
        self.btn_print_queue.configure(text=t.get("print_queue", "Print Queue"))
