import os
import copy
import json

from pkgs import QuotaManager
from pkgs.prompt import check_is_infor, gen_long_term
from dotenv import load_dotenv
from src.analysis_message import executor

load_dotenv()

grand_executor = QuotaManager(model_name= os.getenv("LLM_MONITOR_GEMINI"), api_keys=eval(os.getenv("LIST_GEMINI_API_KEY")))
data_long_term = os.path.join(os.getcwd(), 'data', 'long_term_memo.json')


def load_long_term_memory():
    if os.path.exists(data_long_term):
        with open(data_long_term, 'r', encoding='utf-8') as file:
            try:
                long_term_memory = json.load(file)
                return long_term_memory
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON from long_term_memo.json.")
                return None
    else:
        print("Error: long_term_memo.json file does not exist.")
        return None


def check_if_have_infor(get_conversation):

    model_input = copy.deepcopy(check_is_infor['model_input'])

    user_input = copy.deepcopy(check_is_infor['user_input'])

    user_input += 'Input Message:\n'
    user_input += f'David: {get_conversation["David"]}\n\n'
    user_input += f'Choi: {get_conversation["Choi"]}\n\n'
    user_input += 'Output:\n'

    response = executor.execute(model_input=model_input, user_input=user_input, json_output=True)

    return response['answer']

def update_long_term_memory(new_data):
    # Load the current long term memory
    long_term_memory = load_long_term_memory()

    if long_term_memory is None:
        # If the file does not exist or cannot be decoded, create a new empty dictionary
        long_term_memory = {}

    # Merge the new data into the existing long term memory
    for key, value in new_data.items():
        if key in long_term_memory:
            # Update the existing data if the key already exists
            long_term_memory[key] = value
        else:
            # Add new key-value pairs to the memory
            long_term_memory[key] = value

    # Save the updated memory back to the file
    with open(data_long_term, 'w', encoding='utf-8') as file:
        json.dump(long_term_memory, file, ensure_ascii=False, indent=4)

    print("Long-term memory updated successfully.")

def gen_long_term_memory(get_conversation):

    model_input = copy.deepcopy(gen_long_term['model_input'])
    model_input += str(load_long_term_memory())

    user_input = copy.deepcopy(gen_long_term['user_input'])
    user_input += 'Take a deep breath, think step by step, and then analyze the following message:\n'
    user_input += f'David: {get_conversation["David"]}\n\n'
    user_input += f'Choi: {get_conversation["Choi"]}\n\n'
    user_input += 'Output:\n'

    while True:
        try:
            # Try executing and getting response
            response = grand_executor.execute(model_input=model_input, user_input=user_input, json_output=True)
            update_long_term_memory(response)
            return response
        except Exception as e:
            # Log or handle the exception here if necessary
            print(f"An error occurred: {e}")








