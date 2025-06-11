# utils/load.py

import pandas as pd
from sqlalchemy import create_engine
import gspread
from google.oauth2.service_account import Credentials
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_to_csv(df, path):
    """
    Menyimpan DataFrame ke file CSV.

    Args:
        df (pandas.DataFrame): DataFrame yang akan disimpan.
        path (str): Path file CSV tujuan.
    """
    try:
        df.to_csv(path, index=False)
        logging.info(f"Data berhasil disimpan ke CSV: {path}")
    except IOError as e:
        logging.error(f"Gagal menyimpan data ke CSV di {path}: {e}")

def load_to_gsheets(df, creds_path, sheet_url, worksheet_name="products"):
    """
    Mengunggah DataFrame ke Google Sheets.

    Args:
        df (pandas.DataFrame): DataFrame yang akan diunggah.
        creds_path (str): Path ke file JSON kredensial Google Service Account.
        sheet_url (str): URL dari Google Sheet tujuan.
        worksheet_name (str): Nama worksheet yang akan digunakan.
    """
    try:
        # Otentikasi ke Google Sheets
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Buka spreadsheet dan worksheet
        spreadsheet = client.open_by_url(sheet_url)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1", cols="1")

        # Mengubah kolom timestamp menjadi string agar kompatibel dengan JSON
        df_gsheets = df.copy()
        df_gsheets['timestamp'] = df_gsheets['timestamp'].astype(str)
            
        # Bersihkan worksheet dan tulis data baru
        worksheet.clear()
        worksheet.update([df_gsheets.columns.values.tolist()] + df_gsheets.values.tolist())
        logging.info(f"Data berhasil diunggah ke Google Sheets: {sheet_url}")
    except Exception as e:
        logging.error(f"Gagal mengunggah data ke Google Sheets: {e}")


def load_to_postgres(df, db_uri, table_name="products"):
    """
    Menyimpan DataFrame ke tabel database PostgreSQL.

    Args:
        df (pandas.DataFrame): DataFrame yang akan disimpan.
        db_uri (str): URI koneksi database (contoh: 'postgresql://user:password@host:port/dbname').
        table_name (str): Nama tabel tujuan.
    """
    try:
        # Membuat koneksi ke database menggunakan SQLAlchemy
        engine = create_engine(db_uri)
        
        # Menyimpan DataFrame ke tabel, jika tabel sudah ada, ganti isinya
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data berhasil disimpan ke tabel PostgreSQL: {table_name}")
    except Exception as e:
        logging.error(f"Gagal menyimpan data ke PostgreSQL: {e}")