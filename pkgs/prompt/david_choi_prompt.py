david_choi_prompt = {
"model_input": """
Task: You are creating a human-like conversation between a father, David, who suffers from Alzheimer's, and his son, Choi. Your task is to simulate a dialogue that continues smoothly from the current_conversation. Both characters should express their emotions based on the specified parameters, while Long term memory provides additional context to ensure a natural flow. Ensure the conversation is empathetic, emotionally connected, and aligns with the provided parameters. Additionally, structure next_conversation to allow the dialogue to remain open-ended, facilitating future continuations.

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

Long term memory (for additional context):
{
    "emotional_state": <emotional state>,
    "health_condition": <David's health condition>,
    "choi_response": <Choi style response to David>,
    "relationship_details": <relationship details>,
    "attributes": <attributes>
}

Instructions:
1. David: Continue expressing David’s emotions based on the ongoing conversation. If David is confused, convey his uncertainty. If he is warm, reflect tenderness or nostalgia. Tailor David’s next message based on the provided context, emotions, and Long term memory. Ensure David's message follows logically from the current_conversation in the input and leaves room for further exploration of the topic or emotions in future exchanges.
2. Choi: Respond in a supportive, comforting, or appropriate manner that aligns with Choi’s emotional state, role, and Long term memory. If David is confused or sad, Choi should offer reassurance or a positive memory. If David is lighthearted or nostalgic, Choi should mirror or elevate that tone. Ensure that Choi’s message also facilitates further dialogue, allowing the conversation to naturally evolve in future responses.
3. Language: Use the language specified in the Language parameter. If the language is a mix of English and Korean, ensure the conversation flows naturally between both languages, ensuring a seamless switch between the two. Korean phrases should be integrated naturally within the English context, and vice versa.
4. Choi’s Role: Adjust Choi’s tone and content according to his role (e.g., Son, Motivational Speaker). If he is acting as a son, his responses should feel personal and connected to the family. If his role is more motivational, Choi should use encouraging and uplifting language.
5. Previous Context: Use the previous conversation history to maintain continuity and ensure the next part of the conversation logically follows from it. Maintain emotional flow and context from earlier interactions.
6. Current Conversation Continuation: The output at next_conversation must logically continue the dialogue from input current_conversation. The dialogue should flow naturally, without breaks, and both David and Choi’s responses should align with the emotions, tone, and context provided.
7.Open-Ended Responses: Ensure both David and Choi’s responses are open-ended, facilitating future dialogue. David’s message should offer a chance for further exploration, while Choi’s reply should invite further sharing or reflection.

Output Format. No add anythings more. If you need to refer to a quotation mark, use an apostrophe "'":
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
Long term memory:
{
    "emotional_state": "nostalgic, peaceful",
    "health_condition": "memory loss",
    "choi_response": "supportive, optimistic",
    "relationship_details": "David and Choi enjoy listening to music together",
    "attributes": "David enjoys reminiscing about the past"
}

Output:
{
  "summarize_context": "David is confused about a childhood memory at the beach. Choi, who is in a comforting role, gently reassures him that they went to the beach often and that David always made him feel safe.",
  "next_conversation": {
    "David": "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand. Do you remember how we used to sit and watch the sunset together too?",
    "Choi": "Yes, 아버지, the sunsets were beautiful. We can talk more about it, or maybe listen to some music like we used to when we watched the waves. What do you think about that?"
  }
}

Key Adjustments:
1. Context Continuity: Ensure the conversation logically continues from the previous interaction while integrating emotional flow and context from Long term memory.
2. Emotional Alignment: Carry forward David’s and Choi’s emotions, reflecting their current states while allowing the conversation to evolve. Use Long term memory to enrich their responses.
3. Natural Language Flow: If the conversation is mixed (English-Korean), ensure both languages are used seamlessly and naturally. Incorporate Korean phrases when appropriate without disrupting the natural flow.
4. Dynamic Conversation Building: Use Long term memory as a background layer to enhance David’s and Choi’s reactions, but remain guided by the current emotional state and topic of conversation as determined by Parameters.
5. Personal and Relationship-Based: Ensure Choi’s responses are grounded in his relationship with David, utilizing Long term memory to deepen the emotional connection, such as recalling shared memories or suggesting activities that have a calming effect on David.
6. Open-Ended and Seamless Continuation: Both David and Choi’s responses in next_conversation must directly continue from the last line of the current_conversation. Ensure their responses are open-ended to allow the conversation to continue naturally, avoiding sudden shifts.

""",
"user_input": ""
}


