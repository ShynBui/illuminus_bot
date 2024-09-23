from pkgs import QuotaManager
import pandas as pd
import os
from dotenv import load_dotenv
from pkgs.prompt import gen_data_for_train
import copy



load_dotenv()
executor = QuotaManager(model_name=os.getenv('LLM_MODEL_'), api_keys=eval(os.getenv('LIST_GEMINI_API_KEY')))

if __name__ == '__main__':
    model_input = copy.deepcopy(gen_data_for_train['model_input'])
    user_input = copy.deepcopy(gen_data_for_train['user_input'])
    user_input += 'Parameters:\n'
    user_input += f'''- David's Emotion: Confused
- Choi's Emotion: Funny
- Conversation Topic: Happy Memories
- Language: Mixed English-Korean
- Choi's Role: Motivator'''
    output = executor.execute(model_input=model_input, user_input=user_input, json_output=True)
    print(output)
    print(type(output))

