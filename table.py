import sqlite3

conn = sqlite3.connect("fashion_store.db")
cursor = conn.cursor()

# Tabel users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'kasir', 'pelanggan'))
)
""")

# Tabel kategori_barang
cursor.execute("""
CREATE TABLE IF NOT EXISTS kategori_barang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kategori TEXT NOT NULL UNIQUE
)
""")

# Tabel barang
cursor.execute("""
CREATE TABLE IF NOT EXISTS barang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_barang TEXT NOT NULL,
    kategori_id INTEGER NOT NULL,
    stok INTEGER NOT NULL,
    harga REAL NOT NULL,
    FOREIGN KEY (kategori_id) REFERENCES kategori_barang(id)
)
""")

# Tabel pelanggan
cursor.execute("""
CREATE TABLE IF NOT EXISTS pelanggan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pelanggan TEXT NOT NULL
)
""")

# Tabel transaksi
cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tanggal TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Tabel detail_transaksi
cursor.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaksi_id INTEGER NOT NULL,
    barang_id INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
    FOREIGN KEY (barang_id) REFERENCES barang(id)
)
""")

conn.commit()
conn.close()

def get_connection():
    return sqlite3.connect("toko.db")

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'customer')) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        harga REAL NOT NULL,
        stok INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        produk_id INTEGER,
        jumlah INTEGER,
        total REAL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(produk_id) REFERENCES produk(id)
    )
    """)

    conn.commit()
    conn.close()

def database():
    print("Database initialized.")

print("Database dan tabel berhasil dibuat.")

