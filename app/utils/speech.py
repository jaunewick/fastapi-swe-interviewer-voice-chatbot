from fastapi import UploadFile
from transformers import pipeline
import aiofiles
import requests
from ..config import HUGGINGFACEHUB_API_TOKEN

# Set device=0 if using gpu
whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium', device=-1)
API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"

async def speech2text(file: UploadFile):
    async with aiofiles.open(file.filename, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    message = whisper(file.filename)
    return {"role": "user", "content":message['text']}

def text2speech(bot_response):
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    payloads = {
        "inputs": bot_response
    }
    response = requests.post(API_URL, headers=headers, json=payloads)
    return response.content