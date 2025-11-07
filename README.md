# Sistem Informasi Inventori Barang (Desktop)

Proyek akhir mata kuliah Sistem Informasi: aplikasi desktop berbasis **Python + Tkinter** untuk membantu usaha kecil mengelola stok barang, pemasok, dan transaksi sederhana. Aplikasi mengadopsi pola **MVC sederhana** dengan SQLite sebagai basis data lokal dan mendukung ekspor laporan ke PDF maupun Excel.

---

## Fitur Utama

- **Login & Autentikasi**: dua level pengguna (`admin`, `staf`) dengan hashing SHA-256.
- **Dashboard Ringkas**: total barang & stok, daftar stok rendah, transaksi terbaru, grafik stok (matplotlib).
- **Manajemen Barang**: tambah/ubah/hapus data, pencarian, validasi stok, keterkaitan kategori & pemasok.
- **Manajemen Pemasok**: CRUD data pemasok, pencarian, relasi ke barang.
- **Transaksi Stok**: catat IN/OUT, otomatis menyesuaikan stok, tolak jika stok tidak cukup.
- **Laporan**: ekspor PDF (ReportLab) & Excel (OpenPyXL) untuk data stok barang.
- **Role-Based UI**: Tab pemasok, tombol hapus & ekspor hanya tersedia untuk admin.
  
Bonus:
- Penerapan hashing password.
- Dashboard dengan grafik stok.
- Struktur modular / MVC sederhana.

---

## Prasyarat

- **Python** 3.10 atau lebih baru
- Sistem Operasi: Windows 10/11 (uji utama)
- Library eksternal: `reportlab`, `openpyxl`, `matplotlib`

Jika ingin melakukan build `.exe`, butuh **PyInstaller** (opsional).

---

## Instalasi & Menjalankan Aplikasi

1. Clone / salin proyek ini.
2. (Opsional) Buat virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Unix/Mac
   ```
3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   python main.py
   ```
5. Login menggunakan kredensial default:
   - Admin: `admin` / `admin123`
   - Staf: `staf` / `staf123`

> Catatan: Jika file database `data/inventori.db` belum ada, aplikasi otomatis membuatnya beserta data dummy. Untuk reset data, hapus file tersebut atau jalankan skrip SQL di `data/database_setup.sql`.

---

## Cara Penggunaan (Singkat)

1. **Login:** Masukkan username/password sesuai level pengguna.
2. **Dashboard:** Lihat ringkasan stok, transaksi terbaru, grafik stok.
3. **Tab Barang:**
   - Cari barang berdasar kode/nama/kategori.
   - Tambah barang baru dengan memilih kategori & pemasok.
   - Edit/hapus barang (khusus admin).
   - Ekspor data barang ke PDF/Excel (khusus admin).
4. **Tab Pemasok:** Kelola data pemasok (hanya admin).
5. **Tab Transaksi:** Catat stok masuk/keluar, sistem otomatis menambah/mengurangi stok.
6. **Role-based UI:** Pengguna `staf` hanya dapat melihat/menambah transaksi dan mengelola barang terbatas (tanpa hapus/ekspor/pemasok).

---

## Struktur Proyek (Ringkas)

```
├── main.py                 # Entry point aplikasi
├── controllers/            # Logika bisnis per fitur
├── models/                 # Akses database & ORM sederhana
├── views/                  # Tkinter GUI (LoginView, MainView)
├── utils/                  # Helper (hashing, format, chart)
├── reports/                # ReportService (PDF/Excel)
├── data/
│   ├── inventori.db        # Database SQLite (di-generate)
│   └── database_setup.sql  # Skrip SQL setup & data dummy
├── docs/DOKUMENTASI_PROYEK.md  # Dokumentasi lengkap tugas
└── requirements.txt
```

---

## Dokumentasi Tambahan

- `docs/DOKUMENTASI_PROYEK.md`: Laporan tugas (latar belakang, analisis, desain, implementasi, pengujian, kesimpulan).
- ERD, DFD, mockup (format teks/ASCII) ada di dokumentasi tersebut.

---

## Known Issues & Pengembangan Lanjutan

- Saat ini pembatasan hak akses tambahan di level controller masih pending. Sebutkan rencana ini pada presentasi.
- Tambahkan constraint database (CHECK `stock >= 0`) dan penanganan exception yang lebih spesifik agar integritas data terjaga.
- Rencana ke depan:
  - Import data (CSV/Excel) ke tabel barang/pemasok.
  - Pengaturan pengguna lewat GUI.
  - Notifikasi stok minimum / reminder.
  - Migrasi ke hashing bcrypt / password salted.

---

## Lisensi & Kontributor

Proyek akademik untuk tugas akhir. Silakan modifikasi sesuai kebutuhan tugas / implementasi lanjutan.


