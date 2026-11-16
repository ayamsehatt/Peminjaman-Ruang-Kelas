"""
APLIKASI DEMO BUG & FIX - Peminjaman Ruang Kelas
================================================
Satu file, Python standar (tkinter bawaan Python).
Cukup tekan RUN, jendela aplikasi akan terbuka.

Empat bug yang dipraktikkan:
    BUG 1: ruang yang sama bisa dipinjam dua orang di waktu yang bertabrakan
    BUG 2: jam selesai lebih awal dari / sama dengan jam mulai tetap diterima
    BUG 3: format jam salah (misal "abc") membuat program crash (ValueError)
    BUG 4: data KOSONG (nama / tanggal / jam) tetap diterima

Cara memakai:
    1. Data contoh sudah terisi: Budi meminjam Ruang A101 jam 08:00 - 10:00.
    2. Pilih "Versi BUG", kosongkan Nama peminjam lalu klik Ajukan
       -> data tetap MASUK (bug 4). Coba juga Ruang A101 jam 09:00 - 11:00
       atas nama Siti -> diterima (BENTROK, bug 1).
    3. Pilih "Versi FIX", ulangi -> ditolak dengan pesan yang jelas.
    4. Klik "Jalankan Tes Otomatis" untuk melihat tes merah (BUG) vs hijau (FIX).
"""

import tkinter as tk
from tkinter import ttk
from datetime import date, datetime

DAFTAR_RUANG = ["Ruang A101", "Ruang A102", "Lab Komputer", "Aula"]

peminjaman = []   # penyimpanan sementara (di memori)


# ====================================================================
# FUNGSI BANTU
# ====================================================================
def ke_menit(teks_jam):
    """'09:30' -> 570. Melempar ValueError jika format salah."""
    t = datetime.strptime(teks_jam.strip(), "%H:%M")
    return t.hour * 60 + t.minute


def data_contoh(tanggal):
    """Satu peminjaman awal supaya bentrok mudah dicoba."""
    return [{"nama": "Budi", "ruang": "Ruang A101", "tanggal": tanggal,
             "mulai": "08:00", "selesai": "10:00", "m": 480, "s": 600}]


def cek_dasar(nama, ruang, tanggal):
    """Pemeriksaan data kosong / dasar. Dipakai di VERSI FIX saja."""
    if not nama.strip():
        return "Nama peminjam tidak boleh kosong."
    if ruang not in DAFTAR_RUANG:
        return "Pilih ruang yang tersedia."
    try:
        datetime.strptime(tanggal.strip(), "%Y-%m-%d")
    except ValueError:
        return "Tanggal harus berformat YYYY-MM-DD (contoh 2026-11-16)."
    return None


def bentrok(ruang, tanggal, m, s):
    """Kembalikan peminjaman yang bertabrakan, atau None."""
    for b in peminjaman:
        if b["ruang"] == ruang and b["tanggal"] == tanggal and m < b["s"] and s > b["m"]:
            return b
    return None


# ====================================================================
# LOGIKA APLIKASI
# ====================================================================
def pinjam_bug(nama, ruang, tanggal, mulai, selesai):
    """VERSI BUG: kode awal yang punya kesalahan."""
    # BUG 4: tidak ada pengecekan data kosong (nama / tanggal / jam)
    #        (jam yang dikosongkan dianggap 00:00 agar tetap lolos)

    # BUG 3: ke_menit() error (crash) jika format jam salah, mis. "abc"
    m = ke_menit(mulai) if mulai.strip() else 0
    s = ke_menit(selesai) if selesai.strip() else 0

    # BUG 2: tidak ada pengecekan jam selesai > jam mulai
    # BUG 1: tidak ada pengecekan bentrok dengan peminjaman lain
    peminjaman.append({"nama": nama.strip(), "ruang": ruang, "tanggal": tanggal.strip(),
                       "mulai": mulai.strip(), "selesai": selesai.strip(), "m": m, "s": s})
    return True, "Peminjaman berhasil disimpan."


