import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

model = None

def get_model():
    global model

    if model is None:
        model = ChatterboxTTS.from_pretrained(device="cpu")

    return model

def generate_tts(text, speaker, output):
    model = get_model()

    wav = model.generate(
        text=text,
        audio_prompt_path=speaker
    )

    ta.save(
        output,
        wav,
        model.sr
    )
