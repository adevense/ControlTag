from tkinter import messagebox


class NavigationMixin:
    def _ultima_linha(self):
        if self.ws is None:
            return 2
        for i in range(self.ws.max_row, 1, -1):
            if self.ws[f"A{i}"].value:
                return i
        return 2

    def proximo(self):
        if self.ws is None:
            return
        if self.linha_atual < self._ultima_linha():
            self.linha_atual += 1
            self._atualizar_dados()

    def anterior(self):
        if self.linha_atual > 2:
            self.linha_atual -= 1
            self._atualizar_dados()

    def buscar_patrimonio(self):
        if self.ws is None:
            return
        entry = self.view.pages["Gerador"].entry_busca
        termo = entry.get().strip()
        for i in range(2, self.ws.max_row + 1):
            if str(self.ws[f"A{i}"].value).strip() == termo:
                self.linha_atual = i
                self._atualizar_dados()
                entry.delete(0, "end")  
                return
        messagebox.showwarning("Busca", "404")
        entry.delete(0, "end")
