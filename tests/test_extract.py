# tests/test_extract.py

import pytest
import pandas as pd
import requests_mock
from utils.extract import scrape_products

@pytest.fixture
def mock_html_page1():
    """Fixture untuk menyediakan konten HTML palsu halaman 1."""
    return """
    <html><body>
        <div class="collection-card">
            <h3 class="product-title">T-shirt 2</h3>
            <span class="price">$102.15</span>
            <p>Rating: 3.9 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Women</p>
        </div>
        <div class="collection-card">
            <h3 class="product-title">Unknown Product</h3>
            <p class="price">Price Unavailable</p>
            <p>Rating: Not Rated</p>
            <p>5 Colors</p>
            <p>Size: L</p>
            <p>Gender: Men</p>
        </div>
    </body></html>
    """

@pytest.fixture
def mock_html_empty_page():
    """Fixture untuk konten HTML halaman kosong."""
    return "<html><body></body></html>"

def test_scrape_products_success(requests_mock, mock_html_page1, mock_html_empty_page):
    """Menguji skenario scraping berhasil."""
    # Mock request untuk halaman 1 agar mengembalikan HTML palsu
    requests_mock.get('https://fashion-studio.dicoding.dev/index.php?page=1', text=mock_html_page1)
    # Mock request untuk halaman 2 agar mengembalikan halaman kosong (akhir dari scraping)
    requests_mock.get('https://fashion-studio.dicoding.dev/index.php?page=2', text=mock_html_empty_page)
    
    df = scrape_products(max_pages=2)
    
    # Assertions
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'timestamp' in df.columns
    assert df.iloc[0]['Title'] == 'T-shirt 2'
    assert df.iloc[1]['Price'] == 'Price Unavailable'

def test_scrape_products_network_error(requests_mock):
    """Menguji penanganan error saat koneksi gagal."""
    # Mock request agar mengembalikan error koneksi
    requests_mock.get('https://fashion-studio.dicoding.dev/index.php?page=1', exc=requests.exceptions.ConnectionError)
    
    df = scrape_products(max_pages=1)
    
    # Assertions
    assert df is None