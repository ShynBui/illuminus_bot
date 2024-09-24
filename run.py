import gradio as gr
import json
import os
from huggingface_hub import InferenceClient
from src.chatbot import get_conversation
from src import load_config_and_select, analysis_message, check_if_have_infor, gen_long_term_memory, load_long_term_memory

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
        history: list[str],  # Điều chỉnh định dạng history
        choi_emotion,
        david_emotion,
        conversation_topic,
        language,
        choi_role,
):
    if message != '':  # Nếu người dùng gửi tin nhắn
        message_analyse = analysis_message(message)  # Phân tích tin nhắn
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
    long_term_json = load_long_term_memory()

    response = get_conversation(my_config=my_config, long_term_memory=long_term_json)

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

    #Update long-term-memory:
    check_important_info = check_if_have_infor(current_conversation)
    str_long_term_mem = '<h1> Long term Memory </h1>'

    if check_important_info:
        long_term_mem = gen_long_term_memory(current_conversation)

        for item, value in long_term_mem.items():
            str_long_term_mem += f'<b>{item}</b>: {value}<br>\n'
    else:
        for item, value in long_term_json.items():
            str_long_term_mem += f'<b>{item}</b>: {value} <br>\n'


    # Hiển thị tin nhắn của David và Choi trong cùng một box
    combined_message = f"David: {current_conversation['David']}\n\nChoi: {current_conversation['Choi']}"

    updated_history = history + [(combined_message, "Monitor request: \n" + str(message_analyse) if message != '' else 'Monitor không đưa ra yêu cầu')]  # Gộp tin nhắn David và Choi lại thành một message trong history
    return updated_history, f"{str_long_term_mem}"


with gr.Blocks() as demo:
    with gr.Row():
        # Cột bên trái: khung chat giữa David và Choi
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(label="Chat between David and Choi")
            message_input = gr.Textbox(label="Enter your message", placeholder="Type your message here")

            # Các lựa chọn cho cảm xúc, chủ đề, ngôn ngữ, và vai trò
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

            submit_btn = gr.Button("Submit")

        # Cột bên phải: hiển thị tin nhắn của người dùng
        with gr.Column(scale=2):
            user_message_display = gr.HTML("""
            <div style='height: 100%; display: flex; align-items: center; justify-content: center;' id="user_message_display">
                <p style='font-size: 20px; color: gray;'>Long term memory</p>
            </div>
            """)


    # Cập nhật khung chat với tin nhắn của David và Choi, và hiển thị tin nhắn người dùng bên phải khi nhấn nút submit
    def update_ui(chat_history, user_message):
        # Cập nhật hiển thị bên phải với tin nhắn của người dùng
        user_message_display.update(f"""
        <div style='height: 100%; display: flex; align-items: center; justify-content: center;' id="user_message_display">
            <p style='font-size: 20px; color: gray;'>Long term memory\n: {user_message}</p>
        </div>
        """)
        # Trả về lịch sử trò chuyện
        return chat_history


    submit_btn.click(respond,
                     inputs=[message_input, chatbot, choi_emotion, david_emotion, conversation_topic, language,
                             choi_role],
                     outputs=[chatbot, user_message_display])

if __name__ == "__main__":
    demo.launch()
