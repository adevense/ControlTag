import os
from tkinter import filedialog
from app.core import printing, rendering


class QueueMixin:
    def add_fila(self):
        if self.dado is None:
            return
        item = {"linha": self.linha_atual, "id": self.dado}
        if self.queue_service.add_to_queue(item):
            fila_page = self.view.pages["Fila"]
            fila_page.add_item(item["id"])
            fila_page.set_count(self.queue_service.queue_count())

    def limpar_fila(self):
        self.queue_service.clear_queue()
        fila_page = self.view.pages["Fila"]
        fila_page.clear_list()
        fila_page.set_count(0)

    def gerar_pdf_fila(self):
        fila = self.queue_service.get_queue()
        if not fila:
            return
        if self.direct_print_mode:
            self._gerar_pdf(fila, os.path.join(os.environ["TEMP"], "fila_temp.pdf"))
        else:
            p = filedialog.asksaveasfilename(defaultextension=".pdf")
            if p:
                self._gerar_pdf(fila, p)

    def exportar_pdf_unico(self):
        if self.dado is None:
            return
        items = [{"linha": self.linha_atual, "id": self.dado}]
        if self.direct_print_mode:
            self._gerar_pdf(items, os.path.join(os.environ["TEMP"], f"temp_{self.dado}.pdf"))
        else:
            self._gerar_pdf(items, f"Tag_{self.dado}.pdf")

    def gerar_lote_intervalo(self):
        if self.ws is None:
            return
        page = self.view.pages["Gerador"]
        try:
            start = int(page.batch_start.get())
            end = int(page.batch_end.get())
            lista = [
                {"linha": r, "id": str(self.ws[f"A{r}"].value)}
                for r in range(start, end + 1)
                if self.ws[f"A{r}"].value
            ]
            if self.direct_print_mode:
                self._gerar_pdf(lista, os.path.join(os.environ["TEMP"], "lote_temp.pdf"))
            else:
                p = filedialog.asksaveasfilename(defaultextension=".pdf")
                if p:
                    self._gerar_pdf(lista, p)
        except (ValueError, TypeError):
            from tkinter import messagebox
            messagebox.showerror("Erro", "Intervalo Inválido")

    def _gerar_pdf(self, lista_dicts, filepath):
        printing.gerar_pdf_generico(
            lista_dicts, filepath, self.print_cfg,
            rendering.renderizar_imagem,
            lambda f: printing.enviar_arquivo_para_impressora(f, self.direct_print_mode, self.target_printer)
        )
