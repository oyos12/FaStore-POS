import sqlite3

DB_NAME = "fashion_store.db"

# Data pakaian sementara
sample_data = [
    ("Uniqlo Airism", "T-shirt", "Slim fit", "Halus", "M", "Katun", "Casual", 149000),
    ("H&M Polo", "Polo", "Regular", "Lembut", "L", "Katun-Pique", "Smart Casual", 199000),
    ("Adidas Jersey", "Olahraga", "Fit", "Mesh", "XL", "Poliester", "Sport", 299000),
    ("Zara Jacket", "Jaket", "Loose", "Halus", "M", "Nylon", "Urban", 499000),
    ("Levi’s Jeans", "Celana", "Straight", "Denim", "32", "Denim", "Classic", 699000),
    ("Erigo Hoodie", "Hoodie", "Oversize", "Fluffy", "XL", "Fleece", "Streetwear", 349000),
    ("Converse Tee", "T-shirt", "Regular", "Ringan", "S", "Katun", "Urban", 179000),
    ("Nike Tracksuit", "Training", "Slim", "Elastis", "M", "Dri-Fit", "Sport", 599000),
    ("Pull&Bear Shirt", "Kemeja", "Slim", "Halus", "L", "Katun Linen", "Casual", 229000),
    ("Marks&Spencer Coat", "Jas", "Fit", "Rapi", "M", "Wool", "Formal", 799000)
]

def buat_tabel_barang_detail():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barang_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barang_id INTEGER NOT NULL,
            bentuk TEXT,
            tekstur TEXT,
            ukuran TEXT,
            bahan TEXT,
            style TEXT,
            FOREIGN KEY (barang_id) REFERENCES barang(id)
        )
    """)
    conn.commit()
    conn.close()

def insert_data_otomatis():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for nama, kategori, bentuk, tekstur, ukuran, bahan, style, harga in sample_data:
        # Cek atau insert kategori
        cursor.execute("SELECT id FROM kategori_barang WHERE nama_kategori=?", (kategori,))
        kategori_data = cursor.fetchone()
        if kategori_data:
            kategori_id = kategori_data[0]
        else:
            cursor.execute("INSERT INTO kategori_barang (nama_kategori) VALUES (?)", (kategori,))
            kategori_id = cursor.lastrowid

        # Insert ke barang
        cursor.execute("INSERT INTO barang (nama_barang, kategori_id, stok, harga) VALUES (?, ?, ?, ?)", (nama, kategori_id, 10, harga))
        barang_id = cursor.lastrowid

        # Insert ke barang_detail
        cursor.execute("INSERT INTO barang_detail (barang_id, bentuk, tekstur, ukuran, bahan, style) VALUES (?, ?, ?, ?, ?, ?)",
                       (barang_id, bentuk, tekstur, ukuran, bahan, style))

    conn.commit()
    conn.close()
    print("\nData otomatis berhasil dimasukkan ke database.")

def update_manual():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("\n--- Update Manual Data Pakaian ---")
    barang_id = input("Masukkan ID barang yang ingin diupdate: ")

    cursor.execute("SELECT id FROM barang WHERE id=?", (barang_id,))
    if not cursor.fetchone():
        print("Barang tidak ditemukan.")
        return

    kolom = input("Kolom yang ingin diubah (nama_barang/harga/stok): ")
    nilai = input("Masukkan nilai baru: ")

    if kolom in ["nama_barang", "harga", "stok"]:
        cursor.execute(f"UPDATE barang SET {kolom} = ? WHERE id = ?", (nilai, barang_id))
        conn.commit()
        print("Data berhasil diubah.")
    else:
        print("Kolom tidak valid.")

    conn.close()

def menu_data_barang():
    buat_tabel_barang_detail()
    while True:
        print("\n=== Menu Data Barang (Admin/Kasir) ===")
        print("1. Insert Data Otomatis")
        print("2. Update Manual Data Barang")
        print("3. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            insert_data_otomatis()
        elif pilihan == "2":
            update_manual()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    print("🔧 Menyiapkan tabel dan data awal...")
    buat_tabel_barang_detail()
    insert_data_otomatis()
    print("✅ Setup awal berhasil! Data produk dan detail sudah dimasukkan.") 