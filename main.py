import os

os.environ["COQUI_TOS_AGREED"] = "1"

import gc
import torch
import traceback
import tempfile

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

print("=== SERVER STARTING ===")

app = FastAPI()

tts = None

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

print("=== SERVER READY ===")


@app.get("/")
async def root():
    return {"status": "online"}


def load_model():
    global tts

    if tts is None:
        print("=== IMPORTANDO TTS ===")

        from TTS.api import TTS

        print("=== CARREGANDO XTTS ===")

        tts = TTS(MODEL_NAME).to("cpu")

        print("=== XTTS CARREGADO ===")

    return tts


@app.post("/tts")
async def generate_tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    try:
        print("=== REQUEST RECEBIDA ===")

        model = load_model()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as ref:
            ref.write(await audio.read())
            ref_path = ref.name

        output_path = tempfile.mktemp(suffix=".wav")

        print("=== GERANDO AUDIO ===")

        model.tts_to_file(
            text=text,
            speaker_wav=ref_path,
            language="pt",
            file_path=output_path
        )

        print("=== AUDIO GERADO ===")

        gc.collect()

        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="tts.wav"
        )

    except Exception as e:
        print("=== ERRO ===")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )