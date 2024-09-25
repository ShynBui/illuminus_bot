# Human-Like Chatbot System Using RAG and Qwen

## Introduction

The **Human-Like Chatbot System** is designed to create dynamic and emotionally resonant conversations between David, a father suffering from Alzheimer's, and his son Choi. The system's primary objective is to build a long-term memory that evolves over time, allowing the chatbot to provide personalized and emotionally aware responses.

The system utilizes **RAG (Retrieval-Augmented Generation)** technology, which combines a large language model (LLM) with information retrieval from a memory base. This enables the chatbot to generate contextually appropriate, human-like responses that maintain continuity across multiple interactions.
## Key Features

- **Long-Term Memory**: Captures critical information from previous conversations to enhance future interactions. This includes emotional states, health conditions, and relationship dynamics.

- **Emotional Responses**: Tracks and generates emotionally aligned responses for both David and Choi. Depending on the situation, the chatbot can express support, comfort, or motivation.

- **Role Customization**: Choi can adopt various roles, such as a caring son, humorous storyteller, or motivational speaker, depending on the context or user requirements.

- **Multi-language Support**: The system can handle mixed-language responses, including English, Korean, or a combination of both, based on user input.

- **Monitor Feedback**: A built-in system allows a monitor to adjust conversation parameters, such as the emotional tone or topic of discussion, in real-time.

## How It Works

The system operates by combining **RAG (Retrieval-Augmented Generation)** with long-term memory storage to ensure a continuous and natural conversation flow.

- **Conversation Analysis**: Each new conversation between David and Choi is analyzed to extract key data, such as emotional tone, relationship details, and health updates.

- **Retrieve and Generate Response**: Using RAG, the system retrieves relevant information from the long-term memory base and generates an appropriate response, ensuring the continuity of the dialogue.

- **Memory Update**: New information is constantly stored in the long-term memory, enriching future conversations by retaining context and emotional flow.

- **Monitor Feedback Integration**: The system enables real-time adjustments based on monitor feedback, allowing the chatbot to adapt to different scenarios, emotional tones, or conversation topics.

- **Long-term and Short-term Memory Management**: While long-term memory helps the system recall critical information, the short-term memory, such as the previous context, ensures that each response is logically connected to the immediate conversation.
## Installation and Setup

### System Requirements
- Python 3.8 or higher
- Key Libraries:
  - `transformers`
  - `torch`
  - `python-dotenv`
  - `langchain`

### Installation Steps

1. **Clone the repository**:
```bash
https://github.com/ShynBui/illuminus_bot.git
cd \illuminus_bot
``` 
2. **Install dependencies**:
```bash
pip install -r requirements.txt
```
### Set up environment variables:
3. **Create a `.env` file and add the necessary API keys**:
```env
GEMINI_API_KEY= <YOUR_GEMINI_API_KEY>
LIST_GEMINI_API_KEY = '["your_api_key_1", "your_api_key_2",...]'
OPEN_AI_KEY = <YOUR_OPEN_AI_API_KEY>
LLM_MODEL="gpt-4o-mini"
LLM_MODEL_="gemini-1.5-flash"
LLM_MONITOR_GEMINI = 'gemini-1.5-pro'
EMBEDDING_MODEL = 'text-embedding-3-small'
```
### Usage

Once the environment is set up, you can run the chatbot system by executing the main script:

```bash
python run.py
```

### Project Structure
```text
├── .env                             # Environment variables file
├── config/                          # Configuration files
│   ├── generate_data_config.json
│   └── train_model_config.json
├── data/                            # Training and testing data
│   ├── conversation_data.json
│   ├── long_term_memo.json
├── logs/                            # System logs
│   └── app.log
├── models/                          # Trained models and checkpoints
│   ├── checkpoint-150/
│   └── ...
├── notebooks/                       # Jupyter Notebooks for training/testing
│   ├── Qwen 3B finetuned.ipynb
│   └── test_model.ipynb
├── pkgs/                            # Core system packages
│   ├── llm_executor.py
│   ├── quota_manager.py
│   └── prompt/
│       ├── david_choi_prompt.py
│       ├── generate_data_for_train.py
│       └── long_term_memory.py
├── src/                             # Main source code
│   ├── analysis_message.py
│   ├── chatbot.py
│   ├── generate_data.py
│   └── rag_retriever.py
├── test/                            # Unit and integration tests
│   ├── unit_test_rag_retrieve.py
│   ├── test_generate_data.py
│   ├── test_language_detection.py
│   ├── unit_test_llm_executor.py
│   ├── unit_test_quota_manager.py
│   └── __init__.py
├── README.md                        # Project documentation
├── requirements.txt                 # Dependencies list
└── run.py                           # Main chatbot execution script
```
## Getting Started

After installation:
### Start the Chatbot:
```bash
python run.py
```
### Interact with the Chatbot:
The system will prompt you to engage in a conversation between David and Choi. You can adjust Choi’s role (e.g., caring son, humorous storyteller, motivational speaker), the language used (English, Korean, or a combination), or monitor the chatbot in real-time to ensure it meets specific emotional or contextual requirements.

### Monitor Input:
Adjust conversation parameters such as emotional tone or topic in real-time using the monitor feedback system to guide the flow of conversation based on current needs.

## Contributing

We welcome contributions to improve this system! Please submit pull requests or issues on GitHub.
## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
