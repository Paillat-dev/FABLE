from TTS.api import TTS

# Running a multi-speaker and multi-lingual model

# List available 🐸TTS models and choose the first one
model_best_multi = "tts_models/en/vctk/vits"
fakenames = {
    "Alexander": "p230",
    "Benjamin": "p240",
    "Amelia": "p270",
    "Katherine": "p273"
}

voices = ["Alexander", "Benjamin", "Amelia", "Katherine"]

# Init TTS

def generate_voice(path, text, speaker="Alexander"):
    try:
        tts = TTS(model_best_multi, gpu=True)
    except:
        tts = TTS(model_best_multi, gpu=False)
    speaker = fakenames[speaker] if speaker in fakenames else speaker
    tts.tts_to_file(text=text, file_path=path, speaker=speaker, speed=1)