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
5.Choi's Role:
["Son", "Doctor", "Humorous storyteller", "Motivational speaker", etc.]
This parameter describes the way Choi positions himself in the conversation, influencing the tone and intention behind his words.

Task: Based on the selected parameters, generate a dialogue between Choi and David, in which Choi responds in a way that is appropriate to the situation, emotion, and role. The output should be in JSON format with the following fields:
```json
{

"previous_context": "<Previous context>",

"topic": "<Conversation topic>",

"language": "<Language>",

"conversation": [ {"speaker": "David","emotion": "<Cảm xúc của David>","text": "<Lời nói của David>"}, "speaker": "Choi", "role": "<Vai trò của Choi>", "emotion": "<Cảm xúc của Choi>", "text": "<Lời nói của Choi>" }] 
}

""",
    "user_input": """

"""
}