# FABLE

**The *Film and Artistic Bot for Lively Entertainment***

This repository contains a software that connectsa whole bunch of scripts and tools together to automate the process of generatig unlimited videos from a given subject. It handles everything from creating the script, to generating the video, to uploading it to YouTube as well as creating the thumbnail and the description.

# READ THIS FIRST
This repository is a labor of love, the result of countless hours of work, and a testament to my passion for open-source software. You see, I'm a big fan of open source. I've developed and participated in many such projects, and I believe in the power of community collaboration.

However, for this particular project, there's a twist. While I'm more than happy for you to use, modify, and learn from this software, I've decided to impose certain restrictions on its commercial use. Let me explain why.

In a nutshell, I don't want anyone to make a profit directly from this specific project or the content generated from it. This includes selling the videos created by this software, offering services to generate such videos, or monetizing these videos on any online platform (think YouTube, Twitch, Patreon, and so forth).

The reason is simple. This project was created out of passion, not for profit, and I want to ensure that it is used in the spirit it was created in. It's about learning, sharing knowledge, and having fun while doing so. It's not about turning a quick profit.

In the spirit of clarity, even a small part of the code used elsewhere still falls under these rules. So, if you're thinking of using just a tiny piece of the code for commercial purposes, please think again. The terms are pretty straightforward - use the software, enjoy it, but don't profit from it.

And lastly, when using this software, I'd appreciate it if you mention me, Paillat-dev (https://paillat.dev), in any licensing or attribution notes. It's a small ask that goes a long way in supporting individual developers like me.

Now, with all that said, I hope you enjoy exploring this project as much as I did creating it. Your support means the world to me, and I can't wait to see what amazing things you do with it (within the rules, of course 😉).

Happy coding!

***For more detailed information about the license conditions, please refer to the LICENSE file in the root directory of this project.***

# Getting Started
:warning: <strong> This is not a tutorial on how to use the software. You will need to know how to use the command line and how to install dependencies, <ins>as well as some knowledge on how to look for other tutorials on the internet if you get stuck.</ins></strong>

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
