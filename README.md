# Proyek Fundamental Data: ETL Pipeline untuk Analisis Produk Fashion

## 👤 Informasi Pengembang

- **Nama:** Muhammad Husain Fadhlillah
- **ID Dicoding:** MC006D5Y2343

## 🚀 Ikhtisar Proyek

Proyek ini adalah implementasi dari pipeline **Extract, Transform, Load (ETL)** sederhana yang dibangun dengan Python. Pipeline ini dirancang untuk mengumpulkan data produk dari situs web kompetitor, membersihkan dan mentransformasikannya menjadi format yang siap dianalisis, lalu memuatnya ke dalam beberapa sistem penyimpanan data.

Tujuan utama proyek ini adalah untuk:

1.  **Mengekstrak (Extract)** data produk secara otomatis dari situs web publik.
2.  **Mentransformasi (Transform)** data mentah dengan melakukan pembersihan, konversi tipe data, perhitungan kolom baru, dan memastikan kualitas data.
3.  **Memuat (Load)** data yang sudah bersih ke dalam tiga jenis repositori data yang berbeda: Flat File (CSV), Google Sheets, dan database relasional (PostgreSQL).
4.  Memastikan keandalan dan kualitas kode melalui **Unit Testing** yang komprehensif.

## 📊 Sumber Data

- **Nama Sumber:** Situs E-commerce "Fashion Studio"
- **URL:** `https://fashion-studio.dicoding.dev`
- **Deskripsi:** Sumber data adalah sebuah situs web fiktif yang berisi katalog produk fashion. Data yang diekstrak mencakup atribut produk seperti `Title` (nama), `Price` (harga), `Rating`, `Colors` (jumlah warna), `Size` (ukuran), dan `Gender`.

## ⚙️ Struktur Proyek & Alur Kerja ETL

Proyek ini dibangun dengan prinsip kode modular, di mana setiap tahapan ETL dipisahkan ke dalam modulnya sendiri untuk kemudahan pengelolaan dan pengujian.

1.  **Tahap Ekstraksi (`utils/extract.py`):**

    - Melakukan _web scraping_ ke 50 halaman situs "Fashion Studio".
    - Mengambil semua informasi mentah dari setiap kartu produk yang tersedia.
    - Menangani format URL yang berbeda untuk halaman pertama dan halaman selanjutnya.
    - Dilengkapi dengan penanganan kesalahan untuk mengatasi kegagalan koneksi atau `request`.

2.  **Tahap Transformasi (`utils/transform.py`):**

    - Mengubah data mentah hasil ekstraksi menjadi DataFrame Pandas.
    - **Pembersihan Data:** Menghapus data tidak valid (misal: "Unknown Product"), nilai yang hilang (`null`), dan data duplikat.
    - **Transformasi Kolom:**
      - `Price`: Mengonversi dari Dolar AS ke Rupiah (kurs Rp16.000) dan mengubah tipe data menjadi `float`.
      - `Rating`, `Colors`: Mengekstrak nilai numerik dari string dan mengubah tipe datanya.
      - `Size`, `Gender`: Menghapus teks prefiks yang tidak perlu.
    - **Penambahan Kolom:** Menambahkan kolom `timestamp` untuk mencatat waktu data diproses.

3.  **Tahap Pemuatan/Load (`utils/load.py`):**

    - Menerima DataFrame yang sudah bersih dari tahap transformasi.
    - Menyimpan data ke tiga tujuan berbeda:
      1.  **File CSV:** Menyimpan output dalam format `products.csv`.
      2.  **Google Sheets:** Mengunggah data secara otomatis ke Google Sheet yang telah ditentukan.
      3.  **PostgreSQL:** Memasukkan data ke dalam tabel pada database PostgreSQL.

4.  **Pengujian (`tests/`):**
    - Setiap modul (`extract`, `transform`, `load`) memiliki file tesnya sendiri.
    - Menggunakan `pytest` untuk menjalankan tes dan `pytest-cov` untuk mengukur cakupan tes (_test coverage_).
    - Menerapkan _mocking_ secara ekstensif untuk mengisolasi tes dari layanan eksternal (internet, API, database).

