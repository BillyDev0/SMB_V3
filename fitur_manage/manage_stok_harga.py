from DB.db_setup import get_db,Barang
import logging
from logger_config import *
from fastapi import FastAPI
logger = logging.getLogger(__name__)

app=FastAPI()

@app.post('/s')
def tambah_stok(nama_barang:str,stok_tambahan:int):
    session=get_db()
    try:
        nama_barang=nama_barang.lower()
        barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
        if not barang:
            return {'msg':'barang tidak ditemukan'}
        barang.stok_barang=barang.stok_barang+stok_tambahan
        session.commit()
        logger.info(f"{nama_barang} menambah stok ")

        return {
                "status": "sukses",
                "pesan": f"Barang '{nama_barang}' berhasil menambah stok sebanyak {stok_tambahan}.",
                "data": {
                    "nama_barang": nama_barang,
                    "harga_barang": barang.harga_barang,
                    "stok_barang": barang.stok_barang,
                },
            }
    except Exception as e:
        logger.exception(f"gagal menambah stok barang: {str(e)}")
        return {"status":"error","pesan":f"gagal menambah stok barang"}

    finally:
        session.close()

def diskon(min_stok:int=None,nama_barang:str=None,besar_diskon:int=20):
    session=get_db()
    try:
        if besar_diskon <=0:
            return {"status": "error", "pesan": f"'{besar_diskon}' diskon tidak valid"}
        
        if nama_barang is None and min_stok is None:
            return {"status": "error", "pesan": f"informasi barang tidak valid"}


        query=session.query(Barang)
        if nama_barang is not None:
            query=query.filter(Barang.nama_barang.ilike(f"%{nama_barang}%"))

        if min_stok is not None:
            query=query.filter(Barang.stok_barang>=min_stok)

        barang=query.all()
        for i in barang:
            harga_asli=i.harga_barang
            diskon=i.harga_barang*(besar_diskon/100)
            i.harga_barang=i.harga_barang-diskon
            logger.info(f"{i.nama_barang} berhasil menambah stok")

        data = {
                "status": "sukses",
                "pesan": f"berhasil menerapkan diskon sebesar {besar_diskon}%.",
                "data": [{
                        "nama_barang": i.nama_barang,
                        "harga_asli": harga_asli,
                        "harga_diskon":i.harga_barang,
                        "stok_barang": i.stok_barang,
                    }for i in barang],
                }
        session.commit()
        return data
        
    except Exception as e:
        session.rollback()
        logger.exception(f"diskon gagal diterapkan: {str(e)}")
        return{'status':'error','pesan':f'diskon gagal diterapkan'}

    finally:
        session.close()
    

    
        

    
# print(tambah_stok('marjan',1))