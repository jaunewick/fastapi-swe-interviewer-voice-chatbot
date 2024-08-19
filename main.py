import os
import json
from fastapi import FastAPI, UploadFile
from transformers import pipeline

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/audio")
async def post_audio(file: UploadFile):
    user_message = speech2text(file)
    bot_response = get_bot_response(user_message)

def speech2text(file):
    audio_file = open(file.filename, "rb")
    whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium', device=0)
    message = whisper(str(audio_file.name))
    return {"role": "user", "content":message['text']}

def get_bot_response(user_message):
    messages = load_messages()
    messages.append(user_message)
    pipe = pipeline("text-generation", model="HuggingFaceTB/SmolLM-360M-Instruct", device=0)
    parsed_bot_response = pipe(messages, max_new_tokens=128)[0]['generated_text'][-1]
    save_messages(user_message, parsed_bot_response)


# Helper functions
def load_messages():
    messages = []
    file = 'db.json'
    empty= os.stat(file).st_size == 0
    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {
                "role": "system",
                "content":"You are interviewing the user for a software engineering internship position. "+
                "Ask short questions that are relevant to a intern level developer. Your name is Greg. "+
                "The user is Daniel. Keep responses under 30 words and be funny sometimes, but keep it moving."
            }
        )
    return messages

def save_messages(user_message, bot_response):
    file = 'db.json'
    messages = load_messages()
    messages.append(user_message)
    messages.append(bot_response)
    with open(file, 'w') as f:
        json.dump(messages, f)
