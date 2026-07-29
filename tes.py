import requests
import json
import asyncio

async def generate(message):
    AI_generate='http://localhost:11434/api/generate'

    payload={
        "model":"qwen2.5:7b",
        "prompt":message,
        "stream":True,
        "options":{
            "temperature":0.3,
            "top_p":0.5
        },
    }

    res=requests.post(AI_generate,json=payload)
    for line in res.iter_lines():
        if line:
            line=json.loads(line)
            yield line['response']
            

async def collect_stream(prompt: str):
    output=[]
    async for chunk in generate(prompt):
        print(chunk,end="",flush=True)
        output.append(chunk)

        await asyncio.sleep(0.05)

    print()

def main():
    prompt=input("Prompt Streaming: ")

    asyncio.run(collect_stream(prompt))

main()