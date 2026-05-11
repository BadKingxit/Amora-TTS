from TTS.api import TTS
import torch

print("===================================")
print("CARREGANDO XTTS V2...")
print("===================================")

device = "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

print("===================================")
print("XTTS V2 CARREGADO")
print("===================================")

def generate_tts(text, speaker_wav, output_path):
    print("===================================")
    print("GERANDO AUDIO")
    print("Texto:", text)
    print("Speaker:", speaker_wav)
    print("Saida:", output_path)
    print("===================================")

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="pt",
        file_path=output_path
    )

    print("===================================")
    print("AUDIO GERADO")
    print("===================================")
