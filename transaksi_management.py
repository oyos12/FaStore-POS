import sqlite3
from datetime import datetime

DB_NAME = "fashion_store.db"

def menu_transaksi():
    while True:
        print("\n=== Menu Transaksi Pembelian ===")
        print("1. Tambah Transaksi")
        print("2. Cetak Struk Pembelian")
        print("3. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_transaksi()
        elif pilihan == "2":
            cetak_struk_manual()
        elif pilihan == "3":
            break
        else:
            print("❌ Pilihan tidak valid.")

def tambah_transaksi():
    pelanggan_id = input("ID pelanggan: ").strip()
    barang_id = input("ID barang: ").strip()
    jumlah_input = input("Jumlah beli: ").strip()

    if not (pelanggan_id and barang_id and jumlah_input.isdigit()):
        print("❌ Input tidak valid. Pastikan semua diisi dengan benar.")
        return

    jumlah = int(jumlah_input)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Validasi pelanggan
    cursor.execute("SELECT nama_pelanggan FROM pelanggan WHERE id=?", (pelanggan_id,))
    pelanggan = cursor.fetchone()
    if not pelanggan:
        print("❌ Pelanggan tidak ditemukan.")
        conn.close()
        return

    # Validasi barang
    cursor.execute("SELECT nama_barang, harga, stok FROM barang WHERE id=?", (barang_id,))
    barang = cursor.fetchone()
    if not barang:
        print("❌ Barang tidak ditemukan.")
        conn.close()
        return

    nama_barang, harga, stok = barang

    if jumlah > stok:
        print(f"❌ Stok tidak mencukupi. Stok tersedia: {stok}")
        conn.close()
        return

    total = harga * jumlah
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Simpan transaksi (user_id sementara 1 sebagai placeholder)
        cursor.execute("INSERT INTO transaksi (user_id, tanggal, total) VALUES (?, ?, ?)", (1, tanggal, total))
        transaksi_id = cursor.lastrowid

        # Simpan detail transaksi
        cursor.execute(
            "INSERT INTO detail_transaksi (transaksi_id, barang_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
            (transaksi_id, barang_id, jumlah, total)
        )

        # Update stok barang
        cursor.execute("UPDATE barang SET stok = stok - ? WHERE id=?", (jumlah, barang_id))
        conn.commit()

        print(f"\n✅ Transaksi berhasil ditambahkan untuk {pelanggan[0]}")
        print(f"🛒 Barang : {nama_barang}")
        print(f"💲 Jumlah: {jumlah} x {harga} = {total}\n")

    except Exception as e:
        print(f"❌ Gagal menambahkan transaksi: {e}")
    finally:
        conn.close()
        print("Transaksi berhasil ditambahkan.")
        
def cetak_struk_manual():
    transaksi_id = input("Masukkan ID transaksi: ").strip()
    if not transaksi_id.isdigit():
        print("❌ ID tidak valid.")
        return

    from struk_generator import buat_struk_pdf
    buat_struk_pdf(int(transaksi_id))
