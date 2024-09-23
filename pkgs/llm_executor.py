import re
import copy
import os
import concurrent.futures
import time
import json
from langchain_core.runnables import RunnableLambda
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
import threading
import multiprocessing
import concurrent.futures
import copy

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


class LangChainExecutor:
    def __init__(self, model_name):
        self.init_default_config(model_name)

    def init_default_config(self, model_name):
        self.model_name = model_name
        self.platform = 'gpt' if 'gpt' in model_name else 'gemini'
        self.api_key = os.getenv("OPEN_AI_API_KEY") if self.platform == "gpt" else os.getenv("GEMINI_API_KEY")
        if self.platform == "gpt":
            self.default_config = {
                "temperature": 0,
                "max_tokens": 1024,
            }
        elif self.platform == "gemini":
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
            self.default_config = {
                "temperature": 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 1024,             
            }

    def create_model(self, model_name, cp_config):
        # redefine by model_name
        self.init_default_config(model_name)  
        if self.platform == "gpt":
            return ChatOpenAI(
                model=model_name,
                api_key=self.api_key,
                temperature=cp_config["temperature"],
                max_tokens=cp_config.get("max_tokens")
            )
        elif self.platform == "gemini":
            print("safety_settings: \n", self.safety_settings)
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=self.api_key,
                temperature=cp_config["temperature"],
                top_p=cp_config.get("top_p"),
                top_k=cp_config.get("top_k"),
                max_output_tokens=cp_config.get("max_output_tokens"),
                safety_settings=self.safety_settings
            )

        print("Model name use: ", model_name)

    def clean_response(self, response):
        if response.startswith("```") and response.endswith("```"):
            pattern = r'^(?:```json|```csv|```)\s*(.*?)\s*```$'
            return re.sub(pattern, r'\1', response, flags=re.DOTALL).strip()
        return response.strip()

    def extract_and_convert_to_json(self, error_message):
        """
            Lấy phần JSON từ thông báo lỗi.

            :param error_message: Chuỗi thông báo lỗi chứa JSON.
            :return: Chuỗi JSON được trích xuất.
            """
        try:
            # Tìm vị trí bắt đầu của '{' và kết thúc của '}'
            start_index = error_message.index('{')
            end_index = error_message.rindex('}') + 1

            # Trích xuất và trả về phần JSON
            json_part = error_message[start_index:end_index]
            json_string = json_part.replace("'", '"')
            json_resutl = json.loads(json_string)
            return json_resutl
        except ValueError as exc:
            print("Error ValueError in extract_and_convert_to_json")
            return None  # Nếu không tìm thấy, trả về None

    def execute(self, model_input, user_input, model_name="", temperature=0, prefix=None, infix=None, suffix=None, json_output=False):
        cp_config = copy.deepcopy(self.default_config)
        cp_config["temperature"] = temperature
        if model_name == "":
            model_name = self.model_name

        model = self.create_model(model_name, cp_config)

        full_prompt_parts = []

        if prefix:
            full_prompt_parts.append(prefix)
        if infix:
            full_prompt_parts.append(infix)
        full_prompt_parts.append(model_input)
        if suffix:
            full_prompt_parts.append(suffix)

        # Kết hợp các phần thành một chuỗi duy nhất
        full_prompt = "\n".join(full_prompt_parts)

        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", "{full_prompt}"),
                ("human", "{user_input}"),
            ]
        )

        if json_output:
            parser = JsonOutputParser()
            # parser = RunnableLambda(self.extract_and_convert_to_json)
        else:
            parser = StrOutputParser()

        run_chain = chat_template | model | parser

        map_args = {
            "full_prompt": full_prompt,
            "user_input": user_input,
        }
        response = run_chain.invoke(map_args)

        if json_output == False:
            # print('Yess')
            response = self.clean_response(response)

        # print("Nooo")

        return response

    def execute_with_image(self, model_input, user_input, base64_image, model_name="", temperature=0, prefix=None, infix=None, suffix=None, json_output=False):

        full_prompt_parts = []
        if prefix:
            full_prompt_parts.append(prefix)
        if infix:
            full_prompt_parts.append(infix)
        full_prompt_parts.append(model_input)
        if suffix:
            full_prompt_parts.append(suffix)

        # Kết hợp các phần thành một chuỗi duy nhất
        full_prompt = "\n".join(full_prompt_parts)


        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{full_prompt}\n{user_input}"),
                (
                    "user",
                    [
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                        }
                    ],
                ),
            ]
        )

        cp_config = copy.deepcopy(self.default_config)
        cp_config["temperature"] = temperature
        if model_name == "":
            model_name = self.model_name

        model = self.create_model(model_name, cp_config)

        if json_output:
            parser = JsonOutputParser()
            # parser = RunnableLambda(self.extract_and_convert_to_json)
        else:
            parser = StrOutputParser()

        run_chain = prompt | model | parser

        response = run_chain.invoke({
            "image_data": base64_image,
            "full_prompt": full_prompt,
            "user_input": user_input
        })

        if json_output == False:
            # print('Yess')
            response = self.clean_response(response)

        # print("Nooo")

        return response

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
        The goal is to reduce execution time.

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
            raise Exception("Some responses are None after processing.")

        return responses


