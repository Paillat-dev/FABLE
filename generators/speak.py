
import os

fakenames = {
    "Alexander": "p230",
    "Benjamin": "p240",
    "Amelia": "p270",
    "Katherine": "p273",
    "Johanne": "p347",
}

voices = ["Alexander", "Benjamin", "Amelia", "Katherine", "Johanne"]

class VoiceGenerator:
    def __init__(self, mode="Bark", speaker=""):
        self.mode = mode
        self.speaker = speaker
        if mode == "Bark":
            os.environ["XDG_CACHE_HOME"] = os.path.join(os.getcwd(), "bark_cache")
            from bark import preload_models, generation

            preload_models()
            self.speaker = "v2/en_speaker_6"
        else:
            from TTS.api import TTS
            model = "tts_models/en/vctk/vits"
            self.speaker = fakenames[speaker] if speaker in fakenames else speaker
            print(f"Generating voice for {model} with speaker {speaker}")
            try:
                self.tts = TTS(model, gpu=True)
            except:
                self.tts = TTS(model, gpu=False)
            if self.speaker == "": self.speaker = "p230"
            else:
                self.speaker = fakenames[self.speaker] if self.speaker in fakenames else fakenames["Alexander"]
    
    def generate_voice(self, path, text):
        if self.mode == "Bark":
            from bark import SAMPLE_RATE, generate_audio, preload_models
            from scipy.io.wavfile import read as wavread, write as wavwrite
            import noisereduce as nr
            import soundfile
            import numpy as np
            import nltk
            sentences = nltk.sent_tokenize(text)
            pieces = []
            silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
            for sentence in sentences:
                audio_array = generate_audio(sentence, history_prompt=self.speaker)
                pieces += [audio_array, silence.copy()]
            audio_array = np.concatenate(pieces)
            soundfile.write(path, audio_array, SAMPLE_RATE, format="WAV", subtype="PCM_16")
            rate, data = wavread(path)
            reduced_noise = nr.reduce_noise(y=data, sr=rate)
            os.remove(path)
            wavwrite(path, rate, reduced_noise)
        else:
            self.tts.tts_to_file(text=text, file_path=path, speaker=self.speaker, speed=1, emotion="Happy")
if __name__ == "__main__":
    generator = VoiceGenerator()
    generator.generate_voice("test/test_r.wav", "Hello there!")
    generator.generate_voice("test/teste_r.wav", "This is a test. I like the words python, django and flask. Betty bought a bit of butter but the butter was bitter. So she bought some better butter to make the bitter butter better.")