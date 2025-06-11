# tests/test_transform.py

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from utils.transform import transform_data

@pytest.fixture
def raw_dataframe():
    """Fixture untuk menyediakan DataFrame mentah sebagai input tes."""
    data = {
        'Title': ['T-shirt 2', 'Unknown Product', 'Pants 4', 'T-shirt 2'],
        'Price': ['$100.00', 'Price Unavailable', '$50.50', '$100.00'],
        'Rating': ['Rating: 4.8 / 5', 'Not Rated', 'Rating: 3.3 / 5', 'Rating: 4.8 / 5'],
        'Colors': ['3 Colors', '5 Colors', '2 Colors', '3 Colors'],
        'Size': ['Size: L', 'Size: M', 'Size: XL', 'Size: L'],
        'Gender': ['Gender: Unisex', 'Gender: Men', 'Gender: Women', 'Gender: Unisex'],
        'timestamp': [datetime.now()] * 4
    }
    return pd.DataFrame(data)

def test_transform_data(raw_dataframe):
    """Menguji keseluruhan fungsi transformasi data."""
    cleaned_df = transform_data(raw_dataframe)
    
    # Assertions
    assert cleaned_df is not None
    assert isinstance(cleaned_df, pd.DataFrame)
    
    # Seharusnya baris "Unknown Product" dan duplikat sudah dihapus
    # Sisa data: T-shirt 2 dan Pants 4
    assert len(cleaned_df) == 2
    
    # Cek nilai yang sudah ditransformasi
    # Data pertama (T-shirt 2)
    assert cleaned_df.iloc[0]['Price_IDR'] == 100.00 * 16000
    assert cleaned_df.iloc[0]['Rating'] == 4.8
    assert cleaned_df.iloc[0]['Colors'] == 3
    assert cleaned_df.iloc[0]['Size'] == 'L'
    
    # Cek tipe data
    assert cleaned_df['Price_IDR'].dtype == 'float64'
    assert cleaned_df['Rating'].dtype == 'float64'
    assert cleaned_df['Colors'].dtype == 'int64'

def test_transform_data_empty_input():
    """Menguji fungsi dengan input None."""
    assert transform_data(None) is None