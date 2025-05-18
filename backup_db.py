import shutil
import os
import sqlite3
from datetime import datetime

DB_NAME = "fashion_store.db"
BACKUP_FOLDER = "backup"

def backup_database():
    if not os.path.exists(DB_NAME):
        print("❌ Database tidak ditemukan.")
        return

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{BACKUP_FOLDER}/backup_{timestamp}.db"
    shutil.copy2(DB_NAME, backup_filename)
    print(f"✅ Backup berhasil disimpan di: {backup_filename}")

    # Tambahan fitur untuk menyalin isi database backup ke sistem saat ini
    restore_confirm = input("Ingin langsung menambahkan data dari backup ke sistem saat ini? (y/n): ").lower()
    if restore_confirm == 'y':
        restore_database_merge(backup_filename)

def restore_database(backup_file):
    if not os.path.exists(backup_file):
        print("❌ File backup tidak ditemukan.")
        return

    shutil.copy2(backup_file, DB_NAME)
    print(f"✅ Database berhasil dipulihkan dari: {backup_file}")

def restore_database_merge(backup_file):
    if not os.path.exists(backup_file):
        print("❌ File backup tidak ditemukan.")
        return

    try:
        conn_main = sqlite3.connect(DB_NAME)
        conn_backup = sqlite3.connect(backup_file)
        cursor_main = conn_main.cursor()
        cursor_backup = conn_backup.cursor()

        tables = [
            "kategori_barang", "barang", "barang_detail",
            "users", "pelanggan", "transaksi", "detail_transaksi"
        ]

        for table in tables:
            cursor_backup.execute(f"SELECT * FROM {table}")
            rows = cursor_backup.fetchall()

            if rows:
                placeholders = ','.join(['?' for _ in rows[0]])
                for row in rows:
                    try:
                        cursor_main.execute(f"INSERT OR IGNORE INTO {table} VALUES ({placeholders})", row)
                    except Exception as e:
                        print(f"⚠️ Gagal insert data ke tabel {table}: {e}")

        conn_main.commit()
        print("✅ Data dari backup berhasil ditambahkan ke sistem saat ini.")

    except Exception as e:
        print(f"❌ Gagal menambahkan data dari backup: {e}")

    finally:
        conn_main.close()
        conn_backup.close()


# === test_system.py ===
import sqlite3

DB_NAME = "fashion_store.db"

def test_koneksi_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            print("✅ Koneksi ke database berhasil. Tabel yang ditemukan:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("⚠️ Database kosong atau tabel tidak ditemukan.")

    except Exception as e:
        print(f"❌ Gagal mengakses database: {e}")

def test_query_sample():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Jumlah akun pengguna di database: {user_count}")
        conn.close()
    except Exception as e:
        print(f"❌ Gagal menjalankan query: {e}")
