import os
from dotenv import load_dotenv

# Memuat variabel dari file .env ke dalam environment
load_dotenv()

# --- Konfigurasi Website ---
# URL dasar dari website yang akan di-scrape
BASE_URL = os.getenv("BASE_URL", "https://fashion-studio.dicoding.dev")
# Jumlah total halaman yang akan di-scrape
PAGE_COUNT = int(os.getenv("PAGE_COUNT", 50))

# --- Konfigurasi Konversi ---
# Nilai tukar dari USD ke IDR
EXCHANGE_RATE_USD_TO_IDR = float(os.getenv("EXCHANGE_RATE_USD_TO_IDR", 16000))

# --- Konfigurasi Database PostgreSQL ---
# Informasi untuk koneksi ke database
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_TABLE_NAME = os.getenv("DB_TABLE_NAME", "products")
# Membuat URL koneksi database yang akan digunakan oleh SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Konfigurasi Google Sheets ---
# Path ke file kredensial JSON dari Google Service Account
GSHEET_CREDENTIALS_PATH = os.getenv("GSHEET_CREDENTIALS_PATH")
# URL lengkap dari Google Sheet tujuan
GSHEET_URL = os.getenv("GSHEET_URL")

# --- Konfigurasi Output ---
# Path untuk menyimpan file CSV hasil proses ETL
CSV_OUTPUT_PATH = os.getenv("CSV_OUTPUT_PATH", "products.csv")