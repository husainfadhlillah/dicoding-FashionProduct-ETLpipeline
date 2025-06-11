# utils/extract.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Konfigurasi logging untuk mencatat informasi dan error
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_page(page_number):
    """
    Mengambil data dari satu halaman website Fashion Studio.
    
    Args:
        page_number (int): Nomor halaman yang akan di-scrape.
        
    Returns:
        list: Sebuah list berisi dictionary, di mana setiap dictionary adalah data satu produk.
              Mengembalikan None jika terjadi error.
    """
    url = f"https://fashion-studio.dicoding.dev/page/{page_number}"
    try:
        # Menggunakan session untuk koneksi yang lebih efisien
        session = requests.Session()
        response = session.get(url, timeout=10) # Timeout 10 detik
        response.raise_for_status() # Akan melempar error jika status code bukan 2xx
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='collection-card')
        
        page_products = []
        for product in products:
            try:
                title = product.find('h3', class_='product-title').text.strip()
                
                # Menangani harga yang bisa berada di tag span atau p
                price_container = product.find('div', class_='price-container')
                price_span = price_container.find('span', class_='price')
                if price_span:
                    price = price_span.text.strip()
                else:
                    price = "Price Unavailable" # Default jika harga tidak ditemukan
                
                # Menangani rating yang bisa memiliki format berbeda
                rating_p = product.find('p', style="font-size: 14px; color: #777;")
                rating = rating_p.text.strip().replace('Rating: ', '') if rating_p else "Not Rated"

                details = product.find_all('p', style="font-size: 14px; color: #777;")
                
                # Ekstrak Warna, Ukuran, dan Gender dengan aman
                colors = details[1].text.strip() if len(details) > 1 else "N/A"
                size = details[2].text.strip() if len(details) > 2 else "N/A"
                gender = details[3].text.strip() if len(details) > 3 else "N/A"

                page_products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                })
            except Exception as e:
                logging.error(f"Error parsing product card: {e}")
                continue # Lanjut ke produk berikutnya jika ada error di satu kartu
                
        logging.info(f"Successfully scraped page {page_number}, found {len(page_products)} products.")
        return page_products
        
    except requests.exceptions.RequestException as e:
        # Penanganan error koneksi (Kriteria Advanced)
        logging.error(f"Error fetching website on page {page_number}: {e}")
        return None

def extract_all_data():
    """
    Fungsi utama untuk melakukan scraping ke semua halaman (1-50).
    
    Returns:
        pandas.DataFrame: DataFrame berisi semua data produk mentah yang berhasil diekstrak,
                          ditambah kolom 'Timestamp'.
    """
    all_products = []
    # Mengambil data dari halaman 1 sampai 50
    for i in range(1, 51):
        products_on_page = scrape_page(i)
        if products_on_page:
            all_products.extend(products_on_page)
    
    if not all_products:
        logging.warning("No products were extracted. Exiting.")
        return pd.DataFrame()

    df = pd.DataFrame(all_products)
    
    # Menambahkan kolom timestamp (Kriteria Skilled)
    df['Timestamp'] = datetime.now()
    
    logging.info(f"Extraction complete. Total products extracted: {len(df)}")
    return df

if __name__ == '__main__':
    # Contoh cara menjalankan fungsi extract secara mandiri
    raw_df = extract_all_data()
    if not raw_df.empty:
        print(raw_df.head())
        print(f"\nTotal data mentah: {len(raw_df)} baris")