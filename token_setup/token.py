from jose import jwt,JWTError
from datetime import datetime,timedelta
from DB.db_setup import get_db, Karyawan
import secrets
import logging
from logger_config import *

logger = logging.getLogger(__name__)

SECRET_KEY=secrets.token_hex(32)
ALGORITHM="HS256"

def create_token(username):
    payload={
        "username":username,
        "exp":datetime.utcnow() + timedelta(minutes=60)
    }

    try:
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token
        
    except JWTError as e:
        logger(f"token gagal dibuat: {str(e)}")
        return {"status": "error", "pesan": f"Gagal membuat token"}

def verify_token(token):
    try:
        session=get_db()
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        karyawan=session.query(Karyawan).filter(Karyawan.username==payload['username']).first()
        session.close()
        if not karyawan:
            return None
        return payload['username']
        
    except JWTError:
        return None
        
        

    
