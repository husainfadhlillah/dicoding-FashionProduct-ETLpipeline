import unittest
from unittest.mock import patch, MagicMock # 'patch' untuk mengganti objek/fungsi, 'MagicMock' untuk membuat objek tiruan
import pandas as pd

# Mengimpor fungsi-fungsi yang akan kita uji dari modul 'utils.load'
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres

# Mendefinisikan kelas tes untuk modul 'load', yang mewarisi dari 'unittest.TestCase'
class TestLoad(unittest.TestCase):

    # Metode 'setUp' ini dijalankan secara otomatis SEBELUM setiap metode tes (def test_...) dieksekusi.
    def setUp(self):
        """Menyiapkan DataFrame sampel yang konsisten untuk digunakan di setiap tes."""
        # Membuat DataFrame kecil sebagai data masukan tiruan untuk fungsi-fungsi 'save'
        self.sample_df = pd.DataFrame({
            'title': ['Test Product'],
            'price': [160000.0],
            'rating': [5.0]
        })

    # Mendefinisikan decorator 'patch' untuk menginterupsi dan mengganti objek/fungsi selama tes berlangsung.
    # Decorator dieksekusi dari bawah ke atas, tetapi argumennya masuk ke fungsi tes dari kiri ke kanan.
    @patch('utils.load.config')           # Mengganti modul 'config' di 'utils.load' dengan mock (mock_config)
    @patch('pandas.DataFrame.to_csv')     # Mengganti metode 'to_csv' dengan mock (mock_to_csv)
    def test_save_to_csv(self, mock_to_csv, mock_config):
        """Tes fungsi penyimpanan ke CSV tanpa benar-benar menulis file ke disk."""
        # 1. ARRANGE: Menyiapkan kondisi tes
        # Mengatur nilai tiruan untuk path file CSV pada objek config tiruan.
        mock_config.CSV_OUTPUT_PATH = "mock_path.csv"
        
        # 2. ACT: Menjalankan fungsi yang diuji dengan data sampel.
        save_to_csv(self.sample_df)
        
        # 3. ASSERT: Memverifikasi hasil
        # Memastikan bahwa metode 'to_csv' ipanggil TEPAT SATU KALI
        mock_to_csv.assert_called_once_with("mock_path.csv", index=False)

    # --- Pengujian untuk Google Sheets ---
    # Mengubah target patch dari 'gspread_dataframe.set_with_dataframe' ke 'utils.load.set_with_dataframe'.
    @patch('utils.load.set_with_dataframe') # Target: 'set_with_dataframe' yang ada di namespace 'utils.load'
    @patch('gspread.service_account')       # Mock otentikasi gspread
    @patch('utils.load.config')             # Mock modul config
    def test_save_to_gsheet(self, mock_config, mock_gspread_auth, mock_set_with_df):
        """Tes fungsi penyimpanan ke Google Sheets tanpa koneksi internet atau API call sungguhan."""
        # 1. ARRANGE: Menyiapkan kondisi tes
        mock_config.GSHEET_CREDENTIALS_PATH = "mock_creds.json"
        mock_config.GSHEET_URL = "mock_url"
        
        # Membuat serangkaian objek mock untuk mensimulasikan rantai pemanggilan library gspread
        mock_gc = MagicMock()           # Mock untuk objek koneksi utama
        mock_spreadsheet = MagicMock()  # Mock untuk objek spreadsheet
        mock_worksheet = MagicMock()    # Mock untuk objek worksheet
        
        # Menambahkan atribut yang dibutuhkan oleh library gspread pada mock object.
        mock_worksheet.row_count = 1000
        mock_worksheet.col_count = 20
        
        # Mengatur 'return_value' dari setiap pemanggilan mock
        mock_gspread_auth.return_value = mock_gc                  # gspread.service_account(...) akan mengembalikan mock_gc
        mock_gc.open_by_url.return_value = mock_spreadsheet       # gc.open_by_url(...) akan mengembalikan mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet # spreadsheet.get_worksheet(...) akan mengembalikan mock_worksheet
        
        # 2. ACT: Menjalankan fungsi yang diuji
        save_to_gsheet(self.sample_df)

        # 3. ASSERT: Memverifikasi setiap langkah dalam fungsi telah dipanggil dengan benar
        # Memastikan otentikasi dipanggil dengan nama file kredensial yang benar
        mock_gspread_auth.assert_called_once_with(filename="mock_creds.json")
        # Memastikan sheet dibuka dengan URL yang benar
        mock_gc.open_by_url.assert_called_once_with("mock_url")
        # Memastikan worksheet pertama (index 0) yang dipilih
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        # Memastikan worksheet dibersihkan sebelum data baru dimasukkan
        mock_worksheet.clear.assert_called_once()
        # Memastikan fungsi untuk menulis DataFrame dipanggil dengan argumen yang benar
        mock_set_with_df.assert_called_once_with(mock_worksheet, self.sample_df)

    # --- Pengujian untuk PostgreSQL ---
    @patch('utils.load.create_engine') # Patch 'create_engine' di mana ia digunakan (di utils.load)
    @patch('pandas.DataFrame.to_sql')  # Patch metode 'to_sql' dari pandas
    @patch('utils.load.config')        # Patch modul config
    def test_save_to_postgres(self, mock_config, mock_to_sql, mock_create_engine):
        """Tes fungsi penyimpanan ke PostgreSQL tanpa koneksi database sungguhan."""
        # 1. ARRANGE: Menyiapkan kondisi tes
        mock_config.DATABASE_URL = "postgresql://user:pass@host/db" # Gunakan format URL yang valid untuk SQLAlchemy
        mock_config.DB_TABLE_NAME = "mock_table"
        mock_engine = MagicMock() # Membuat objek engine database tiruan
        mock_create_engine.return_value = mock_engine # Saat create_engine dipanggil, ia akan mengembalikan engine tiruan kita
        
        # 2. ACT: Menjalankan fungsi yang diuji
        save_to_postgres(self.sample_df)
        
        # 3. ASSERT: Memverifikasi hasil
        # Memastikan engine database dibuat dengan URL koneksi yang benar
        mock_create_engine.assert_called_once_with(mock_config.DATABASE_URL)
        # Memastikan metode to_sql dipanggil dengan semua parameter yang benar
        mock_to_sql.assert_called_once_with(
            name="mock_table",
            con=mock_engine,
            if_exists='replace',
            index=False
        )

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)