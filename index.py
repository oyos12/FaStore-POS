from auth import login, register, hapus_akun, logout
from table import database
from data_barang_management import menu_data_barang
from user_management import pelanggan
from produk_management import menu_produk
from transaksi_management import menu_transaksi
from pelanggan_menu import tampil_produk_lengkap, tampil_produk_ringkas, menu_pelanggan, tambah_transaksi_pelanggan, tampilkan_produk_per_kategori, tampilkan_produk_per_style
from reset_db import reset_database

# ✅ Import baru untuk backup dan test sistem
from backup_db import backup_database
from test import test_koneksi_database

def main():
    database()

    user = None
    while True:
        print("\n=== Selamat Datang ===")
        print("1. Login Admin/Kasir")
        print("2. Registrasi Admin/Kasir")
        print("3. Login Pelanggan")
        print("4. Registrasi Pelanggan")
        print("5. Hapus Akun")
        print("6. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            user = login()
            if user and user["role"] in ["admin", "kasir"]:
                menu_admin_kasir(user)
            elif user:
                print("Anda bukan admin/kasir.")
        elif pilihan == "2":
            register(role_filter=["admin", "kasir"])
        elif pilihan == "3":
            user = login()
            if user and user["role"] == "pelanggan":
                menu_pelanggan(user)
            elif user:
                print("Anda bukan pelanggan.")
        elif pilihan == "4":
            register(role_filter=["pelanggan"])
        elif pilihan == "5":
            hapus_akun()
        elif pilihan == "6":
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")

def menu_admin_kasir(user):
    while True:
        print("\n=== Menu Utama (Admin/Kasir) ===")
        print(f"Login sebagai: {user['username']} (ID: {user['id']}, Role: {user['role']})")  # ✅ ID ditampilkan
        print("1. Kelola Data Pelanggan")
        print("2. Kelola Data Produk")
        print("3. Kelola Transaksi")
        print("4. Kelola Data Barang Tambahan")
        print("5. Hapus Akun")
        print("6. Reset Database")
        print("7. Backup Database")
        print("8. Test Sistem (Cek Koneksi)")
        print("9. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            pelanggan()
        elif pilihan == "2":
            menu_produk()
        elif pilihan == "3":
            menu_transaksi()
        elif pilihan == "4":
            menu_data_barang()
        elif pilihan == "5":
            hapus_akun()
        elif pilihan == "6":
            reset_database()
        elif pilihan == "7":
            backup_database()  # ✅ Dipanggil saat admin memilih menu 7
        elif pilihan == "8":
            test_koneksi_database()  # ✅ Dipanggil saat admin memilih menu 8
        elif pilihan == "9":
            logout(user)
            break
        else:
            print("Pilihan tidak valid.")

def menu_pelanggan(user):
    while True:
        print(f"\n--- Menu Pelanggan ({user['username']}) ---")
        print(f"Login sebagai: {user['username']} (ID: {user['id']}, Role: pelanggan)")
        print("1. Lihat Produk (Ringkas)")
        print("2. Lihat Produk (Lengkap)")
        print("3. Lakukan Pembelian")
        print("4. Cari Produk Berdasarkan Kategori")
        print("5. Cari Produk Berdasarkan Style")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampil_produk_ringkas()  # ✅ versi ringkas
        elif pilihan == "2":
            tampil_produk_lengkap()  # ✅ versi lengkap
        elif pilihan == "3":
            tambah_transaksi_pelanggan(user)
        elif pilihan == "4":
            tampilkan_produk_per_kategori()
        elif pilihan == "5":
            tampilkan_produk_per_style()
        elif pilihan == "6":
            print("Keluar dari menu pelanggan.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    print("Fitur ini tidak bisa dijalankan langsung. Silakan login sebagai admin/kasir dari index.py.")
    main()
    