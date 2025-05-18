import sqlite3
from produk_management import tampil_produk
from datetime import datetime
from struk_generator import buat_struk_pdf

DB_NAME = "fashion_store.db"

def tampil_produk_lengkap():
    print("\n--- Daftar Produk Detail ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT 
        b.id, 
        b.nama_barang, 
        k.nama_kategori, 
        d.bentuk, 
        d.tekstur, 
        d.ukuran, 
        d.bahan, 
        d.style, 
        b.harga, 
        b.stok
    FROM barang b
    JOIN kategori_barang k ON b.kategori_id = k.id
    LEFT JOIN barang_detail d ON b.id = d.barang_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Belum ada data produk.")
        return

    for row in rows:
        status = "🚫 Stok habis" if row[9] == 0 else "✅ Barang tersedia kembali!"
        print(f"""
ID Barang     : {row[0]}
Nama          : {row[1]}
Kategori      : {row[2]}
Bentuk        : {row[3] or 'N/A'}
Tekstur       : {row[4] or 'N/A'}
Ukuran        : {row[5] or 'N/A'}
Bahan         : {row[6] or 'N/A'}
Style         : {row[7] or 'N/A'}
Harga         : Rp{row[8]:,.0f}
Stok          : {row[9]}  {status}
-------------------------------
""")

def tampil_produk_ringkas():
    print("\n--- Daftar Produk Ringkas ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT b.id, b.nama_barang, k.nama_kategori, b.harga, b.stok
    FROM barang b
    JOIN kategori_barang k ON b.kategori_id = k.id
    ORDER BY b.id
    """

    cursor.execute(query)
    hasil = cursor.fetchall()
    conn.close()

    if hasil:
        for row in hasil:
            status = "Stok Habis" if row[4] == 0 else f"Stok: {row[4]}"
            print(f"ID: {row[0]} | Nama: {row[1]} | Kategori: {row[2]} | Harga: Rp{row[3]:,.0f} | {status}")
    else:
        print("❎ Belum ada produk.")


def menu_pelanggan(user):
    while True:
        print("\n=== Menu Pelanggan ===")
        print(f"Login sebagai: {user['username']} (ID: {user['id']}, Role: pelanggan)")  # ✅ ID ditampilkan
        print("1. Lihat Produk")
        print("2. Lakukan Pembelian")
        print("3. Lihat Produk Lengkap")
        print("4. Cari Produk Berdasarkan Kategori")
        print("5. Cari Produk Berdasarkan Style")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampil_produk()
        elif pilihan == "2":
            tampil_produk_lengkap()
        elif pilihan == "3":
            tambah_transaksi_pelanggan(user)
        elif pilihan == "4":
            tampilkan_produk_per_kategori()
        elif pilihan == "5":
            tampilkan_produk_per_kategori()
        elif pilihan == "6":
            print("Keluar dari menu pelanggan.")
            break
        else:
            print("Pilihan tidak valid.")

def tambah_transaksi_pelanggan(user):
    pelanggan_id = input("ID pelanggan: ").strip()
    barang_id = input("ID barang: ").strip()
    jumlah_input = input("Jumlah beli: ").strip()

    if not (pelanggan_id and barang_id and jumlah_input.isdigit()):
        print("❌ Input tidak valid. Pastikan semua isian benar.")
        return

    jumlah = int(jumlah_input)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT nama_pelanggan FROM pelanggan WHERE id=?", (pelanggan_id,))
    pelanggan = cursor.fetchone()
    if not pelanggan:
        print("❌ Pelanggan tidak ditemukan.")
        conn.close()
        return

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
        cursor.execute("INSERT INTO transaksi (user_id, tanggal, total) VALUES (?, ?, ?)", (user['id'], tanggal, total))
        transaksi_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO detail_transaksi (transaksi_id, barang_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
            (transaksi_id, barang_id, jumlah, total)
        )

        cursor.execute("UPDATE barang SET stok = stok - ? WHERE id=?", (jumlah, barang_id))
        conn.commit()

        print(f"\n✅ Transaksi berhasil ditambahkan untuk {pelanggan[0]}")
        print(f"🛒 Barang : {nama_barang}")
        print(f"💲 Jumlah: {jumlah} x {harga} = {total}\n")

    except Exception as e:
        print(f"❌ Gagal menambahkan transaksi: {e}")
    finally:
        conn.close()
        # Buat struk PDF otomatis
        buat_struk_pdf(transaksi_id)

def tampilkan_produk_per_kategori():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ambil daftar kategori
    cursor.execute("SELECT id, nama_kategori FROM kategori_barang ORDER BY id")
    kategori_list = cursor.fetchall()

    if not kategori_list:
        print("❌ Belum ada kategori tersedia.")
        conn.close()
        return

    # Tampilkan daftar kategori
    print("\n--- Daftar Kategori ---")
    for idx, (kategori_id, nama_kategori) in enumerate(kategori_list, start=1):
        print(f"{idx}. {nama_kategori}")

    try:
        pilihan = int(input("Pilih kategori berdasarkan nomor: "))
        if not (1 <= pilihan <= len(kategori_list)):
            print("❌ Nomor kategori tidak valid.")
            conn.close()
            return
    except ValueError:
        print("❌ Input harus berupa angka.")
        conn.close()
        return

    kategori_id_terpilih = kategori_list[pilihan - 1][0]
    nama_kategori_terpilih = kategori_list[pilihan - 1][1]

    # Tampilkan produk berdasarkan kategori
    cursor.execute("""
        SELECT b.id, b.nama_barang, b.harga, b.stok
        FROM barang b
        WHERE b.kategori_id = ?
    """, (kategori_id_terpilih,))
    produk = cursor.fetchall()
    conn.close()

    print(f"\n--- Produk dalam Kategori: {nama_kategori_terpilih} ---")
    if produk:
        for row in produk:
            status = "Stok Habis" if row[3] == 0 else f"Stok: {row[3]}"
            print(f"ID: {row[0]} | Nama: {row[1]} | Harga: Rp{row[2]:,.0f} | {status}")
    else:
        print("❎ Tidak ada produk dalam kategori ini.")

def tampilkan_produk_per_style():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ambil daftar style unik dari barang_detail
    cursor.execute("SELECT DISTINCT style FROM barang_detail WHERE style IS NOT NULL ORDER BY style")
    style_list = cursor.fetchall()

    if not style_list:
        print("❌ Tidak ada data style yang tersedia.")
        conn.close()
        return

    # Tampilkan daftar style dengan nomor
    print("\n--- Daftar Style Pakaian ---")
    for idx, (style,) in enumerate(style_list, start=1):
        print(f"{idx}. {style}")

    try:
        pilihan = int(input("Pilih style berdasarkan nomor: "))
        if not (1 <= pilihan <= len(style_list)):
            print("❌ Nomor style tidak valid.")
            conn.close()
            return
    except ValueError:
        print("❌ Input harus berupa angka.")
        conn.close()
        return

    style_terpilih = style_list[pilihan - 1][0]

    # Tampilkan produk berdasarkan style
    query = """
    SELECT 
        b.id, b.nama_barang, k.nama_kategori, d.style, b.harga, b.stok
    FROM barang b
    JOIN kategori_barang k ON b.kategori_id = k.id
    LEFT JOIN barang_detail d ON b.id = d.barang_id
    WHERE d.style = ?
    """
    cursor.execute(query, (style_terpilih,))
    hasil = cursor.fetchall()
    conn.close()

    print(f"\n--- Produk dengan Style: {style_terpilih} ---")
    if hasil:
        for row in hasil:
            status = "Stok Habis" if row[5] == 0 else f"Stok: {row[5]}"
            print(f"ID: {row[0]} | Nama: {row[1]} | Kategori: {row[2]} | Harga: Rp{row[4]:,.0f} | {status}")
    else:
        print("❎ Tidak ditemukan produk dengan style ini.")
