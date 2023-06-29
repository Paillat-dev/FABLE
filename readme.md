# Videos Automator
This repository contains a whole bunch of scripts and tools connected together to automate the process of generatig unlimited videos from a given subject. It handles everything from creating the script, to generating the video, to uploading it to YouTube as well as creating the thumbnail and the description.

# Getting Started
:warning: <strong> This is not a tutorial on how to use the scripts. You will need to know how to use the command line and how to install dependencies, <ins>as well as some knowledge on how to look for other tutorials on the internet if you get stuck.</ins></strong>

If it is the first time you are using this repository, you will need to install the dependencies. To do so, run the following command:
```
pip install -r requirements.txt
```
You will also need to install [FFmpeg](https://ffmpeg.org/download.html) in order for `moviepy` to work.

You will need an `openai_api_key` and an `unsplash_access_key` in order to use the script. You can get them [here](https://beta.openai.com/), and [here](https://unsplash.com/developers). You will be told when to paste them. You can always change them later in the `env.yaml` file.

You should also prepare google oauth client id json for the youtube api for each account you want to automate. You can find a tutorial on how to do that [here](https://developers.google.com/youtube/v3/quickstart/python). You will be asked to add it to the corresponding folder when you run the script for the first time for each channel.

Now, you can run the `main.py` script to generate the videos. If it is the first time you are running the script, it will ask you to log in to your Google account, as well as creating and moving or creating some files. The created videos will be saved in the `videos` folder, and automatically uploaded to YouTube. The script will also create a thumbnail and a description for each video, and add a nice background music to it.

# Other stuff
In each channel's folder there will be a `channel.yaml` file with all of the channel's settings. You can change them manually, but you will need to restart the script for the changes to take effect.
