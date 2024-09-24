from pkgs.prompt import david_choi_prompt
from run import respond
from src import load_config_and_select, executor
import os
import copy
from dotenv import load_dotenv

load_dotenv()


def get_coversation(my_config=None):

    model_input = copy.deepcopy(david_choi_prompt['model_input'])

    if not my_config:
        my_config = load_config_and_select()

    user_input = copy.deepcopy(david_choi_prompt['user_input'])

    user_input += f'''
{{
  "previous_context": "David is not good now",
  "current_conversation": {{
    "David": "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand.",
    "Choi": "Yes, exactly, 아버지. You always made me feel safe. It was one of my favorite memories."
  }},
  "David's Emotion": "{my_config["David's Emotion"]}",
  "Choi's Emotion": "{my_config["Choi's Emotion"]}",
  "Topic of Conversation": "{my_config["Conversation Topic"]}",
  "Language": "{my_config["Language"]}",
  "Choi's Role": "{my_config["Choi's Role"]}"
}}\n'''

    user_input += "Output:\n"

    response = executor.execute(model_input=model_input, user_input=user_input, json_output=True)

    print(user_input)
    print(response)

    return response


if __name__ == '__main__':
    rp = get_coversation()
    print(type(rp))
