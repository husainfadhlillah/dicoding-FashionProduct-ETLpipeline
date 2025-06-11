# tests/test_load.py

import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

# Import fungsi yang akan di-test
from utils.load import load_to_csv, load_to_gsheets, load_to_postgres

@pytest.fixture
def sample_dataframe():
    """Fixture untuk menyediakan DataFrame sampel."""
    return pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})

def test_load_to_csv(mocker, sample_dataframe):
    """Menguji fungsi load_to_csv."""
    # Mock method to_csv dari pandas DataFrame
    mock_to_csv = mocker.patch.object(pd.DataFrame, 'to_csv')
    
    load_to_csv(sample_dataframe, 'test.csv')
    
    # Pastikan mock dipanggil sekali dengan argumen yang benar
    mock_to_csv.assert_called_once_with('test.csv', index=False)

def test_load_to_gsheets(mocker, sample_dataframe):
    """Menguji fungsi load_to_gsheets."""
    # Mock seluruh rantai pemanggilan gspread
    mock_creds = mocker.patch('utils.load.Credentials.from_service_account_file')
    mock_client = mocker.patch('utils.load.gspread.authorize')
    mock_worksheet = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_client.return_value.open_by_url.return_value = mock_spreadsheet

    load_to_gsheets(sample_dataframe, 'creds.json', 'sheet_url')

    # Pastikan method update dipanggil
    assert mock_worksheet.clear.called
    assert mock_worksheet.update.called

def test_load_to_postgres(mocker, sample_dataframe):
    """Menguji fungsi load_to_postgres."""
    # Mock create_engine dan method to_sql
    mock_create_engine = mocker.patch('utils.load.create_engine')
    mock_to_sql = mocker.patch.object(pd.DataFrame, 'to_sql')

    load_to_postgres(sample_dataframe, 'db_uri', 'table')

    # Pastikan mock dipanggil
    mock_create_engine.assert_called_once_with('db_uri')
    mock_to_sql.assert_called_once_with('table', mock_create_engine.return_value, if_exists='replace', index=False)