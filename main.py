from fastapi import FastAPI, UploadFile
from transformers import pipeline

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/audio")
async def post_audio(file: UploadFile):
    user_message = speech2text(file)

def speech2text(file):
    audio_file = open(file.filename, "rb")
    whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium')
    message = whisper(str(audio_file.name))
    print(message)
    return {"message": "Audio has been transcribed"}