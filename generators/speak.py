import os
from pydub import AudioSegment, silence

fakenames = {
    "Alexander": "p230",
    "Benjamin": "p240",
    "Amelia": "p270",
    "Katherine": "p273",
    "Johanne": "p347",
}

voices = ["Alexander", "Benjamin", "Amelia", "Katherine", "Johanne"]


def remove_blank_moments(file_path, silence_thresh= -50, silence_chunk_len=500):
    # Load audio file
    audio = AudioSegment.from_wav(file_path)

    # Detect non-silent parts
    nonsilent_data = silence.detect_nonsilent(audio, min_silence_len=silence_chunk_len, silence_thresh=silence_thresh)

    # Create new audio file
    final_audio = AudioSegment.empty()

    # Iterate over non-silent parts and append to the final_audio with 0.5 seconds before and after each segment
    for idx, (start_i, end_i) in enumerate(nonsilent_data):
        start_i = max(0, start_i - 500)  # 0.5 seconds before
        end_i += 500  # 0.5 seconds after

        segment = audio[start_i:end_i]

        # Only append silence after the first segment
        if idx > 0:
            final_audio += AudioSegment.silent(duration=500)

        final_audio += segment
    # Save the result
    if not os.path.exists(os.path.abspath(os.path.join(os.getcwd(), "temp"))):
        os.mkdir(os.path.abspath(os.path.join(os.getcwd(), "temp")))
    tempfile_path = os.path.abspath(os.path.join(os.getcwd(), "temp", "temp.wav"))
    final_audio.export(tempfile_path, format="wav")
    os.remove(file_path)
    os.rename(tempfile_path, file_path)


def optimize_string_groups(strings):
    optimized_groups = []
    current_group = []
    current_length = 0

    for string in strings:
        string_length = len(string) + len(current_group)  # Account for spaces between strings
        if current_length + string_length <= 100:
            current_group.append(string)
            current_length += string_length
        else:
            optimized_groups.append(' '.join(current_group))  # Join strings with spaces
            current_group = [string]
            current_length = len(string)

    if current_group:
        optimized_groups.append(' '.join(current_group))

    return optimized_groups

class VoiceGenerator:
    def __init__(self, mode="Bark", speaker=""):
        self.mode = mode
        self.speaker = speaker
        if mode == "Bark":
            os.environ["XDG_CACHE_HOME"] = os.path.join(os.getcwd(), "bark_cache")
            from bark import preload_models
            print("Loading Bark voice generator")
            preload_models()
            #self.speaker = os.path.abspath(os.path.join(os.getcwd(), "audio_prompts", "en_male_professional_reader.npz"))
            self.speaker = os.path.join(os.getcwd(), "audio_prompts", "en_narrator_light_bg.npz")
            print(f"Generating voice for Bark with speaker {self.speaker}")
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
            sentences = optimize_string_groups(sentences)
            print(sentences)
            pieces = []
            silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
            for sentence in sentences:
                if not sentence == "":
                    audio_array = generate_audio(sentence, history_prompt=self.speaker)
                    pieces += [audio_array, silence.copy()]
            audio_array = np.concatenate(pieces)
            soundfile.write(path, audio_array, SAMPLE_RATE, format="WAV", subtype="PCM_16")
            '''
            remove  silence
            '''
            remove_blank_moments(path)
        else:
            self.tts.tts_to_file(text=text, file_path=path, speaker=self.speaker, speed=1, emotion="Happy")
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    print("Testing voice generator")
    generator = VoiceGenerator()
    print("Loaded voice generator")
#    generator.generate_voice("test/test_r.wav", "Hello there!")
    generator.generate_voice("test/tast_timbernerslee.wav", "But his greatest claim to fame is undoubtedly his invention of the World Wide Web back in 1989. Can you imagine a world without the internet? [Laughs] No, thank you!")