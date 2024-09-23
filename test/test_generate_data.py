import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys

# Add src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

# Import the functions to test
from src.generate_data import load_existing_data, generate_and_save_data, load_config_and_select

class TestGenerateData(unittest.TestCase):

    @patch('src.generate_data.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"test": "data"}]')
    def test_load_existing_data_with_valid_json(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = load_existing_data('fake_path')
        self.assertEqual(result, [{"test": "data"}])
        mock_file.assert_called_once_with('fake_path', 'r', encoding='utf-8')

    @patch('src.generate_data.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_load_existing_data_with_empty_file(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = load_existing_data('fake_path')
        self.assertEqual(result, [])
        mock_file.assert_called_once_with('fake_path', 'r', encoding='utf-8')

    @patch('src.generate_data.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid_json')
    def test_load_existing_data_with_invalid_json(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = load_existing_data('fake_path')
        self.assertEqual(result, [])
        mock_file.assert_called_once_with('fake_path', 'r', encoding='utf-8')

    @patch('src.generate_data.os.path.exists')
    def test_load_existing_data_when_file_does_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = load_existing_data('fake_path')
        self.assertEqual(result, [])


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, verbosity=2)
