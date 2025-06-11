import unittest
from unittest.mock import patch, Mock
# Menambahkan import ini agar 'requests.exceptions.RequestException' dikenali.
import requests
from utils.extract import scrape_all_products

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_scrape_all_products_success(self, mock_get):
        """Tes skenario sukses saat scraping semua produk."""
        # Membuat mock HTML content untuk simulasi response dari website
        mock_html_content = """
        <div class="collection-card">
            <h3 class="product-title">T-shirt Keren</h3>
            <div class="price-container"><span class="price">$10.00</span></div>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        # Mengatur mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = mock_html_content
        mock_get.return_value = mock_response

        # Memanggil fungsi yang akan diuji
        products = scrape_all_products()

        # Melakukan assertions
        self.assertEqual(len(products), 50) # Karena mock 1 produk per halaman, untuk 50 halaman
        self.assertEqual(products[0]['title'], 'T-shirt Keren')
        self.assertEqual(products[0]['price'], '$10.00')

    @patch('utils.extract.requests.get')
    def test_scrape_all_products_request_exception(self, mock_get):
        """Tes skenario saat terjadi exception pada request."""
        # Mengatur mock untuk memunculkan exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        # Memanggil fungsi dan memastikan hasilnya adalah list kosong karena gagal
        products = scrape_all_products()
        self.assertEqual(len(products), 0)

    @patch('utils.extract.requests.get')
    def test_url_generation(self, mock_get):
        """Tes logika pembuatan URL untuk halaman 1 dan halaman lainnya."""
        # Mengatur mock response
        mock_response = Mock(status_code=200, text="<html></html>")
        mock_get.return_value = mock_response

        # Memanggil fungsi
        scrape_all_products()

        # Memeriksa apakah halaman pertama dipanggil dengan URL dasar
        mock_get.assert_any_call('https://fashion-studio.dicoding.dev', timeout=15)
        
        # URL yang benar adalah tanpa garis miring sebelum nomor halaman.
        mock_get.assert_any_call('https://fashion-studio.dicoding.dev/page2', timeout=15)
        
        # Memeriksa total panggilan sesuai jumlah halaman
        self.assertEqual(mock_get.call_count, 50)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)