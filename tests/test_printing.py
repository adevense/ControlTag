import sys
import unittest
from unittest.mock import MagicMock, patch
from app.core import printing

class TestPrintingModule(unittest.TestCase):

    def test_importerror_win32api(self):
        """Testa o except ImportError para cobertura de HAS_WIN32 = False."""
        module_name = "app.core.printing"
        # Remove o módulo do cache para forçar reload
        if module_name in sys.modules:
            del sys.modules[module_name]
        with unittest.mock.patch.dict("sys.modules", {"win32api": None}):
            import app.core.printing as printing_reload
            self.assertFalse(printing_reload.HAS_WIN32)

    @patch("os.startfile")
    def test_enviar_arquivo_para_impressora_sem_win32(self, mock_startfile):
        printing.enviar_arquivo_para_impressora("dummy.pdf", False, None)
        mock_startfile.assert_called_once_with("dummy.pdf")

    @patch("os.startfile")
    @patch("tkinter.messagebox.showwarning")
    def test_enviar_arquivo_para_impressora_sem_impressora_valida(self, mock_warning, mock_startfile):
        printing.enviar_arquivo_para_impressora("dummy.pdf", True, "Erro")
        mock_warning.assert_called_once()
        mock_startfile.assert_called_once_with("dummy.pdf")

    @patch("os.startfile")
    @patch("win32api.ShellExecute")
    def test_enviar_arquivo_para_impressora_com_sucesso(self, mock_shellexecute, mock_startfile):
        printing.enviar_arquivo_para_impressora("dummy.pdf", True, "Printer_Name")
        mock_shellexecute.assert_called_once_with(0, "printto", "dummy.pdf", '"Printer_Name"', ".", 0)
        mock_startfile.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    @patch("win32api.ShellExecute", side_effect=Exception("Erro de impressão"))
    @patch("os.startfile")
    def test_enviar_arquivo_para_impressora_erro(self, mock_startfile, mock_shellexecute, mock_error):
        printing.enviar_arquivo_para_impressora("dummy.pdf", True, "Printer_Name")
        mock_error.assert_called_once()
        mock_startfile.assert_called_once_with("dummy.pdf")

    @patch("app.core.printing.canvas.Canvas")
    @patch("tkinter.messagebox.showerror")
    def test_gerar_pdf_generico_com_sucesso(self, mock_error, mock_canvas):
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        from PIL import Image
        pil_img = Image.new("RGB", (100, 50), color="white")
        mock_renderizar_imagem = MagicMock(return_value=pil_img)
        mock_enviar_para_impressora = MagicMock()

        lista_dicts = [{"id": "123"}]
        print_cfg = {
            "width": 45.0,
            "height": 15.0,
            "margin_x": 2.5,
            "gap": 0.3,
            "offset_x": 0.0,
            "offset_y": 0.0
        }

        printing.gerar_pdf_generico(lista_dicts, "dummy.pdf", print_cfg, mock_renderizar_imagem, mock_enviar_para_impressora)

        print("Mock renderizar_imagem configurado com retorno:", mock_renderizar_imagem.return_value)
        print("Dados de entrada para lista_dicts:", lista_dicts)
        print("Configuração de impressão:", print_cfg)
        print("Verificando chamadas ao canvas...")
        print(mock_canvas_instance.method_calls)

        mm_to_pt = 2.834645669291339
        expected_x = print_cfg["margin_x"] * mm_to_pt
        expected_y = print_cfg["offset_y"] * mm_to_pt
        expected_width = print_cfg["width"] * mm_to_pt
        expected_height = print_cfg["height"] * mm_to_pt

        from unittest.mock import ANY
        mock_canvas_instance.drawImage.assert_any_call(
            ANY, expected_x, expected_y, width=expected_width, height=expected_height
        )
        mock_canvas_instance.save.assert_called_once()
        mock_enviar_para_impressora.assert_called_once_with("dummy.pdf")
        mock_error.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    @patch("reportlab.pdfgen.canvas.Canvas", side_effect=Exception("Erro ao gerar PDF"))
    def test_gerar_pdf_generico_erro(self, mock_canvas, mock_error):
        mock_renderizar_imagem = MagicMock()
        mock_enviar_para_impressora = MagicMock()

        lista_dicts = [{"id": "123"}]
        print_cfg = {
            "width": 45.0,
            "height": 15.0,
            "margin_x": 2.5,
            "gap": 0.3,
            "offset_x": 0.0,
            "offset_y": 0.0
        }

        printing.gerar_pdf_generico(lista_dicts, "dummy.pdf", print_cfg, mock_renderizar_imagem, mock_enviar_para_impressora)

        mock_error.assert_called_once_with("Erro PDF", "Erro ao gerar PDF")
        mock_enviar_para_impressora.assert_not_called()

if __name__ == "__main__":
    unittest.main()