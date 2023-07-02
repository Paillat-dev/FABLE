import json
import os
import requests
import pysrt
import random

from generators.speak import VoiceGenerator, voices
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import concatenate_videoclips, CompositeAudioClip, concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.fx.all import volumex, audio_fadein, audio_fadeout # type: ignore
from utils.misc import getenv
from utils.wiki_downloader import download_image as wiki_download_image

unsplash_access = getenv("unsplash_access_key")
if not unsplash_access:
    raise Exception("UNSPLASH_ACCESS_KEY is not set in .env file")
unsplash_url = "https://source.unsplash.com/random/?"

async def prepare(path):
    with open(os.path.join(path, "script.json"), 'r', encoding='utf-8') as f:
        script = json.load(f)
        f.close()
    if not os.path.exists(path + "/slides"): os.mkdir(path + "/slides")
    if not os.path.exists(path + "/audio"): os.mkdir(path + "/audio") 
    choosen_voice = random.choice(voices)
    with open(os.path.join(os.getcwd(), "prompts", "marp.md"), 'r', encoding='utf-8') as f:
        marp = f.read()
        f.close()
    for i in range(len(script)):
        audio_path = os.path.join(path, "audio", "audio" + str(i) + ".wav")
        generator = None
        if not os.path.exists(audio_path):
            if not generator:
                    generator = VoiceGenerator(speaker=choosen_voice)
            print("Generating audio for slide " + str(i))
            generator.generate_voice(audio_path, script[i]['spoken'])
        if "image" in script[i]:
            if os.path.exists(os.path.join(path, "slides", "slide" + str(i) + ".md")) and os.path.exists(os.path.join(path, "slides", "slide" + str(i) + ".png")):
                #skip this slide
                continue
            if not os.path.exists(path + "/slides/assets"):
                os.mkdir(path + "/slides/assets")
            url= unsplash_url + script[i]['image'].replace("+", ",")
            #r = requests.get(url)
            #real_url = r.json()['urls']['raw']
            real_url = url
            with open(path + "/slides/assets/slide" + str(i) + ".jpg", 'wb') as f:
                f.write(requests.get(real_url, allow_redirects=True).content)
                f.close()
            content = marp.replace("[imagesrc]", "assets/slide" + str(i) + ".jpg")
            with open(path + "/slides/slide" + str(i) + ".md", 'w', encoding='utf-8') as f:
                f.write(content)
        elif "wikimage" in script[i]:
            if os.path.exists(os.path.join(path, "slides", "slide" + str(i) + ".md")) and os.path.exists(os.path.join(path, "slides", "slide" + str(i) + ".png")):
                #skip this slide
                continue
            if not os.path.exists(path + "/slides/assets"):
                os.mkdir(path + "/slides/assets")
            r = 0
            while True:
                try: 
                    print("Trying to download image for slide " + str(i))
                    wiki_download_image(script[i]['wikimage'], os.path.abspath(os.path.join(path, "slides", "assets", "slide" + str(i) + ".jpg")))
                    print("Downloaded image for slide with wikiimage " + str(i))
                    if not os.path.exists(os.path.join(path, "slides", "assets", "slide" + str(i) + ".jpg")):
                        raise FileNotFoundError
                    else:
                        break
                except:
                    r += 1
                    if r > 5:
                        break
                    continue
            content = marp + f"\n\n![bg 70%](assets/slide{i}.jpg)"
            with open(path + "/slides/slide" + str(i) + ".md", 'w', encoding='utf-8') as f:
                f.write(content)
        elif "markdown" in script[i]:
            if os.path.exists(path + "/slides/slide" + str(i) + ".md") and os.path.exists(path + "/slides/slide" + str(i) + ".png"):
                #skip this slide
                continue
            with open(path + "/slides/slide" + str(i) + ".md", 'w', encoding='utf-8') as f:
                f.write(marp + "\n\n" + script[i]['markdown'])
        elif "huge" in script[i]:
            #use fit
            if os.path.exists(path + "/slides/slide" + str(i) + ".md") and os.path.exists(path + "/slides/slide" + str(i) + ".png"):
                #skip this slide
                continue
            with open(path + "/slides/slide" + str(i) + ".md", 'w', encoding='utf-8') as f:
                f.write(marp + "\n\n# <!-- fit --> " + script[i]['huge'])
        else:
            if os.path.exists(path + "/slides/slide" + str(i) + ".md") and os.path.exists(path + "/slides/slide" + str(i) + ".png"):
                #skip this slide
                continue
            with open(path + "/slides/slide" + str(i) + ".md", 'w', encoding='utf-8') as f:
                f.write(marp + "\n\n") # blank slide
    for i in range(len(script)):
        markdown_path = os.path.join(path, f"slides/slide{i}.md")
        markdown_path = os.path.abspath(markdown_path)
        image_path = os.path.join(path, f"slides/slide{i}.png")
        image_path = os.path.abspath(image_path)
        if not os.path.exists(image_path):
            command = f'marp.exe "{markdown_path}" -o "{image_path}" --allow-local-files'
            os.system(command)
    return script

def convert_seconds_to_time_string(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def subs(length, total, text, srt, index):
    #first format the start and end in xx:xx:xx,xxx from float seconds like xx.xxxxxx
    start = convert_seconds_to_time_string(total - length)
    stop = convert_seconds_to_time_string(total)
    sub = pysrt.SubRipItem(index=index, start=start, end=stop, text=text)
    srt.append(sub)
    return srt

async def mount(path, script):
    if not os.path.exists(path + "/montage.mp4"):
        num_slides = len(os.listdir(path + "/audio"))
        clips = []
        srt = pysrt.SubRipFile()
        total_length = 0
        for i in range(num_slides):
            audio = AudioFileClip(path + "/audio/audio" + str(i) + ".wav")
            complete_audio = CompositeAudioClip([
                AudioFileClip("silence.mp3").set_duration(1),
                audio,
                AudioFileClip("silence.mp3").set_duration(1)
            ])
            length = complete_audio.duration
            total_length += length
            srt = subs(length, total_length, script[i]['spoken'], srt, i)
            slide = ImageClip(path + "/slides/slide" + str(i) + ".png").set_duration(length)
            slide = slide.set_audio(complete_audio)
            clips.append(slide)
        randmusic = random.choice(os.listdir("musics"))
        while randmusic.endswith(".txt"): randmusic = random.choice(os.listdir("musics"))
        randpath = "musics/" + randmusic
        music = AudioFileClip(randpath)
        music = audio_fadein(music, 20)
        music = audio_fadeout(music, 20)
        music = volumex(music, 0.2)
        musics = []
        if music.duration < total_length:
            for i in range(int(total_length / music.duration)):
                musics.append(music)
            music = concatenate_audioclips(musics)
        music = music.set_duration(total_length)
        final_clip = concatenate_videoclips(clips, method="compose")
        existing_audio = final_clip.audio
        final_audio = CompositeAudioClip([existing_audio, music])
        final_clip = final_clip.set_audio(final_audio)
        final_clip.write_videofile(path + "/montage.mp4", fps=60, codec="nvenc")
        srt.save(path + "/montage.srt")
        with open (randpath.split(".")[0] + ".txt", 'r', encoding='utf-8') as f:
            music_credit = f.read()
            f.close()
        return music_credit or ""
    else:
        return ""