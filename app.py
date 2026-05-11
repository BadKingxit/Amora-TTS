import os

os.environ["COQUI_TOS_AGREED"] = "true"

import gc
import torch
import traceback
import tempfile

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from TTS.api import TTS

print("=== STARTING SERVER ===")


torch.set_num_threads(1)

app = FastAPI()

tts = None

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

print("=== CONFIG READY ===")


@app.get("/")
async def root():
    return {"status": "online"}


def load_model():
    global tts

    if tts is None:
        print("=== LOADING XTTS MODEL ===")

        tts = TTS(MODEL_NAME).to("cpu")

        print("=== MODEL LOADED ===")

    return tts


@app.post("/tts")
async def generate_tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    try:
        print("=== REQUEST RECEIVED ===")

        model = load_model()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as ref:
            ref.write(await audio.read())
            ref_path = ref.name

        print(f"=== REF SAVED: {ref_path} ===")

        output_path = tempfile.mktemp(suffix=".wav")

        print("=== STARTING GENERATION ===")

        model.tts_to_file(
            text=text,
            speaker_wav=ref_path,
            language="pt",
            file_path=output_path
        )

        print("=== GENERATION DONE ===")

        gc.collect()

        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="tts.wav"
        )

    except Exception as e:
        print("=== ERROR ===")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )