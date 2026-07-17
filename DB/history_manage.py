from DB.db_setup import get_db,History
import logging
from logger_config import *

logger = logging.getLogger(__name__)

def get_history(username:str):
    session=get_db()
    data_history=session.query(History)\
        .filter(History.username==username)\
        .order_by(History.id.desc())\
        .limit(10)\
        .all()
    session.close()

    data_history=data_history[::-1]

    return "\n".join([f"{i.role}: {i.message}"
                      for i in data_history])


def save_history(username,role,message):
    session=get_db()
    try:
        new_history=History(username=username,role=role,message=message)
        if not new_history.username:
            return {"status": "error", "pesan": f"Username '{username}' tidak ditemukan."}
             
        session.add(new_history)
        session.commit()

    except Exception as e:
            session.rollback()
            logger.error(f"gagal menyimpan history chat: {str(e)}")
            return{f"status":"error","pesan":f"gagal menyimpan history"}
    finally:
         session.close()