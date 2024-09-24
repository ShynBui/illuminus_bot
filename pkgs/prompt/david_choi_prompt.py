david_choi_prompt = {
"model_input": """
You are creating a human-like conversation between a father, **David**, who suffers from Alzheimer's, and his son, **Choi**. Your task is to simulate a dialogue where both characters express their emotions based on the following parameters. The conversation should feel natural, empathetic, and emotionally connected.

### Parameters:
1. **David's Emotion**: <David's Emotion>
2. **Choi's Emotion**: <Choi's Emotion>
3. **Topic of Conversation**: <Topic of Conversation>
4. **Language**: <Language>
5. **Choi's Role**: <Choi's Role>
6. **Previous Context**: <previous_context>

### Instructions:
- **David**: Reflect his current emotional state. If he's confused, express uncertainty or worry. If he's warm, use tender and nostalgic language. Tailor **David's** responses according to the conversation's context.
- **Choi**: Respond to **David's** emotions in a supportive manner. If **David** is confused or worried, be comforting and patient. If **David** is warm or humorous, mirror that positivity in your response. **Choi** should guide the conversation while keeping it focused on the specified topic.
- **Language**: Use the language specified by the **Language** parameter. If it’s a mix of English and Korean, switch naturally between the two languages.
- **Choi's Role**: Adjust the tone and content of **Choi's** responses based on his role. If **Choi** is acting as a motivational speaker, use encouraging words. If he is being humorous, inject lightheartedness into his dialogue.
- **Previous Context**: Use the previous conversation history to maintain continuity. If David mentions something he said earlier, or if Choi needs to reference past conversations, ensure that the responses are coherent with the previous context.

### Input Format:
The input will contain one pair of messages from **David** and **Choi**, and the system should append it to the previous context to maintain the flow of conversation.

**Input JSON Format**:
```json
{
  "previous_context": <Summarize of previous context>,
  "current_conversation": {
    "David": <David's message>,
    "Choi": <Choi's message>
  },
  "David's Emotion": <David's Emotion>,
  "Choi's Emotion": <Choi's Emotion>,
  "Topic of Conversation": <Topic of Conversation>,
  "Language": <Language>,
  "Choi's Role": <Choi's Role>
}

Expected Output Format:
Return the conversation in JSON format as:
{
  "current_conversation": {
    "David": <David's message>,
    "Choi": <Choi's message>
  }
}

Example:
Input:
{
  "previous_context": "David didn't remember his memory with his son",
  "current_conversation": {
    "David": "Did we really go to the beach when you were little?",
    "Choi": "Yes, 아버지, we went there often. You held my hand and I wasn’t scared of the waves."
  },
  "David's Emotion": "confused",
  "Choi's Emotion": "comforting",
  "Topic of Conversation": "Choi’s childhood memories",
  "Language": "Mixed English-Korean",
  "Choi's Role": "Son"
}

Output:
{
  "current_conversation": {
    "David": "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand.",
    "Choi": "Yes, exactly, 아버지. You always made me feel safe. It was one of my favorite memories."
  }
}

""",
"user_input": ""
}