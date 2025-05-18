# FaStore-POS
project struktur data pembelian pakaian dari toko ModaWear

Sistem **Point of Sale (POS)** berbasis Python dan SQLite untuk toko pakaian. Aplikasi ini dirancang untuk memudahkan pengelolaan data pelanggan, produk, transaksi, serta pencetakan struk pembelian otomatis. Sangat cocok untuk digunakan sebagai studi kasus atau tugas akhir.

---

## ✨ Fitur Utama

### 👨‍💼 Admin / Kasir
- Login dan Registrasi aman (hashed password)
- Manajemen Produk (tambah, edit, hapus, update stok)
- Manajemen Kategori Barang & Data Tambahan (tekstur, style, ukuran, bahan)
- Manajemen Pelanggan
- Transaksi pembelian
- Backup & Reset database
- Cetak struk transaksi otomatis (format PDF)

### 👥 Pelanggan
- Login dan Registrasi
- Melihat daftar produk (ringkas & lengkap)
- Pencarian produk berdasarkan kategori atau style
- Melakukan pembelian

---

## 💾 Teknologi yang Digunakan

- Python 3
- SQLite3
- [fpdf2](https://pypi.org/project/fpdf2/) — untuk pembuatan PDF struk

---

## 🧑‍💻 Cara Menjalankan

1. **Clone repositori:**

```bash
git clone C:\Users\HP ELITEBOOK\OneDrive\Documents\GitHub\FaStore-POS.git
cd FaStore-POS
