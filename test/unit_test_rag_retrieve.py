import unittest
from unittest.mock import patch, MagicMock
from pkgs import QuotaManager


class TestQuotaManager(unittest.TestCase):

    @patch('os.getenv')
    def test_quota_manager_initialization(self, mock_getenv):
        mock_getenv.return_value = "fake_api_key"

        # Khởi tạo QuotaManager
        model_name = "gpt-3.5-turbo"
        api_keys = ["api_key_1", "api_key_2"]
        manager = QuotaManager(model_name, api_keys)

        # Kiểm tra xem class có khởi tạo đúng không
        self.assertEqual(manager.api_keys, api_keys)
        self.assertEqual(manager.current_key_index, 0)
        self.assertEqual(manager.use_quota, False)
        self.assertFalse(manager.use_quota)

    @patch('os.getenv')
    def test_quota_manager_gemini_initialization(self, mock_getenv):
        mock_getenv.return_value = "fake_api_key"

        # Khởi tạo QuotaManager với mô hình gemini
        model_name = "gemini"
        api_keys = ["api_key_1", "api_key_2"]
        manager = QuotaManager(model_name, api_keys)

        # Kiểm tra xem class có khởi tạo đúng không
        self.assertEqual(manager.api_keys, api_keys)
        self.assertEqual(manager.current_key_index, 0)
        self.assertTrue(manager.use_quota)

    @patch('os.environ', {})
    def test_rotate_api_key(self):
        # Khởi tạo QuotaManager với nhiều API keys
        model_name = "gemini"
        api_keys = ["api_key_1", "api_key_2", "api_key_3"]
        manager = QuotaManager(model_name, api_keys)

        # Xoay vòng API key và kiểm tra
        manager.rotate_api_key()
        self.assertEqual(manager.api_key, "api_key_2")

        manager.rotate_api_key()
        self.assertEqual(manager.api_key, "api_key_3")

        manager.rotate_api_key()
        self.assertEqual(manager.api_key, "api_key_1")  # Quay lại key đầu tiên

    @patch('pkgs.LangChainExecutor.execute')
    @patch('os.getenv')
    def test_execute_with_quota_rotation(self, mock_getenv, mock_execute):
        mock_getenv.return_value = "fake_api_key"

        # Giả lập lỗi 429 từ lần gọi đầu tiên
        mock_execute.side_effect = [Exception("429 Too Many Requests"), "Successful Response"]

        # Khởi tạo QuotaManager
        model_name = "gemini"
        api_keys = ["api_key_1", "api_key_2"]
        manager = QuotaManager(model_name, api_keys)

        result = manager.execute("input", "user input")

        # Kiểm tra rằng API key đã xoay vòng và kết quả cuối cùng thành công
        self.assertEqual(manager.api_key, "api_key_2")
        self.assertEqual(result, "Successful Response")


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, verbosity=2)


