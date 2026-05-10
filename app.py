from fastapi import FastAPI
from app.routes.tts import router as tts_router
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=10000
    )
