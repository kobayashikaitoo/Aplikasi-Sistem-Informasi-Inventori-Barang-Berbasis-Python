# SISTEM INFORMASI INVENTORI BARANG

**Tugas Proyek Akhir Sistem Informasi Berbasis Desktop**

Nama: Friederik Ferdinand & Ibren Holysa Yalloken Ginting
NIM: 240211060035 & 240211060040
Kelas: B

---

## Daftar Isi
- [1. Latar Belakang dan Tujuan](#1-latar-belakang-dan-tujuan)
- [2. Analisis Kebutuhan Pengguna](#2-analisis-kebutuhan-pengguna)
- [3. Desain Sistem](#3-desain-sistem)
- [4. Desain Basis Data](#4-desain-basis-data)
- [5. Desain Antarmuka Pengguna](#5-desain-antarmuka-pengguna)
- [6. Implementasi dan Pengujian](#6-implementasi-dan-pengujian)
- [7. Kesimpulan dan Saran](#7-kesimpulan-dan-saran)
- [Lampiran A. Instruksi Menjalankan Aplikasi](#lampiran-a-instruksi-menjalankan-aplikasi)

---

## 1. Latar Belakang dan Tujuan
Usaha kecil seperti toko kelontong atau gudang sederhana sering mengalami kendala dalam memantau stok barang, pemasok, dan transaksi harian. Pencatatan manual rawan kesalahan serta lambat ketika diperlukan laporan stok. Sistem Informasi Inventori Barang ini dibangun untuk:
- Mempermudah pencatatan transaksi stok masuk dan keluar.
- Menyediakan informasi stok terkini dengan cepat.
- Mengelola data pemasok secara terpusat.
- Menghasilkan laporan stok dalam format PDF maupun Excel.

## 2. Analisis Kebutuhan Pengguna
**Aktor Sistem:**
- *Admin*: mengelola master data, pengguna, serta melakukan ekspor laporan.
- *User (Kasir/Operator)*: melakukan transaksi stok dan melihat laporan singkat.

**Kebutuhan Fungsional:**
- Autentikasi dengan dua level akses (admin dan user).
- CRUD data barang: kode, nama, kategori, stok, harga beli, harga jual, pemasok.
- CRUD data pemasok: nama dan alamat.
- Pencarian barang dan pemasok berdasarkan kata kunci.
- Pencatatan transaksi masuk/keluar beserta pencatatan stok otomatis.
- Pembuatan laporan stok ke PDF/Excel.
- Dashboard ringkas dengan grafik stok dan notifikasi stok rendah.

**Kebutuhan Non-Fungsional & Asumsi:**
- Aplikasi berjalan di OS Windows 10+ dengan Python 3.10+.
- Pengguna memiliki hak akses ke file sistem untuk menyimpan laporan.
- Data tersimpan di SQLite dan dapat dipindahkan melalui file `.db`.
- Pengguna memahami operasi dasar komputer dan pengelolaan file.

## 3. Desain Sistem
**Pendekatan Arsitektur:**
- Pola MVC sederhana: *Model* untuk akses data, *Controller* menangani logika bisnis, *View* menggunakan Tkinter.
- Modul utilitas untuk hashing password, validasi, dan pembuatan grafik.

**Diagram Konteks (teks):**
```
 +------------+        Login & Operasi       +---------------------------+
 |   Admin    | ---------------------------> | Sistem Inventori Desktop  |
 |   User     | <--------------------------- | (Tkinter + SQLite)        |
 +------------+        Laporan & Feedback    +---------------------------+
```

**DFD Level 0 (ASCII):**
```
            +----------------+
            |    Pengguna    |
            +--------+-------+
                     |
                     v
        +---------------------------+
        |       Proses Inti         |
        |---------------------------|
        | 1. Kelola Barang          |
        | 2. Kelola Pemasok         |
        | 3. Catat Transaksi        |
        | 4. Buat Laporan           |
        +-----------+---------------+
                    |
        +-----------+-----------+
        |   Basis Data SQLite    |
        +------------------------+
```

**Deskripsi Use Case Utama:**
- UC-01 Login: Pengguna memasukkan kredensial, sistem memvalidasi hash password.
- UC-02 Kelola Barang: Admin menambah, mengubah, menghapus barang; user dapat melihat.
- UC-03 Kelola Pemasok: Admin mengelola data pemasok, user melihat.
- UC-04 Catat Transaksi: Pengguna mencatat stok masuk/keluar, sistem memperbarui stok otomatis.
- UC-05 Cetak Laporan: Admin mengekspor laporan stok ke PDF atau Excel.
- UC-06 Lihat Dashboard: Pengguna melihat ringkasan stok, grafik, dan transaksi terakhir.

## 4. Desain Basis Data
**ERD (teks):**
- *users* (1) ---< *transactions* (melalui relasi pengguna sebagai pelaku, implisit melalui audit aplikasi).
- *categories* (1) ---< *items*.
- *suppliers* (1) ---< *items*.
- *items* (1) ---< *transactions*.

**Struktur Tabel:**
- `users(id, username, password, level)`
- `categories(id, name)`
- `suppliers(id, supplier_name, address)`
- `items(id, item_code, item_name, category_id, stock, purchase_price, selling_price, supplier_id)`
- `transactions(id, transaction_date, item_id, quantity, transaction_type, notes)`

Relasi kunci asing menjaga konsistensi data dan memperbarui stok secara otomatis melalui proses aplikasi.

## 5. Desain Antarmuka Pengguna
**Panduan Gaya:**
- Palet warna dasar biru (#3f72af) untuk grafik dan aksen tombol.
- Menggunakan `ttk` untuk tampilan modern dan konsisten.

**Mockup ASCII:**
```
Login Form
+-----------------------------------+
| Inventori Toko                    |
| [Username.................]       |
| [Password.................]       |
| [  Masuk  ]                       |
+-----------------------------------+

Dashboard Tab
+--------------------------------------------------------------+
| Ringkasan Stok | Grafik Stok Barang                          |
| - Total Barang | [Chart Batang 8 Barang Teratas]             |
| - Total Stok   |                                            |
| Stok Rendah    | Transaksi Terbaru                           |
+--------------------------------------------------------------+

Manajemen Barang
+----------------------------------+---------------------------+
| Pencarian: [..........] [Cari]   | Form Barang               |
|----------------------------------| Kode   : [.........]      |
| Treeview Barang (kolom lengkap) | Nama   : [.........]      |
| ...                              | Kategori: [Combo ]        |
|                                  | ... tombol Simpan/Hapus   |
+----------------------------------+---------------------------+

Transaksi Stok
+--------------------------------------------------------------+
| Barang : [Combo]  Jumlah : [..]  Jenis : [IN/OUT]            |
| Catatan: [.................................]                 |
| [ Simpan Transaksi ]                                        |
| Treeview Riwayat Transaksi                                  |
+--------------------------------------------------------------+
```

**Deskripsi Screenshot (teks):**
- Screenshot login form: tampilan sederhana dengan input username, password, dan tombol masuk.
- Screenshot dashboard: menampilkan ringkasan total barang, total stok, tabel stok rendah, grafik stok, dan daftar transaksi terbaru.
- Screenshot manajemen barang: tabel daftar barang lengkap, form input di sisi kanan dengan tombol simpan, hapus, bersihkan, serta tombol ekspor PDF/Excel.
- Screenshot transaksi: form transaksi stok di atas dan tabel riwayat transaksi di bawah.

## 6. Implementasi dan Pengujian
**Langkah Implementasi:**
1. Menyusun struktur folder `models/`, `controllers/`, `views/`, `utils/`, `reports/`, `data/`.
2. Membuat kelas `Database` untuk koneksi dan inisialisasi tabel.
3. Mengimplementasikan model CRUD (`UserModel`, `ItemModel`, `SupplierModel`, `TransactionModel`).
4. Menulis controller untuk logika bisnis serta utilitas validasi dan hashing.
5. Mendesain antarmuka Tkinter menggunakan `ttk.Notebook` dan `Treeview`.
6. Mengintegrasikan ekspor laporan PDF (ReportLab) dan Excel (OpenPyXL).
7. Menambahkan grafik stok menggunakan `matplotlib`.

**Pengujian Fungsional (ringkas):**
| No | Skenario                         | Langkah Uji                                   | Hasil |
|----|----------------------------------|-----------------------------------------------|-------|
| 1  | Login admin                      | Masuk dengan admin/admin123                   | Berhasil |
| 2  | Tambah barang baru               | Input lengkap dan simpan                      | Data bertambah |
| 3  | Stok keluar melebihi persediaan  | Catat OUT lebih besar dari stok               | Ditolak dengan pesan |
| 4  | Pencarian barang                 | Cari kata kunci "Gula"                        | Data terfilter |
| 5  | Ekspor PDF                       | Tekan Export PDF, simpan file                 | File PDF terbentuk |
| 6  | Ekspor Excel                     | Tekan Export Excel, simpan file               | File Excel terbentuk |

**Pengujian Non-Fungsional:**
- Performa: respons GUI < 1 detik untuk dataset 100 entri.
- Keamanan: password tersimpan dalam bentuk hash SHA-256.
- Keandalan: database otomatis membuat data awal jika kosong.

## 7. Kesimpulan dan Saran
Sistem informasi inventori berbasis Tkinter ini berhasil memenuhi kebutuhan usaha kecil dalam memantau stok barang, pemasok, dan transaksi. Fitur login berlevel, pencarian, laporan PDF/Excel, serta dashboard grafik memberikan nilai tambah bagi pengguna.

**Saran Pengembangan:**
- Menambahkan modul manajemen pengguna melalui GUI.
- Menyediakan fitur impor data dari CSV.
- Integrasi dengan barcode scanner untuk percepatan transaksi.
- Menambahkan notifikasi email atau WhatsApp untuk stok kritis.

## Lampiran A. Instruksi Menjalankan Aplikasi
1. Pastikan Python 3.10+ telah terinstal.
2. Instal dependensi dengan perintah: `pip install -r requirements.txt` (lihat daftar library di bawah).
   - `tkinter` (bawaan Python).
   - `reportlab`
   - `openpyxl`
   - `matplotlib`
3. Jalankan aplikasi: `python main.py`.
4. Login menggunakan kredensial awal:
   - Admin: `admin / admin123`
   - User: `staf / staf123`
5. Untuk reset database, gunakan skrip `data/database_setup.sql` melalui SQLite CLI atau DB Browser.

---

**Catatan:** Dokumentasi ini dapat dikembangkan menjadi laporan PDF resmi dengan menambahkan halaman pengesahan dan lampiran tambahan sesuai pedoman kampus.

