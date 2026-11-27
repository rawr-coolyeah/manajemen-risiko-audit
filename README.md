# Catatan Risiko & Audit

Situs belajar Manajemen Risiko dan Audit Sistem Informasi dalam bahasa Indonesia. Rangkuman mencakup 15 topik dari 16 PDF (135 halaman) dan satu gambar, dilengkapi delapan pelajaran singkat, 12 soal dengan pembahasan, serta kasus terpadu.

Alamat publik: https://rawr-coolyeah.github.io/manajemen-risiko-audit/

## Menjalankan lokal

```sh
python3 -m http.server 8000
```

Buka `http://localhost:8000`. Situs memakai HTML, CSS, dan JavaScript biasa tanpa dependensi. Seluruh materi tetap terbaca tanpa JavaScript. Pengaturan tema disimpan hanya di browser; jawaban latihan tidak dikirim ke server.

## Memperbarui isi

- `content/rangkuman.txt`: rangkuman dan pembahasan kasus.
- `content/latihan.json`: pertanyaan, pilihan, kunci, dan penjelasan.
- `content/pelajaran.json`: delapan pelajaran singkat.
- `content/sumber.json`: katalog sumber tanpa identitas atau lokasi file pribadi.
- `assets/`: stylesheet dan interaksi bersama.

Setelah mengubah isi, jalankan `python3 scripts/build.py`, periksa hasil, lalu commit file sumber dan HTML yang dihasilkan.

## GitHub Pages

Situs disajikan dari branch `main`, direktori `/` (root). File `.nojekyll` menonaktifkan pemrosesan Jekyll. Tidak diperlukan build atau GitHub Actions khusus.

Bahan PDF asli dan tugas mahasiswa tidak diunggah. Rujukan halaman, perbedaan konteks opini audit, serta ketidaksesuaian angka dalam bahan kuliah dijelaskan pada situs. Ini bahan belajar, bukan hasil audit profesional atau informasi kondisi perusahaan saat ini.
