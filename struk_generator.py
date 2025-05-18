from fpdf import FPDF
import os
import sqlite3

DB_NAME = "fashion_store.db"
STRUK_FOLDER = "struk"

def buat_struk_pdf(transaksi_id):
    if not os.path.exists(STRUK_FOLDER):
        os.makedirs(STRUK_FOLDER)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ambil info transaksi dan user
    cursor.execute("""
        SELECT t.id, u.username, t.tanggal, t.total
        FROM transaksi t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = ?
    """, (transaksi_id,))
    transaksi = cursor.fetchone()

    if not transaksi:
        print("❌ Data transaksi tidak ditemukan.")
        conn.close()
        return

    # Ambil detail produk yang dibeli
    cursor.execute("""
        SELECT b.nama_barang, dt.jumlah, dt.subtotal
        FROM detail_transaksi dt
        JOIN barang b ON dt.barang_id = b.id
        WHERE dt.transaksi_id = ?
    """, (transaksi_id,))
    detail_items = cursor.fetchall()
    conn.close()

    # Buat PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "STRUK PEMBELIAN", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(100, 10, f"ID Transaksi: {transaksi[0]}", ln=True)
    pdf.cell(100, 10, f"Pelanggan   : {transaksi[1]}", ln=True)
    pdf.cell(100, 10, f"Tanggal     : {transaksi[2]}", ln=True)
    pdf.cell(100, 10, f"Total       : Rp{transaksi[3]:,.0f}", ln=True)
    pdf.ln(10)

    pdf.cell(100, 10, "Detail Barang:", ln=True)
    for item in detail_items:
        nama, jumlah, subtotal = item
        pdf.cell(200, 10, f"{nama} x {jumlah} - Rp{subtotal:,.0f}", ln=True)

    nama_file = f"{STRUK_FOLDER}/struk_{transaksi[0]}_{transaksi[2].replace(':','-').replace(' ','_')}.pdf"
    pdf.output(nama_file)
    print(f"📄 Struk berhasil dibuat: {nama_file}")
