import openai 
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
subject = os.getenv("SUBJECT")
with open('prompts/ideas.txt') as f:
    prompt = f.read().replace('[subject]', subject)
    f.close()


async def generate_ideas():
    with open('ideas/ideas.json', 'r') as f:
        ideas = f.read()
        f.close()
    prmpt = prompt.replace('[existing ideas]', ideas)
    print(prmpt)
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":prmpt},
        ],
        )
    return response['choices'][0]['message']['content']