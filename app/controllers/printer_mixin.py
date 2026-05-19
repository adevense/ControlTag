try:
    import win32print
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


class PrinterMixin:
    def _listar_impressoras(self):
        if not HAS_WIN32:
            return ["PyWin32 não instalado"]
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            return [p[2] for p in printers]
        except Exception as e:
            return [f"Erro: {str(e)}"]

    def selecionar_impressora(self, p_name):
        self.target_printer = p_name
        self.salvar_config()

    def toggle_impressao_direta(self):
        self.direct_print_mode = bool(self.view.pages["Config"].switch_direct.get())
        self.salvar_config()
