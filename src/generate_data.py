import os
import copy
import json
import random
from dotenv import load_dotenv
from pkgs import QuotaManager
from pkgs.prompt import gen_data_for_train

# Load environment variables
load_dotenv()

# Initialize QuotaManager, config_path, train_data_path with environment variables
executor = QuotaManager(model_name=os.getenv('LLM_MODEL_'), api_keys=eval(os.getenv('LIST_GEMINI_API_KEY')))
config_path = os.path.join(os.path.dirname(os.getcwd()), 'config', 'generate_data_config.json')
train_data_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'train_data.json')
test_data_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'test_data.json')

# Function to choose a random value based on weighted probability
def weighted_choice(choices):
    items = list(choices.keys())
    weights = list(choices.values())
    return random.choices(items, weights=weights, k=1)[0]

# Function to load config file and select random parameters
def load_config_and_select(config_path=config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Randomly select values based on the weighted probabilities
    chosen_parameters = {
        "Choi's Emotion": weighted_choice(config["Choi's Emotion"]),
        "David's Emotion": weighted_choice(config["David's Emotion"]),
        "Conversation Topic": weighted_choice(config["Conversation Topic"]),
        "Language": weighted_choice(config["Language"]),
        "Choi's Role": weighted_choice(config["Choi's Role"])
    }

    return chosen_parameters


def load_existing_data(output_path):
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()  # Remove any leading/trailing whitespace
                if file_content:  # If the file is not empty
                    return json.loads(file_content)
                else:
                    return []  # Return empty list if the file is empty
        except json.JSONDecodeError:
            print(f"Warning: The file {output_path} does not contain valid JSON. Returning an empty list.")
            return []  # Return empty list if JSON is invalid
    else:
        return []  # Return empty list if file does not exist


# Define the function to generate data and save it to a JSON file
def generate_and_save_data(output_path=train_data_path, config_path=config_path):
    # Deep copy input data to avoid mutation
    model_input = copy.deepcopy(gen_data_for_train['model_input'])
    user_input = copy.deepcopy(gen_data_for_train['user_input'])

    # Load config and select random parameters
    selected_params = load_config_and_select(config_path)

    # Add parameters to user_input
    user_input += 'Parameters:\n'
    user_input += f'''- David's Emotion: {selected_params["David's Emotion"]}
- Choi's Emotion: {selected_params["Choi's Emotion"]}
- Conversation Topic: {selected_params["Conversation Topic"]}
- Language: {selected_params["Language"]}
- Choi's Role: {selected_params["Choi's Role"]}'''

    # Execute the model with the prepared inputs
    output = executor.execute(model_input=model_input, user_input=user_input, json_output=True)

    # Load existing data from file if it exists
    existing_data = load_existing_data(output_path)

    # Append new output to the list of existing data
    existing_data.append(output)

    # Ensure the directory exists before saving the file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the updated list of data to the specified JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Data saved successfully to {output_path}")

# Call the function
if __name__ == '__main__':
    #Generate data_train
    for i in range(400):
        generate_and_save_data()

    # #Generate data_test
    for i in range(10):
        generate_and_save_data(output_path=test_data_path)
