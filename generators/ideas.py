import openai 
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
with open('prompts/ideas.txt') as f:
    prompt = f.read()
    f.close()


async def generate_ideas(path, subject):
    prmpt = prompt.replace('[subject]', subject)
    try:
        with open(f'{path}/ideas.json', 'r') as f:
            ideas = f.read()
            ides_json = json.loads(ideas)
            f.close()
    except:
        ides_json = []
        ideas = "There are no existing ideas."
    prmpt = prmpt.replace('[existing ideas]', ideas)
    print(prmpt)
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":prmpt},
        ],
        )
    json_in_str= response['choices'][0]['message']['content']
    json_obj = json.loads(json_in_str)
    for idea in json_obj:
        ides_json.append(idea)
    with open(f'{path}/ideas.json', 'w') as f:
        f.write(json.dumps(ides_json))
        f.close()