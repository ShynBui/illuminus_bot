import unittest
from unittest.mock import patch, MagicMock
import os

# Giả sử file của bạn là 'analysis_module.py'
from src import analysis_message


class TestAnalysisMessage(unittest.TestCase):

    @patch('src.analysis_module.QuotaManager')
    @patch('src.analysis_module.os.getenv')
    def test_analysis_message(self, mock_getenv, mock_quota_manager):
        # Mock giá trị trả về của các biến môi trường
        mock_getenv.side_effect = lambda key: 'mocked_model' if key == 'LLM_MODEL_' else '["mocked_api_key"]'

        # Tạo mock executor
        mock_executor_instance = MagicMock()
        mock_executor_instance.execute.return_value = {'answer': 'mocked response'}

        # Gán mock executor vào mock QuotaManager
        mock_quota_manager.return_value = mock_executor_instance

        # Giả lập một thông điệp để phân tích
        message = 'David lo lắng và Choi đang an ủi anh ấy về sức khỏe.'

        # Gọi hàm analysis_message với message giả lập
        result = analysis_message(message)

        # Kiểm tra nếu hàm execute đã được gọi với các tham số mong đợi
        mock_executor_instance.execute.assert_called_once()

        # Kiểm tra kết quả trả về từ hàm analysis_message
        self.assertEqual(result, {'answer': 'mocked response'})

    @patch('src.analysis_module.QuotaManager')
    @patch('src.analysis_module.os.getenv')
    def test_analysis_message_with_empty_message(self, mock_getenv, mock_quota_manager):
        # Mock các biến môi trường giống như test trước
        mock_getenv.side_effect = lambda key: 'mocked_model' if key == 'LLM_MODEL_' else '["mocked_api_key"]'

        # Tạo mock executor
        mock_executor_instance = MagicMock()
        mock_executor_instance.execute.return_value = {'answer': 'empty message response'}

        # Gán mock executor vào mock QuotaManager
        mock_quota_manager.return_value = mock_executor_instance

        # Giả lập một thông điệp rỗng
        message = ''

        # Gọi hàm analysis_message với thông điệp rỗng
        result = analysis_message(message)

        # Kiểm tra nếu hàm execute đã được gọi
        mock_executor_instance.execute.assert_called_once()

        # Kiểm tra kết quả trả về
        self.assertEqual(result, {'answer': 'empty message response'})



if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, verbosity=2)


