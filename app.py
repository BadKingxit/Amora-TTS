from fastapi import FastAPI
from app.routes.tts import router as tts_router
import uvicorn
import os

app = FastAPI(
    title="Amora-TTS",
    version="1.0.0"
)

app.include_router(tts_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Amora-TTS"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
