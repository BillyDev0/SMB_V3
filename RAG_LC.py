import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os
import asyncio
import json
AI_serv='http://localhost:11434/api/generate'
embedding = OllamaEmbeddings(model="nomic-embed-text:latest")

def embed_docs():
    if os.path.exists("./vector_db"):
       return Chroma(
          persist_directory="./vector_db",
          embedding_function=embedding
       )
    
    with open("documents.txt") as f:
       text = f.read()

    chunks=text.split("\n\n")

    return Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        persist_directory="./vector_db"
    )

def RAG(prompt:str):
   vector_db=embed_docs()
   retriever=vector_db.as_retriever()
   output=retriever.invoke(prompt)
   return output[0]

def tanya_ai(prompt):
   context=RAG(prompt)
   messages=f"""
**ROLE**
Kamu adalah AI assistant untuk PT Nusantara Digital Solutions. Jawab pertanyaan berdasarkan context yang diberikan.

**REQUEST**
Jawab pertanyaan pengguna menggunakan informasi dari context. Jika informasi tidak tersedia di context, katakan bahwa informasi tersebut tidak tersedia.

**RULES**

1. Jangan mengarang informasi.
2. Gunakan hanya informasi yang terdapat dalam context.
3. Jawab secara singkat dan jelas.
4. Jika pertanyaan tidak berhubungan dengan context, katakan bahwa informasi tersebut tidak tersedia.
5. Jangan menyebutkan bahwa kamu sedang melakukan retrieval atau embedding.

**CONTEXT**
{context}

**USER QUESTION**
{prompt}
"""
   payload={
           "model":"qwen2.5:7b",
           "prompt":messages,
           "options":{
               "temperature":0.3,
               "num_predict":150,
               "top_p":0.5
           }
       }
   res=requests.post(AI_serv,json=payload,stream=True)
   res.raise_for_status()
   for line in res.iter_lines():
      if line:
         line=json.loads(line)
         yield line["response"]


async def collect_stream(prompt):
   for chunk in tanya_ai(prompt):
      print(chunk,end="",flush=True)

      await asyncio.sleep(0.5)

   print()


def main():
   prompt=input("prompt: ")
   asyncio.run(collect_stream(prompt))

main()