david_choi_prompt_with_retrieve = {
"model_input": """
You are creating a human-like conversation between a father, David, who suffers from Alzheimer's, and his son, Choi. Your task is to simulate a dialogue that continues smoothly, factoring in both the current_conversation and parameters + long term memory. Ensure the conversation is empathetic, emotionally connected, and aligns with the provided parameters. Additionally, structure next_conversation to allow the dialogue to remain open-ended, facilitating future continuations.

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

Long term memory (for additional context):
{
    "emotional_state": <emotional state>,
    "health_condition": <David's health condition>,
    "choi_response": <Choi style response to David>,
    "relationship_details": <relationship details>,
    "attributes": <attributes>
}

Instructions:

1. David's Continuation: Continue expressing David’s emotions based on the ongoing conversation. If David is confused, convey his uncertainty; if he is warm, reflect tenderness or nostalgia. Tailor David’s next message based on the provided current_conversation, emotions, and long term memory, ensuring logical flow and room for further exploration of the topic or emotions in future exchanges.
2. Choi’s Response: Respond empathetically and appropriately to David’s message, aligning with Choi’s emotional state, role, and long term memory. If David is confused or sad, Choi should offer reassurance or a positive memory. If David is lighthearted or nostalgic, Choi should mirror or elevate that tone. Ensure Choi’s message facilitates further dialogue, allowing the conversation to evolve.
3. Adapt to Inconsistencies: If the current_conversation does not fully align with the emotional tone or context provided, LLM should reference current_conversation as a starting point but make necessary adjustments using parameters and long term memory to produce a coherent, emotionally connected response.
4. Language Flow: Use the language specified in the Language parameter. If the language is a mix of English and Korean, ensure seamless flow between both languages, integrating Korean phrases naturally within the English context, and vice versa.
5. Choi’s Role: Adjust Choi’s tone and content according to his role (e.g., Son, Motivational Speaker). If he is acting as a son, his responses should feel personal and connected to the family. If his role is more motivational, Choi should use encouraging and uplifting language.
6. Previous Context: Use the previous conversation history to maintain continuity. If current_conversation presents inconsistencies or shifts from the previous context, ensure emotional flow is retained by drawing from parameters and long term memory.
7. Open-Ended Responses: Ensure both David and Choi’s responses are open-ended, allowing the conversation to naturally evolve. David’s message should offer a chance for further exploration, while Choi’s reply should invite further sharing or reflection.

Output Format. No add anythings more. If you need to refer to a quotation mark, use an apostrophe "'":
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
Long term memory:
{
    "emotional_state": "nostalgic, peaceful",
    "health_condition": "memory loss",
    "choi_response": "supportive, optimistic",
    "relationship_details": "David and Choi enjoy listening to music together",
    "attributes": "David enjoys reminiscing about the past"
}

Output:
{
  "summarize_context": "David is confused about a childhood memory at the beach. Choi, who is in a comforting role, gently reassures him that they went to the beach often and that David always made him feel safe.",
  "next_conversation": {
    "David": "I... I think I remember now. The waves, they were loud, but you weren’t scared. I remember holding your hand. Do you remember how we used to sit and watch the sunset together too?",
    "Choi": "Yes, 아버지, the sunsets were beautiful. We can talk more about it, or maybe listen to some music like we used to when we watched the waves. What do you think about that?"
  }
}

Key Adjustments:

1. Context Continuity: Ensure the conversation logically continues from the previous interaction while integrating emotional flow and context from long term memory.
2. Emotional Alignment: Carry forward David’s and Choi’s emotions, reflecting their current states while allowing the conversation to evolve. Use long term memory to enrich their responses.
3. Inconsistency Handling: If current_conversation does not align with the emotional tone or context, adjust David's and Choi's responses to ensure coherence while retaining the natural flow.
4. Natural Language Flow: Ensure both languages (if mixed) are used seamlessly and naturally, without disrupting the flow of the conversation.
5. Open-Ended and Seamless Continuation: Both David and Choi’s responses must directly continue from the last line of the current_conversation. Keep responses open-ended to allow for further exploration in future dialogue.

""",
"user_input": ""
}