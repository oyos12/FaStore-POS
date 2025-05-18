import sqlite3
import os
import shutil
from table import setup_database

DB_NAME = "fashion_store.db"
BACKUP_FOLDER = "backup"

def reset_database():
    konfirmasi = input("PERINGATAN! Ini akan menghapus semua data utama. Lanjutkan? (y/n): ").lower()
    if konfirmasi != "y":
        print("❎ Reset database dibatalkan.")
        return

    # Hapus database utama
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("🗑️ Database lama dihapus.")

    # Tawarkan untuk menghapus folder backup
    if os.path.exists(BACKUP_FOLDER) and os.listdir(BACKUP_FOLDER):
        hapus_backup = input("Ingin sekalian menghapus semua file backup juga? (y/n): ").lower()
        if hapus_backup == "y":
            try:
                shutil.rmtree(BACKUP_FOLDER)
                print("🗑️ Semua file backup berhasil dihapus.")
            except Exception as e:
                print(f"⚠️ Gagal menghapus folder backup: {e}")
        else:
            print("📂 Folder backup tidak dihapus.")

    # Buat database baru dan tabel-tabel
    conn = sqlite3.connect(DB_NAME)
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
    print("✅ Database berhasil direset dan dibuat ulang.")

    # Tambahkan setup tambahan dari table.py (jika diperlukan)
    setup_database()
    print("✅ Setup tambahan database selesai.")

