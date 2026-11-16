# Testing Bug & Fix - Aplikasi Peminjaman Ruang Kelas

> **Analisis Perbandingan Validasi Input pada Aplikasi Peminjaman Ruang Kelas Berbasis GUI Python (Tkinter)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)](https://docs.python.org/3/library/tkinter.html)
[![Status](https://img.shields.io/badge/status-educational-success)]()
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

Aplikasi demo **satu file Python** yang mensimulasikan sistem peminjaman ruang kelas dengan **dua versi kode** di dalamnya: **VERSI BUG** (sengaja mengandung 4 kesalahan validasi) dan **VERSI FIX** (setelah diperbaiki).
---

## Tim Penyusun

| No | Nama | NIM |
|----|------|-----|
| 1 | **Moh. Abdi Ramadhan** | `F5215210001` |
| 2 | **Flesh Exel Saputra Tangkidi** | `F5212510021` |
| 3 | **Cliff Sbastian Wellem B.** | `F5212510014` |
| 4 | **Saiful** | `F5212510026` |

---

## Fitur

- **Pemilih versi** (BUG / FIX) - banner merah/hijau menandai versi aktif
- **Form peminjaman**: nama, ruang, tanggal, jam mulai, jam selesai
- **Tabel peminjaman** dengan status otomatis: `OK`, `DATA KOSONG`, `JAM TERBALIK`, `BENTROK dengan <nama>`
- **Umpan balik langsung** (diterima / ditolak / crash)
- **Reset Data Contoh**
- **Tes Otomatis 13 skenario** - hasil `PASS`/`FAIL` untuk kedua versi, plus kesimpulan jumlah tes gagal

---

## Bug yang Dipraktikkan

| Kode | Nama Bug | Dampak | Perbaikan (FIX) |
|------|----------|--------|------------------|
| **BUG 1** | Tidak ada pengecekan bentrok jadwal | Satu ruang bisa dipinjam dua orang di waktu yang sama | Fungsi `bentrok()` memeriksa irisan waktu pada ruang + tanggal sama |
| **BUG 2** | Jam selesai <= jam mulai tetap diterima | Data waktu tidak valid (durasi nol/negatif) | Validasi `if s <= m:` menolak jam tidak wajar |
| **BUG 3** | Format jam salah (mis. `"abc"`) menyebabkan crash | `ValueError` menghentikan program | `try/except ValueError` di sekitar `ke_menit()` + pesan galat jelas |
| **BUG 4** | Data kosong (nama/tanggal/jam) tetap diterima | Tersimpan peminjaman tanpa identitas / waktu jelas | Fungsi `cek_dasar()` memeriksa nama, ruang, tanggal sebelum menyimpan |

---

## Instalasi dan Menjalankan

### Prasyarat

- **Python 3.8+** (sudah termasuk modul `tkinter` dan `datetime`)
- Tidak ada dependensi eksternal - tanpa `pip install`

### Langkah

```bash
# 1. Clone repository
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# 2. Jalankan aplikasi
python "peminjaman ruangan_V1.py"
```

Catatan platform:

- **Windows**: jika `python` tidak dikenali, coba `py "peminjaman ruangan_V1.py"`
- **Linux**: pastikan `python3-tk` terpasang dengan `sudo apt install python3-tk`
- **macOS**: Tkinter sudah termasuk di installer Python resmi dari python.org

---

## Cara Mencoba Bug

Data contoh otomatis terisi: **Budi - Ruang A101 - 08:00-10:00**.

| Skenario | Input | VERSI BUG | VERSI FIX |
|----------|-------|-----------|------------|
| **BUG 4** | Nama dikosongkan | Data **tetap masuk** (salah) | Ditolak: "Nama peminjam tidak boleh kosong." (benar) |
| **BUG 1** | Siti, A101, 09:00-11:00 | Diterima (**bentrok**, salah) | Ditolak: "Bentrok! Ruang A101 sudah dipinjam Budi..." (benar) |
| **BUG 2** | Siti, A102, 11:00-09:00 | Diterima (**jam terbalik**, salah) | Ditolak: "Jam selesai harus lebih besar dari jam mulai." (benar) |
| **BUG 3** | Siti, A102, mulai `abc` | **CRASH** (`ValueError`, salah) | Ditolak: "Jam harus berformat HH:MM (contoh 09:30)." (benar) |

---

## Tes Otomatis

Klik tombol **"Jalankan Tes Otomatis (merah vs hijau)"** di dalam aplikasi. Akan muncul jendela berisi **13 skenario pengujian** terhadap VERSI BUG dan VERSI FIX, meliputi:

- Ruang kosong diterima
- Nama kosong / spasi saja ditolak
- Tanggal kosong ditolak
- Jam kosong ditolak
- Bentrok sebagian / total / di dalam ditolak
- Waktu bersebelahan diterima
- Tanggal berbeda diterima
- Jam selesai < mulai / = mulai ditolak
- Format jam salah ditolak

Contoh ringkasan akhir:

```
===== KESIMPULAN =====
Versi BUG: X tes gagal  (MERAH)
Versi FIX: 0 tes gagal  (HIJAU)
```

**VERSI FIX lulus 13/13 tes**, sedangkan VERSI BUG gagal pada sejumlah tes sesuai bug yang disimulasikan.

---


### Struktur Kode (ringkas)

```
peminjaman ruangan_V1.py
├── Konstanta        : DAFTAR_RUANG, peminjaman
├── Fungsi Bantu     : ke_menit, data_contoh, cek_dasar, bentrok
├── Logika Aplikasi  : pinjam_bug, pinjam_fix, status_baris, jalankan_tes
└── Tampilan (GUI)   : kelas Aplikasi (tk.Tk)
    ├── _buat_tampilan
    ├── _perbarui_mode
    ├── _pinjam
    ├── _reset
    ├── _muat_tabel
    └── _tampilkan_tes
```

---

## Konsep Testing

1. **Test Case Design** - menyusun 13 skenario dari *boundary value* dan *equivalence class* (kosong, bentrok sebagian, tepat bersebelahan, jam terbalik, format salah).
2. **Expected vs Actual Behavior** - membandingkan `harus_diterima` dengan `diterima` aktual.
3. **Regression Testing** - VERSI FIX diuji ulang dengan skenario sama untuk memastikan tidak ada bug tersisa.
4. **Error Handling dan Defensive Programming** - `try/except`, validasi input, pesan galat informatif.

---

## Catatan

- Data peminjaman hanya disimpan **di memori** (list Python). Menutup aplikasi akan menghapus data.
- Aplikasi dibuat untuk **tujuan edukasi**, bukan sistem produksi.
- Bug sengaja dipertahankan pada `pinjam_bug()` agar dapat didemonstrasikan.

---
