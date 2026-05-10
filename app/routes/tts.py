from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from app.services.chatterbox import generate_tts
import uuid
import os
import traceback

router = APIRouter()

def log(msg):
    print(f"[TTS-ROUTE] {msg}", flush=True)

@router.post("/tts")
async def tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    try:
        log("Nova request recebida")

        os.makedirs("temp", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        temp_voice = f"temp/{uuid.uuid4()}.wav"
        output_file = f"outputs/{uuid.uuid4()}.wav"

        log(f"Temp voice: {temp_voice}")
        log(f"Output file: {output_file}")

        content = await audio.read()

        log(f"Audio size: {len(content)} bytes")

        with open(temp_voice, "wb") as f:
            f.write(content)

        log("Arquivo temporário salvo")

        generate_tts(
            text=text,
            speaker=temp_voice,
            output=output_file
        )

        log("generate_tts concluído")

        os.remove(temp_voice)

        log("Arquivo temporário removido")

        return FileResponse(
            output_file,
            media_type="audio/wav",
            filename="tts.wav"
        )

    except Exception as e:
        log("ERRO NA ROTA /tts")
        log(str(e))
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )
