# Mengimpor modul dan fungsi yang diperlukan
import utils.extract as extract
import utils.transform as transform
import utils.load as load
import pandas as pd

def main():
    """
    Fungsi utama untuk menjalankan seluruh pipeline ETL.
    1. Ekstrak data dari website.
    2. Transformasi dan bersihkan data.
    3. Muat data ke semua repositori tujuan (CSV, G-Sheets, PostgreSQL).
    """
    print("===== MEMULAI PIPELINE ETL PRODUK FASHION =====")
    
    # 1. Tahap Ekstrak
    # ------------------
    raw_products_data = extract.scrape_all_products()
    
    # Hentikan proses jika tidak ada data yang berhasil diekstrak
    if not raw_products_data:
        print("Pipeline dihentikan: Tidak ada data mentah yang berhasil diekstrak.")
        return
        
    # 2. Tahap Transformasi
    # ----------------------
    cleaned_products_df = transform.transform_and_clean_data(raw_products_data)
    
    # Hentikan proses jika DataFrame kosong setelah dibersihkan
    if cleaned_products_df.empty:
        print("Pipeline dihentikan: Tidak ada data valid setelah proses transformasi.")
        return
        
    print("\n--- Data Bersih Siap Dimuat ---")
    print(cleaned_products_df.head())
    print("\n--- Info DataFrame ---")
    cleaned_products_df.info()
    print("--------------------------\n")

    # 3. Tahap Memuat (Load)
    # -------------------
    # Memuat data ke semua tujuan yang ditentukan
    load.save_to_csv(cleaned_products_df)
    load.save_to_gsheet(cleaned_products_df)
    load.save_to_postgres(cleaned_products_df)
    
    print("\n===== PIPELINE ETL SELESAI =====")


if __name__ == "__main__":
    # Menjalankan fungsi utama saat skrip dieksekusi
    main()