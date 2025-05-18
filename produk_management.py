import sqlite3

DB_NAME = "fashion_store.db"

def menu_produk():
    while True:
        print("\n=== Manajemen Produk ===")
        print("1. Tampilkan Produk")
        print("2. Tambah Produk")
        print("3. Edit Produk")
        print("4. Hapus Produk")
        print("5. Update Stok Barang")  # ✅ Tambahan menu baru
        print("6. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampil_produk()
        elif pilihan == "2":
            tambah_produk()
        elif pilihan == "3":
            edit_produk()
        elif pilihan == "4":
            hapus_produk()
        elif pilihan == "5":
            update_stok()  # ✅ Fungsi tambahan
        elif pilihan == "6":
            break
        else:
            print("❌ Pilihan tidak valid!")

def tampil_produk():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
    SELECT barang.id, barang.nama_barang, kategori_barang.nama_kategori, barang.harga, barang.stok
    FROM barang
    JOIN kategori_barang ON barang.kategori_id = kategori_barang.id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    print("\n--- Daftar Produk ---")
    if data:
        for row in data:
            print(f"ID: {row[0]} | Nama: {row[1]} | Kategori: {row[2]} | Harga: {row[3]} | Stok: {row[4]}")
    else:
        print("❎ Belum ada produk.")

def tambah_produk():
    nama = input("Nama produk: ").strip()
    kategori_id = input("ID kategori: ").strip()
    harga = input("Harga: ").strip()
    stok = input("Stok: ").strip()

    if not (nama and kategori_id and harga and stok):
        print("❌ Semua field harus diisi.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM kategori_barang WHERE id=?", (kategori_id,))
    if not cursor.fetchone():
        print("❌ Kategori tidak ditemukan.")
        conn.close()
        return

    try:
        cursor.execute(
            "INSERT INTO barang (nama_barang, kategori_id, harga, stok) VALUES (?, ?, ?, ?)",
            (nama, kategori_id, harga, stok)
        )
        conn.commit()
        print("✅ Produk berhasil ditambahkan.")
    except Exception as e:
        print(f"❌ Gagal menambahkan produk: {e}")
    finally:
        conn.close()

def edit_produk():
    id_produk = input("ID produk yang akan diedit: ").strip()

    if not id_produk.isdigit():
        print("❌ ID produk tidak valid.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM barang WHERE id=?", (id_produk,))
    if not cursor.fetchone():
        print("❌ Produk tidak ditemukan.")
        conn.close()
        return

    nama = input("Nama baru: ").strip()
    kategori_id = input("ID kategori baru: ").strip()
    harga = input("Harga baru: ").strip()
    stok = input("Stok baru: ").strip()

    if not (nama and kategori_id and harga and stok):
        print("❌ Semua field harus diisi.")
        conn.close()
        return

    try:
        cursor.execute(
            "UPDATE barang SET nama_barang=?, kategori_id=?, harga=?, stok=? WHERE id=?",
            (nama, kategori_id, harga, stok, id_produk)
        )
        conn.commit()
        print("✅ Produk berhasil diubah.")
    except Exception as e:
        print(f"❌ Gagal mengubah produk: {e}")
    finally:
        conn.close()

def hapus_produk():
    id_produk = input("ID produk yang akan dihapus: ").strip()

    if not id_produk.isdigit():
        print("❌ ID tidak valid.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM barang WHERE id=?", (id_produk,))
    if not cursor.fetchone():
        print("❌ Produk tidak ditemukan.")
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM barang WHERE id=?", (id_produk,))
        conn.commit()
        print("✅ Produk berhasil dihapus.")
    except Exception as e:
        print(f"❌ Gagal menghapus produk: {e}")
    finally:
        conn.close()

def update_stok():
    id_produk = input("Masukkan ID produk yang ingin diubah stoknya: ").strip()
    if not id_produk.isdigit():
        print("❌ ID produk harus berupa angka.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nama_barang, stok FROM barang WHERE id=?", (id_produk,))
    data = cursor.fetchone()
    if not data:
        print("❌ Produk tidak ditemukan.")
        conn.close()
        return

    nama, stok_lama = data
    print(f"Produk: {nama} | Stok saat ini: {stok_lama}")
    pilihan = input("Tambah(+) atau Kurangi(-) stok? (+/-): ").strip()

    if pilihan not in ['+', '-']:
        print("❌ Pilihan tidak valid.")
        conn.close()
        return

    try:
        jumlah = int(input("Jumlah perubahan stok: ").strip())
        if pilihan == '-':
            jumlah = -jumlah
        stok_baru = stok_lama + jumlah
        if stok_baru < 0:
            print("❌ Jumlah stok tidak boleh kurang dari 0.")
            conn.close()
            return

        cursor.execute("UPDATE barang SET stok=? WHERE id=?", (stok_baru, id_produk))
        conn.commit()
        print(f"✅ Stok produk berhasil diperbarui menjadi {stok_baru}.")
    except ValueError:
        print("❌ Masukkan angka yang valid.")
    except Exception as e:
        print(f"❌ Gagal memperbarui stok: {e}")
    finally:
        conn.close()
        print("Produk berhasil dihapus.")
