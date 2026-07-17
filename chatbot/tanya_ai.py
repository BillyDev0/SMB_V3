import requests
from fitur_manage.get_daftar_barang import get_barang
from fitur_manage.hapus_barang import hapus_barang
from fitur_manage.tambah_barang import tambah_barang
from fitur_manage.update_stok import update_barang
from DB.history_manage import save_history,get_history
from fitur_manage.manage_stok_harga import tambah_stok,diskon
from fitur_manage.batas_stok import cek_stok_menipis
import logging
from logger_config import *
from fastapi import FastAPI
app=FastAPI()
logger = logging.getLogger(__name__)

AI_server="http://localhost:11434/api/chat"


def jawab_chat(message):
    AI_generate='http://localhost:11434/api/generate'

    prompt=f"""Kamu adalah asisten toko yang ramah dan helpful. 
    Jawab pertanyaan atau sapaan user berikut dengan singkat dan natural dalam bahasa Indonesia.
    
    prompt user:
    {message}
    """
    payload={
        "model":"qwen2.5:7b",
        "prompt":prompt,
        "stream":False,
        "options":{
            "temperature":0.3,
            "num_predict":150,
            "top_p":0.5
        }
    }

    try:
        res=requests.post(AI_generate,json=payload)
        jawaban=res.json()['response']
        return jawaban

    except requests.exceptions.ConnectionError:
        return{f"status":"error","pesan":f"server ollama belum dijalankan"}

def generate(message):
    AI_generate='http://localhost:11434/api/generate'

    prompt=f"""Kamu adalah asisten sistem manajemen barang.

Tugasmu adalah mengubah semua hasil dari backend menjadi jawaban yang alami dan mudah dipahami.

Aturan:
- Jangan mengubah fakta pada data.
- Jangan menambahkan informasi yang tidak ada.
- Gunakan bahasa Indonesia yang sopan dan ringkas.
- Jika data berupa daftar, buat menjadi poin-poin yang rapi.
- Jika status adalah "error", jelaskan pesan error kepada pengguna dengan bahasa yang mudah dipahami.
- Jika status adalah "success", sampaikan hasilnya secara natural.
- jangan bertele - tele
    
    prompt user:
    {message}
    """
    payload={
        "model":"qwen2.5:7b",
        "prompt":prompt,
        "stream":False,
        "options":{
            "temperature":0.3,
            "num_predict":150,
            "top_p":0.5
        }
    }

    try:
        res=requests.post(AI_generate,json=payload)
        jawaban=res.json()['response']
        return jawaban

    except requests.exceptions.ConnectionError:
        return{f"status":"error","pesan":f"server ollama belum dijalankan"}
    

