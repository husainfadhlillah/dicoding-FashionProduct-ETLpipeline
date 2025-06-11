# tests/test_transform.py

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def setUp(self):
        """Menyiapkan data kotor untuk setiap tes."""
        self.dirty_df = pd.DataFrame([
            {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': '3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women'},
            {'Title': 'Hoodie 3', 'Price': '$496.88', 'Rating': '4.8 / 5', 'Colors': '3 Colors', 'Size': 'Size: L', 'Gender': 'Gender: Unisex'},
            {'Title': 'Unknown Product', 'Price': '$100.00', 'Rating': '4.0 / 5', 'Colors': '1 Color', 'Size': 'Size: XL', 'Gender': 'Gender: Men'},
            {'Title': 'Pants 4', 'Price': 'Price Unavailable', 'Rating': 'Not Rated', 'Colors': '2 Colors', 'Size': 'Size: S', 'Gender': 'Gender: Men'},
            {'Title': 'Jacket 5', 'Price': '$50.00', 'Rating': 'Invalid Rating / 5', 'Colors': '5 Colors', 'Size': 'Size: XXL', 'Gender': 'Gender: Women'},
            {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': '3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women'}, # Duplikat
        ])
        self.dirty_df['Timestamp'] = datetime.now()

    def test_transform_data(self):
        """Tes fungsionalitas transformasi data secara keseluruhan."""
        # Jalankan fungsi transformasi
        clean_df = transform_data(self.dirty_df)

        # 1. Periksa apakah baris invalid sudah dihapus
        self.assertNotIn('Unknown Product', clean_df['Title'].values)
        self.assertEqual(clean_df.isnull().sum().sum(), 0) # Tidak ada nilai null

        # 2. Periksa apakah duplikat sudah dihapus
        self.assertEqual(len(clean_df), 2) # Harusnya sisa T-shirt dan Hoodie
        
        # 3. Periksa transformasi harga (contoh T-shirt 2)
        expected_price = 102.15 * 16000
        self.assertAlmostEqual(clean_df.iloc[0]['Price'], expected_price)
        
        # 4. Periksa transformasi rating, colors, size, gender
        self.assertEqual(clean_df.iloc[0]['Rating'], 3.9)
        self.assertEqual(clean_df.iloc[0]['Colors'], 3)
        self.assertEqual(clean_df.iloc[0]['Size'], 'M')
        self.assertEqual(clean_df.iloc[0]['Gender'], 'Women')
        
        # 5. Periksa tipe data final
        self.assertEqual(str(clean_df['Price'].dtype), 'float64')
        self.assertEqual(str(clean_df['Rating'].dtype), 'float64')
        self.assertEqual(str(clean_df['Colors'].dtype), 'int64')

if __name__ == '__main__':
    unittest.main()