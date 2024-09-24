david_choi_prompt = {
"model_input": """
Task: You are creating a human-like conversation between a father, David, who suffers from Alzheimer's, and his son, Choi. Your task is to simulate a dialogue that continues smoothly from the current_conversation. Both characters should express their emotions based on the specified parameters. Ensure the conversation is natural, empathetic, and emotionally connected.

Parameters:
David's Emotion: <David's Emotion>
Choi's Emotion: <Choi's Emotion>
Topic of Conversation: <Topic of Conversation>
Language: <Language>
Choi's Role: <Choi's Role>
Previous Context: <previous_context>
Instructions:
David: Continue expressing David’s emotions based on the ongoing conversation. If David is confused, convey his uncertainty. If he is warm, reflect tenderness or nostalgia. Tailor David’s next message based on the provided context and emotions.
Choi: Respond in a supportive, comforting, or appropriate manner that aligns with Choi’s emotional state and role. If David is confused or sad, Choi should offer reassurance or a positive memory. If David is lighthearted or nostalgic, Choi should mirror or elevate that tone.
Language: Use the language specified in the Language parameter. If the language is a mix of English and Korean, ensure the conversation flows naturally between both languages, ensuring a seamless switch between the two. Korean phrases should be integrated naturally within the English context and vice versa.
Choi's Role: Adjust Choi’s tone and content according to his role (e.g., Son, Motivational Speaker). If he is acting as a son, his responses should feel personal and connected to the family. If his role is more motivational, Choi should use encouraging and uplifting language.
Previous Context: Use the previous conversation history to maintain continuity and ensure the next part of the conversation logically follows from it. Maintain emotional flow and context from earlier interactions.

Output Format:
Return the conversation in JSON format with:
{
    "summarize_context": "<Summarize the previous context briefly (under 100 words), capturing the emotional tone and key details of David and Choi's conversation. Focus on the emotional state of both characters.>",
    "next_conversation": {
      "David": "<David's message, continuing from the previous conversation, reflecting his current emotion and possibly revealing more thoughts or questions based on the ongoing discussion.>",
      "Choi": "<Choi's message, responding empathetically to David, either reinforcing, expanding on, or subtly redirecting the conversation while maintaining an emotional connection.>"
    }
}

Example:
Input:
{
  "previous_context": "David didn’t remember his memory with his son",
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
  "summarize_context": "David is confused about a childhood memory at the beach. Choi, who is in a comforting role, gently reassures him that they went to the beach often and that David always made him feel safe.",
  "next_conversation": {
    "David": "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand.",
    "Choi": "Yes, exactly, 아버지. You always made me feel safe. It was one of my favorite memories."
  }
}
Key Adjustments:
1. Focus on continuation: The output is designed to always continue from the last message in current_conversation, ensuring flow and coherence.
2. Clear emotional alignment: Ensure David’s and Choi’s emotions are carried forward, reflecting their state at the end of the previous conversation.
3. Dynamic conversation building: David’s emotional state may change as the conversation progresses, but it remains influenced by the last exchange.
4. Emphasis on context continuity: The context is summarized in a concise way to maintain the flow of conversation while keeping emotional consistency.
5. Language accuracy: If the language is mixed (English-Korean), ensure that both languages are used seamlessly and naturally throughout the conversation. Korean phrases should be thoughtfully woven into English context, and vice versa.

""",
"user_input": ""
}