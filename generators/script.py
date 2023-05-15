import os
import json
import asyncio
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_script(title, description):
    with open('prompts/script.txt') as f:
        prompt = f.read()
        f.close()
    prompt = prompt.replace("[title]", title)
    prompt = prompt.replace("[description]", description)
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role":"user","content":prompt}
        ],
        )
    return response['choices'][0]['message']['content']