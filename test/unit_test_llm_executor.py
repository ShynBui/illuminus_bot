import os
import unittest
from unittest.mock import patch, MagicMock
from pkgs import LangChainExecutor


class TestLangChainExecutorUnit(unittest.TestCase):

    @patch('os.getenv')
    def test_init_default_config_gpt(self, mock_getenv):
        # Mock API key
        mock_getenv.return_value = "fake-api-key"
        executor = LangChainExecutor("gpt-3.5-turbo")

        self.assertEqual(executor.platform, 'gpt')
        self.assertEqual(executor.default_config["temperature"], 0)
        self.assertEqual(executor.default_config["max_tokens"], 1024)

    @patch('os.getenv')
    def test_init_default_config_gemini(self, mock_getenv):
        # Mock API key
        mock_getenv.return_value = "fake-api-key"
        executor = LangChainExecutor("gemini-1.5-flash")

        self.assertEqual(executor.platform, 'gemini')
        self.assertIn("temperature", executor.default_config)
        self.assertIn("top_p", executor.default_config)

    def test_clean_response(self):
        executor = LangChainExecutor("gpt-3.5-turbo")
        response = "```json\n{\"key\": \"value\"}\n```"
        cleaned_response = executor.clean_response(response)
        self.assertEqual(cleaned_response, '{"key": "value"}')

    def test_extract_and_convert_to_json_valid(self):
        executor = LangChainExecutor("gpt-3.5-turbo")
        error_message = "Some error {\"key\": \"value\"} end error"
        json_data = executor.extract_and_convert_to_json(error_message)
        self.assertEqual(json_data, {"key": "value"})


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, verbosity=2)