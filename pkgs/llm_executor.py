import re
import copy
import os
import concurrent.futures
import time
import json
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
import concurrent.futures
import copy


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
                "temperature": 0.3,
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
            # print("safety_settings: \n", self.safety_settings)
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



