# utils/load.py

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_csv(df, filename):
    """
    Menyimpan DataFrame ke dalam file CSV.
    
    Args:
        df (pandas.DataFrame): DataFrame yang akan disimpan.
        filename (str): Nama file CSV tujuan.
    """
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
    except IOError as e:
        # Penanganan error I/O (Kriteria Advanced)
        logging.error(f"Error saving data to CSV file {filename}: {e}")

def save_to_gsheets(df, sheet_url, credentials_path):
    """
    Menyimpan DataFrame ke Google Sheets.
    
    Args:
        df (pandas.DataFrame): DataFrame yang akan disimpan.
        sheet_url (str): URL lengkap dari Google Sheet tujuan.
        credentials_path (str): Path ke file JSON kredensial service account.
    """
    try:
        # Otentikasi ke Google Sheets
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)
        
        # Buka spreadsheet dan worksheet pertama
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Hapus data lama dan tulis data baru
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        logging.info(f"Data successfully saved to Google Sheet: {sheet_url}")
    except FileNotFoundError:
        logging.error(f"Credentials file not found at {credentials_path}. Skipping Google Sheets upload.")
    except Exception as e:
        # Penanganan error umum (Kriteria Advanced)
        logging.error(f"Error saving data to Google Sheets: {e}")

def save_to_postgresql(df, db_uri, table_name):
    """
    Menyimpan DataFrame ke database PostgreSQL.
    
    Args:
        df (pandas.DataFrame): DataFrame yang akan disimpan.
        db_uri (str): URI koneksi database (contoh: 'postgresql://user:password@host:port/dbname').
        table_name (str): Nama tabel tujuan.
    """
    try:
        engine = create_engine(db_uri)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data successfully saved to PostgreSQL table '{table_name}'")
    except Exception as e:
        # Penanganan error koneksi database (Kriteria Advanced)
        logging.error(f"Error saving data to PostgreSQL: {e}")

if __name__ == '__main__':
    # Contoh data bersih untuk pengujian mandiri
    sample_clean_data = pd.DataFrame({
        'Title': ['T-shirt 2'],
        'Price': [1634400.0],
        'Rating': [3.9],
        'Colors': [3],
        'Size': ['M'],
        'Gender': ['Women'],
        'Timestamp': [datetime.now()]
    })

    # Contoh pemanggilan fungsi (membutuhkan file/setup nyata)
    save_to_csv(sample_clean_data, 'products_test.csv')
    
    # Untuk menjalankan fungsi gsheets dan postgresql, Anda perlu setup nyata.
    # print("Simulating save to Google Sheets...")
    # print("Simulating save to PostgreSQL...")