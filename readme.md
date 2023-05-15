# Videos Automator
This repository contains a whole bunch of scripts and tools connected together to automate the process of generatig unlimited videos from a given subject. It handles everything from creating the script, to generating the video, to uploading it to YouTube as well as creating the thumbnail and the description.

# Getting Started
:warning: **This is not a tutorial on how to use the scripts. You will need to know how to use the command line and how to install dependencies, as well as some knowledge on how to look for other tutorials on the internet if you get stuck.**

If it is the first time you are using this repository, you will need to install the dependencies. To do so, run the following command:
```
pip install -r requirements.txt
```
You will also need to install [FFmpeg](https://ffmpeg.org/download.html) in order for `moviepy` to work.

Now that you have installed the dependencies, you will need to add all the required values to the `.env` file like this:
```
OPENAI_API_KEY=
UNSPLASH_ACCESS_KEY=
DEEPL_ACCESS_KEY=
```
You should be able to find all the required keys with a quick Google search.

Now, open the blank text file called `subjects.txt` in the `env` folder and add the subjects you want to generate videos for, one per line. For example:
```
Educational and simple videos about physics
Python tutorials for both beginners and advanced programmers
```
One per line.

You should also prepare google oauth client id json for the youtube api for each account youo want to automate. You can find a tutorial on how to do that [here](https://developers.google.com/youtube/v3/quickstart/python). You will be asked to add it to the corresponding folder when you run the script for the first time for each subject.

Now, you can run the `main.py` script to generate the videos. If it is the first time you are running the script, it will ask you to log in to your Google account, as well as creating and moving or creating some files. The created videos will be saved in the `videos` folder, and automatically uploaded to YouTube. The script will also create a thumbnail and a description for each video, and add a nice background music to it.