# tests/test_extract.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.extract import scrape_page

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.Session.get')
    def test_scrape_page_success(self, mock_get):
        """Tes scraping halaman berhasil."""
        # Siapkan HTML palsu untuk disimulasikan sebagai respons
        mock_html = """
        <html><body>
            <div class="collection-card">
                <h3 class="product-title">Test Product 1</h3>
                <div class="price-container"><span class="price">$50.00</span></div>
                <p style="font-size: 14px; color: #777;">Rating: 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: L</p>
                <p style="font-size: 14px; color: #777;">Gender: Men</p>
            </div>
        </body></html>
        """
        # Konfigurasi mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # Jalankan fungsi yang diuji
        result = scrape_page(1)
        
        # Periksa hasilnya
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Title'], 'Test Product 1')
        self.assertEqual(result[0]['Price'], '$50.00')
        self.assertEqual(result[0]['Rating'], '4.5 / 5')

    @patch('utils.extract.requests.Session.get')
    def test_scrape_page_request_exception(self, mock_get):
        """Tes jika terjadi error koneksi saat scraping."""
        # Simulasikan error koneksi
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        # Jalankan fungsi dan pastikan mengembalikan None
        result = scrape_page(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()