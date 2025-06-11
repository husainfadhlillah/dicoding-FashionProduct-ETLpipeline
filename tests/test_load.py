# tests/test_load.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_gsheets, save_to_postgresql

class TestLoad(unittest.TestCase):

    def setUp(self):
        """Menyiapkan data bersih untuk pengujian."""
        self.clean_df = pd.DataFrame({'Title': ['Test'], 'Price': [160000]})

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        """Tes penyimpanan ke CSV."""
        save_to_csv(self.clean_df, 'test.csv')
        # Pastikan fungsi to_csv dipanggil sekali dengan argumen yang benar
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('utils.load.gspread.service_account')
    def test_save_to_gsheets(self, mock_gspread_auth):
        """Tes penyimpanan ke Google Sheets."""
        # Mocking seluruh rantai otentikasi gspread
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_gspread_auth.return_value = mock_client
        mock_client.open_by_url.return_value = mock_sheet
        mock_sheet.sheet1 = mock_worksheet

        save_to_gsheets(self.clean_df, 'dummy_url', 'dummy_creds.json')
        
        # Pastikan worksheet dibersihkan dan diupdate
        mock_worksheet.clear.assert_called_once()
        mock_worksheet.update.assert_called_once()

    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_save_to_postgresql(self, mock_to_sql, mock_create_engine):
        """Tes penyimpanan ke PostgreSQL."""
        save_to_postgresql(self.clean_df, 'dummy_uri', 'test_table')
        
        # Pastikan engine dibuat dan to_sql dipanggil
        mock_create_engine.assert_called_once_with('dummy_uri')
        mock_to_sql.assert_called_once()

if __name__ == '__main__':
    unittest.main()