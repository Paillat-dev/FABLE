import os
import json
import asyncio
import logging

from generators.ideas import generate_ideas
from generators.script import generate_script
from generators.montage import mount, prepare, translate
from generators.miniature import generate_miniature

logging.basicConfig(level=logging.INFO)

async def main():
    with open('env/subjects.txt', 'r', encoding='utf-8') as f:
        subjects = f.read().splitlines()
        f.close()
    for i in range(len(subjects)):
        print(str(i) + ". " + subjects[i])
    subject = int(input("Which subject do you want to generate ideas for? (enter the number): "))
    subject = subjects[subject]
    subjectdirpath = subject[:25].replace(" ", "_").replace(":", "")
    if not os.path.exists(subjectdirpath): os.makedirs(subjectdirpath)
    if input("Do you want to generate new ideas? (y/n)") == "y":
        await generate_ideas(subjectdirpath)
    with open('ideas/ideas.json', 'r', encoding='utf-8') as f:
        ideas = json.load(f)
        f.close()
    for i in range(len(ideas)):
        print(str(i) + ". " + ideas[i]['title'])
    idea = int(input("Which idea do you want to generate a script for? (enter the number): "))
    idea = ideas[idea]
    title = idea['title']
    title = title[:25]
    i = 0
    path = subjectdirpath + "/" + title
    path = path.replace(" ", "_").replace(":", "")
    if not os.path.exists(path + "/script.json"):
        script = await generate_script(idea['title'], idea['description'])
        if os.path.exists(path) and os.path.exists(path + "/script.json"):
            if input("There is already a script for this idea. Do you want to overwrite it? (y/n)") != "y":
                print("Exiting...")
                exit(1)
        if not os.path.exists(path): os.makedirs(path)
        with open(path + "/script.json", 'w', encoding='utf-8') as f:
            f.write(script)
            f.close()
    script = prepare(path)
    credits = mount(path, script)
    with open(path + "/meta.txt", 'w', encoding='utf-8') as f:
        f.write(f"Title: {idea['title']}\nDescription: {idea['description']}\nMusic credits: {credits}")
        f.close()
    with open(path + "/meta_FR.txt", 'w', encoding='utf-8') as f:
        transtitle = translate('FR', idea['title']) #use the non formatted title
        transdesc = translate('FR', idea['description'])
        f.write(f"Titre: {transtitle}\nDescription: {transdesc}\nCrédits musicaux: {credits}")
        f.close()
    generate_miniature(path, title=idea['title'], description=idea['description'])
    print(f"Your video is ready! You can find it in {path}.")

if __name__ == "__main__":
    asyncio.run(main())