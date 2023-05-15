import openai
import os

from PIL import Image, ImageDraw, ImageFont
import random
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
'''
Putpose of this file is to generate a miniature of the video.
It has a function that takes a path, title, and description and generates a miniature.
It uses pillow to generate the image, and openai to generate text1 and text2.

text 1 is a short text max 2 words to put on the top of the image.
text 2 is a 3 word text to put in the middle of the image.

The function returns the path of the image.

First open bcg.png. Then create a new image and add a random gradient to it from top to bottom.
then put the png on top of the gradient.
Then add text1 and text2 to the image.
'''

prompt = '''Generate 2 short textes OF MAX 2-4 WORDS each to put on the top of the miniature of the video. Here are some examples:
For the title "Python Exception Handling" the text1 could be "No more crashes!" and the text2 could be "Easy!"
The second text is often shorter than the first one.
Answer without anything else, just with the 2 textes. Answer with text1 on the first line and text2 on the second line. Nothing else.
Here is the title of the video: [TITLE]
Here is the description of the video: [DESCRIPTION]'''

def rand_gradient(image):
    randr = random.SystemRandom().randint(1, 20)
    randg = random.SystemRandom().randint(1, 20)
    randb = random.SystemRandom().randint(1, 20)

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            colors = [i//randr, j//randg, i//randb]
            position1 = [image.size[0]//5, image.size[1]//5]
            position2 = [image.size[0]//5, image.size[1]//2]
            if i == position1[0] and j == position1[1]:
                textcolor1 = colors
            if i == position2[0] and j == position2[1]:
                textcolor2 = colors
            image.putpixel((i,j), (colors[0], colors[1], colors[2]))
    return image, textcolor1, textcolor2

def generate_miniature(path, title, description):
    prmpt = prompt.replace("[TITLE]", title).replace("[DESCRIPTION]", description)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"user","content":prmpt},
        ],
        )
    response['choices'][0]['message']['content']
    text1 = response['choices'][0]['message']['content'].split("\n")[0]
    text2 = response['choices'][0]['message']['content'].split("\n")[1]
    generate_image(path, text1, text2)

def generate_image(path, text1, text2):
    path_to_bcg = path.split("/")[:-1]
    path_to_bcg = "/".join(path_to_bcg)
    print(path_to_bcg)
    if not os.path.exists(f"{path_to_bcg}/bcg.png"):
        input("bcg.png not found. Please put bcg.png in the same folder as the video."+path_to_bcg)
        if not os.path.exists(f"{path_to_bcg}/bcg.png"):
            input("bcg.png still not found. Exiting.")
            exit()
    bcg = Image.open(f"{path_to_bcg}/bcg.png")
    img = Image.new('RGBA', (1920, 1080))
    img, textcolor1, textcolor2 = rand_gradient(img)
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("./Sigmar-Regular.ttf", 200)
    font2 = ImageFont.truetype("./Sigmar-Regular.ttf", 200)
    text1words = text1.split(" ")
    text2words = text2.split(" ")
    text1def = ""
    text2def = ""
    #max charachters per line is 7, but if a word is longer than 7 charachters, do not split it. Howerver if 2 or more words can fit on the same line, put them on the same line.
    for word in text1words:
        if len(text1def.split("\n")[-1]) + len(word) > 7:
            text1def += "\n"
        text1def += word + " "
    for word in text2words:
        if len(text2def.split("\n")[-1]) + len(word) > 7:
            text2def += "\n"
        text2def += word + " "
    maxlen1 = max([len(line) for line in text1def.split("\n")])
    maxlen2 = max([len(line) for line in text2def.split("\n")])
    #if the text is too long, reduce the font size proportionally
    if maxlen1 > 7:
        font1 = ImageFont.truetype("./Sigmar-Regular.ttf", 200 - (maxlen1 - 7)*10)
    if maxlen2 > 7:
        font2 = ImageFont.truetype("./Sigmar-Regular.ttf", 200 - (maxlen2 - 7)*10)
    text1def = text1def.upper().strip()
    text2def = text2def.upper().strip()
    textcolor1 = [255 - textcolor1[0], 255 - textcolor1[1], 255 - textcolor1[2]]
    textcolor2 = [255 - textcolor2[0], 255 - textcolor2[1], 255 - textcolor2[2]]
    imgtext1 = Image.new('RGBA', (1920, 1080))
    imgtext2 = Image.new('RGBA', (1920, 1080))
    drawtext1 = ImageDraw.Draw(imgtext1)
    drawtext1.text((imgtext1.size[0]//8*2, 0), text1def, font=font1, fill=(textcolor1[0], textcolor1[1], textcolor1[2]))
    imgtext1 = imgtext1.rotate(-5, expand=True)
    drawtext2 = ImageDraw.Draw(imgtext2)
    drawtext2.text((imgtext2.size[0]//8*2.5, imgtext2.size[1]//5*2), text2def, font=font2, fill=(textcolor2[0], textcolor2[1], textcolor2[2]))
    imgtext2 = imgtext2.rotate(5, expand=True)
    #paste the textes on the image
    img.paste(bcg, (0, 0), bcg)
    img.paste(imgtext1, (0, 0-img.size[1]//8), imgtext1)
    if len(text1def.split("\n")) > 2: #if the text is too long, put the second text on the third line
        img.paste(imgtext2, (0, img.size[1]//8), imgtext2)
    else:
        img.paste(imgtext2, (0, 0), imgtext2)
    img.save(path + "/miniature.png")
    return path + "/miniature.png"