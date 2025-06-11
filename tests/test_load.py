import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres

class TestLoad(unittest.TestCase):

    def setUp(self):
        """Menyiapkan DataFrame sampel untuk setiap tes."""
        self.sample_df = pd.DataFrame({
            'title': ['Test Product'],
            'price': [160000.0],
            'rating': [5.0]
        })

    @patch('utils.load.config')
    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv, mock_config):
        """Tes fungsi penyimpanan ke CSV."""
        mock_config.CSV_OUTPUT_PATH = "mock_path.csv"
        save_to_csv(self.sample_df)
        # Memastikan metode to_csv dipanggil dengan argumen yang benar
        mock_to_csv.assert_called_once_with("mock_path.csv", index=False)

    @patch('utils.load.config')
    @patch('gspread.service_account')
    @patch('gspread_dataframe.set_with_dataframe')
    def test_save_to_gsheet(self, mock_set_with_df, mock_gspread_auth, mock_config):
        """Tes fungsi penyimpanan ke Google Sheets."""
        mock_config.GSHEET_CREDENTIALS_PATH = "mock_creds.json"
        mock_config.GSHEET_URL = "mock_url"
        
        # Mocking objek gspread
        mock_gc = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        mock_gspread_auth.return_value = mock_gc
        mock_gc.open_by_url.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        
        save_to_gsheet(self.sample_df)

        # Memastikan autentikasi dan pemanggilan API gspread dilakukan
        mock_gspread_auth.assert_called_once_with(filename="mock_creds.json")
        mock_gc.open_by_url.assert_called_once_with("mock_url")
        mock_set_with_df.assert_called_once()

    @patch('utils.load.config')
    @patch('sqlalchemy.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_save_to_postgres(self, mock_to_sql, mock_create_engine, mock_config):
        """Tes fungsi penyimpanan ke PostgreSQL."""
        mock_config.DATABASE_URL = "mock_db_url"
        mock_config.DB_TABLE_NAME = "mock_table"
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        save_to_postgres(self.sample_df)
        
        # Memastikan engine dibuat dan metode to_sql dipanggil dengan benar
        mock_create_engine.assert_called_once_with("mock_db_url")
        mock_to_sql.assert_called_once_with(
            name="mock_table",
            con=mock_engine,
            if_exists='replace',
            index=False
        )

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)