import sqlite3
import hashlib
from table import get_connection

DB_NAME = "fashion_store.db"

#fungsi hasling password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#fungsi logim
def login():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    hashed_pw = hash_password(password)

    cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"\n✅ Login berhasil sebagai {username} ({user[1]})\n")
        return {'id': user[0], 'username': username, 'role': user[1]}
    else:
        print("\n❌ Login gagal! Username atau password salah.\n")
        return None
    

# Fungsi membuat akun (role: admin / kasir / pelanggan)
def register(role_filter=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("=== Registrasi Akun Baru ===")
    username = input("Username baru: ")
    password = input("Password baru: ")

    # Filter role jika diberikan
    if role_filter:
        print(f"Role tersedia: {', '.join(role_filter)}")
        role = input("Role: ").lower()
        if role not in role_filter:
            print("❌ Role tidak diizinkan pada menu ini.")
            conn.close()
            return
    else:
        role = input("Role (admin/kasir/pelanggan): ").lower()

    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
        conn.commit()

        # Tambahkan juga ke tabel pelanggan jika role-nya pelanggan
        if role == "pelanggan":
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO pelanggan (id, nama_pelanggan) VALUES (?, ?)", (user_id, username))
            conn.commit()

        print("✅ Akun berhasil dibuat.")
    except sqlite3.IntegrityError:
        print("❌ Username sudah digunakan.")
    finally:
        conn.close()

# Fungsi menghapus akun sendiri
def hapus_akun():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("=== Hapus Akun ===")
    username = input("Username: ")
    password = input("Password: ")

    hashed_pw = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = cursor.fetchone()

    if user:
        konfirmasi = input("Yakin ingin menghapus akun ini? (y/n): ").lower()
        if konfirmasi == "y":
            cursor.execute("DELETE FROM users WHERE id=?", (user[0],))
            conn.commit()
            print("✅ Akun berhasil dihapus.")
        else:
            print("❎ Penghapusan akun dibatalkan.")
    else:
        print("❌ Username atau password salah.")

    conn.close()

# Fungsi logout
def logout(user):
    konfirmasi = input(f"Yakin ingin logout dari akun {user['username']}? (y/n): ").lower()
    if konfirmasi == "y":
        print(f"\n👋 User {user['username']} telah logout.\n")
        return None
    else:
        print("Logout dibatalkan.")
        return user
