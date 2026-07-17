from DB.db_setup import get_db, Barang
import logging
from logger_config import *

logger = logging.getLogger(__name__)

def update_barang(nama_barang:str,harga_barang:float=None,stok_barang:int=None):

    if nama_barang is None or str(nama_barang).strip() == "":
        return {"status": "error", "pesan": "nama_barang tidak boleh kosong."}

    if harga_barang is not None and harga_barang<=0:
        return {"status":"error","pesan":"input harga barang error"}

    if stok_barang is not None and stok_barang<=0:
        return {"status":"error","pesan":"input stok barang error"}

    session=get_db()
    barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
    if not barang:
        return {"status":"error","pesan":"barang tidak ditemukan"}


    if harga_barang is None and stok_barang is None:
        return {"status":"error","pesan":"query harga dan stok kosong, data tidak dapat diupdate"}
    
    try:
        if harga_barang is not None:
            barang.harga_barang=harga_barang

        if stok_barang is not None:
            barang.stok_barang=stok_barang

        session.commit()
        logger.info(f"data {nama_barang} berhasil diupdate")
        
        return {
                    "status": "sukses",
                    "pesan": f"Barang '{nama_barang}' berhasil diupdate.",
                    "data": {
                        "nama_barang": nama_barang,
                        "harga_barang": barang.harga_barang,
                        "stok_barang": barang.stok_barang,
                    },
                }

    except Exception as e:
        session.rollback()
        logger.exception(f"data gagal diupdate: {str(e)}")
        return {"status": "error", "pesan": "Gagal mengupdate data"}

    finally:
        session.close()

    

        


        

    

    

    
            

    
        