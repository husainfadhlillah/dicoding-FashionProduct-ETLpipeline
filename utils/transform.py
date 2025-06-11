# utils/transform.py

import pandas as pd
import numpy as np
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(df):
    """
    Membersihkan dan mentransformasi DataFrame data produk.
    
    Args:
        df (pandas.DataFrame): DataFrame mentah hasil ekstraksi.
        
    Returns:
        pandas.DataFrame: DataFrame yang sudah bersih dan siap untuk dimuat.
    """
    if df.empty:
        logging.warning("Input DataFrame is empty. No transformation performed.")
        return df

    # Salin DataFrame untuk menghindari SettingWithCopyWarning
    df_transformed = df.copy()

    # 1. Menangani nilai-nilai invalid yang sudah didefinisikan
    try:
        dirty_patterns = {
            "Title": ["Unknown Product"],
            "Rating": ["Invalid Rating / 5", "Not Rated"],
            "Price": ["Price Unavailable"]
        }
        for col, patterns in dirty_patterns.items():
            for pattern in patterns:
                df_transformed[col] = df_transformed[col].replace(pattern, np.nan)
        logging.info("Replaced dirty patterns with NaN.")
    except Exception as e:
        # Error handling (Kriteria Advanced)
        logging.error(f"Error during handling dirty patterns: {e}")
        return pd.DataFrame()

    # 2. Membersihkan dan mengonversi kolom 'Price' ke Rupiah
    try:
        # Hapus '$' dan konversi ke float, lalu kalikan 16000
        df_transformed['Price'] = df_transformed['Price'].str.replace('$', '', regex=False).astype(float)
        df_transformed['Price'] = df_transformed['Price'] * 16000
        logging.info("Transformed 'Price' column to Rupiah.")
    except Exception as e:
        logging.error(f"Error transforming 'Price' column: {e}")
        df_transformed['Price'] = np.nan # Jika gagal, jadikan NaN

    # 3. Membersihkan dan mengonversi kolom 'Rating'
    try:
        # Ekstrak angka dari string rating
        df_transformed['Rating'] = df_transformed['Rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
        logging.info("Transformed 'Rating' column to float.")
    except Exception as e:
        logging.error(f"Error transforming 'Rating' column: {e}")
        df_transformed['Rating'] = np.nan

    # 4. Membersihkan kolom 'Colors', 'Size', dan 'Gender'
    try:
        df_transformed['Colors'] = df_transformed['Colors'].str.extract(r'(\d+)').astype(int)
        df_transformed['Size'] = df_transformed['Size'].str.replace('Size: ', '', regex=False)
        df_transformed['Gender'] = df_transformed['Gender'].str.replace('Gender: ', '', regex=False)
        logging.info("Cleaned 'Colors', 'Size', and 'Gender' columns.")
    except Exception as e:
        logging.error(f"Error cleaning text columns: {e}")

    # 5. Menghapus baris dengan nilai null (setelah semua pembersihan)
    df_cleaned = df_transformed.dropna()
    logging.info(f"Dropped {len(df_transformed) - len(df_cleaned)} rows with null values.")

    # 6. Menghapus data duplikat
    initial_rows = len(df_cleaned)
    df_final = df_cleaned.drop_duplicates()
    logging.info(f"Dropped {initial_rows - len(df_final)} duplicate rows.")

    # 7. Memastikan tipe data sesuai dengan kriteria
    try:
        df_final = df_final.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object'
        })
        logging.info("Final data types have been set.")
    except Exception as e:
        logging.error(f"Error setting final data types: {e}")
    
    logging.info(f"Transformation complete. Final data has {len(df_final)} rows.")
    return df_final

if __name__ == '__main__':
    # Contoh data mentah untuk pengujian mandiri
    sample_raw_data = pd.DataFrame([
        {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': '3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women', 'Timestamp': datetime.now()},
        {'Title': 'Unknown Product', 'Price': '$100.00', 'Rating': '4.0 / 5', 'Colors': '1 Color', 'Size': 'Size: L', 'Gender': 'Gender: Men', 'Timestamp': datetime.now()},
        {'Title': 'Pants 4', 'Price': 'Price Unavailable', 'Rating': 'Not Rated', 'Colors': '2 Colors', 'Size': 'Size: XL', 'Gender': 'Gender: Unisex', 'Timestamp': datetime.now()},
    ])
    
    clean_df = transform_data(sample_raw_data)
    print(clean_df)
    print("\nInfo tipe data:")
    clean_df.info()