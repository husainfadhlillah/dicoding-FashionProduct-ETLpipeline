# main.py

from utils.extract import extract_all_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheets, save_to_postgresql
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- KONFIGURASI ---
# Ganti dengan path dan URL Anda yang sebenarnya
CSV_PATH = 'products.csv'
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/your-sheet-id/edit?usp=sharing' # GANTI INI
GOOGLE_API_CREDENTIALS = 'google-sheets-api.json' # Pastikan file ini ada
POSTGRES_DB_URI = 'postgresql://user:password@localhost:5432/dbname' # GANTI INI
POSTGRES_TABLE_NAME = 'fashion_products'
# --------------------

def main():
    """Fungsi utama untuk menjalankan pipeline ETL."""
    
    # 1. TAHAP EKSTRAKSI
    logging.info("Starting ETL pipeline...")
    logging.info("--- STAGE 1: EXTRACT ---")
    raw_df = extract_all_data()
    
    if raw_df.empty:
        logging.warning("Extraction resulted in an empty DataFrame. Terminating pipeline.")
        return

    # 2. TAHAP TRANSFORMASI
    logging.info("--- STAGE 2: TRANSFORM ---")
    clean_df = transform_data(raw_df)

    if clean_df.empty:
        logging.warning("Transformation resulted in an empty DataFrame. Terminating pipeline.")
        return

    # 3. TAHAP LOAD (memenuhi kriteria Advanced)
    logging.info("--- STAGE 3: LOAD ---")
    
    # Memuat ke CSV (Basic)
    save_to_csv(clean_df, CSV_PATH)
    
    # Memuat ke Google Sheets (Skilled/Advanced)
    save_to_gsheets(clean_df, GOOGLE_SHEET_URL, GOOGLE_API_CREDENTIALS)

    # Memuat ke PostgreSQL (Skilled/Advanced)
    save_to_postgresql(clean_df, POSTGRES_DB_URI, POSTGRES_TABLE_NAME)

    logging.info("ETL pipeline completed successfully.")

if __name__ == '__main__':
    main()