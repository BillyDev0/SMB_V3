from DB.db_setup import get_db,Barang
import logging
from logger_config import *
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

@tool
def get_barang(nama_barang:str=None,max_harga:float=None,min_harga:float=None):
    
    """Mencari atau menampilkan data barang yang sudah ada di database.
    Gunakan tool ini saat user ingin melihat, mencari, atau mengecek barang
    berdasarkan nama, rentang harga (minimum/maksimum), atau menampilkan semua
    barang jika tidak ada filter yang diberikan.
    JANGAN gunakan untuk menambah, mengubah, atau menghapus data barang.
    """

    session=get_db()
    try:
        query=session.query(Barang)

        if nama_barang is not None:
            query=query.filter(Barang.nama_barang.ilike(f"%{nama_barang}%"))

        if max_harga is not None:
            query=query.filter(Barang.harga_barang<=max_harga)

        if min_harga is not None:
            query=query.filter(Barang.harga_barang>=min_harga)

        query=query.all() 
        if not query:
            return {"status": "error", "pesan": f"barang tidak ditemukan"}

        return [{"nama_barang":i.nama_barang,
                "harga_barang":i.harga_barang,
                "stok_barang":i.stok_barang} 
        for i in query]

    except Exception as e:
            logger.exception(f"gagal menampilkan barang: {str(e)}")
            return {"status":"error","pesan":f"gagal menampilkan barang"}
        
    finally:
            session.close()