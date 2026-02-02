# Aplikasi Pengelola Uang Saku

**Aplikasi terminal sederhana untuk membantu mencatat pemasukan dan pengeluaran uang saku.** Aplikasi ini menyimpan saldo dan riwayat transaksi, menerima keterangan untuk setiap transaksi, serta menampilkan informasi dengan highlight berwarna agar mudah dibaca di terminal.

---

## Fitur utama ✅
- Menambah pemasukan dan pengeluaran dengan keterangan opsional
- Menyimpan riwayat transaksi (tipe, jumlah, keterangan, timestamp)
- Melihat riwayat pemasukan, riwayat pengeluaran, atau semua riwayat
- Tampilan terminal yang ramah dengan warna dan notifikasi sukses/error
- Data tersimpan otomatis di file `data.json`

---

## Persyaratan
- Python 3.8+ (direkomendasikan)
- (opsional, untuk Windows) `colorama` agar warna ANSI bekerja baik di Command Prompt: `pip install colorama`

---

## Cara menjalankan 💻
1. Clone atau download repository ini.
2. (Opsional) Buat virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux / macOS
   .\.venv\Scripts\activate  # Windows (PowerShell/Command Prompt)
   ```

3. (Opsional untuk Windows) Pasang `colorama`:

   ```bash
   pip install colorama
   ```

4. Jalankan program:

   ```bash
   python main.py
   ```

5. Ikuti menu di terminal. Pilihan menu:
   - 1: Tambah Pemasukan — masukkan jumlah dan keterangan (opsional)
   - 2: Tambah Pengeluaran — masukkan jumlah dan keterangan (opsional)
   - 3: Lihat Saldo
   - 4: Lihat Riwayat Pemasukan
   - 5: Lihat Riwayat Pengeluaran
   - 6: Lihat Semua Riwayat
   - 7: Reset Data (menghapus `data.json`/data yang ada setelah konfirmasi)
   - 8: Keluar

> Catatan: Input jumlah menerima format desimal umum (mis. `1000`, `1000.50`, atau `1.000,50`).

---

## File data
- `data.json` akan dibuat secara otomatis pada folder proyek untuk menyimpan `saldo` dan `history`.

Contoh struktur `data.json`:

```json
{
  "saldo": 150000,
  "history": [
    {
      "type": "Pemasukan",
      "amount": 200000,
      "description": "Uang jajan",
      "time": "2026-02-02T12:34:56.789"
    }
  ]
}
```

---

## Pengembangan lebih lanjut (opsional)
- Ekspor history ke CSV
- Filter riwayat berdasarkan tanggal
- GUI sederhana menggunakan `tkinter`

---

Terima kasih telah menggunakan aplikasi ini! Jika Anda ingin fitur baru atau perbaikan tampilan, silakan buka issue atau beri tahu saya di repo ini.
