# main.py

from utils.extract import scrape_products
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_gsheets, load_to_postgres
import logging

# Konfigurasi logging utama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- KONFIGURASI ---
# Ganti dengan path dan URL Anda
CSV_PATH = "products.csv"
GOOGLE_SHEETS_CREDS_PATH = "google-sheets-api.json" # Pastikan file ini ada
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/your-sheet-id/edit" # Ganti dengan URL Anda
POSTGRES_DB_URI = "postgresql://user:password@host:port/dbname" # Ganti dengan URI database Anda

def main():
    """
    Fungsi utama untuk menjalankan pipeline ETL.
    """
    logging.info("Memulai pipeline ETL...")

    # 1. TAHAP EXTRACT
    logging.info("Tahap 1: Ekstraksi Data dari Website.")
    raw_df = scrape_products(max_pages=50)

    # Lanjutkan hanya jika ekstraksi berhasil
    if raw_df is not None and not raw_df.empty:
        logging.info("Ekstraksi data berhasil.")
        
        # 2. TAHAP TRANSFORM
        logging.info("Tahap 2: Transformasi dan Pembersihan Data.")
        cleaned_df = transform_data(raw_df)
        
        if cleaned_df is not None and not cleaned_df.empty:
            logging.info("Transformasi data berhasil.")
            
            # 3. TAHAP LOAD
            logging.info("Tahap 3: Memuat Data ke Repositori.")
            
            # Memuat ke CSV (Wajib)
            load_to_csv(cleaned_df, CSV_PATH)
            
            # Memuat ke Google Sheets (Untuk nilai Skilled/Advanced)
            # Pastikan GOOGLE_SHEETS_URL tidak placeholder
            if "your-sheet-id" not in GOOGLE_SHEETS_URL:
                 load_to_gsheets(cleaned_df, GOOGLE_SHEETS_CREDS_PATH, GOOGLE_SHEETS_URL)
            else:
                logging.warning("URL Google Sheets belum diatur. Melewati proses load ke Google Sheets.")

            # Memuat ke PostgreSQL (Untuk nilai Skilled/Advanced)
            # Pastikan POSTGRES_DB_URI tidak placeholder
            if "user:password" not in POSTGRES_DB_URI:
                 load_to_postgres(cleaned_df, POSTGRES_DB_URI)
            else:
                logging.warning("URI PostgreSQL belum diatur. Melewati proses load ke PostgreSQL.")

        else:
            logging.error("Transformasi data gagal atau menghasilkan data kosong.")
    else:
        logging.error("Ekstraksi data gagal atau tidak menghasilkan data.")
        
    logging.info("Pipeline ETL selesai.")

if __name__ == "__main__":
    main()