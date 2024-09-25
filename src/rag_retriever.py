from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import os
import json
from dotenv import load_dotenv
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI

# Load biến môi trường
load_dotenv()

# Đường dẫn tới file dữ liệu cuộc hội thoại
conversation_file_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'test_data.json') if os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'data', 'test_data.json')) else os.path.join(os.getcwd(), 'data', 'test_data.json')

# Đường dẫn lưu trữ vector store
vectorstore_dir = os.path.join(os.path.dirname(os.getcwd()), 'data', 'vectorstore')

# Metadata field info
metadata_field_info = [
    AttributeInfo(
        name="topic",
        description="The main topic of the conversation, such as 'David's current health'",
        type="string"
    ),
    AttributeInfo(
        name="language",
        description="The language of the conversation, such as 'English' or 'Korean'",
        type="string"
    ),
    AttributeInfo(
        name="previous_context",
        description="The context that sets the stage for the current conversation",
        type="string"
    )
]


# Hàm load dữ liệu từ file JSON
def load_conversation(config_path=conversation_file_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        conversation = json.load(f)
    return conversation


# Hàm tạo documents từ dữ liệu cuộc hội thoại
def create_documents_from_data(data):
    documents = []
    for index, entry in enumerate(data):
        conversation_text = " ".join(
            [f"{turn['speaker']} ({turn['emotion']}): {turn['text']}" for turn in entry['conversation']]
        )
        # Tạo Document với metadata
        doc = Document(
            page_content=conversation_text,
            metadata={
                "previous_context": entry.get("previous_context"),
                "topic": entry.get("topic"),
                "language": entry.get("language"),
                "index": index,
            }
        )
        documents.append(doc)
    return documents


# Hàm tạo hoặc tải vectorstore và retriever từ dữ liệu
def create_or_load_vectorstore_and_retriever(conversation_data, update=False):
    # Kiểm tra biến môi trường
    embedding_model = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')  # Đặt mặc định nếu không có giá trị
    gpt_model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    openai_api_key = os.getenv('OPEN_AI_KEY')

    if not openai_api_key:
        raise ValueError("OPEN_AI_KEY environment variable is not set.")

    # Kiểm tra xem vectorstore đã tồn tại chưa
    if os.path.exists(vectorstore_dir):
        # Nếu đã tồn tại, tải lại vectorstore từ ổ đĩa
        vectorstore = Chroma(persist_directory=vectorstore_dir,
                             embedding_function=OpenAIEmbeddings(model=embedding_model, openai_api_key=openai_api_key))
        print("Vectorstore loaded from disk.")
    else:
        # Nếu chưa tồn tại, tạo documents và lưu lại vectorstore
        documents = create_documents_from_data(conversation_data)
        vectorstore = Chroma.from_documents(documents,
                                            OpenAIEmbeddings(model=embedding_model, openai_api_key=openai_api_key),
                                            persist_directory=vectorstore_dir)
        print("Vectorstore created and saved to disk.")

    # Cập nhật vectorstore nếu cần
    if update:
        new_documents = create_documents_from_data(conversation_data)  # Tạo documents mới từ dữ liệu cập nhật
        vectorstore.add_documents(new_documents)  # Thêm tài liệu mới
        print("Vectorstore updated with new documents and saved to disk.")

    # Sử dụng ChatOpenAI
    llm = ChatOpenAI(temperature=0, api_key=openai_api_key, model=gpt_model)

    # Tạo SelfQueryRetriever
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectorstore,
        "Conversation between David and Choi",
        metadata_field_info,
        enable_limit=True
    )

    return vectorstore, retriever


# Main function
if __name__ == '__main__':
    conversation_data = load_conversation()
    print(conversation_data[15])

    # Cập nhật vectorstore nếu có dữ liệu mới
    vectorstore, retriever = create_or_load_vectorstore_and_retriever(conversation_data, update=False)

    # Kiểm tra kết quả
    print(retriever.invoke("David and Choi are reminiscing about their childhood trips to the beach.")[0].metadata['index'])
    print(retriever.invoke("David and Choi are reminiscing about their childhood trips to the beach.")[0])