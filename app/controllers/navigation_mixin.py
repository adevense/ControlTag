from tkinter import messagebox


class NavigationMixin:
    def proximo(self):
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