tools={
        "tambah_barang":tambah_barang,
        "get_barang":get_barang,
        "hapus_barang":hapus_barang,
        "update_barang":update_barang,
        "tambah_stok":tambah_stok,
        "diskon_barang":diskon,
        "cek_stok_menipis":cek_stok_menipis,
        "chat":jawab_chat
}
@app.get('/d')
def tanya_ai(username,prompt):
    logger.info(f"username {username} mengirim prompt {prompt}")

    history=get_history(username)
    

    payload={
        "model":"qwen2.5:7b",
        "messages":[
            {
                "role":"system",
                "content":f"""
                
                Konteks (jika relevan): {history}

                ATURAN:
                - Pilih action paling sesuai
                - Semua nilai WAJIB dari INPUT USER, jangan mengarang, jangan pakai isi contoh
                - Field yang tidak disebutkan user: JANGAN disertakan
                JSON:"""
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        "stream":False,
        "tools":[
            {
            "type":"function",
            "function":{
                "name":"get_barang",
                "description":"fitur ini untuk mencari barang berdasarkan nama barang, maksimum harga, minimum harga, dan menampilkan semua barang",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "nama_barang":{
                            "type":"string",
                            "description":"untuk mencari nama barang"
                        },
                        "max_harga":{
                            "type":"number",
                            "description":"untuk mencari maksimum harga barang"
                        },
                        "min_harga":{
                            "type":"number",
                            "description":"untuk mencari minimum harga barang"
                        }
                    }
                }
            }
        },

        {
            "type":"function",
            "function":{
                "name":"tambah_barang",
                "description":"fitur ini untuk menambah barang yang user mau",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "nama_barang":{
                            "type":"string",
                            "description":"berisi nama barang yang akan ditambah"
                        },
                        "harga_barang":{
                            "type":"number",
                            "description":"berisi harga satuan barang"
                        },
                        "stok_barang":{
                            "type":"integer",
                            "description":"berisi jumlah stok"
                        }
                    },
                    "required":[
                        "nama_barang",
                        "harga_barang",
                        "stok_barang"
                    ]
                }
            }
        },

        {
            "type":"function",
            "function":{
                "name":"hapus_barang",
                "description":"fitur ini untuk menghapus barang yang user inginkan",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "nama_barang":{
                            "type":"string",
                            "description":"berisi nama barang yang akan dihapus"
                        }
                    },
                    "required":[
                        "nama_barang"
                    ]
                }
            }
        },

        {
            "type":"function",
            "function":{
                "name":"update_barang",
                "description":"fitur ini untuk update data barang",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "nama_barang":{
                            "type":"string",
                            "description":"berisi nama barang yang akan diupdate"
                        },
                        "harga_barang":{
                            "type":"number",
                            "description":"berisi harga satuan barang",
                        },
                        "stok_barang":{
                            "type":"integer",
                            "description":"beriski jumlah stok barang"
                        }
                    },
                    "required":[
                        "nama_barang"
                    ]
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"tambah_stok",
                "description":"fitur ini untuk menambah stok barang",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "nama_barang":{
                            "type":"string",
                            "description":"berisi nama barang"
                        },
                        "stok_tambahan":{
                            "type":"integer",
                            "description":"berisi jumlah stok barang yang mau ditambahkan, ambil angka nya saja"
                        }
                    },
                    "required":[
                        "nama_barang",
                        "stok_tambahan"
                    ]
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"diskon_barang",
                "description":"fitur ini untuk memberikan diskon pada barang",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "min_stok":{
                            "type":"integer",
                            "description":"berisi minimum stok barang. contoh: yang kurang dari 50"
                        },
                        "nama_barang":{
                            "type":"string",
                            "discription":"berisi nama barang"
                        },
                        "besar_diskon":{
                            "type":"number",
                            "discription":"berisi besar diskon yang diberikan"
                        }
                    },
                    "required":[
                        "besar_diskon"
                    ]
                }
            }
        },

        {
            "type":"function",
            "function":{
                "name":"cek_stok_menipis",
                "description":"fitur ini untuk cek stok yang menipis atau dibawah batas maksimal",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "stok_max":{
                            "type":"integer",
                            "description":"berisi batas maksimal stok barang "
                        }
                    }
                }
            }
        },

        {
            "type":"function",
            "function":{
                "name":"chat",
                "description":"fitur ini untuk obrolan random dengan user",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "message":{
                            "type":"string",
                            "description":"isi obrolan"
                        }
                    },
                    "required":[
                        "message"
                    ]
                }
            }
        }
    ],
        "options":{
            "temperature":0,
            "num_predict":80,
            "top_p":0.5
        }
    }

    try:
        save_history(username,"User",prompt)
        res=requests.post(AI_server,json=payload)
    
        if res.status_code!=200:
            return res.text
        logger.info(f"{res.json()}")
        output_AI=res.json()['message']
        tool_calls=output_AI.get('tool_calls')
        if tool_calls:
            all_action=[]
            for data in tool_calls:
                nama=data['function']['name']
                args=data['function']['arguments']

                logger.info({f"output AI to function: tools:{nama}, args:{args}"})

                tools_dipakai=tools[nama]
                jawaban=tools_dipakai(**args)
                all_action.append(jawaban)

            output=generate(all_action)
            save_history(username,"AI",output)
            logger.info({f"output AI to user: tools:{nama}, output:{output}"})
            return output
    
        else:
            content=output_AI['content']

            if content:
                logger.info({f"output content to user: {content}"})
                return content
              

            else:
                return {
                    "status": "error",
                    "pesan": "Permintaan tidak dapat diproses. Pastikan data yang dimasukkan lengkap dan sesuai format."
                }

    except Exception as e:
        logger.exception(f"Error tidak terduga: {str(e)}")
        return {"status": "error", "pesan": "terjadi kesalahan pada sistem"}
