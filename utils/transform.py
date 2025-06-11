# utils/transform.py

import pandas as pd
import numpy as np
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(df):
    """
    Fungsi untuk membersihkan dan mentransformasi data produk.

    Args:
        df (pandas.DataFrame): DataFrame mentah hasil scraping.

    Returns:
        pandas.DataFrame: DataFrame yang sudah bersih dan siap di-load.
    """
    if df is None:
        logging.error("DataFrame input kosong, proses transformasi dibatalkan.")
        return None
        
    # Membuat salinan untuk menghindari SettingWithCopyWarning
    df_transformed = df.copy()

    # --- TAHAP 1: Membersihkan Nilai Tidak Valid ---
    # Pola data kotor yang perlu dibersihkan
    dirty_patterns = {
        "Title": ["Unknown Product"],
        "Rating": ["Invalid Rating / 5", "Not Rated"],
        "Price": ["Price Unavailable"]
    }

    # Mengganti pola kotor dengan NaN (Not a Number) agar mudah dihapus
    for column, patterns in dirty_patterns.items():
        for pattern in patterns:
            df_transformed[column] = df_transformed[column].replace(pattern, np.nan)

    logging.info("Selesai mengganti pola data kotor dengan NaN.")

    # --- TAHAP 2: Transformasi Kolom ---
    # Fungsi transformasi individual dengan error handling (kriteria Advanced)
    
    try:
        # Membersihkan dan konversi kolom 'Price'
        df_transformed['Price'] = df_transformed['Price'].str.replace('$', '', regex=False).astype(float)
        # Konversi ke Rupiah (asumsi 1 USD = 16000 IDR)
        df_transformed['Price'] = df_transformed['Price'] * 16000
        df_transformed.rename(columns={'Price': 'Price_IDR'}, inplace=True)
        logging.info("Kolom 'Price' berhasil diubah ke 'Price_IDR' dan dikonversi ke Rupiah.")
    except Exception as e:
        logging.error(f"Error saat transformasi kolom Price: {e}")
        # Jika ada error, kolom ini bisa di-drop atau diisi nilai default
        df_transformed['Price_IDR'] = np.nan

    try:
        # Ekstrak angka dari kolom 'Rating'
        df_transformed['Rating'] = df_transformed['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        logging.info("Kolom 'Rating' berhasil diekstrak dan diubah ke float.")
    except Exception as e:
        logging.error(f"Error saat transformasi kolom Rating: {e}")
        df_transformed['Rating'] = np.nan

    try:
        # Ekstrak angka dari kolom 'Colors'
        df_transformed['Colors'] = df_transformed['Colors'].str.extract(r'(\d+)').astype(int)
        logging.info("Kolom 'Colors' berhasil diekstrak dan diubah ke integer.")
    except Exception as e:
        logging.error(f"Error saat transformasi kolom Colors: {e}")
        df_transformed['Colors'] = np.nan

    try:
        # Membersihkan kolom 'Size' dan 'Gender' dari teks awalan
        df_transformed['Size'] = df_transformed['Size'].str.replace('Size: ', '', regex=False).str.strip()
        df_transformed['Gender'] = df_transformed['Gender'].str.replace('Gender: ', '', regex=False).str.strip()
        logging.info("Kolom 'Size' dan 'Gender' berhasil dibersihkan.")
    except Exception as e:
        logging.error(f"Error saat membersihkan kolom teks: {e}")

    # --- TAHAP 3: Membersihkan Nilai Kosong dan Duplikat ---
    initial_rows = len(df_transformed)
    # Menghapus baris dengan nilai NaN (yang berasal dari data kotor atau error)
    df_transformed.dropna(inplace=True)
    rows_after_na = len(df_transformed)
    
    # Menghapus data duplikat
    df_transformed.drop_duplicates(inplace=True)
    rows_after_duplicates = len(df_transformed)
    
    logging.info(f"Pembersihan data selesai. Baris awal: {initial_rows}, setelah dropna: {rows_after_na}, setelah drop_duplicates: {rows_after_duplicates}.")
    
    # --- TAHAP 4: Mengatur Ulang Tipe Data ---
    # Memastikan tipe data sesuai dengan ekspektasi
    final_dtypes = {
        'Title': 'object',
        'Price_IDR': 'float64',
        'Rating': 'float64',
        'Colors': 'int64',
        'Size': 'object',
        'Gender': 'object',
        'timestamp': 'datetime64[ns]'
    }
    df_transformed = df_transformed.astype(final_dtypes)
    logging.info("Tipe data akhir telah disesuaikan.")
    
    return df_transformed