from DB.db_setup import get_db,Barang
import logging
from logger_config import *

logger = logging.getLogger(__name__)

def hapus_barang(nama_barang):

    if nama_barang is None or str(nama_barang).strip() == "":
            return {"status": "error", "pesan": "nama_barang tidak boleh kosong."}

    session=get_db()
    try:
        barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
        if not barang:
            if not barang:
                return {"status": "error", "pesan": f"{nama_barang} tidak ditemukan"}
        session.delete(barang)
        data={"nama_barang": barang.nama_barang,"harga_barang": barang.harga_barang,"stok_barang": barang.stok_barang}
        session.commit()
        logger.info(f"{nama_barang} di hapus dari inventory")

        return {
                    "status": "sukses",
                    "pesan": f"Barang '{nama_barang}' berhasil dihapus.",
                    "data": data
                }

    except Exception as e:
        session.rollback()
        logger.exception(f"barang gagal di delete: {str(e)}")
        return{f"status":"error","pesan":"gagal menghapus data"}

    finally:
        session.close()
    