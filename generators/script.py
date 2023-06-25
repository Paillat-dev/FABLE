import os

from utils.openaicaller import openai

with open('prompts/script.txt') as f:
    global_prompt = f.read()
    f.close()

async def generate_script(title, description):
    prompt = global_prompt
    prompt = prompt.replace("[title]", title)
    prompt = prompt.replace("[description]", description)
    '''response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role":"user","content":prompt}
        ],
        )''' # Deprecated. Use openaicaller.py instead
    response = await openai.generate_response(model="gpt-4", messages=[{'role':'user', 'content': prompt}])
    return response['choices'][0]['message']['content'] # type: ignore