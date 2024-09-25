# Human-Like Chatbot System Using RAG

## Introduction
The **Human-Like Chatbot System** is developed to create natural, emotionally resonant conversations between **David**, a father suffering from Alzheimer’s, and his son **Choi**. The primary goal of this system is to build a long-term memory for the chatbot that enhances personalized, realistic, and emotionally aware responses over time.

The system leverages **RAG (Retrieval-Augmented Generation)** technology, combining a large language model with information retrieval from a memory base to generate contextually appropriate responses.
## Key Features

- **Long-Term Memory**: The system records critical information from previous conversations between David and Choi, ensuring future interactions are more natural and maintain continuity.
  
- **Emotional Responses**: It analyzes and tracks the emotional state of David and Choi, generating responses that are comforting, supportive, or motivational, depending on the context.
  
- **Role Customization**: Choi can switch between different roles, such as a caring son, a comedian, or a motivational speaker, based on the user’s needs.
  
- **Multi-language Support**: The chatbot can respond in both English and Korean based on the user’s input.

## How It Works

The system uses **RAG** to combine a large language model with retrieval capabilities from previous conversations. Here's how it functions:

1. **Analyze Conversation**: The system analyzes new conversations between David and Choi to extract key information like emotions, health conditions, and the relationship between them.

2. **Retrieve and Generate Response**: Using RAG, the system retrieves relevant information from the memory base and generates an appropriate response based on the current context.

3. **Update Long-Term Memory**: Any new information regarding emotions, health, and relationships is stored in long-term memory for future use.

## Installation and Setup

### System Requirements
- Python 3.8 or higher
- Required libraries:
  - `transformers`
  - `torch`
  - `python-dotenv`

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
