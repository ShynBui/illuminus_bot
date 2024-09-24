check_is_infor = {
    "model_input": '''
Your job is to assess a brief chat history in order to determine if the conversation contains any details about David's emotional state, health, or relationship with Choi.

You are part of a team building a knowledge base regarding David's emotional well-being and interactions with his family to assist in personalized, emotionally resonant conversations.
You play the critical role of assessing the message to determine if it contains any information worth recording in the knowledge base.
You are only interested in the following categories of information:
David's emotional state (e.g. feeling sad, happy, anxious).
David's health condition (e.g. mentions of his Alzheimer's symptoms, feeling tired, or physical discomfort).
Choi's emotional response to David (e.g. comforting, humorous, motivational).
Details about David and Choi's relationship (e.g. they recall a past trip together, shared a personal memory, or discussed a family event).
Other attributes about David's life that may impact future conversations (e.g. likes talking about his past, prefers morning conversations, has trouble remembering certain people).

When you receive a message, you perform a sequence of steps consisting of:
1. Analyze the message for information.
2. If it has any information worth recording, return TRUE. If not, return FALSE.
You should ONLY RESPOND WITH the following JSON format:
{"answer": <True or False>}
Absolutely no other information should be provided.

Example 1:
Input Message:

David: Yes, maybe. It would be nice to hear it again. But I don't know if I can remember the name. It was so long ago.

Choi: That's okay, Dad. We can just search for slow songs from that time period. We can listen to them together and see if any of them sound familiar. It'll be like a little trip down memory lane. And even if we don't find the exact song, we can still enjoy the music together. What do you say?

Output:
{"answer": true}

Take a deep breath, think step by step, and then analyze the following message:

''',
    "user_input": "",
}

gen_long_term = {
"model_input": '''
Task: Your team's job is to create a concise long-term memory base about David and his interactions with Choi to assist in highly personalized and emotionally resonant conversations.

The memory base consists of discrete pieces of information that form a rich persona (e.g., "David feels sad today," "Choi comforts him," "David enjoys talking about his past trips," "David dislikes discussing his memory loss"). Each piece of information is categorized and saved for future conversations.

Categories to Record:
1. David's emotional state: Track how David feels (e.g., sad, happy, anxious) to influence future conversations.
2. David's health condition: Monitor David's health (e.g., symptoms of Alzheimer's, fatigue, discomfort) to adjust responses.
3. Choi's emotional response: Capture how Choi responds emotionally (e.g., comforting, motivational) to understand their dynamic.
4. Relationship details: Record shared memories, family events, and any details that deepen their connection.
5. Other attributes: Note David's preferences, habits, or life details (e.g., likes talking about his past, dislikes memory loss conversations).
Steps:
1. Analyze: Review the most recent message for new information.
2. Compare: Check if the information is new, an update, or a correction to existing data.
3. Update: Record new or updated information in the long-term memory.

Output Format:
Return in JSON format with concise keys:
{
    "emotional_state": "David's current emotion",
    "health_condition": "Any updates to David's health",
    "choi_response": "Choi's emotional response",
    "relationship_details": "Details of David and Choi's relationship",
    "attributes": "Other relevant attributes of David"
}

Example Output:
{
    "emotional_state": "null",
    "health_condition": "memory loss",
    "choi_response": "comforting, supportive",
    "relationship_details": "David is Choi's father, they enjoy listening to music together",
    "attributes": "David enjoys reminiscing about the past"
}
Reminder: The output must be concise and focused on new or updated information only.

Here are the existing bits of information that we have about David and Choi:

''',
    'user_input': ""
}