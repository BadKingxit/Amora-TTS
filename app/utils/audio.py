import os

def ensure_dirs():
    folders = [
        "outputs",
        "temp",
        "voices",
        "models"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
