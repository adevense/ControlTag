import unittest
from unittest import mock
import os
from app.core import backup

class TestBackup(unittest.TestCase):
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('os.remove', side_effect=Exception('fail'))
    @mock.patch('os.listdir', return_value=['a.xlsx'])
    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('tkinter.messagebox.askyesno', return_value=True)
    def test_limpar_backups_error(self, mock_askyesno, mock_exists, mock_listdir, mock_remove, mock_showerror):
        TEXTS = {'pt': {'msg': ['']*9}}
        backup.limpar_backups('dir', 'pt', TEXTS)
        mock_showerror.assert_called()

    @mock.patch('os.startfile')
    @mock.patch('os.path.exists', return_value=True)
    def test_abrir_pasta_dados_exists(self, mock_exists, mock_startfile):
        backup.abrir_pasta_dados('some_dir')
        mock_startfile.assert_called_once_with('some_dir')

    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('os.path.exists', return_value=False)
    def test_abrir_pasta_dados_not_exists(self, mock_exists, mock_showerror):
        backup.abrir_pasta_dados('some_dir')
        mock_showerror.assert_called_once()

    @mock.patch('tkinter.filedialog.askdirectory', return_value='chosen_dir')
    def test_selecionar_pasta_backup(self, mock_askdirectory):
        called = {}
        def cb(path): called['p'] = path
        result = backup.selecionar_pasta_backup('current', filedialog=mock.Mock(askdirectory=mock_askdirectory), update_callback=cb)
        self.assertEqual(result, 'chosen_dir')
        self.assertEqual(called['p'], 'chosen_dir')

    @mock.patch('tkinter.filedialog.askdirectory', return_value='')
    def test_selecionar_pasta_backup_cancel(self, mock_askdirectory):
        result = backup.selecionar_pasta_backup('current', filedialog=mock.Mock(askdirectory=mock_askdirectory))
        self.assertIsNone(result)

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('os.remove')
    @mock.patch('os.listdir', return_value=['a.xlsx', 'Backup_1.xlsx', 'b.txt'])
    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('tkinter.messagebox.askyesno', return_value=True)
    def test_limpar_backups(self, mock_askyesno, mock_exists, mock_listdir, mock_remove, mock_showerror, mock_showinfo):
        msgs = []
        TEXTS = {'pt': {'msg': ['']*9}}
        TEXTS['pt']['msg'][8] = 'Backups apagados!'
        def status_msg(msg): msgs.append(msg)
        backup.limpar_backups('dir', 'pt', TEXTS, status_msg)
        mock_remove.assert_any_call(os.path.join('dir', 'a.xlsx'))
        mock_remove.assert_any_call(os.path.join('dir', 'Backup_1.xlsx'))
        self.assertIn('Backups apagados!', msgs)
        mock_showinfo.assert_called()

    @mock.patch('tkinter.messagebox.showwarning')
    @mock.patch('os.path.exists', return_value=False)
    def test_fazer_backup_manual_no_excel(self, mock_exists, mock_warning):
        backup.fazer_backup_manual('file.xlsx', 'dir')
        mock_warning.assert_called()

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('shutil.copy2')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists', side_effect=[True, False])
    def test_fazer_backup_manual_success(self, mock_exists, mock_makedirs, mock_copy2, mock_showinfo):
        backup.fazer_backup_manual('file.xlsx', 'dir')
        mock_makedirs.assert_called_with('dir')
        mock_copy2.assert_called()
        mock_showinfo.assert_called()

    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('shutil.copy2', side_effect=Exception('fail'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists', side_effect=[True, False])
    def test_fazer_backup_manual_error(self, mock_exists, mock_makedirs, mock_copy2, mock_showerror):
        backup.fazer_backup_manual('file.xlsx', 'dir')
        mock_showerror.assert_called()

if __name__ == '__main__':
    unittest.main()
