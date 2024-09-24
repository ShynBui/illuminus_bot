from pkgs.prompt import monitor_analyse
import copy
import os
from dotenv import load_dotenv
from pkgs import QuotaManager

load_dotenv()

executor = QuotaManager(model_name=os.getenv('LLM_MODEL_'), api_keys=eval(os.getenv('LIST_GEMINI_API_KEY')))

def analysis_message(message):
    model_input = copy.deepcopy(monitor_analyse['model_input'])

    user_input = copy.deepcopy(monitor_analyse['user_input'])
    user_input += 'Input:\n'
    user_input += "User's Message:\n"
    user_input += message + "\n"
    user_input += 'Output:\n'

    response = executor.execute(model_input=model_input, user_input=user_input, json_output=True)

    return response

if __name__ == '__main__':
    message = 'Tiếp tục từ cuộc trò chuyện trước đó, khi David lo lắng, và Choi cố gắng an ủi anh ấy. Họ nên tiếp tục nói về sức khỏe của anh ấy, và hãy giữ nguyên bằng tiếng Việt."'

    answer = analysis_message(message)
    print(answer)
    print(type(answer))