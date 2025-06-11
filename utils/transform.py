import pandas as pd
from datetime import datetime
import utils.config as config
import re

def transform_and_clean_data(raw_data: list) -> pd.DataFrame:
    """
    Membersihkan, mentransformasi, dan memformat data produk mentah.
    Mengembalikan DataFrame Pandas yang sudah bersih.
    """
    if not raw_data:
        print("Tidak ada data mentah untuk diproses.")
        return pd.DataFrame()

    print("Memulai proses transformasi data...")
    # Mengubah list of dict menjadi DataFrame Pandas
    df = pd.DataFrame(raw_data)

    # 1. Hapus data yang tidak valid atau tidak diinginkan
    invalid_patterns = {
        "title": ["Unknown Product"],
        "price": ["Price Unavailable"],
        "rating": ["Invalid Rating / 5", "Not Rated"]
    }
    df = df[~df['title'].isin(invalid_patterns["title"])]
    df = df[~df['price'].isin(invalid_patterns["price"])]
    df = df[~df['rating'].isin(invalid_patterns["rating"])]

    # 2. Bersihkan dan konversi setiap kolom
    # Kolom 'price': hapus '$', koma, konversi ke float, dan kalikan dengan kurs
    df['price'] = df['price'].str.replace(r'[$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['price'] = df['price'] * config.EXCHANGE_RATE_USD_TO_IDR

    # Kolom 'rating': ekstrak angka rating menggunakan regex
    df['rating'] = df['rating'].str.extract(r'(\d+\.?\d*)').astype(float)

    # Kolom 'colors': ekstrak jumlah warna menggunakan regex
    df['colors'] = df['colors'].str.extract(r'(\d+)').astype(int)

    # Kolom 'size' dan 'gender': hapus prefiks yang tidak perlu
    df['size'] = df['size'].str.replace('Size: ', '', regex=False).str.strip()
    df['gender'] = df['gender'].str.replace('Gender: ', '', regex=False).str.strip()

    # 3. Hapus baris dengan nilai null setelah konversi
    df.dropna(inplace=True)

    # 4. Konversi tipe data untuk memastikan konsistensi
    df = df.astype({
        'price': 'float64',
        'rating': 'float64',
        'colors': 'int64',
        'title': 'object',
        'size': 'object',
        'gender': 'object'
    })

    # 5. Tambahkan kolom timestamp
    df['timestamp'] = datetime.now()

    # 6. Hapus data duplikat
    df.drop_duplicates(inplace=True)
    
    # 7. Reset index DataFrame
    df.reset_index(drop=True, inplace=True)
    
    print(f"Transformasi selesai. Jumlah data bersih: {len(df)}")
    return df