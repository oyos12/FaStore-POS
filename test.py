import sqlite3
import os

DB_NAME = "fashion_store.db"

def test_koneksi_database():
    print("\n=== TEST KONEKSI DATABASE ===")

    if not os.path.exists(DB_NAME):
        print(f"❌ Database '{DB_NAME}' tidak ditemukan.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Cek tabel penting
        tabel_wajib = [
            "users", "pelanggan", "barang", "kategori_barang",
            "transaksi", "detail_transaksi"
        ]
        for tabel in tabel_wajib:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabel}'")
            if not cursor.fetchone():
                print(f"❌ Tabel '{tabel}' tidak ditemukan.")
            else:
                print(f"✅ Tabel '{tabel}' ditemukan.")

        # Cek data dummy minimal
        cursor.execute("SELECT COUNT(*) FROM barang")
        total_barang = cursor.fetchone()[0]
        print(f"📦 Total barang tersedia: {total_barang}")

        cursor.execute("SELECT COUNT(*) FROM users")
        total_user = cursor.fetchone()[0]
        print(f"👤 Total user terdaftar: {total_user}")

        print("\n✅ Sistem siap digunakan.")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengakses database: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

# Untuk dijalankan langsung
if __name__ == "__main__":
    test_koneksi_database()
