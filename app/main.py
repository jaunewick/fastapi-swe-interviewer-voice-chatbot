from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from .utils.speech import speech2text, text2speech
from .utils.bot import get_bot_response

app = FastAPI()

@app.post("/audio")
async def post_audio(file: UploadFile):
    try:
        user_message = await speech2text(file)
        bot_response = get_bot_response(user_message)
        audio_response = text2speech(bot_response)
        def iterfile():
            yield audio_response
        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
