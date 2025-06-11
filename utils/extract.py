# utils/extract.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Konfigurasi logging untuk memberikan informasi saat proses berjalan
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_products(max_pages=50):
    """
    Fungsi untuk melakukan web scraping data produk dari situs Fashion Studio.

    Args:
        max_pages (int): Jumlah maksimum halaman yang akan di-scrape.

    Returns:
        pandas.DataFrame: DataFrame yang berisi data produk mentah,
                          atau None jika terjadi kesalahan.
    """
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []
    
    # Menggunakan session untuk re-use koneksi TCP, lebih efisien
    with requests.Session() as session:
        # Loop untuk scraping dari halaman 1 hingga max_pages
        for page in range(1, max_pages + 1):
            url = f"{base_url}/index.php?page={page}"
            try:
                # Melakukan request GET ke URL
                response = session.get(url, timeout=10)
                # Memastikan request berhasil (status code 200)
                response.raise_for_status()
                logging.info(f"Berhasil mengakses halaman: {url}")

                # Parsing HTML dengan BeautifulSoup dan parser lxml
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Mencari semua kartu produk di halaman
                product_cards = soup.find_all('div', class_='collection-card')

                # Jika tidak ada kartu produk, hentikan loop (sudah mencapai halaman terakhir)
                if not product_cards:
                    logging.info(f"Tidak ada produk di halaman {page}. Proses scraping berhenti.")
                    break
                
                # Ekstraksi data dari setiap kartu produk
                for card in product_cards:
                    # Mencari elemen-elemen data. Menggunakan .text dan .strip() untuk membersihkan spasi
                    title = card.find('h3', class_='product-title').text.strip()
                    
                    # Penanganan untuk harga yang memiliki struktur tag berbeda
                    price_element_span = card.find('span', class_='price')
                    price_element_p = card.find('p', class_='price')
                    
                    if price_element_span:
                        price = price_element_span.text.strip()
                    elif price_element_p:
                        price = price_element_p.text.strip()
                    else:
                        price = None
                        
                    rating_text = card.find('p', string=lambda t: t and 'Rating:' in t).text.strip()
                    colors_text = card.find('p', string=lambda t: t and 'Colors' in t).text.strip()
                    size_text = card.find('p', string=lambda t: t and 'Size:' in t).text.strip()
                    gender_text = card.find('p', string=lambda t: t and 'Gender:' in t).text.strip()

                    # Menambahkan data yang diekstrak ke dalam list
                    all_products.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating_text,
                        "Colors": colors_text,
                        "Size": size_text,
                        "Gender": gender_text
                    })
            
            # Penanganan error untuk kegagalan koneksi atau timeout
            except requests.exceptions.RequestException as e:
                logging.error(f"Gagal mengakses {url}: {e}")
                # Jika terjadi error, kembalikan None untuk menandakan kegagalan
                return None
    
    if not all_products:
        logging.warning("Tidak ada produk yang berhasil di-scrape.")
        return None

    # Mengubah list of dictionaries menjadi DataFrame
    products_df = pd.DataFrame(all_products)
    
    # Menambahkan kolom timestamp sesuai kriteria Skilled
    products_df['timestamp'] = datetime.now()
    
    logging.info(f"Total produk yang berhasil di-scrape: {len(products_df)}")
    return products_df