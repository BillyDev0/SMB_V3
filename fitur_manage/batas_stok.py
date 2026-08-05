from DB.db_setup import Barang,get_db
import logging
from logger_config import *
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

@tool
def cek_stok_menipis(stok_max:int=100):
    """Menampilkan daftar barang yang stoknya di bawah batas tertentu (stok_max).
    Gunakan tool ini saat user ingin tahu barang mana yang stoknya menipis
    atau perlu di-restock. Tool ini bersifat READ-ONLY — tidak melakukan
    perubahan data apapun (bandingkan dengan tambah_stok yang mengubah data).
    Jika user tidak menyebutkan angka batas, gunakan nilai default.
    """
    session=get_db()
    try:
        if stok_max is not None:
            if stok_max <=0:
                return {"status":"error","pesan":f"input stok tidak valid"}
            
            cek_stok=session.query(Barang).filter(Barang.stok_barang<=stok_max).all()
            if not cek_stok:
                logger.info(f"stok barang tidak ada yang kurang dari {stok_max}")
                return {"status": "safe", "pesan": "stok barang aman"}

            return {
                    "status": "warning",
                    "pesan": f"{len(cek_stok)} barang stoknya menipis.",
                    "data": [{
                        "nama_barang": i.nama_barang,
                        "harga_barang": i.harga_barang,
                        "stok_barang": i.stok_barang,
                    }for i in cek_stok],
                }

    except Exception as e:
        logger.exception(f"gagal cek stok barang: {str(e)}")
        return {"status":"error","pesan":"gagal mengecek stok barang"}

    finally:
        session.close()
    