def pinjam_fix(nama, ruang, tanggal, mulai, selesai):
    """VERSI FIX: kode setelah diperbaiki."""
    # FIX 4: tolak data kosong
    salah = cek_dasar(nama, ruang, tanggal)
    if salah:
        return False, salah
    if not mulai.strip() or not selesai.strip():
        return False, "Jam mulai dan jam selesai tidak boleh kosong."

    # FIX 3: format jam diperiksa, tidak crash
    try:
        m, s = ke_menit(mulai), ke_menit(selesai)
    except ValueError:
        return False, "Jam harus berformat HH:MM (contoh 09:30)."

    # FIX 2: jam selesai harus setelah jam mulai
    if s <= m:
        return False, "Jam selesai harus lebih besar dari jam mulai."

    # FIX 1: tolak jika bertabrakan dengan peminjaman lain
    lawan = bentrok(ruang, tanggal.strip(), m, s)
    if lawan:
        return False, (f"Bentrok! {ruang} sudah dipinjam {lawan['nama']} "
                       f"pukul {lawan['mulai']} - {lawan['selesai']}.")

    peminjaman.append({"nama": nama.strip(), "ruang": ruang, "tanggal": tanggal.strip(),
                       "mulai": f"{m // 60:02d}:{m % 60:02d}",
                       "selesai": f"{s // 60:02d}:{s % 60:02d}", "m": m, "s": s})
    return True, "Peminjaman berhasil disimpan."


def status_baris(i):
    """Status sebuah baris di tabel: OK / DATA KOSONG / JAM TERBALIK / BENTROK."""
    b = peminjaman[i]
    if not b["nama"] or not b["tanggal"] or not b["mulai"] or not b["selesai"]:
        return "DATA KOSONG"
    if b["s"] <= b["m"]:
        return "JAM TERBALIK"
    for j, lain in enumerate(peminjaman):
        if (j != i and lain["ruang"] == b["ruang"] and lain["tanggal"] == b["tanggal"]
                and lain["s"] > lain["m"] and b["m"] < lain["s"] and b["s"] > lain["m"]):
            return f"BENTROK dengan {lain['nama']}"
    return "OK"


def jalankan_tes():
    """Tes otomatis untuk kedua versi. Mengembalikan teks hasil."""
    T = "2026-11-16"
    # (deskripsi, nama, ruang, tanggal, mulai, selesai, harus_diterima)
    kasus = [
        ("Ruang kosong diterima",         "Siti", "Ruang A102", T, "09:00", "11:00", True),
        ("Nama kosong ditolak",           "",     "Ruang A102", T, "09:00", "11:00", False),
        ("Nama spasi saja ditolak",       "   ",  "Ruang A102", T, "09:00", "11:00", False),
        ("Tanggal kosong ditolak",        "Siti", "Ruang A102", "", "09:00", "11:00", False),
        ("Jam kosong ditolak",            "Siti", "Ruang A102", T, "",      "",      False),
        ("Bentrok sebagian ditolak",      "Siti", "Ruang A101", T, "09:00", "11:00", False),
        ("Bentrok total ditolak",         "Siti", "Ruang A101", T, "08:00", "10:00", False),
        ("Bentrok di dalam ditolak",      "Siti", "Ruang A101", T, "08:30", "09:30", False),
        ("Waktu bersebelahan diterima",   "Siti", "Ruang A101", T, "10:00", "12:00", True),
        ("Tanggal berbeda diterima",      "Siti", "Ruang A101", "2026-11-17", "08:00", "10:00", True),
        ("Jam selesai < mulai ditolak",   "Siti", "Ruang A102", T, "11:00", "09:00", False),
        ("Jam mulai = selesai ditolak",   "Siti", "Ruang A102", T, "09:00", "09:00", False),
        ("Format jam salah ditolak",      "Siti", "Ruang A102", T, "abc",   "11:00", False),
    ]
    simpanan = list(peminjaman)          # supaya tes tidak merusak data di layar
    baris, gagal_per_versi = [], {}

    for label, fungsi in (("BUG", pinjam_bug), ("FIX", pinjam_fix)):
        baris.append(f"===== TES VERSI {label} =====")
        gagal = 0
        for desk, nama, ruang, tgl, mulai, selesai, harus in kasus:
            peminjaman[:] = data_contoh(T)
            try:
                diterima, _ = fungsi(nama, ruang, tgl, mulai, selesai)
                lulus = diterima == harus
                ket = "lulus" if lulus else "GAGAL"
            except Exception as e:       # program crash = tes gagal
                lulus, ket = False, f"GAGAL (crash: {type(e).__name__})"
            gagal += 0 if lulus else 1
            baris.append(f"  [{'PASS' if lulus else 'FAIL'}] {desk:<31} {ket}")
        gagal_per_versi[label] = gagal
        baris.append(f"  Ringkasan: {len(kasus) - gagal}/{len(kasus)} lulus\n")

    peminjaman[:] = simpanan
    baris.append("===== KESIMPULAN =====")
    baris.append(f"Versi BUG: {gagal_per_versi['BUG']} tes gagal  (MERAH)")
    baris.append(f"Versi FIX: {gagal_per_versi['FIX']} tes gagal  (HIJAU)")
    return "\n".join(baris)


