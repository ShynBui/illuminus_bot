import time
import os
import copy
import concurrent.futures
from pkgs import LangChainExecutor
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class QuotaManager(LangChainExecutor):
    def __init__(self, model_name, api_keys):
        """
        Khởi tạo QuotaManager với danh sách các API key.

        :param model_name: Tên của mô hình LLM.  #gpt-... pr gemini-...
        :param api_keys: Danh sách các API key.
        """

        self.api_keys = api_keys
        self.current_key_index = 0
        self.last_used_time = time.time()

        if 'gpt' in model_name or 'openai' in model_name:
            # Nếu model_name là gpt hoặc openai, sử dụng LangChainExecutor
            print(f"{model_name} model ready")
            super().__init__(model_name)
            self.use_quota = False
        else:
            # Ngược lại, sử dụng cơ chế xoay API key của QuotaManager
            print(f"{model_name} model ready")
            super().__init__(model_name)
            self.update_api_key()
            self.use_quota = True

    def update_api_key(self):
        """
        Cập nhật API key hiện tại từ danh sách.
        """
        self.api_key = self.api_keys[self.current_key_index]
        os.environ["GEMINI_API_KEY"] = self.api_key
        # print(f"Đang sử dụng API key: {self.api_key}")

    def rotate_api_key(self):
        """
        Xoay vòng sang API key tiếp theo khi API key hiện tại bị giới hạn.
        """
        if self.use_quota:
            current_time = time.time()

            # Kiểm tra thời gian, nếu đã qua 60 giây kể từ lần sử dụng cuối, đặt lại chỉ số key
            if current_time - self.last_used_time >= 60:
                self.current_key_index = 0
            else:
                # Chuyển sang API key tiếp theo
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

            self.update_api_key()
            self.last_used_time = current_time

    def execute(self, model_input, user_input, model_name="", temperature=0, prefix=None, infix=None, suffix=None,
                json_output=False):
        """
        Thực thi yêu cầu với kiểm tra và thay đổi API key nếu cần thiết.

        :param model_input: Đầu vào cho mô hình.
        :param user_input: Đầu vào từ người dùng.
        :param model_name: Tên mô hình (tuỳ chọn).
        :param temperature: Nhiệt độ điều chỉnh tính ngẫu nhiên của mô hình.
        :param prefix: Chuỗi tiền tố tuỳ chọn.
        :param infix: Chuỗi xen giữa tuỳ chọn.
        :param suffix: Chuỗi hậu tố tuỳ chọn.
        :param json_output: Cờ để xác định có trả về kết quả JSON hay không.
        :return: Kết quả từ mô hình.
        """
        if not self.use_quota:
            # print("Model:", )
            # Nếu đang sử dụng mô hình gpt hoặc openai, không sử dụng API key quota
            return super().execute(model_input, user_input, model_name, temperature, prefix, infix, suffix, json_output)
        else:
            # Sử dụng cơ chế xoay vòng API key của QuotaManager
            try:
                return super().execute(model_input, user_input, model_name, temperature, prefix, infix, suffix, json_output)
            except Exception as e:
                if "429" in str(e):
                    # print(f"API key bị giới hạn: {self.api_key}. Đang chuyển sang API key khác...")
                    self.rotate_api_key()
                    return self.execute(model_input, user_input, model_name, temperature, prefix, infix, suffix, json_output)
                else:
                    # print("Error: ", e)
                    pass
                    raise e

