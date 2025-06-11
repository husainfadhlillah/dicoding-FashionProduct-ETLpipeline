import unittest
import pandas as pd
from utils.transform import transform_and_clean_data

class TestTransform(unittest.TestCase):

    def test_transform_and_clean_data(self):
        """Tes fungsionalitas transformasi dan pembersihan data."""
        # Membuat data mentah 'kotor' untuk diuji
        raw_data = [
            {'title': 'T-shirt Bagus', 'price': '$15.00', 'rating': 'Rating: ⭐ 4.5 / 5', 'colors': '3 Colors', 'size': 'Size: L', 'gender': 'Gender: Men'},
            {'title': 'Unknown Product', 'price': '$10.00', 'rating': 'Rating: ⭐ 4.0 / 5', 'colors': '1 Color', 'size': 'Size: S', 'gender': 'Gender: Unisex'},
            {'title': 'Celana Mahal', 'price': 'Price Unavailable', 'rating': 'Not Rated', 'colors': '2 Colors', 'size': 'Size: M', 'gender': 'Gender: Women'},
            {'title': 'Jaket Keren', 'price': '$2,000.00', 'rating': 'Rating: ⭐ 3.9 / 5', 'colors': '5 Colors', 'size': 'Size: XL', 'gender': 'Gender: Unisex'},
        ]
        
        # Memanggil fungsi transformasi
        cleaned_df = transform_and_clean_data(raw_data)

        # Assertions
        # 1. Pastikan data tidak valid sudah terhapus (hanya 2 baris yang valid)
        self.assertEqual(len(cleaned_df), 2)
        
        # 2. Periksa nilai yang sudah ditransformasi pada baris pertama
        self.assertEqual(cleaned_df.loc[0, 'title'], 'T-shirt Bagus')
        self.assertAlmostEqual(cleaned_df.loc[0, 'price'], 15.00 * 16000) # 240000
        self.assertEqual(cleaned_df.loc[0, 'rating'], 4.5)
        self.assertEqual(cleaned_df.loc[0, 'colors'], 3)
        self.assertEqual(cleaned_df.loc[0, 'size'], 'L')

        # 3. Periksa nilai yang sudah ditransformasi pada baris kedua (termasuk koma)
        self.assertAlmostEqual(cleaned_df.loc[1, 'price'], 2000.00 * 16000) # 32000000

        # 4. Periksa tipe data
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['price']))
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_df['rating']))
        self.assertTrue(pd.api.types.is_integer_dtype(cleaned_df['colors']))
        
        # 5. Pastikan kolom timestamp ada
        self.assertIn('timestamp', cleaned_df.columns)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)