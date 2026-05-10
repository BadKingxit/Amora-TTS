import traceback
import time
import os
import gc

print("[BOOT] chatterbox.py carregado")

model = None

def log(msg):
    print(f"[AMORA-TTS] {msg}", flush=True)

def get_model():
    global model

    if model is not None:
        log("Modelo já carregado na memória")
        return model

    try:
        log("Importando torch...")
        import torch

        log(f"Torch version: {torch.__version__}")

        log("Importando torchaudio...")
        import torchaudio as ta

        log("Torchaudio importado")

        log("Importando ChatterboxTTS...")
        from chatterbox.tts import ChatterboxTTS

        log("ChatterboxTTS importado")

        log("Iniciando load do modelo...")

        start = time.time()

        model = ChatterboxTTS.from_pretrained(
            device="cpu"
        )

        elapsed = time.time() - start

        log(f"Modelo carregado com sucesso em {elapsed:.2f}s")

        return model

    except Exception as e:
        log("ERRO NO LOAD DO MODELO")
        log(str(e))
        traceback.print_exc()
        raise e

def generate_tts(text, speaker, output):
    try:
        log("generate_tts iniciado")

        log(f"Texto recebido: {text[:80]}")

        log(f"Speaker path: {speaker}")

        log("Importando torchaudio...")
        import torchaudio as ta

        log("Torchaudio OK")

        model = get_model()

        log("Gerando áudio...")

        start = time.time()

        wav = model.generate(
            text=text,
            audio_prompt_path=speaker
        )

        elapsed = time.time() - start

        log(f"Áudio gerado em {elapsed:.2f}s")

        log(f"Salvando wav em: {output}")

        ta.save(
            output,
            wav,
            model.sr
        )

        log("Áudio salvo com sucesso")

        gc.collect()

        log("GC executado")

    except Exception as e:
        log("ERRO NO GENERATE_TTS")
        log(str(e))
        traceback.print_exc()
        raise e
