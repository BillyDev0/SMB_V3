from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import json

embedding = OllamaEmbeddings(model="nomic-embed-text:latest")


def embed_file():
    if os.path.exists("./vector_db"):
        return Chroma(
            embedding_function=embedding,
            persist_directory="./vector_db"
        )

    with open("documents.txt") as f:
        text=f.read()
    
    chunk=text.split("\n\n")

    return Chroma.from_texts(
        embedding=embedding,
        texts=chunk,
    )

def similarity_search(prompt):
    vector_db=embed_file()
    retriever=vector_db.as_retriever()
    context=retriever.invoke(prompt)
    return context[0]

