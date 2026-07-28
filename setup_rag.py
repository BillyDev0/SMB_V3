import requests
import chromadb

# =========================
# ChromaDB
# =========================
client = chromadb.Client()
collection = client.create_collection("barang")

EMBED_URL = "http://localhost:11434/api/embed"


def embed_documents():

    # Membaca dokumen
    with open("documents.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk manual berdasarkan paragraf
    chunks = text.split("\n\n")

    # Generate embedding
    response = requests.post(
        EMBED_URL,
        json={
            "model": "nomic-embed-text:latest",
            "input": chunks
        }
    )

    embeddings = response.json()["embeddings"]

    # Simpan ke ChromaDB
    collection.add(
        ids=[f"chunk_{i}" for i in range(1,len(chunks)+1)],
        documents=chunks,
        embeddings=embeddings
    )

def embed_query(query):
    response = requests.post(EMBED_URL,json={"model":"nomic-embed-text:latest","input":query})
    embedding=response.json()['embeddings'][0]


embed_documents()
