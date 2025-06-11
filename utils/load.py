import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from sqlalchemy import create_engine
import utils.config as config

def save_to_csv(df: pd.DataFrame):
    """
    Menyimpan DataFrame ke dalam file CSV.
    """
    try:
        print(f"Menyimpan data ke CSV di path: {config.CSV_OUTPUT_PATH}...")
        df.to_csv(config.CSV_OUTPUT_PATH, index=False)
        print("Data berhasil disimpan ke CSV.")
    except Exception as e:
        print(f"Gagal menyimpan data ke CSV: {e}")

def save_to_gsheet(df: pd.DataFrame):
    """
    Menyimpan DataFrame ke dalam Google Sheets.
    """
    try:
        print(f"Menyimpan data ke Google Sheets...")
        # Autentikasi menggunakan file kredensial
        gc = gspread.service_account(filename=config.GSHEET_CREDENTIALS_PATH)
        # Buka spreadsheet berdasarkan URL
        spreadsheet = gc.open_by_url(config.GSHEET_URL)
        # Pilih worksheet pertama (index 0)
        worksheet = spreadsheet.get_worksheet(0)
        
        # Bersihkan worksheet sebelum menulis data baru
        worksheet.clear()
        
        # Tulis DataFrame ke worksheet
        set_with_dataframe(worksheet, df)
        print("Data berhasil disimpan ke Google Sheets.")
    except FileNotFoundError:
        print(f"File kredensial tidak ditemukan di path: {config.GSHEET_CREDENTIALS_PATH}")
    except Exception as e:
        print(f"Gagal menyimpan data ke Google Sheets: {e}")

def save_to_postgres(df: pd.DataFrame):
    """
    Menyimpan DataFrame ke dalam tabel database PostgreSQL.
    """
    try:
        print(f"Menyimpan data ke PostgreSQL...")
        # Buat engine koneksi ke database menggunakan SQLAlchemy
        engine = create_engine(config.DATABASE_URL)
        
        # Simpan DataFrame ke tabel, ganti tabel jika sudah ada
        df.to_sql(
            name=config.DB_TABLE_NAME,
            con=engine,
            if_exists='replace',
            index=False
        )
        print(f"Data berhasil disimpan ke tabel '{config.DB_TABLE_NAME}' di PostgreSQL.")
    except Exception as e:
        print(f"Gagal menyimpan data ke PostgreSQL: {e}")