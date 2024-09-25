import gradio as gr
import json
import os
import logging
from huggingface_hub import InferenceClient
from src.chatbot import get_conversation, get_conversation_with_retrieve
from src import load_config_and_select, analysis_message, check_if_have_infor, gen_long_term_memory, \
    load_long_term_memory, load_conversation, create_or_load_vectorstore_and_retriever

# Cấu hình logger
logging.basicConfig(filename=os.path.join(os.getcwd(),'logs','app.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Đường dẫn đến file lưu lịch sử cuộc trò chuyện
conversation_file_path = os.path.join(os.getcwd(), 'data', 'conversation_data.json')

# Load những đoạn hội thoại mẫu
conversation_data = load_conversation()

_, retriever = create_or_load_vectorstore_and_retriever(conversation_data, update=False)


def load_last_conversation():
    """Đọc tin nhắn gần nhất từ file conversation_data.json"""
    logging.info("Loading the last conversation from the file.")
    if os.path.exists(conversation_file_path):
        with open(conversation_file_path, 'r') as file:
            conversation_data = json.load(file)
            if conversation_data:
                logging.info("Successfully loaded last conversation.")
                return conversation_data[-1]
    logging.warning("No conversation file found or the conversation is empty.")
    return None


def save_conversation(conversation_entry):
    """Lưu tin nhắn vào file conversation_data.json"""
    conversation_data = []
    if os.path.exists(conversation_file_path):
        with open(conversation_file_path, 'r') as file:
            conversation_data = json.load(file)

    conversation_data.append(conversation_entry)

    with open(conversation_file_path, 'w') as file:
        json.dump(conversation_data, file, indent=4)

    logging.info(f"Conversation saved: {conversation_entry}")


def respond(
        message,
        history: list[str],
        choi_emotion,
        david_emotion,
        conversation_topic,
        language,
        choi_role,
        retrieve_old_conversation,
):
    logging.info(f"New message received: {message}")

    if message != '':  # Nếu người dùng gửi tin nhắn
        message_analyse = analysis_message(message)  # Phân tích tin nhắn
        logging.info(f"Message analyzed: {message_analyse}")
    else:
        message_analyse = {'previous_context': None,
                           "David's Emotion": None,
                           "Choi's Emotion": None,
                           'Topic of Conversation': None,
                           'Language': None,
                           "Choi's Role": None}

    last_conversation = load_last_conversation()
    previous_context = last_conversation['previous_context'] if last_conversation else "No previous context available"
    david_last_conversation = last_conversation['conversation'][0]['text'] if last_conversation else ""
    choi_last_conversation = last_conversation['conversation'][1]['text'] if last_conversation else ""

    my_config = {
        "Choi's Emotion": choi_emotion,
        "David's Emotion": david_emotion,
        "Conversation Topic": conversation_topic,
        "Language": language,
        "Choi's Role": choi_role,
        "previous_context": previous_context,
        "David_last_conversation": david_last_conversation,
        "Choi_last_conversation": choi_last_conversation,
    }

    for item, value in message_analyse.items():
        if value:
            my_config[item] = value

    if retrieve_old_conversation:
        data_query = f'''David ({my_config["David's Emotion"]}): {my_config["David_last_conversation"]}\nChoi: {my_config["Choi's Emotion"]}: {my_config["Choi_last_conversation"]}
The conversation in: {language}
Topic of Conversation: {conversation_topic}
The previous context: {previous_context}
'''
        try:
            query_in_db = retriever.invoke(data_query)[0]
            get_next_conversation_id = query_in_db.metadata['index']
            logging.info(f"Retrieved similar conversation with ID: {get_next_conversation_id}")
            my_config['exmaple_conversation'] = conversation_data[int(get_next_conversation_id) + 1]
        except Exception as e:
            logging.error(f"Error retrieving conversation: {e}")
            my_config['exmaple_conversation'] = conversation_data[0]

    long_term_json = load_long_term_memory()

    if retrieve_old_conversation:
        my_config["David_last_conversation"] = my_config['exmaple_conversation']['conversation'][0]['text']
        my_config["Choi_last_conversation"] = my_config['exmaple_conversation']['conversation'][1]['text']

        response = get_conversation_with_retrieve(my_config=my_config, long_term_memory=long_term_json)
    else:
        response = get_conversation(my_config=my_config, long_term_memory=long_term_json)

    summarize_context = response['summarize_context']
    current_conversation = response['next_conversation']

    response_text = f"Summary: {summarize_context}\n\nDavid: {current_conversation['David']}\nChoi: {current_conversation['Choi']}"
    logging.info(f"Response generated: {response_text}")

    conversation_entry = {
        "previous_context": summarize_context,
        "topic": conversation_topic,
        "language": language,
        "conversation": [
            {
                "speaker": "David",
                "emotion": david_emotion,
                "text": current_conversation['David']
            },
            {
                "speaker": "Choi",
                "role": choi_role,
                "emotion": choi_emotion,
                "text": current_conversation['Choi']
            }
        ]
    }
    save_conversation(conversation_entry)

    check_important_info = check_if_have_infor(current_conversation)
    str_long_term_mem = '<h1> Long term Memory </h1>'

    if check_important_info:
        long_term_mem = gen_long_term_memory(current_conversation)

        for item, value in long_term_mem.items():
            str_long_term_mem += f'<b>{item}</b>: {value}<br>\n'
    else:
        for item, value in long_term_json.items():
            str_long_term_mem += f'<b>{item}</b>: {value} <br>\n'

    combined_message = f"David: {current_conversation['David']}\n\nChoi: {current_conversation['Choi']}"
    updated_history = history + [(combined_message, "Monitor request: \n" + str(
        message_analyse) if message != '' else 'Monitor không đưa ra yêu cầu')]

    return updated_history, f"{str_long_term_mem}"


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(label="Chat between David and Choi")
            message_input = gr.Textbox(label="Enter your message", placeholder="Type your message here")

            choi_emotion = gr.Dropdown(choices=["comforting", "supportive", "nostalgic", "joyful", "patient"],
                                       value="comforting", label="Choi's Emotion")
            david_emotion = gr.Dropdown(choices=["warm", "confused", "worried", "sad", "humorous"], value="confused",
                                        label="David's Emotion")
            conversation_topic = gr.Dropdown(
                choices=["Choi's childhood memories", "David's old job in the U.S.", "David's early days in Korea",
                         "David's current health", "Choi's achievements in research"],
                value="David's old job in the U.S.", label="Conversation Topic")
            language = gr.Dropdown(choices=["English", "Korean", "Mixed English-Korean"], value="Mixed English-Korean",
                                   label="Language")
            choi_role = gr.Dropdown(choices=["Son", "Doctor", "Humorous storyteller", "Motivational speaker"],
                                    value="Son", label="Choi's Role")

            retrieve_toggle = gr.Checkbox(label="Retrieve old conversation", value=False)
            submit_btn = gr.Button("Submit")

        with gr.Column(scale=2):
            user_message_display = gr.HTML("""
            <div style='height: 100%; display: flex; align-items: center; justify-content: center;' id="user_message_display">
                <p style='font-size: 20px; color: gray;'>Long term memory</p>
            </div>
            """)

    submit_btn.click(respond,
                     inputs=[message_input, chatbot, choi_emotion, david_emotion, conversation_topic, language,
                             choi_role, retrieve_toggle],
                     outputs=[chatbot, user_message_display])

if __name__ == "__main__":
    logging.info("Launching Gradio application.")
    demo.launch()
