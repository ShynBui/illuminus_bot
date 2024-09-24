import gradio as gr
import json
import os
from huggingface_hub import InferenceClient
from src.chatbot import get_conversation
from src import load_config_and_select, analysis_message

# Đường dẫn đến file lưu lịch sử cuộc trò chuyện
conversation_file_path = os.path.join(os.getcwd(), 'data', 'conversation_data.json')

def load_last_conversation():
    """Đọc tin nhắn gần nhất từ file conversation_data.json"""
    if os.path.exists(conversation_file_path):
        with open(conversation_file_path, 'r') as file:
            conversation_data = json.load(file)
            if conversation_data:
                return conversation_data[-1]
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

def respond(
    message,
    history: list[tuple[str, str]],
    choi_emotion,
    david_emotion,
    conversation_topic,
    language,
    choi_role,
):
    if message != '':
        message_analyse = analysis_message(message)
    else:
        message_analyse = {'previous_context': None,
                           "David's Emotion": None,
                           "Choi's Emotion": None,
                           'Topic of Conversation': None,
                           'Language': None,
                           "Choi's Role": None}

    # Đọc tin nhắn gần nhất để tạo context cho cuộc trò chuyện mới
    last_conversation = load_last_conversation()
    previous_context = last_conversation['previous_context'] if last_conversation else "No previous context available"

    # Lấy đoạn hội thoại gần nhất của cả David và Choi
    david_last_conversation = last_conversation['conversation'][0]['text'] if last_conversation else ""
    choi_last_conversation = last_conversation['conversation'][1]['text'] if last_conversation else ""

    # Tạo config từ các lựa chọn được chọn trong giao diện Gradio
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

    # Gọi hàm get_conversation với cấu hình đã chọn
    response = get_conversation(my_config=my_config)

    summarize_context = response['summarize_context']
    current_conversation = response['next_conversation']

    # Tạo response từ summarize_context và current_conversation
    response_text = f"Summary: {summarize_context}\n\nDavid: {current_conversation['David']}\nChoi: {current_conversation['Choi']}"

    # Lưu cuộc trò chuyện vào file JSON
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

    yield response_text


demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        # Các lựa chọn cho cảm xúc, chủ đề, ngôn ngữ, và vai trò
        gr.Dropdown(choices=["comforting", "supportive", "nostalgic", "joyful", "patient"], value="comforting", label="Choi's Emotion"),
        gr.Dropdown(choices=["warm", "confused", "worried", "sad", "humorous"], value="confused", label="David's Emotion"),
        gr.Dropdown(choices=["Choi's childhood memories", "David's old job in the U.S.", "David's early days in Korea", "David's current health", "Choi's achievements in research"], value="David's old job in the U.S.", label="Conversation Topic"),
        gr.Dropdown(choices=["English", "Korean", "Mixed English-Korean"], value="Mixed English-Korean", label="Language"),
        gr.Dropdown(choices=["Son", "Doctor", "Humorous storyteller", "Motivational speaker"], value="Son", label="Choi's Role"),
    ],
)


if __name__ == "__main__":
    demo.launch()