## 🛠️ Teknologi dan Pustaka yang Digunakan

- **Python**
- **Manajemen Environment**: `venv` / `conda`
- **Core Libraries**:
  - `Pandas`: Untuk manipulasi dan analisis data.
  - `Requests`: Untuk melakukan permintaan HTTP ke website.
  - `BeautifulSoup4` & `lxml`: Untuk parsing HTML.
- **Database**:
  - `SQLAlchemy`: Untuk berinteraksi dengan database PostgreSQL.
  - `psycopg2-binary`: Driver PostgreSQL untuk Python.
- **Google Sheets API**:
  - `gspread`: Untuk berinteraksi dengan Google Sheets.
  - `gspread-dataframe`: Untuk kemudahan transfer data antara Pandas dan gspread.
  - `google-auth` & `oauth2client`: Untuk proses autentikasi.
- **Konfigurasi**:
  - `python-dotenv`: Untuk mengelola variabel lingkungan dari file `.env`.
- **Pengujian**:
  - `pytest`: Framework untuk menjalankan unit test.
  - `pytest-cov`: Plugin untuk mengukur _test coverage_.

## 📁 Berkas dalam Repositori

```
.
├── .env                  # File konfigurasi
├── main.py               # Skrip utama untuk menjalankan pipeline ETL
├── requirements.txt      # Daftar dependency proyek
├── submission.txt        # Panduan menjalankan proyek untuk reviewer
├── products.csv          # Contoh output data dalam format CSV
├── google-sheets-api.json# Kunci autentikasi Google API
├── README.md             # File ini
├── utils/                  # Modul-modul untuk logika inti ETL
│   ├── config.py         # Memuat konfigurasi dari .env
│   ├── extract.py        # Logika untuk tahap Ekstrak
│   ├── transform.py      # Logika untuk tahap Transformasi
│   └── load.py           # Logika untuk tahap Pemuatan/Load
└── tests/                  # Direktori untuk semua unit test
    ├── test_extract.py     # Tes untuk modul extract.py
    ├── test_transform.py   # Tes untuk modul transform.py
    └── test_load.py        # Tes untuk modul load.py
```

## 🚀 Cara Menjalankan Proyek

1.  **Prasyarat:**

    - Pastikan **PostgreSQL** sudah terpasang dan berjalan. Buat database dan user sesuai yang ada di file `.env`.
    - Siapkan **Google Sheets API** dengan membuat _Service Account_, unduh file kredensial `.json`, dan bagikan akses **Editor** pada Google Sheet Anda ke `client_email` yang ada di file `.json`.

2.  **Setup Lingkungan:**

    - Kloning repositori ini.
    - Buat dan aktifkan _virtual environment_ (`venv` atau `conda`).
    - Buat file `.env` di direktori utama dan isi konfigurasinya sesuai kebutuhan.
    - Install semua _dependency_:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Menjalankan Pipeline ETL:**

    ```bash
    python main.py
    ```

4.  **Menjalankan Unit Test:**

    ```bash
    python -m pytest tests
    ```

5.  **Melihat Laporan Test Coverage:**
    ```bash
    coverage run -m pytest tests
    coverage report -m
    ```

## ✨ Ringkasan Hasil Utama

- Pipeline berhasil mengekstrak **1000 data produk mentah** dari 50 halaman web.
- Setelah proses transformasi dan pembersihan, dihasilkan dataset bersih sebanyak **867 data produk** yang valid dan siap digunakan.
- Data bersih berhasil dimuat ke tiga sistem: file `products.csv`, Google Sheets, dan tabel di database PostgreSQL.
- Kualitas kode divalidasi dengan **7 unit test** yang semuanya berhasil (`passed`), dengan **cakupan tes (coverage) mencapai 90%**, melebihi target 80% untuk kriteria Advanced.
