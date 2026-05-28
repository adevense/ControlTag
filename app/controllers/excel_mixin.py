import os
import shutil
from app.core import excel, rendering
from app.config.translations import TEXTS


class ExcelMixin:
    def _abrir_planilha(self):
        self.wb, self.ws = excel.abrir_planilha_inicial(self.excel_path)
        if self.ws:
            self._atualizar_dados()
            self.carregar_dados_tabela()
            self.view.set_status("File Loaded")

    def _atualizar_dados(self):
        if self.ws is None:
            return
        page = self.view.pages["Gerador"]
        self.dado = excel.atualizar_dados(
            self.ws, self.linha_atual,
            lbl_desc=page.lbl_desc,
            entry_id=page.entry_id,
            renderizar_imagem=lambda v: rendering.renderizar_imagem(v, titulo=self.titulo_etiqueta),
            img_label=page.img_label
        )

    def importar_arquivo(self):
        p = excel.selecionar_arquivo_inicial()
        if p:
            self.excel_path = p
            self.linha_atual = 2
            self.salvar_config()
            self._abrir_planilha()

    def salvar_edicao(self):
        if self.ws is None or not self.excel_path:
            return
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        try:
            shutil.copy2(self.excel_path, os.path.join(self.backup_dir, "autobackup.xlsx"))
        except Exception:
            pass
        novo = self.view.pages["Gerador"].entry_id.get()
        self.ws[f"A{self.linha_atual}"] = novo
        self.wb.save(self.excel_path)
        self._atualizar_dados()
        self.carregar_dados_tabela()
        self.view.set_status(TEXTS[self.idioma]["msg"][1])

    def carregar_dados_tabela(self):
        if self.ws is None:
            return
        rows = [
            (r[0].row, r[0].value, r[1].value, r[2].value)
            for r in self.ws.iter_rows(min_row=2, max_row=5000, values_only=False)
            if r[0].value
        ]
        self.view.pages["Tabela"].populate(rows)

    def selecionar_na_tabela(self, event):
        page = self.view.pages["Tabela"]
        selection = page.tree.selection()
        if not selection:
            return
        self.linha_atual = int(page.tree.item(selection[0], "values")[0])
        self._atualizar_dados()
        self.view.show_page("Gerador")
