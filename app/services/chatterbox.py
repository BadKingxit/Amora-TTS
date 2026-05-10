import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

device = "cuda" if torch.cuda.is_available() else "cpu"

model = ChatterboxTTS.from_pretrained(device=device)

def generate_tts(text, speaker, output):
    wav = model.generate(
        text=text,
        audio_prompt_path=speaker
    )

    ta.save(
        output,
        wav,
        model.sr
    )
