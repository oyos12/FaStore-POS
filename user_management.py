import sqlite3

DB_NAME = "fashion_store.db"

def pelanggan():
    while True:
        print("\n=== Manajemen Pelanggan ===")
        print("1. Tampilkan Pelanggan")
        print("2. Tambah Pelanggan")
        print("3. Hapus Pelanggan")
        print("4. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampil_pelanggan()
        elif pilihan == "2":
            tambah_pelanggan()
        elif pilihan == "3":
            hapus_pelanggan()
        elif pilihan == "4":
            break
        else:
            print("❌ Pilihan tidak valid.")

def tampil_pelanggan():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_pelanggan FROM pelanggan")
    data = cursor.fetchall()
    conn.close()

    print("\n--- Daftar Pelanggan ---")
    if data:
        for row in data:
            print(f"ID: {row[0]} | Nama: {row[1]}")
    else:
        print("❎ Belum ada data pelanggan.")

def tambah_pelanggan():
    nama = input("Nama pelanggan: ").strip()
    if not nama:
        print("❌ Nama tidak boleh kosong.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pelanggan (nama_pelanggan) VALUES (?)", (nama,))
    conn.commit()
    conn.close()
    print("✅ Pelanggan berhasil ditambahkan.")

def hapus_pelanggan():
    id_pelanggan = input("ID pelanggan yang akan dihapus: ").strip()
    if not id_pelanggan.isdigit():
        print("❌ ID tidak valid.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pelanggan WHERE id=?", (id_pelanggan,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM pelanggan WHERE id=?", (id_pelanggan,))
        conn.commit()
        print("✅ Pelanggan berhasil dihapus.")
    else:
        print("❌ ID pelanggan tidak ditemukan.")
    conn.close()
    print("Pelanggan berhasil dihapus.")