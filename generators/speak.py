from TTS.api import TTS

# Running a multi-speaker and multi-lingual model

# List available 🐸TTS models and choose the first one
model_best_multi = "tts_models/en/vctk/vits"
fakenames = {
    "Alexander": "p230",
    "Benjamin": "p240",
    "Amelia": "p270",
    "Katherine": "p273",
    "Johanne": "p347",
}

voices = ["Alexander", "Benjamin", "Amelia", "Katherine", "Johanne"]

# Init TTS

def generate_voice(path, text, speaker="Alexander"):
    model = model_best_multi
    speaker = fakenames[speaker] if speaker in fakenames else speaker
    print(f"Generating voice for {model} with speaker {speaker}")
    try:
        tts = TTS(model, gpu=True)
    except:
        tts = TTS(model, gpu=False)
    tts.tts_to_file(text=text, file_path=path, speaker=speaker, speed=1, emotion="Happy")

if __name__ == "__main__":
    generate_voice("test/test.mp3", "This is a test. I like the words python, django and flask. Betty bought a bit of butter but the butter was bitter. So she bought some better butter to make the bitter butter better.")