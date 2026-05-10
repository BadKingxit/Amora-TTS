from fastapi import FastAPI
from app.routes.tts import router as tts_router
import uvicorn
import os
import traceback

print("[BOOT] app.py iniciado", flush=True)

app = FastAPI(
    title="Amora-TTS",
    version="1.0.0"
)

print("[BOOT] Registrando router", flush=True)

app.include_router(tts_router)

@app.get("/")
async def root():
    print("[ROUTE] / chamada", flush=True)

    return {
        "status": "online",
        "service": "Amora-TTS"
    }

@app.get("/health")
async def health():
    print("[ROUTE] /health chamada", flush=True)

    return {
        "status": "healthy"
    }

@app.on_event("startup")
async def startup_event():
    print("[BOOT] FastAPI startup completo", flush=True)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8080))

        print(f"[BOOT] Iniciando uvicorn na porta {port}", flush=True)

        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=port,
            log_level="debug"
        )

    except Exception as e:
        print("[FATAL] ERRO AO INICIAR UVICORN", flush=True)
        print(str(e), flush=True)
        traceback.print_exc()
