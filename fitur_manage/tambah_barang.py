from DB.db_setup import get_db,Barang
import logging
from logger_config import *

logger = logging.getLogger(__name__)

def tambah_barang(nama_barang, harga_barang, stok_barang):

    # ── Validasi input kosong / None ──────────────────────────────────────────
    if nama_barang is None or str(nama_barang).strip() == "":
        return {"status": "error", "pesan": "nama_barang tidak boleh kosong."}

    if harga_barang is None or str(harga_barang).strip() == "":
        return {"status": "error", "pesan": "harga_barang tidak boleh kosong."}

    if stok_barang is None or str(stok_barang).strip() == "":
        return {"status": "error", "pesan": "stok_barang tidak boleh kosong."}

    # ── Validasi tipe & nilai ─────────────────────────────────────────────────
    try:
        harga_barang = float(harga_barang)
    except (ValueError, TypeError):
        return {"status": "error", "pesan": "harga_barang harus berupa angka."}

    try:
        stok_barang = int(stok_barang)
    except (ValueError, TypeError):
        return {"status": "error", "pesan": "stok_barang harus berupa bilangan bulat."}

    if harga_barang <= 0:
        return {"status": "error", "pesan": "harga_barang harus lebih dari 0."}

    if stok_barang < 0:
        return {"status": "error", "pesan": "stok_barang tidak boleh negatif."}

    nama_barang = nama_barang.strip()

    # ── Simpan ke database ────────────────────────────────────────────────────
    session = get_db()
    cek_barang=session.query(Barang).filter(Barang.nama_barang==nama_barang).first()
    if cek_barang:
        return {"status": "error", "pesan": "barang sudah ada dalam inventory."}
    try:
        barang_baru = Barang(
            nama_barang=nama_barang,
            harga_barang=harga_barang,
            stok_barang=stok_barang,
        )
        session.add(barang_baru)
        session.commit()
        logger.info(f"{nama_barang} berhasil ditambahkan")
        session.refresh(barang_baru)

        return {
            "status": "sukses",
            "pesan": f"Barang '{nama_barang}' berhasil ditambahkan.",
            "data": {
                "nama_barang": barang_baru.nama_barang,
                "harga_barang": barang_baru.harga_barang,
                "stok_barang": barang_baru.stok_barang,
            },
        }

    except Exception as e:
        session.rollback()
        logger.exception(f"gagal menyimpan data: {str(e)}")
        return {"status": "error", "pesan": "Gagal menyimpan data"}

    finally:
        session.close()
