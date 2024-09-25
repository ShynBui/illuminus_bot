import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from src import load_conversation, create_documents_from_data, create_or_load_vectorstore_and_retriever

class TestConversationRetrieval(unittest.TestCase):

    # Mock the environment variables
    @patch.dict(os.environ, {
        'OPEN_AI_KEY': 'mock_openai_key',
        'EMBEDDING_MODEL': 'mock_embedding_model',
        'LLM_MODEL': 'mock_gpt_model'
    })
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{
        "previous_context": "context1",
        "topic": "health",
        "language": "English",
        "conversation": [
            {"speaker": "David", "emotion": "happy", "text": "I'm feeling great!"},
            {"speaker": "Choi", "emotion": "concerned", "text": "That's good to hear!"}
        ]
    }]))
    def test_load_conversation(self, mock_file):
        # Test load_conversation function
        result = load_conversation()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["topic"], "health")
        self.assertEqual(result[0]["language"], "English")

    def test_create_documents_from_data(self):
        # Test create_documents_from_data function with mock data
        mock_data = [{
            "previous_context": "context1",
            "topic": "health",
            "language": "English",
            "conversation": [
                {"speaker": "David", "emotion": "happy", "text": "I'm feeling great!"},
                {"speaker": "Choi", "emotion": "concerned", "text": "That's good to hear!"}
            ]
        }]
        documents = create_documents_from_data(mock_data)
        self.assertEqual(len(documents), 1)
        self.assertIn("David (happy): I'm feeling great!", documents[0].page_content)
        self.assertIn("Choi (concerned): That's good to hear!", documents[0].page_content)
        self.assertEqual(documents[0].metadata["topic"], "health")
        self.assertEqual(documents[0].metadata["language"], "English")


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner, verbosity=2)
