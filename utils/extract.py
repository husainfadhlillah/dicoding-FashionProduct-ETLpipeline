import requests
from bs4 import BeautifulSoup
import utils.config as config
from typing import List, Dict, Optional

def scrape_product_details(product_card) -> Optional[Dict[str, any]]:
    """
    Mengekstrak detail dari satu kartu produk.
    Mengembalikan dictionary berisi detail produk, atau None jika ada error.
    """
    try:
        title = product_card.find('h3', class_='product-title').text.strip()
        
        # Penanganan harga yang memiliki struktur HTML berbeda
        price_container = product_card.find('div', class_='price-container')
        if price_container:
            price_element = price_container.find('span', class_='price')
            if price_element:
                price = price_element.text.strip()
            else:
                price = "Price Unavailable" # Jika span tidak ditemukan di dalam container
        else:
            # Fallback untuk struktur lama atau jika container tidak ada
            price_element = product_card.find('p', class_='price')
            price = price_element.text.strip() if price_element else "Price Unavailable"

        # Ekstrak detail lain dari tag <p>
        details = product_card.find_all('p')
        rating_text = details[0].text.strip() if len(details) > 0 else "Not Rated"
        colors_text = details[1].text.strip() if len(details) > 1 else ""
        size_text = details[2].text.strip() if len(details) > 2 else ""
        gender_text = details[3].text.strip() if len(details) > 3 else ""

        return {
            "title": title,
            "price": price,
            "rating": rating_text,
            "colors": colors_text,
            "size": size_text,
            "gender": gender_text,
        }
    except AttributeError as e:
        print(f"Error parsing product card: {e}")
        return None

def scrape_all_products() -> List[Dict[str, any]]:
    """
    Melakukan scraping data produk dari semua halaman yang ditentukan di konfigurasi.
    Mengembalikan daftar (list) dari dictionary produk.
    """
    all_products = []
    print("Memulai proses scraping...")

    # Looping untuk setiap halaman dari 1 sampai PAGE_COUNT
    for page_num in range(1, config.PAGE_COUNT + 1):
        # Struktur URL berbeda untuk halaman pertama dan halaman berikutnya
        if page_num == 1:
            url = config.BASE_URL
        else:
            url = f"{config.BASE_URL}/page/{page_num}"
        
        print(f"Scraping halaman: {url}")

        try:
            # Melakukan request GET ke URL dengan timeout
            response = requests.get(url, timeout=15)
            # Memunculkan error jika status code bukan 2xx
            response.raise_for_status()

            # Parsing HTML menggunakan BeautifulSoup dengan parser lxml
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Mencari semua elemen kartu produk
            product_cards = soup.find_all('div', class_='collection-card')
            
            for card in product_cards:
                product_details = scrape_product_details(card)
                if product_details:
                    all_products.append(product_details)
        
        # Penanganan kesalahan jika terjadi masalah dengan request (koneksi, timeout, dll)
        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil data dari {url}: {e}")
            # Bisa dilanjutkan ke halaman berikutnya atau dihentikan
            continue
        # Penanganan kesalahan umum lainnya
        except Exception as e:
            print(f"Terjadi kesalahan saat memproses halaman {page_num}: {e}")
            continue

    print(f"Scraping selesai. Total produk mentah yang didapat: {len(all_products)}")
    return all_products