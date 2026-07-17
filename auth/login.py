from DB.db_setup import Karyawan,get_db
from passlib.hash import bcrypt
from token_setup.token import create_token
from chatbot.tanya_ai import logging
from fitur_manage.batas_stok import cek_stok_menipis
import logging
from logger_config import *


logger = logging.getLogger(__name__)

def login(username,password):
    # ── Validasi kosong / None ────────────────────────────────────────────────
        logger.info(f"{username} mencoba login")
        if username is None or str(username).strip() == "":
            return {"status": "error", "pesan": "Username tidak boleh kosong."}
    
        if password is None or str(password).strip() == "":
            return {"status": "error", "pesan": "Password tidak boleh kosong."}
    
        username = username.strip()
        password = password.strip()
    
        # ── Cek username sudah terdaftar atau belum ───────────────────────────────
        session=get_db()
        try:
            cek_karyawan=session.query(Karyawan).filter(Karyawan.username==username).first()
            if not cek_karyawan:
                return {"status": "error", "pesan": f"Username '{username}' belum terdaftar."}

            if not bcrypt.verify(password,cek_karyawan.password):
                 return {"status": "error", "pesan": "Password salah."}
            logger.info(f"{username} berhasil login")

            token=create_token(cek_karyawan.username)
            if not token:
                 return{"status":"error","pesan":f"Token error"}

            return{'token': token,
                   'notifikasi':cek_stok_menipis()}

        except Exception as e:
             session.rollback()
             logger.exception(f"Login error: {str(e)}")
             return {"status": "error", "pesan": f"Login error"}

        finally:
             session.close()

