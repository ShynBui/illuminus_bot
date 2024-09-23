import time
import os
import copy
import concurrent.futures
from pkgs import LangChainExecutor
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import multiprocessing

def process_request_batch_target(executor_instance, batch, result_queue):
    """
    Hàm mục tiêu để xử lý một nhóm các request bằng cách sử dụng ThreadPoolExecutor trong một tiến trình riêng.
    """
    def process_request_wrapper(index, request):
        try:
            result = executor_instance.process_request(index, request)
            result_queue.put((index, result))
        except Exception as exc:
            result_queue.put((index, (None, exc)))

    # print("Workers: ", len(batch))
    with concurrent.futures.ThreadPoolExecutor(max_workers= len(batch)) as executor:
        futures = {executor.submit(process_request_wrapper, index, request): index for index, request in batch}
        for future in concurrent.futures.as_completed(futures):
            pass  # Tương tác với futures nếu cần, hiện tại chỉ để đảm bảo futures được hoàn thành


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

    def execute_with_image(self, model_input, user_input, base64_image, model_name="", temperature=0, prefix=None,
                           infix=None, suffix=None, json_output=False):
        """
        Thực thi yêu cầu với ảnh, kiểm tra và thay đổi API key nếu cần thiết.

        :param model_input: Đầu vào cho mô hình.
        :param user_input: Đầu vào từ người dùng.
        :param base64_image: Ảnh được mã hóa base64.
        :param model_name: Tên mô hình (tuỳ chọn).
        :param temperature: Nhiệt độ điều chỉnh tính ngẫu nhiên của mô hình.
        :param prefix: Chuỗi tiền tố tuỳ chọn.
        :param infix: Chuỗi xen giữa tuỳ chọn.
        :param suffix: Chuỗi hậu tố tuỳ chọn.
        :param json_output: Cờ để xác định có trả về kết quả JSON hay không.
        :return: Kết quả từ mô hình.
        """
        if not self.use_quota:
            # Nếu đang sử dụng mô hình gpt hoặc openai, không sử dụng API key quota
            return super().execute_with_image(model_input, user_input, base64_image, model_name, temperature, prefix, infix, suffix, json_output)
        else:
            try:
                return super().execute_with_image(model_input, user_input, base64_image, model_name, temperature, prefix, infix, suffix, json_output)
            except Exception as e:
                if "429" in str(e):
                    # print(f"API key bị giới hạn: {self.api_key}. Đang chuyển sang API key khác...")
                    self.rotate_api_key()
                    return self.execute_with_image(model_input, user_input, base64_image, model_name, temperature, prefix, infix, suffix, json_output)
                else:
                    # print("Error:", e)
                    pass
                    raise e

    def batch_execute(self, requests):
        """
        Thực thi nhiều yêu cầu song song với việc kiểm tra và thay đổi API key nếu cần thiết.

        :param requests: Danh sách các yêu cầu.
        :return: Danh sách các phản hồi, tương ứng với từng yêu cầu.
        """
        responses = [None] * len(requests)

        def process_request(index, request):
            model_input = request.get("model_input", "")
            user_input = request.get("user_input", "")
            prefix = request.get("prefix", None)
            infix = request.get("infix", None)
            suffix = request.get("suffix", None)
            model_name = request.get("model_name", self.model_name)
            temperature = request.get("temperature", 0)
            base64_image = request.get("base64_image", None)
            json_output = request.get("json_output", False)

            if base64_image:
                result = self.execute_with_image(model_input, user_input, base64_image, model_name, temperature, prefix,
                                                 infix, suffix, json_output)
            else:
                result = self.execute(model_input, user_input, model_name, temperature, prefix, infix, suffix, json_output)

            responses[index] = result

        with concurrent.futures.ThreadPoolExecutor(30) as executor:
            futures = {executor.submit(process_request, i, request): i for i, request in enumerate(requests)}

            for future in concurrent.futures.as_completed(futures):
                index = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    # pass
                    responses[index] = f"Exception occurred: {exc}"

        return responses

    def process_request(self, index, request):
        model_input = request.get("model_input", "")
        user_input = request.get("user_input", "")
        prefix = request.get("prefix", None)
        infix = request.get("infix", None)
        suffix = request.get("suffix", None)
        model_name = request.get("model_name", self.model_name)
        temperature = request.get("temperature", 0)
        base64_image = request.get("base64_image", None)
        json_output = request.get("json_output", False)

        if base64_image:
            result = self.execute_with_image(
                model_input, user_input, base64_image, model_name,
                temperature, prefix, infix, suffix, json_output
            )
        else:
            result = self.execute(
                model_input, user_input, model_name, temperature,
                prefix, infix, suffix, json_output
            )
        return result

    def batch_execute_auto_recall(self, requests, timeout=20):
        """
        Execute multiple requests in parallel using ThreadPoolExecutor.
        If a request times out, retry it once more.
        If all results have been returned, return the results.
        Otherwise, throw an error.

        :param requests: List of request dictionaries.
        :param timeout: Maximum time to wait for each batch (in seconds).
        :return: List of responses corresponding to each request.
        """
        responses = [None] * len(requests)
        failed_indexes = list(range(len(requests)))
        max_retries = 1
        retry_count = {i: 0 for i in failed_indexes}
        batch_size = 20  # Adjust the batch size as needed

        while failed_indexes:
            # Create a ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
                future_to_index = {}
                # Submit tasks for failed indexes
                for index in failed_indexes:
                    request = requests[index]
                    future = executor.submit(self.process_request, index, request)
                    future_to_index[future] = index

                # Wait for all futures with a timeout
                done, not_done = concurrent.futures.wait(
                    future_to_index.keys(),
                    timeout=timeout,
                    return_when=concurrent.futures.ALL_COMPLETED
                )

                # Collect results and handle exceptions
                new_failed_indexes = []
                for future in future_to_index.keys():
                    index = future_to_index[future]
                    if future in done:
                        try:
                            result = future.result()
                            responses[index] = result  # Successfully processed
                        except Exception as exc:
                            error_message = str(exc)
                            print(f"Exception at index {index}: {error_message}")
                            if "Invalid json output" in error_message:
                                print("Json output is invalid")
                                try:
                                    responses[index] = super().extract_and_convert_to_json(error_message)
                                except Exception as exc:
                                    print(f"Exception at index {index}. Can not covert to Json: {error_message}")
                                    responses[index] = None
                            else:
                                retry_count[index] += 1
                                if retry_count[index] <= max_retries:
                                    print(f"Retrying index {index} due to exception.")
                                    new_failed_indexes.append(index)
                                else:
                                    print(f"Exception occurred: {exc}")
                                    responses[index] = None
                    else:
                        # Future did not complete in time
                        retry_count[index] += 1
                        if retry_count[index] <= max_retries:
                            print(f"Timeout at index {index}, retrying...")
                            new_failed_indexes.append(index)
                        else:
                            print(f"Request at index {index} failed after {max_retries} retries due to timeout.")
                            responses[index] = None
                            future.cancel()

            # Update the list of failed indexes for the next iteration
            failed_indexes = new_failed_indexes

            if not failed_indexes:
                print("All requests have been processed")
                break
            elif all(retry_count[index] > max_retries for index in failed_indexes):
                # All remaining requests have exceeded max retries
                raise Exception("Some requests failed after maximum retries.")

        # After processing, check if any element in responses is None
        if any(response is None for response in responses):
            raise Exception(f"Some responses are None after {max_retries + 1} processing:", [i for i, k in enumerate(responses) if k is None])

        return responses


