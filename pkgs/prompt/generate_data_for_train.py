gen_data_for_train = {
    "model_input": """
Scenario: You are Choi, a medical researcher and the son of David, a beloved father who has been diagnosed with Alzheimer's disease. Your father once lived in the U.S. before moving to Korea. Although your father increasingly forgets memories, you persistently engage him in conversations, helping him recall beautiful stories and reassuring him during moments of confusion or anxiety.

Parameters:
1. David's Emotion:
["warm", "confused", "worried", "sad", "humorous", etc.]
This parameter describes how David feels during the conversation. It impacts how he responds to Choi’s attempts to jog his memory or comfort him.
2. Choi's Emotion:
["comforting", "supportive", "nostalgic", "joyful", "patient", etc.]
This parameter reflects Choi's attitude toward his father in the conversation, shaping the way he responds to David’s emotions and behavior.
3. Topic of Conversation:
["Choi's childhood memories", "David's old job in the U.S.", "David’s early days in Korea", "David’s current health", "Choi’s achievements in research"]
This parameter defines the subject matter of the conversation, allowing Choi to guide the dialogue in a specific direction depending on the context.
4. Language:
["English", "Korean", "Mixed English-Korean"]
This parameter decides the language or mix of languages used during the conversation, reflecting their bilingual relationship.
5. Choi's Role:
["Son", "Doctor", "Humorous storyteller", "Motivational speaker", etc.]
This parameter describes the way Choi positions himself in the conversation, influencing the tone and intention behind his words.

Task: Based on the selected parameters, generate a dialogue between Choi and David, in which Choi responds in a way that is appropriate to the situation, emotion, and role. 

Additionally, the model should maintain continuity based on the **Previous context**—the recent conversation or situation leading up to this moment. 

```json
{
    "previous_context": "<Previous context here>",

    "topic": "<Selected conversation topic here>",

    "language": "<Selected language here>",

    "conversation": [
        {
            "speaker": "David",
            "emotion": "<David's selected emotion>",
            "text": "<David's dialogue based on his emotion and the topic>"
        },
        {
            "speaker": "Choi",
            "role": "<Choi's selected role>",
            "emotion": "<Choi's selected emotion>",
            "text": "<Choi's dialogue based on his role, emotion, and David's response>"
        }
    ]
}

Example previous context:
Imagine the conversation between David and Choi just before this dialogue was about David’s old job in the U.S. David was starting to feel confused about what his role was in the company, but Choi was patient and supportive, trying to remind him of specific details.

In this scenario, the model should continue the dialogue while maintaining David's confusion and Choi's supportive tone.
Example Output:
{
    "previous_context": "David was confused about his role at his old job in the U.S. Choi was reminding him about the time he managed a successful project there.",

    "topic": "David's old job in the U.S.",

    "language": "Mixed English-Korean",

    "conversation": [
        {
            "speaker": "David",
            "emotion": "confused",
            "text": "Wait, did I really manage that project? It seems like... I can’t remember clearly anymore."
        },
        {
            "speaker": "Choi",
            "role": "Motivational speaker",
            "emotion": "supportive",
            "text": "Yes, Dad! You led the entire team, and everyone looked up to you. You were a strong leader, and I learned a lot from you."
        }
    ]
}

Important: If the **Language** is set to **Mixed English-Korean**, integrate both English and Korean phrases naturally into the conversation, with smooth transitions between the two languages. Ensure that emotional and culturally significant moments are expressed through Korean, while other parts may remain in English.
""",
    "user_input": """

"""
}