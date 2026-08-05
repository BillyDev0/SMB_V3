import requests
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.update_stok import update_barang
from DB.history_manage import save_history,get_history
from fitur_manage.manage_stok_harga import tambah_stok,diskon
from fitur_manage.batas_stok import cek_stok_menipis
from chatbot import daftar_tools
import logging
from logger_config import *
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json
from RAG_AI import similarity_search
from langchain_ollama import ChatOllama,OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app=FastAPI()
logger = logging.getLogger(__name__)

AI_server="http://localhost:11434/api/chat"


async def generate(user_prompt):
    model=OllamaLLM(model="qwen2.5:7b",
                    top_p=0.3,
                    num_predict=80,
                    temperature=0.5)

    template="""Kamu adalah asisten sistem manajemen barang.

Tugasmu adalah mengubah semua hasil dari backend menjadi jawaban yang alami dan mudah dipahami, kecuali hasil yang berupa pengetahuan umum


Aturan:
- Jangan mengubah fakta pada data.
- Jangan menambahkan informasi yang tidak ada.
- Gunakan bahasa Indonesia yang sopan dan ringkas.
- Jika data berupa daftar, buat menjadi poin-poin yang rapi.
- Jika status adalah "error", jelaskan pesan error kepada pengguna dengan bahasa yang mudah dipahami.
- Jika status adalah "success", sampaikan hasilnya secara natural.
- jangan bertele - tele
- jika prompt berisi pengetahuan umum maka tidak perlu di sederhanakan
- Jika informasi tidak tersedia di context, katakan "informasi tersebut tidak tersedia."

    
    prompt user:
    {prompt}
    """
    try:
        prompt=ChatPromptTemplate.from_template(template)
        chain=prompt|model
        
        for chunk in chain.stream({"prompt":user_prompt}):
            yield chunk
    except requests.Exception as e:
        logger.exception(f"Error tidak terduga: {str(e)}")
        print("terjadi kesalahan pada sistem")
    


async def streame_collect(username:str,message:str):
    tokens=[]
    async for chunk in generate(message):
        tokens.append(chunk)
        yield chunk

    save_history(username,"AI","".join(tokens))

tools=[
        tambah_barang,
        get_barang,
        hapus_barang,
        update_barang,
        tambah_stok,
        diskon,
        cek_stok_menipis,
]

map_tools={
        "tambah_barang":tambah_barang,
        "get_barang":get_barang,
        "hapus_barang":hapus_barang,
        "update_barang":update_barang,
        "tambah_stok":tambah_stok,
        "diskon":diskon,
        "cek_stok_menipis":cek_stok_menipis,
}

@app.get('/d')
async def tanya_ai(username,user_prompt):
    logger.info(f"username {username} mengirim prompt {user_prompt}")

    history=get_history(username)
    
    context=similarity_search(user_prompt)

    model=ChatOllama(model="qwen2.5:7b",
                     top_p=0.3,
                     temperature=0.5
                     ).bind_tools(tools)

    template="""

Context (jika relevan): {context}

ATURAN:
- Pilih action paling sesuai
- Semua nilai WAJIB dari INPUT USER, jangan mengarang, jangan pakai isi contoh
- Field yang tidak disebutkan user: JANGAN disertakan
-Gunakan tool HANYA jika user meminta operasi atau informasitentang data barang.
-Jika user bertanya pengetahuan umum seperti "apa itu API?", "apa itu Python?", "apa itu RAG?", JANGAN gunakan tool.
-Jika pertanyaan tidak berhubungan dengan sistem barang,jawab menggunakan context jika relevan.
-Jangan memanggil tool hanya karena tool tersedia.
-Jika tidak yakin apakah tool diperlukan, JANGAN gunakan tool.

prompt: {user_prompt}
"""

   
    try:
        prompt=ChatPromptTemplate.from_template(template)
        chain=prompt|model
        result=chain.invoke({"context":context,"user_prompt":user_prompt})
        save_history(username,"User",user_prompt)

        output_AI=result
        tool_calls=output_AI.tool_calls
        logger.info(output_AI)

        all_action=[]
        if tool_calls:
            for data in tool_calls:
                nama=data['name']
                args=data['args']

                logger.info(f"output AI to function: tools:{nama}, args:{args}")

                tools_dipakai=map_tools[nama]
                jawaban=tools_dipakai.invoke(args)
                all_action.append(jawaban)
    
        else:
            content=output_AI.content

            if not content:
                all_action.append({
                        "status": "error",
                        "pesan": "Permintaan tidak dapat diproses. Pastikan data yang dimasukkan lengkap dan sesuai format."
                    })

            jawaban=content
            all_action.append(jawaban)

        async for chunk in streame_collect(username,"\n".join(map(str,all_action))):
            print(chunk,end="",flush=True)
            await asyncio.sleep(0.05)

        print()
        
    except Exception as e:
        logger.exception(f"Error tidak terduga: {str(e)}")
        print("terjadi kesalahan pada sistem")


def main():
    while True:
        prompt=input("prompt: ")
        if prompt=="close":
            break
        asyncio.run(tanya_ai("b",prompt))
main()