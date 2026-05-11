from fastapi import FastAPI
from app.routes.tts import router

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online"}

app.include_router(router)
