from pkgs.prompt import david_choi_prompt
from src import load_config_and_select, executor
import os
import copy
from dotenv import load_dotenv

load_dotenv()


def get_conversation(my_config=None):

    model_input = copy.deepcopy(david_choi_prompt['model_input'])

    if not my_config:
        my_config = load_config_and_select()
        my_config["previous_context"] = 'David is not good now'
        my_config["David_last_conversation"] = "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand."
        my_config["Choi_last_conversation"] = "Yes, exactly, 아버지. You always made me feel safe. It was one of my favorite memories."

    user_input = copy.deepcopy(david_choi_prompt['user_input'])
    user_input += 'Input:\n'
    user_input += f'''
{{
  "previous_context": "{my_config["previous_context"]}",
  "current_conversation": {{
    "David": {my_config["David_last_conversation"]},
    "Choi": {my_config["Choi_last_conversation"]}
  }},
  "David's Emotion": "{my_config["David's Emotion"]}",
  "Choi's Emotion": "{my_config["Choi's Emotion"]}",
  "Topic of Conversation": "{my_config["Conversation Topic"]}",
  "Language": "{my_config["Language"]}",
  "Choi's Role": "{my_config["Choi's Role"]}"
}}\n'''

    user_input += f'Output in {my_config["Language"]}:\n'

    while True:
        try:
            response = executor.execute(model_input=model_input, user_input=user_input, json_output=True)
            print(user_input)
            print(response)
            return response
        except Exception as e:
            print(f"Error encountered: {e}")
            print("Retrying...")

if __name__ == '__main__':
    rp = get_conversation()
    print(type(rp))
