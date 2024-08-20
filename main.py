import os
import json
from fastapi import FastAPI, UploadFile, HTTPException
from transformers import pipeline
import aiofiles

app = FastAPI()

whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium', device=0)
smol = pipeline("text-generation", model="HuggingFaceTB/SmolLM-360M-Instruct", device=0)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/audio")
async def post_audio(file: UploadFile):
    try:
        user_message = await speech2text(file)
        bot_response = get_bot_response(user_message)
        print(bot_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def speech2text(file: UploadFile):
    async with aiofiles.open(file.filename, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    message = whisper(file.filename)
    return {"role": "user", "content":message['text']}

def get_bot_response(user_message):
    messages = load_messages()
    messages.append(user_message)
    parsed_bot_response = smol(messages, max_new_tokens=128)[0]['generated_text'][-1]
    save_messages(user_message, parsed_bot_response)
    return parsed_bot_response['content']


# Helper functions
def load_messages():
    messages = []
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
                "Ask technical questions that are relevant to a junior level developer. Your name is John. "+
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
