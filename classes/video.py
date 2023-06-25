import os
import json
import yaml

from utils.openaicaller import openai
from utils.normalize_file import normalize_file as nf
from utils.config import bcolors
from utils.misc import clear_screen, open_explorer_here, realbcolors, printm
from utils.uploader import upload_video

from generators.script import generate_script
from generators.montage import mount, prepare
from generators.thumbnail import generate_thumbnail

class Video:
    def __init__(self, idea, parent):
        self.parent = parent # The parent class, which is a Channel class
        self.id = None
        self.url = None
        self.script = None
        self.path = None
        self.idea = idea
        self.title = self.idea['title']
        self.description = self.idea['description']
        self.metadata = None
    
    async def generate(self):
        normalized_title = await nf(self.idea['title'])
        self.path = os.path.join(self.parent.path, "videos", normalized_title)
        if not os.path.exists( self.path):
            os.makedirs( self.path)
        script = None
        if os.path.exists(os.path.join( self.path, "script.json")):
            printm("Video script already exists. Do you want to overwrite it ?")
            if input("y/N") == "y":
                os.remove(os.path.join( self.path, "script.json"))
    
        if not os.path.exists(os.path.join( self.path, "script.json")):
            script = await generate_script(self.idea['title'], self.idea['description'])
            with open(os.path.join( self.path, "script.json"), "w") as f:
                json.dump(json.loads(script), f)
                f.close()
        else:
            with open(os.path.join( self.path, "script.json"), "r") as f:
                script = json.load(f)
                f.close()
        await prepare( self.path)
        credits = await mount(self.path, script)
        self.metadata = {
            "title": self.idea['title'],
            "description": self.idea['description'] + "\n\n" + credits,
        }
        await generate_thumbnail( self.path, self.idea['title'], self.idea['description'])
        videoid = await upload_video( self.path, self.idea['title'], self.metadata['description'], 28, "", "private", self.path)
        printm(f"Your video is ready! You can find it in { self.path}")
        video_meta_file = {
            "title": self.idea['title'],
            "description": self.metadata['description'],
            "id": videoid,
            "path":  self.path,
            "url": f"https://www.youtube.com/watch?v={videoid}",
        }
        with open(os.path.join( self.path, "video.yaml"), "w") as f:
            yaml.dump(video_meta_file, f)
            f.close()
        return video_meta_file