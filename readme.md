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
You can check the wiki's [Introduction here](https://github.com/Paillat-dev/FABLE/wiki/1.-Introduction).

# Other stuff
In each channel's folder there will be a `channel.yaml` file with all of the channel's settings. You can change them manually, but you will need to restart the script for the changes to take effect.

# Contributing
If you want to contribute to this project, you can do so by creating a pull request. You can check the #TODO section below.

# TODO
- [ ] Add a way to change the settings without restarting the script
- [ ] Add a more detailed tutorial on how to use the script & readme
- [ ] Add a generator for more beautiful thumbnails
- [ ] Add a way to change the background music / add a way to add more background music / add a way to have channel specific background music
- [ ] Same as with channel specifis script prompt, also for the marp heading and the oîdeas prompts. Make the optionally channel specific.
- [ ] Add a global settings dict with all of the settings, and a listener to changes in the settings file, to akkow changing the settings without restarting the script. Also allow all te settings to be passed as cli arguments.
- [ ] Add transtitions between photos
- [ ] Add generation of a video from a given text
- [ ] Add a way to add a watermark to the video
- [ ] Add a way to choose / make the AI choose the background image to the marp slides
- [ ] Ability to change speaker file or set it to no speaker file per channel option.
