from transformers import pipeline
import os
import json

smol = pipeline("text-generation", model="HuggingFaceTB/SmolLM-360M-Instruct", device=0)

def get_bot_response(user_message):
    messages = load_messages()
    messages.append(user_message)
    parsed_bot_response = smol(messages, max_new_tokens=128)[0]['generated_text'][-1]
    save_messages(user_message, parsed_bot_response)
    return parsed_bot_response['content']

def load_messages():
    messages = []
    #chat history
    file = 'db.json'
    if os.path.exists(file) and os.stat(file).st_size > 0:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {
                "role": "system",
                "content":"You are a hiring manager interviewing someone for a junior frontend developer position. "+
                "Ask technical questions that are relevant to a junior level developer. Your name is Billy. "+
                "The person your are interviewing, his name is Daniel. Keep responses under 30 words and be funny sometimes."
            }
        )
    return messages

def save_messages(user_message, bot_response):
    file = 'db.json'
    messages = load_messages()
    messages.extend([user_message, bot_response])
    with open(file, 'w') as f:
        json.dump(messages, f)