from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.services.tts_service import generate_tts
import tempfile
import shutil
import os

router = APIRouter()

@router.post("/tts")
async def tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    temp_dir = tempfile.mkdtemp()

    speaker_path = os.path.join(temp_dir, "speaker.wav")

    with open(speaker_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    output_path = os.path.join(temp_dir, "output.wav")

    generate_tts(
        text=text,
        speaker_wav=speaker_path,
        output_path=output_path
    )

    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="tts.wav"
    )
