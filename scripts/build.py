"""Render the course as buildless HTML for GitHub Pages."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = (ROOT / 'content/rangkuman.txt').read_text()
SOURCES = json.loads((ROOT / 'content/sumber.json').read_text())
QUIZZES = json.loads((ROOT / 'content/latihan.json').read_text())
LESSONS = json.loads((ROOT / 'content/pelajaran.json').read_text())
TITLES = ['Dasar audit sistem informasi', 'Risiko SI dan manajemen risiko', 'Pengendalian internal', 'Standar, kerangka kerja, dan etika', 'Materialitas, risiko audit, dan bukti', 'Proses dan rencana audit', 'Pendekatan audit dan TABK', 'COBIT 4.1 dan tingkat kematangan', 'Studi kasus Erajaya', 'Studi kasus PUSRI', 'Laporan audit dan tindak lanjut', 'Inti tugas 1, 2, dan 3', 'Empat opini laporan keuangan', 'Kualitas data dan data warehouse', 'Catatan pembacaan kritis']


def inline(text, prefix=''):
    value = escape(text)
    value = re.sub(r'\b([SE]\d{2})\b', lambda m: f'<a href="{prefix}reference/sumber.html#{m[1]}">{m[1]}</a>', value)
    return value


def prose(text, prefix=''):
    output = []
    list_kind = None
    for paragraph in text.strip().split('\n\n'):
        lines = paragraph.splitlines()
        for line in lines:
            bullet = line.startswith('• ')
            number = re.match(r'^(\d+)\. (.*)', line)
            kind = 'ul' if bullet else ('ol' if number else None)
            if list_kind and list_kind != kind:
                output.append(f'</{list_kind}>')
                list_kind = None
            if kind and list_kind is None:
                start = f' start="{number[1]}"' if number and number[1] != '1' else ''
                output.append(f'<{kind}{start}>')
                list_kind = kind
            if kind:
                output.append(f'<li>{inline(line[2:] if bullet else number[2], prefix)}</li>')
            elif line.startswith('Sumber:'):
                output.append(f'<p class="source">{inline(line, prefix)}</p>')
            else:
                output.append(f'<p>{inline(line, prefix)}</p>')
        if list_kind:
            output.append(f'</{list_kind}>')
            list_kind = None
    return '\n'.join(output)


def page(title, body, prefix='', current='rangkuman', single=False):
    nav = [('rangkuman', 'index.html', 'Rangkuman'), ('latihan', 'latihan.html', 'Latihan'), ('sumber', 'reference/sumber.html', 'Sumber')]
    links = ''.join(f'<a href="{prefix}{url}"' + (' aria-current="page"' if key == current else '') + f'>{label}</a>' for key, url, label in nav)
    return f'''<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Rangkuman kuliah Manajemen Risiko dan Audit Sistem Informasi. Materi lengkap, studi kasus, latihan, dan referensi.">
<meta name="theme-color" content="#236346"><title>{escape(title)} | Catatan Risiko &amp; Audit</title>
<link rel="stylesheet" href="{prefix}assets/belajar.css"><script src="{prefix}assets/belajar.js" defer></script></head>
<body><a class="skip" href="#isi">Lewati ke isi</a>
<header class="site-header"><a class="home-link" href="{prefix}index.html">Catatan Risiko &amp; Audit</a><div class="header-actions"><nav class="top-nav" aria-label="Navigasi utama">{links}</nav><button type="button" data-theme-toggle hidden>Mode gelap</button></div></header>
<main id="isi" class="page{' single-page' if single else ''}">{body}</main>
<footer class="site-footer"><p>Bahan belajar dari materi kuliah semester 7. Penjelasan tambahan dan batas sumber ditandai di setiap topik.</p><a href="https://github.com/rawr-coolyeah/manajemen-risiko-audit">Lihat repositori dan sumber situs</a></footer></body></html>'''


def quiz(index, prefix=''):
    q = QUIZZES[index]
    choices = ''.join(f'<label for="q{index}-{n}"><input type="radio" id="q{index}-{n}" name="q{index}" value="{n}"><span>{escape(option)}</span></label>' for n, option in enumerate(q['options']))
    return f'''<section class="quiz-item" id="soal-{index + 1}" data-quiz data-answer="{q['answer']}"><fieldset><legend>{escape(q['question'])}</legend><div class="quiz-options">{choices}</div></fieldset><button type="button" data-check hidden>Periksa jawaban</button><div class="feedback" data-feedback role="status" aria-live="polite" hidden><strong data-result></strong><div data-explanation><p>{escape(q['explanation'])}</p><a href="{prefix}index.html#topik-{q['chapter']:02d}">Baca materi terkait</a></div></div><noscript><details class="recall"><summary>Periksa dengan pembahasan</summary><p>Jawaban: {escape(q['options'][q['answer']])}. {escape(q['explanation'])}</p></details></noscript></section>'''


def intro(title, lead, meta=''):
    return f'<div class="intro"><h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p>' + (f'<p class="meta">{escape(meta)}</p>' if meta else '') + '</div>'


def main():
    for q in QUIZZES:
        assert len({len(option.split()) for option in q['options']}) == 1, q['question']
        assert 0 <= q['answer'] < len(q['options'])
    sections = re.split(r'^\d{2}\. [A-Z][A-Z /,:.0-9()–-]+\n', SUMMARY.split('LATIHAN MENGINGAT TANPA MELIHAT CATATAN')[0], flags=re.M)[1:]
    assert len(sections) == len(TITLES) == 15
    toc = '<details class="contents" open><summary>Daftar topik</summary><nav aria-label="Daftar topik"><ol>' + ''.join(f'<li><a href="#topik-{n:02d}">{title}</a></li>' for n, title in enumerate(TITLES, 1)) + '</ol></nav></details>'
    chapters = ''.join(f'<section class="chapter" id="topik-{n:02d}" data-chapter><h2>{title}</h2>{prose(text)}</section>' for n, (title, text) in enumerate(zip(TITLES, sections), 1))
    concept = '''<section class="concept"><h2>Pahami alurnya dulu</h2><ol><li>Tujuan organisasi</li><li>Risiko</li><li>Pengendalian</li><li>Pengujian audit</li><li>Laporan</li><li>Tindak lanjut</li></ol><p><strong>Manajemen menangani risiko.</strong> Auditor menguji pengelolaannya berdasarkan bukti. Hasil audit menjadi masukan untuk perbaikan berikutnya.</p></section>'''
    search = '''<div class="search-area" hidden><label for="topic-search">Cari dalam materi</label><div class="search-row"><input id="topic-search" type="search" placeholder="Misalnya: COBIT, bukti, atau ransomware" aria-describedby="search-count"><button type="button" data-clear-search>Hapus</button></div><p id="search-count" class="search-feedback" role="status" aria-live="polite"></p><p id="no-results" class="no-results" hidden>Topik tidak ditemukan. Gunakan kata yang lebih singkat atau hapus pencarian.</p></div>'''
    body = intro('Manajemen Risiko dan Audit Sistem Informasi', 'Rangkuman untuk memahami hubungan antara risiko, pengendalian, bukti, dan keputusan audit.', '15 topik · 16 PDF, 135 halaman, dan 1 gambar · Bahan kuliah semester 7')
    body += f'<div class="reading-layout">{toc}<div class="reader">{concept}<p>Baca satu topik, lalu tutup catatan dan jelaskan kembali dengan kata-katamu sendiri. <a href="latihan.html">Kerjakan latihan</a> untuk memeriksa pemahamanmu.</p><p class="screen-only"><button type="button" data-print hidden>Cetak rangkuman / simpan PDF</button></p>{search}{chapters}</div></div>'
    (ROOT / 'index.html').write_text(page('Rangkuman Manajemen Risiko dan Audit SI', body))

    lesson_list = '<ol class="lesson-list">' + ''.join(f'<li><a href="lessons/{n:04d}-{lesson["slug"]}.html">{escape(lesson["title"])}</a><span>{escape(lesson["win"])}</span></li>' for n, lesson in enumerate(LESSONS, 1)) + '</ol>'
    case = SUMMARY.split('KASUS LATIHAN TERPADU (ILUSTRASI)\n')[1].split('SUMBER TAMBAHAN UNTUK KLARIFIKASI')[0]
    prompt, solution = case.split('PEMBAHASAN KASUS\n')
    practice_body = intro('Latih cara berpikir audit', 'Mulai dari satu pelajaran singkat, atau langsung kerjakan soal. Coba jawab dari ingatan sebelum membaca pembahasannya.')
    practice_body += '<section><h2>Pelajaran singkat</h2>' + lesson_list + '</section><section class="chapter"><h2>Periksa pemahamanmu</h2><p>Pilih jawaban, lalu tekan “Periksa jawaban”. Kamu dapat mencoba kembali setelah membaca penjelasannya.</p><p class="quiz-status" id="quiz-status" role="status" aria-live="polite">Belum ada jawaban diperiksa. Hasil latihan tidak dikirim ke server.</p>' + ''.join(quiz(i) for i in range(len(QUIZZES))) + '</section>'
    practice_body += '<section class="chapter"><h2>Kasus terpadu: portal akademik</h2><p class="quiet">Ilustrasi pembelajaran, bukan hasil audit organisasi nyata.</p>' + prose(prompt) + '<details class="recall"><summary>Buka pembahasan setelah mencoba</summary>' + prose(solution) + '</details></section><section class="chapter"><h2>Ulangi dengan jarak</h2><p>Pelajari ulang bagian yang belum tepat besok, tiga hari kemudian, dan satu minggu kemudian. Ini saran belajar, bukan jadwal ujian resmi.</p><p>Jika masih bingung, tanyakan kepada agen: “Beri saya contoh lain untuk membedakan risiko SI dan risiko audit.”</p></section>'
    (ROOT / 'latihan.html').write_text(page('Latihan Manajemen Risiko dan Audit SI', practice_body, current='latihan', single=True))

    for n, lesson in enumerate(LESSONS, 1):
        body = intro(lesson['title'], lesson['win'], 'Pelajaran singkat · Latihan mandiri')
        body += f'<section><h2>Inti yang perlu dipahami</h2><p>{escape(lesson["explain"])}</p><p class="source">Bacaan utama: <a href="../reference/sumber.html#{lesson["source"]}">{lesson["source"]}, hlm. {lesson["pages"]}</a>. Sumber lokal dirangkum; dokumen asli tidak diunggah.</p><h3>Contoh</h3><p>{escape(lesson["example"])}</p></section><section class="chapter"><h2>Coba tanpa melihat catatan</h2>{quiz(lesson["quiz"], "../")}<p>{escape(lesson["recall"])}</p><details class="recall"><summary>Bandingkan dengan penjelasan</summary><p>{escape(lesson["solution"])}</p></details></section><p>Masih ada yang kurang jelas? Tanyakan bagian ini kepada agen dan minta contoh tambahan.</p>'
        body += f'<p><a href="../index.html#topik-{lesson["chapter"]:02d}">Baca rangkuman topik ini</a> · <a href="../reference/rangkuman-cepat.html">Lihat pengingat konsep</a></p><nav class="lesson-nav" aria-label="Urutan pelajaran"><a href="../latihan.html">Kembali ke latihan</a>'
        if n < len(LESSONS):
            body += f'<a href="{n+1:04d}-{LESSONS[n]["slug"]}.html">Pelajaran berikutnya</a>'
        body += '</nav>'
        (ROOT / f'lessons/{n:04d}-{lesson["slug"]}.html').write_text(page(lesson['title'], body, '../', 'latihan', True))

    catalog = intro('Sumber dan batas materi', 'Setiap topik merujuk ke kode sumber dan halaman PDF. Bahan kuliah asli disimpan lokal dan tidak dipublikasikan di situs ini.', '16 PDF / 135 halaman + 1 gambar; dua versi Tugas 3 mempunyai teks identik.')
    catalog += '<section><h2>Bahan kuliah dan latihan</h2><ul class="source-list">'
    for source in SOURCES:
        if not source['id'].startswith('S'):
            continue
        pages = f' · {source["pages"]} halaman PDF' if source.get('pages') else ' · 1 gambar'
        catalog += f'<li id="{source["id"]}"><strong>{source["id"]}: {escape(source["title"])}</strong><p>{escape(source["note"])}{pages}</p></li>'
    catalog += '</ul></section><section class="chapter"><h2>Sumber primer untuk klarifikasi</h2><ul class="source-list">'
    resources = ['# Manajemen Risiko dan Audit SI Resources', '', '## Knowledge', '', 'Bahan kuliah lokal dirangkum dengan kode S01–S17. [Katalog lengkap](reference/sumber.html) mencantumkan cakupan dan batasnya. Tugas dipakai sebagai bahan latihan, bukan standar profesional.', '']
    for source in SOURCES:
        if not source['id'].startswith('E'):
            continue
        catalog += f'<li id="{source["id"]}"><strong>{source["id"]}: <a href="{escape(source["url"])}">{escape(source["title"])}</a></strong><p>{escape(source["note"])}</p></li>'
        resources += [f'- [{source["title"]}]({source["url"]})', f'  {source["note"]}']
    catalog += '</ul></section><section class="chapter"><h2>Cara membaca sumber</h2><p>Nomor halaman mengikuti halaman PDF, bukan nomor cetak jurnal. Persentase keberhasilan pada slide tidak dijadikan fakta umum tanpa rujukan yang dapat ditelusuri. Studi Erajaya dan PUSRI menggambarkan periode penelitian, bukan kondisi perusahaan saat ini.</p><p><a href="../index.html#topik-15">Baca seluruh catatan pembacaan kritis</a></p></section>'
    (ROOT / 'reference/sumber.html').write_text(page('Sumber materi dan klarifikasi', catalog, '../', 'sumber', True))
    resources += ['', '## Wisdom (Communities)', '', '- Diskusi kelas/tutorial: konfirmasi istilah soal, cara penilaian, dan harapan pengajar. Tidak ada komunikasi yang dikirim kepada pihak lain.', '', '## Gaps', '', '- Belum tersedia kisi-kisi ujian resmi atau bukti penguasaan pembaca.', '- Statistik beberapa slide dan agregasi nilai PUSRI memerlukan klarifikasi sebelum dipakai sebagai bukti formal.', '- Gambar strategi asli soal Tugas 1 tidak ditemukan sebagai berkas tersendiri.']
    (ROOT / 'RESOURCES.md').write_text('\n'.join(resources) + '\n')

    quick = intro('Pengingat konsep', 'Baca cepat setelah belajar, lalu jelaskan kembali tanpa melihat. Rujukan ini tidak menyatakan bahwa kamu sudah menguasai seluruh istilah.')
    quick += '''<section><h2>Rantai jawaban kasus</h2><p>Tujuan → risiko → pengendalian → bukti pengujian → temuan → rekomendasi → tindak lanjut.</p><h3>Empat pertanyaan sebelum menyimpulkan</h3><ol><li>Apa yang seharusnya terjadi menurut kriteria?</li><li>Apa yang benar-benar terjadi menurut bukti?</li><li>Apa dampak kesenjangannya terhadap tujuan?</li><li>Perbaikan apa yang bisa diuji efektivitasnya?</li></ol></section><section class="chapter"><h2>Pasangan yang perlu dibedakan</h2><dl><dt><strong>Efektif / efisien</strong></dt><dd>Mencapai tujuan / menggunakan sumber daya dengan tepat.</dd><dt><strong>Ancaman / kerentanan</strong></dt><dd>Penyebab potensial insiden / kelemahan yang dapat dimanfaatkan.</dd><dt><strong>Risiko SI / risiko audit</strong></dt><dd>Risiko terhadap sistem dan organisasi / risiko kesimpulan auditor yang keliru.</dd><dt><strong>Cukup / tepat</strong></dt><dd>Kuantitas bukti / kualitas, relevansi dan keandalan bukti.</dd><dt><strong>Kontrol tersedia / efektif</strong></dt><dd>Kontrol direncanakan atau ada / kontrol terbukti bekerja sesuai tujuan.</dd><dt><strong>Tidak wajar / tidak menyatakan pendapat</strong></dt><dd>Salah saji material dan meluas terbukti / bukti tidak cukup dengan kemungkinan dampak material dan meluas, dalam audit laporan keuangan.</dd></dl></section><section class="chapter"><h2>Urutan yang sering muncul</h2><ul><li>CIA: kerahasiaan, integritas, ketersediaan.</li><li>Risiko: identifikasi, analisis, evaluasi, penanganan; disertai konteks, komunikasi dan pemantauan.</li><li>Audit: perencanaan, lapangan, pelaporan, tindak lanjut.</li><li>COBIT 4.1: PO, AI, DS, ME.</li><li>Maturity 0–5: belum ada, ad hoc, berulang, ditetapkan, diukur, dioptimalkan.</li></ul><p class="source">Rujukan: <a href="sumber.html#S01">S01</a>, <a href="sumber.html#S06">S06</a>, <a href="sumber.html#S07">S07</a>, <a href="sumber.html#S09">S09</a>, <a href="sumber.html#S13">S13</a>, <a href="sumber.html#S15">S15</a> dan <a href="sumber.html#E06">E06</a>.</p></section><p><a href="../latihan.html">Uji dengan latihan</a> · <a href="../index.html">Buka rangkuman lengkap</a></p><button class="screen-only" type="button" data-print hidden>Cetak pengingat konsep</button>'''
    (ROOT / 'reference/rangkuman-cepat.html').write_text(page('Pengingat konsep audit', quick, '../', 'rangkuman', True))
    print(f'Rendered 12 HTML pages, {len(TITLES)} topics, {len(LESSONS)} lessons, {len(QUIZZES)} questions.')


if __name__ == '__main__':
    main()
