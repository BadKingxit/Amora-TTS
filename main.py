import os
import gc
import uuid
import torch

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

print("=== SERVER STARTING ===")

app = FastAPI()

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

tts = None


def load_model():
    global tts

    if tts is None:
        print("=== IMPORTANDO TTS ===")

        from TTS.api import TTS

        print("=== CONFIGURANDO CPU ===")

        torch.set_num_threads(1)

        print("=== CARREGANDO XTTS ===")

        tts = TTS(MODEL_NAME)

        tts.to("cpu")

        print("=== XTTS CARREGADO ===")

    return tts


@app.on_event("startup")
async def startup_event():
    try:
        load_model()
    except Exception as e:
        print("=== ERRO NO PRELOAD ===")
        print(str(e))


@app.get("/")
async def root():
    return {
        "status": "online",
        "model": MODEL_NAME
    }


@app.post("/tts")
async def generate_tts(
    text: str = Form(...),
    audio: UploadFile = File(...)
):
    temp_input = None
    temp_output = None

    try:
        print("=== REQUEST RECEBIDA ===")

        if len(text) > 300:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Texto muito grande. Máximo: 300 caracteres."
                }
            )

        model = load_model()

        temp_input = f"/tmp/{uuid.uuid4()}.wav"
        temp_output = f"/tmp/{uuid.uuid4()}.wav"

        print("=== SALVANDO AUDIO ===")

        with open(temp_input, "wb") as f:
            f.write(await audio.read())

        print("=== LIMPEZA MEMORIA ===")

        gc.collect()

        try:
            torch.cuda.empty_cache()
        except:
            pass

        print("=== GERANDO TTS ===")

        model.tts_to_file(
            text=text,
            speaker_wav=temp_input,
            language="pt",
            file_path=temp_output
        )

        print("=== TTS GERADO ===")

        return FileResponse(
            temp_output,
            media_type="audio/wav",
            filename="tts.wav"
        )

    except Exception as e:
        import traceback

        print("=== ERRO ===")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )

    finally:
        try:
            if temp_input and os.path.exists(temp_input):
                os.remove(temp_input)
        except:
            pass


print("=== SERVER READY ===")