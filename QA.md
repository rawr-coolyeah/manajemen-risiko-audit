# Verifikasi situs

Pemeriksaan Chrome lokal mencakup 12 halaman pada lebar 320, 390, 768, 1024 dan 1440 piksel. Semua 62 tautan/anchor internal diperiksa. Dua tema, teks 200%, pencarian, cetak, semua soal, dan pembacaan tanpa JavaScript diperiksa. Screenshot serta PDF cetak hanya disimpan sebagai artefak lokal yang diabaikan Git.

## Hard Gate

- R-02 PASS: tidak ada karakter em dash dalam salinan halaman yang dihasilkan.
- R-03 PASS: 12 halaman diperiksa pada lima lebar tanpa overflow horizontal; daftar topik melipat pada ruang sempit.
- R-17 PASS: cakupan 16 PDF/135 halaman/1 gambar berasal dari inventaris; angka studi dikaitkan ke sumber dan diberi batas interpretasi.
- R-18 PASS: tidak ada testimonial atau avatar.
- R-23 PASS: navigasi hanya menuju rangkuman, latihan dan sumber yang diminta; tidak ada logo atau aset visual rekaan.
- R-24 PASS: 62 tautan/anchor internal menuju target yang tersedia.
- R-25 PASS: rasio teks terendah yang diuji 5,94:1 pada tema terang dan 8,30:1 pada tema gelap; batas kontrol minimal 3,36:1 dan 4,67:1.
- R-26 PASS: pencarian, hapus, tema, cetak, semua pilihan soal dan disclosure diklik; feedback tidak disampaikan hanya lewat warna.
- R-27 PASS: pencarian kosong/tidak ditemukan dan pilihan soal belum diisi memiliki pesan; materi statis tidak memerlukan status pemuatan jaringan.
- R-28 PASS: tidak ada bagian FAQ generik.
- R-32 PASS: elemen interaktif memakai kontrol native, skip link tersedia, fokus keyboard diperiksa dan outline terlihat didefinisikan untuk setiap jenis kontrol.
- R-33 PASS: CSS/JS ditulis sebagai sumber; build.py merender template HTML dari isi terstruktur, tidak menambal CSS dengan skrip eksternal.
- R-34 PASS: kedua tema diuji; pengaturan tema bertahan setelah reload bila penyimpanan tersedia.
- R-35 PASS: seluruh halaman disajikan melalui server lokal dan dikunjungi Chrome; seluruh 12 soal serta 8 soal pelajaran diperiksa.
- R-36 PASS: tidak ada klaim sertifikasi, keamanan, pelanggan, atau performa situs.
- R-37 PASS: arah buku pegangan, dials, alasan tipografi, warna dan komposisi dicatat dalam DESIGN.md sebelum render.
- R-38 PASS: studi historis dibedakan dari ilustrasi latihan; materi sumber yang bermasalah ditandai.
- R-39 PASS: lang id, title unik, landmark dan satu h1 per halaman diperiksa; label terlihat, pointer, fokus, hover dan active tersedia; gerak menghormati reduced-motion.
- R-40 PASS: tidak ada media yang menggeser tata letak, font unduhan, atau skrip pihak ketiga; script interaksi dimuat defer.

## Purpose Gate

- R-01 PASS: warna datar dipilih untuk membaca; tidak ada gradient atau glow.
- R-04 PASS: tidak memakai ikon dekoratif atau pustaka ikon.
- R-06 PASS: Georgia pada judul dan font sistem pada isi mempunyai alasan keterbacaan dalam DESIGN.md.
- R-07 PASS: tidak ada pola latar dekoratif.
- R-08 PASS: tombol dan tautan tidak diberi panah dekoratif.
- R-09 PASS: tidak ada capsule badge atau label status rekaan.
- R-10 PASS: tidak ada glassmorphism.
- R-12 PASS: tidak ada bayangan berulang.
- R-13 PASS: tidak ada glow.
- R-14 PASS: materi menggunakan paragraf/daftar; struktur soal seragam karena tugasnya sama.
- R-19 PASS: tidak ada animasi template; perubahan tombol mendukung feedback interaksi.
- R-22 PASS: tidak memakai ilustrasi generik.

## Liveliness

- Dials PASS: ENERGY 1 / RHYTHM 2 / MOTION 1 ditetapkan dalam DESIGN.md.
- Konsistensi PASS: judul buku pegangan, bacaan tenang, variasi daftar, kasus dan latihan sesuai dials.
- Focal point PASS: judul atau soal menjadi fokus pada halaman terkait; screenshot desktop dan mobile diperiksa.
- Whitespace PASS: jarak memisahkan topik, sementara sumber tetap dekat dengan penjelasan.
- Accent PASS: hijau tua menandai tautan dan interaksi utama, dengan kontras terukur.
- Identity PASS: alur tujuan–risiko–kontrol–audit berulang pada pengantar, kasus dan pelajaran.
- Design Read PASS: catatan kuliah digital bagi mahasiswa SI, bahasa buku pegangan, tercatat sebelum render.

## Craftsmanship dan Quality Locks

- C-1 PASS: keputusan utama dan alasannya ada di DESIGN.md.
- C-2 PASS: semua kelas kontrol diuji; tanpa JavaScript tombol yang memerlukan script disembunyikan dan pembahasan native tersedia.
- C-3 PASS: setiap bagian berasal dari cakupan materi, latihan, atau sumber; tidak ada bagian pemasaran pengisi.
- C-4 PASS: tema, lima ukuran layar, teks 200%, dan fallback tanpa JavaScript diperiksa.
- C-5 PASS: statistik dan hasil studi bersumber; ilustrasi latihan ditandai.
- R-05 PASS: komposisi mengikuti bacaan, daftar topik dan latihan, tanpa template pemasaran.
- R-11 PASS: kontrol memakai radius kecil; teks dan bagian bacaan tidak berbentuk pil.
- R-15 PASS: label tindakan menyebut hasil: periksa jawaban, hapus, cetak, atau baca materi terkait.
- R-16 PASS: tidak ada jargon pemasaran dalam UI.
- R-20 PASS: tipografi buku pegangan dan alur konsep membentuk identitas situs kuliah.
- R-21 PASS: pembaca dapat memilih tema terang atau gelap; kedua tema diuji.
- R-29 PASS: palet utama netral dan hijau; warna fokus terpisah untuk keterlihatan.
- R-30 PASS: komposisi dibangun untuk materi mata kuliah, tanpa menyalin antarmuka produk lain.
- R-31 PASS: alasan warna, tata letak, tipografi, jarak, kontrol dan ketiadaan ilustrasi dicatat.

Pemeriksaan ini menguji fungsi yang dijelaskan, bukan sertifikasi kesesuaian WCAG menyeluruh. Tidak dilakukan pengujian perangkat fisik atau screen reader.
