import requests
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
import os
import asyncio
import json

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

def tanya_ai(user_prompt):
   context=RAG(user_prompt)
   model=OllamaLLM(model="qwen2.5:7b")

   template="""
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
{user_prompt}
"""

   prompt=ChatPromptTemplate.from_template(template)
   chain=prompt|model
   for chunk in chain.stream({"context":context, "user_prompt":user_prompt, "options": {"temperature":0.3, "top_p":0.5}}):
      yield chunk

async def collect_stream(prompt):
   for chunk in tanya_ai(prompt):
      print(chunk,end="",flush=True)

      await asyncio.sleep(0.5)

   print()


def main():
   prompt=input("prompt: ")
   asyncio.run(collect_stream(prompt))

main()
