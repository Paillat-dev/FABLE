import openai 
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
subject = os.getenv("SUBJECT")
with open('prompts/ideas.txt') as f:
    prompt = f.read().replace('[subject]', subject)
    f.close()


async def generate_ideas(path):
    with open(f'{path}/ideas.json', 'r') as f:
        ideas = f.read()
        ides_json = json.loads(ideas)
        f.close()
    prmpt = prompt.replace('[existing ideas]', ideas)
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