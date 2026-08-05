tools=[
        {
        "type":"function",
        "function":{
            "name":"get_barang",
            "description":"fitur ini untuk mencari barang berdasarkan nama barang, maksimum harga, minimum harga, dan menampilkan semua barang",
            "parameters":{
                "type":"object",
                "properties":{
                    "nama_barang":{
                        "type":"string",
                        "description":"untuk mencari nama barang"
                    },
                    "max_harga":{
                        "type":"number",
                        "description":"untuk mencari maksimum harga barang"
                    },
                    "min_harga":{
                        "type":"number",
                        "description":"untuk mencari minimum harga barang"
                    }
                }
            }
        }
    },

    {
        "type":"function",
        "function":{
            "name":"tambah_barang",
            "description":"fitur ini untuk menambah barang yang user mau",
            "parameters":{
                "type":"object",
                "properties":{
                    "nama_barang":{
                        "type":"string",
                        "description":"berisi nama barang yang akan ditambah"
                    },
                    "harga_barang":{
                        "type":"number",
                        "description":"berisi harga satuan barang"
                    },
                    "stok_barang":{
                        "type":"integer",
                        "description":"berisi jumlah stok"
                    }
                },
                "required":[
                    "nama_barang",
                    "harga_barang",
                    "stok_barang"
                ]
            }
        }
    },

    {
        "type":"function",
        "function":{
            "name":"hapus_barang",
            "description":"fitur ini untuk menghapus barang yang user inginkan",
            "parameters":{
                "type":"object",
                "properties":{
                    "nama_barang":{
                        "type":"string",
                        "description":"berisi nama barang yang akan dihapus"
                    }
                },
                "required":[
                    "nama_barang"
                ]
            }
        }
    },

    {
        "type":"function",
        "function":{
            "name":"update_barang",
            "description":"fitur ini untuk update data barang",
            "parameters":{
                "type":"object",
                "properties":{
                    "nama_barang":{
                        "type":"string",
                        "description":"berisi nama barang yang akan diupdate"
                    },
                    "harga_barang":{
                        "type":"number",
                        "description":"berisi harga satuan barang",
                    },
                    "stok_barang":{
                        "type":"integer",
                        "description":"beriski jumlah stok barang"
                    }
                },
                "required":[
                    "nama_barang"
                ]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"tambah_stok",
            "description":"fitur ini untuk menambah stok barang",
            "parameters":{
                "type":"object",
                "properties":{
                    "nama_barang":{
                        "type":"string",
                        "description":"berisi nama barang"
                    },
                    "stok_tambahan":{
                        "type":"integer",
                        "description":"berisi jumlah stok barang yang mau ditambahkan, ambil angka nya saja"
                    }
                },
                "required":[
                    "nama_barang",
                    "stok_tambahan"
                ]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"diskon_barang",
            "description":"fitur ini untuk memberikan diskon pada barang",
            "parameters":{
                "type":"object",
                "properties":{
                    "min_stok":{
                        "type":"integer",
                        "description":"berisi minimum stok barang. contoh: yang kurang dari 50"
                    },
                    "nama_barang":{
                        "type":"string",
                        "discription":"berisi nama barang"
                    },
                    "besar_diskon":{
                        "type":"number",
                        "discription":"berisi besar diskon yang diberikan"
                    }
                },
                "required":[
                    "besar_diskon"
                ]
            }
        }
    },

    {
        "type":"function",
        "function":{
            "name":"cek_stok_menipis",
            "description":"fitur ini untuk cek stok yang menipis atau dibawah batas maksimal",
            "parameters":{
                "type":"object",
                "properties":{
                    "stok_max":{
                        "type":"integer",
                        "description":"berisi batas maksimal stok barang "
                    }
                }
            }
        }
    },
]