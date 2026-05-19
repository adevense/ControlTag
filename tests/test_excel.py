import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import excel

class TestExcelModule(unittest.TestCase):
    @patch('core.excel.os.path.exists', return_value=True)
    @patch('core.excel.load_workbook')
    def test_abrir_planilha_inicial_sucesso(self, mock_load, mock_exists):
        wb_mock = MagicMock()
        ws_mock = MagicMock()
        wb_mock.active = ws_mock
        mock_load.return_value = wb_mock
        wb, ws = excel.abrir_planilha_inicial('dummy.xlsx')
        self.assertEqual(wb, wb_mock)
        self.assertEqual(ws, ws_mock)

    @patch('core.excel.os.path.exists', return_value=False)
    @patch('core.excel.messagebox.showerror')
    def test_abrir_planilha_inicial_arquivo_nao_encontrado(self, mock_msg, mock_exists):
        wb, ws = excel.abrir_planilha_inicial('inexistente.xlsx')
        mock_msg.assert_called_once()
        self.assertIsNone(wb)
        self.assertIsNone(ws)

    @patch('core.excel.os.path.exists', return_value=True)
    @patch('core.excel.load_workbook', side_effect=Exception('erro'))
    @patch('core.excel.messagebox.showerror')
    def test_abrir_planilha_inicial_erro_ao_abrir(self, mock_msg, mock_load, mock_exists):
        wb, ws = excel.abrir_planilha_inicial('erro.xlsx')
        mock_msg.assert_called_once()
        self.assertIsNone(wb)
        self.assertIsNone(ws)

    @patch('core.excel.filedialog.askopenfilename', return_value='arquivo.xlsx')
    def test_selecionar_arquivo_inicial_sucesso(self, mock_dialog):
        result = excel.selecionar_arquivo_inicial()
        self.assertEqual(result, 'arquivo.xlsx')

    @patch('core.excel.filedialog.askopenfilename', return_value='')
    def test_selecionar_arquivo_inicial_cancelado(self, mock_dialog):
        result = excel.selecionar_arquivo_inicial()
        self.assertIsNone(result)

    @patch('core.excel.selecionar_arquivo_inicial', return_value='importado.xlsx')
    def test_importar_arquivo(self, mock_sel):
        result = excel.importar_arquivo()
        self.assertEqual(result, 'importado.xlsx')

    def test_atualizar_dados_basico(self):
        ws = MagicMock()
        ws.__getitem__.side_effect = lambda k: MagicMock(value={'A2': 'VAL', 'B2': 'DESC', 'C2': 'SETOR'}.get(k, None))
        dado = excel.atualizar_dados(ws, 2)
        self.assertEqual(dado, 'VAL')

    @patch('PIL.ImageTk.PhotoImage')
    def test_atualizar_dados_interface(self, mock_imgtk):
        ws = MagicMock()
        ws.__getitem__.side_effect = lambda k: MagicMock(value={'A3': 'VAL2', 'B3': 'DESC2', 'C3': 'SETOR2'}.get(k, None))
        lbl_desc = MagicMock()
        entry_id = MagicMock()
        renderizar_imagem = MagicMock()
        img_label = MagicMock()
        mock_imgtk.return_value = 'imgtk'
        dado = excel.atualizar_dados(ws, 3, lbl_desc, entry_id, renderizar_imagem, img_label)
        lbl_desc.configure.assert_called_once_with(text='DESC2\nSETOR2')
        entry_id.delete.assert_called_once_with(0, 'end')
        entry_id.insert.assert_called_once_with(0, 'VAL2')
        renderizar_imagem.assert_called_once_with('VAL2')
        img_label.configure.assert_called_once_with(image='imgtk')
        self.assertEqual(img_label.image, 'imgtk')
        self.assertEqual(dado, 'VAL2')

    def test_atualizar_dados_ws_none(self):
        dado = excel.atualizar_dados(None, 1)
        self.assertEqual(dado, "")

if __name__ == '__main__':
    unittest.main()
