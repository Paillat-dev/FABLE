import os
import asyncio
import logging
import yaml

from utils.settings import settings
from classes.channel import Channel
from utils.config import loadingmessage, bcolors
from utils.misc import clear_screen, printm, getenv
from utils.openaicaller import openai
from utils.license import check_license_agreement
from utils.marpdownloader import download_marp_cli

logging.basicConfig(level=logging.INFO)

async def main():
    clear_screen()
    await check_license_agreement()
    printm(loadingmessage)
    await asyncio.sleep(0.5)
    printm("Welcome in FABLE, the Film and Artistic Bot for Lively Entertainment!")
    await asyncio.sleep(0.5)
    printm(f"This program will generate for you complete {bcolors.FAIL}{bcolors.BOLD}YouTube{bcolors.ENDC} videos, as well as uploading them to YouTube.")
    printm("Please wait until we have downloaded the necessary files...")
    await asyncio.sleep(0.5)
    download_marp_cli(force_download=bool(settings.force_download_marp_cli))
    settings.set_setting('force_download_marp_cli', False)
    if not os.path.exists('env.yaml'):
        printm("It looks like you don't have an OpenAI API key yet. Please paste it here:")
        openai_api_key = input("Paste the key here: ")
        openai.set_api_key(openai_api_key)
        env_file = {
            "openai_api_key": openai_api_key
        }
        with open('env.yaml', 'w') as f:
            yaml.dump(env_file, f)
            f.close()
    else:
        openai_api_key = getenv('openai_api_key')
        openai.set_api_key(openai_api_key)
    channels = os.listdir('channels')
    if len(channels) == 0:
        printm("It looks like you don't have any channels yet. Let's create one!")
        channel = Channel()
        await channel.create()
    else:
        if settings.skip_channel_default != None:
            if type(settings.skip_channel_default) == str:
                channel_name = settings.skip_channel_default
            elif type(settings.skip_channel_default) == int:
                channel_name = channels[settings.skip_channel_default]
            else:
                raise TypeError("The skip_channel_default setting must be either a string or an integer.")
            channel = Channel()
            await channel.load(channel_name)
        else:
            printm("Here are your channels:")
            for i, channel in enumerate(channels):
                printm(f"{i+1}. {channel}")
            printm(f"{len(channels)+1}. Create a new channel")
            index = input("Which channel do you want to use : ")
            if index == str(len(channels)+1):
                channel = Channel()
                await channel.create()
            else:
                channel_name = channels[int(index)-1]
                channel = Channel()
                await channel.load(channel_name)
    printm("Now, let's create a video!")
    printm("Here are all the ideas you have:")
    printm("0. Generate new ideas")
    for i, idea in enumerate(channel.ideas):
        printm(f"{i+1}. {idea['title']}")
    index = input("Which idea do you want to create a video for : ")
    if index == "0":
        printm("Generating new ideas...")
        await channel.generate_ideas()
        printm("Here are your new ideas:")
        for i, idea in enumerate(channel.ideas):
            printm(f"{i+1}. {idea['title']}")
        index = input("Which idea do you want to create a video for : ")
    idea = channel.ideas[int(index)-1]
    video = await channel.generate_video(idea)
    printm("Done!")
    printm("Here is the video:")
    printm(video.url)
    input("Press enter to continue...")
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
            input("Press enter to continue or type ctrl+c to quit : ")
            clear_screen()
        except KeyboardInterrupt:
            break