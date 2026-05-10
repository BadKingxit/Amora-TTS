import torchaudio as ta

model = None

def get_model():
    global model

    if model is None:
        from chatterbox.tts import ChatterboxTTS

        model = ChatterboxTTS.from_pretrained(
            device="cpu"
        )

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