# ====================================================================
# TAMPILAN (GUI)
# ====================================================================
WARNA_BUG = "#c0392b"
WARNA_FIX = "#1e8449"
LATAR = "#f4f6f8"


class Aplikasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peminjaman Ruang Kelas - Demo Bug & Fix")
        self.geometry("760x740")
        self.minsize(700, 700)
        self.configure(bg=LATAR)

        self.mode = tk.StringVar(value="bug")
        self.var_nama = tk.StringVar()
        self.var_ruang = tk.StringVar(value=DAFTAR_RUANG[0])
        self.var_tanggal = tk.StringVar(value=date.today().isoformat())
        self.var_mulai = tk.StringVar(value="09:00")
        self.var_selesai = tk.StringVar(value="11:00")

        peminjaman[:] = data_contoh(self.var_tanggal.get())
        self._buat_tampilan()
        self._perbarui_mode()
        self._muat_tabel()

    # ---------------------------------------------------------------
    def _buat_tampilan(self):
        self.banner = tk.Label(self, text="", font=("Segoe UI", 13, "bold"),
                               fg="white", pady=10)
        self.banner.pack(fill="x")

        isi = tk.Frame(self, bg=LATAR, padx=18, pady=10)
        isi.pack(fill="both", expand=True)

        pilih = tk.LabelFrame(isi, text=" Pilih versi kode ", bg=LATAR,
                              font=("Segoe UI", 10, "bold"), padx=10, pady=6)
        pilih.pack(fill="x")
        for teks, nilai in (("Versi BUG (kode salah)", "bug"),
                            ("Versi FIX (kode diperbaiki)", "fix")):
            tk.Radiobutton(pilih, text=teks, value=nilai, variable=self.mode,
                           command=self._perbarui_mode, bg=LATAR,
                           font=("Segoe UI", 10)).pack(side="left", padx=12)

        form = tk.LabelFrame(isi, text=" Ajukan peminjaman ", bg=LATAR,
                             font=("Segoe UI", 10, "bold"), padx=10, pady=8)
        form.pack(fill="x", pady=(8, 0))
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        def label(teks, r, c):
            tk.Label(form, text=teks, bg=LATAR, font=("Segoe UI", 10)).grid(
                row=r, column=c, sticky="w", pady=4, padx=(0, 8))

        label("Nama peminjam", 0, 0)
        e_nama = ttk.Entry(form, textvariable=self.var_nama, font=("Segoe UI", 11))
        e_nama.grid(row=0, column=1, sticky="ew", pady=4)

        label("Ruang", 0, 2)
        ttk.Combobox(form, textvariable=self.var_ruang, values=DAFTAR_RUANG,
                     state="readonly", font=("Segoe UI", 11)).grid(
            row=0, column=3, sticky="ew", pady=4)

        label("Tanggal (YYYY-MM-DD)", 1, 0)
        e_tgl = ttk.Entry(form, textvariable=self.var_tanggal, font=("Segoe UI", 11))
        e_tgl.grid(row=1, column=1, sticky="ew", pady=4)

        label("Jam mulai (HH:MM)", 1, 2)
        e_mulai = ttk.Entry(form, textvariable=self.var_mulai, font=("Segoe UI", 11))
        e_mulai.grid(row=1, column=3, sticky="ew", pady=4)

        label("Jam selesai (HH:MM)", 2, 2)
        e_selesai = ttk.Entry(form, textvariable=self.var_selesai, font=("Segoe UI", 11))
        e_selesai.grid(row=2, column=3, sticky="ew", pady=4)

        tombol = tk.Frame(form, bg=LATAR)
        tombol.grid(row=3, column=0, columnspan=4, sticky="e", pady=(8, 0))
        ttk.Button(tombol, text="Ajukan Peminjaman", command=self._pinjam).pack(side="left")
        ttk.Button(tombol, text="Reset Data Contoh",
                   command=self._reset).pack(side="left", padx=(8, 0))
        for e in (e_nama, e_tgl, e_mulai, e_selesai):
            e.bind("<Return>", lambda _e: self._pinjam())

        self.pesan = tk.Label(isi, text="Isi form lalu klik Ajukan Peminjaman.",
                              bg=LATAR, fg="#555", anchor="w", justify="left",
                              wraplength=700, font=("Segoe UI", 10, "bold"))
        self.pesan.pack(fill="x", pady=(10, 4))

        tabel_frame = tk.Frame(isi)
        tabel_frame.pack(fill="both", expand=True)
        kolom = ("no", "nama", "ruang", "tanggal", "waktu", "status")
        self.tabel = ttk.Treeview(tabel_frame, columns=kolom, show="headings", height=7)
        for k, judul, lebar, rata in (("no", "No", 40, "center"),
                                      ("nama", "Peminjam", 100, "w"),
                                      ("ruang", "Ruang", 100, "w"),
                                      ("tanggal", "Tanggal", 90, "center"),
                                      ("waktu", "Waktu", 100, "center"),
                                      ("status", "Status", 190, "w")):
            self.tabel.heading(k, text=judul)
            self.tabel.column(k, width=lebar, anchor=rata)
        self.tabel.tag_configure("salah", background="#fadbd8", foreground="#922b21")
        scroll = ttk.Scrollbar(tabel_frame, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        petunjuk = ("Coba di Versi BUG lalu Versi FIX (data contoh: Budi, Ruang A101, 08:00-10:00):\n"
                    "  0) Nama peminjam dikosongkan             -> data kosong\n"
                    "  1) Siti, Ruang A101, jam 09:00 - 11:00   -> bentrok dengan Budi\n"
                    "  2) Siti, Ruang A102, jam 11:00 - 09:00   -> jam terbalik\n"
                    "  3) Siti, Ruang A102, jam mulai 'abc'     -> format jam salah")
        tk.Label(isi, text=petunjuk, bg=LATAR, fg="#444", justify="left",
                 anchor="w", font=("Segoe UI", 9)).pack(fill="x", pady=(8, 0))

        ttk.Button(isi, text="Jalankan Tes Otomatis (merah vs hijau)",
                   command=self._tampilkan_tes).pack(fill="x", pady=(8, 0))

    # ---------------------------------------------------------------
    def _perbarui_mode(self):
        if self.mode.get() == "bug":
            self.banner.config(text="VERSI BUG  -  bentrok jadwal tidak dicek", bg=WARNA_BUG)
        else:
            self.banner.config(text="VERSI FIX  -  validasi sudah diperbaiki", bg=WARNA_FIX)
        self.pesan.config(text="Versi diganti. Coba ajukan peminjaman.", fg="#555")

    def _pinjam(self):
        fungsi = pinjam_bug if self.mode.get() == "bug" else pinjam_fix
        try:
            ok, teks = fungsi(self.var_nama.get(), self.var_ruang.get(),
                              self.var_tanggal.get(), self.var_mulai.get(),
                              self.var_selesai.get())
        except Exception as e:   # di versi BUG, jam salah membuat program "crash"
            self.pesan.config(
                text=f"CRASH! Program error: {type(e).__name__}: {e}\n"
                     "(Di aplikasi nyata, program akan berhenti. Inilah bug #3.)",
                fg=WARNA_BUG)
            return

        if ok:
            self.pesan.config(text="[OK] " + teks, fg=WARNA_FIX)
            self.var_nama.set("")
        else:
            self.pesan.config(text="[DITOLAK] " + teks, fg=WARNA_BUG)
        self._muat_tabel()

    def _reset(self):
        peminjaman[:] = data_contoh(date.today().isoformat())
        self._muat_tabel()
        self.pesan.config(text="Data dikembalikan ke data contoh.", fg="#555")

    def _muat_tabel(self):
        self.tabel.delete(*self.tabel.get_children())
        for i, b in enumerate(peminjaman):
            status = status_baris(i)
            self.tabel.insert("", "end",
                              values=(i + 1, b["nama"], b["ruang"], b["tanggal"],
                                      f"{b['mulai']} - {b['selesai']}", status),
                              tags=() if status == "OK" else ("salah",))

    def _tampilkan_tes(self):
        jendela = tk.Toplevel(self)
        jendela.title("Hasil Tes Otomatis")
        jendela.geometry("660x680")
        teks = tk.Text(jendela, font=("Consolas", 10), padx=10, pady=10, wrap="none")
        teks.pack(fill="both", expand=True)
        teks.tag_configure("merah", foreground=WARNA_BUG)
        teks.tag_configure("hijau", foreground=WARNA_FIX)
        for baris in jalankan_tes().split("\n"):
            tag = "merah" if ("FAIL" in baris or "(MERAH)" in baris) else \
                  "hijau" if ("PASS" in baris or "(HIJAU)" in baris) else ""
            teks.insert("end", baris + "\n", tag)
        teks.config(state="disabled")


if __name__ == "__main__":
    Aplikasi().mainloop()
