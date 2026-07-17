from chatbot.tanya_ai import tanya_ai
from fastapi import FastAPI 
from auth.login import login
from auth.registrasi import registrasi
from token_setup.token import verify_token
from pydantic import BaseModel
import logging
from logger_config import *

logger = logging.getLogger(__name__)

app=FastAPI()

class RegisterScema(BaseModel):
    username:str
    password:str

@app.post('/tanyaa_AI')
def chatbot_AI(token:str,prompt:str):
    username=verify_token(token)
    if not username:
        logger.error("token error")
        return{'status':'error','pesan':'token error'}
    respon_ai=tanya_ai(username,prompt)
    return respon_ai

@app.post('/login')
def loginn(karyawan:RegisterScema):
    return login(karyawan.username,karyawan.password)

@app.post('/register')
def registt(karyawan:RegisterScema):
    return registrasi(karyawan.username,karyawan.password)
   



