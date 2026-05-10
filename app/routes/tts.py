from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.services.chatterbox import generate_tts
import uuid
import os

router = APIRouter()

@router.post("/tts")
async def tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    os.makedirs("temp", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    temp_voice = f"temp/{uuid.uuid4()}.wav"
    output_file = f"outputs/{uuid.uuid4()}.wav"

    with open(temp_voice, "wb") as f:
        f.write(await audio.read())

    generate_tts(
        text=text,
        speaker=temp_voice,
        output=output_file
    )

    os.remove(temp_voice)

    return FileResponse(
        output_file,
        media_type="audio/wav",
        filename="tts.wav"
    )
