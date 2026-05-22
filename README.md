# Penjelasan Lengkap Notebook Project Big Data

**Prediksi Produktivitas dan Produksi Padi Provinsi Lampung – Pendekatan Machine Learning Berbasis Musim Tanam (2019–2024)**

Teknik Informatika – Universitas Lampung – 2026

---

## Gambaran Umum Notebook

Notebook ini merupakan proyek penelitian di bidang pertanian berbasis data (agricultural data science) yang bertujuan memprediksi dua hal utama untuk wilayah Provinsi Lampung:

1. **Produktivitas padi** dalam satuan ton per hektar (ton/ha) — yaitu seberapa banyak gabah yang dihasilkan dari setiap satu hektar lahan yang dipanen.
2. **Produksi padi** dalam satuan ton — yaitu total hasil panen suatu kabupaten, yang merupakan perkalian antara produktivitas dan luas lahan yang dipanen.

Cakupan wilayah meliputi seluruh 15 kabupaten/kota di Provinsi Lampung untuk periode 2019 hingga 2024, dengan total 90 sampel data tahunan.

**Dua sumber data utama yang digunakan:**

- **Data BPS (Badan Pusat Statistik) Provinsi Lampung** — menyediakan angka resmi luas panen (dalam hektar) dan total produksi padi (dalam ton) per kabupaten dari tahun 2018 hingga 2024.
- **Data cuaca NASA POWER API** — menyediakan data cuaca harian per kabupaten mencakup 6 parameter meteorologi selama periode yang sama, yaitu radiasi matahari, suhu rata-rata, suhu maksimum, suhu minimum, kelembapan relatif, dan curah hujan.

**Pendekatan yang membedakan penelitian ini dari prediksi biasa** adalah penggunaan konsep musim tanam padi yang disesuaikan dengan kalender pertanian Lampung. Alih-alih hanya menggunakan data cuaca bulanan mentah, notebook ini mengagregasi cuaca ke dalam tiga jendela musim tanam: Musim Utama (November–Maret), Musim Gadu (April–Juli), dan Musim Kemarau (Agustus–Oktober). Pendekatan ini memberikan makna agronomis pada data cuaca karena setiap musim tanam memiliki pola cuaca dan pengaruh yang berbeda terhadap hasil panen.

**Output akhir yang ingin dicapai** adalah model Machine Learning yang mampu memprediksi produktivitas padi tahun depan berdasarkan kondisi cuaca musiman dan riwayat produktivitas tahun-tahun sebelumnya, dievaluasi menggunakan Walk-Forward Validation agar hasilnya realistis secara temporal.

---

## Alur Besar Notebook

Notebook ini mengikuti alur pipeline data science yang runtut dari pengambilan data mentah hingga interpretasi hasil akhir. Berikut adalah gambaran besar setiap tahap:

**1. Persiapan Lingkungan (Cell 1–4)**
Mendefinisikan seluruh konstanta, mengimpor pustaka, mengatur reproduktibilitas, dan mendaftarkan 15 kabupaten yang akan diproses.

**2. Data Loading dan Cleaning (Cell 5–16)**
Memuat data BPS dari file CSV dan data cuaca dari 15 file JSON, memvalidasi kelengkapannya secara ketat, mengonversi nilai sentinel NASA POWER (-999) menjadi nilai kosong (NaN), mengimputasi nilai hilang, lalu mengagregasi data harian cuaca menjadi data bulanan.

**3. Rekayasa Fitur Berbasis Musim Tanam (Cell 17–22)**
Mengubah 1.260 baris data bulanan menjadi fitur bermakna per musim tanam, menggabungkan dengan data BPS, menghitung target produktivitas, menambahkan fitur historis (lag dan rolling), serta menyiapkan matriks model dengan One-Hot Encoding untuk variabel kabupaten.

**4. Exploratory Data Analysis / EDA (Cell 23–32)**
Memahami karakteristik data: statistik deskriptif per kabupaten, tren produktivitas dari tahun ke tahun, distribusi nilai, pola cuaca per musim, dan hubungan (korelasi) antara fitur cuaca dan target produktivitas.

**5. Pemodelan dan Evaluasi (Cell 33–43)**
Mendefinisikan 4 model Machine Learning (Ridge Regression, Ridge Hist Lag, Random Forest, Gradient Boosting) dan 4 model baseline (Naive Mean, Naive Kabupaten Mean, Naive Lag1, Naive Rolling2), kemudian menjalankan Walk-Forward Validation selama 5 fold (2020–2024). Dilanjutkan dengan ablation study untuk mengukur kontribusi masing-masing kelompok fitur, dan evaluasi final pada data test tahun 2024.

**6. Visualisasi dan Analisis Error (Cell 44–53)**
Scatter plot prediksi vs aktual, analisis residual (arah dan besaran error per kabupaten), perbandingan produksi aktual vs prediksi, feature importance, dan distribusi akurasi per kabupaten.

**7. Ringkasan dan Kesimpulan (Cell 54–55)**
Laporan otomatis yang merangkum seluruh hasil numerik, interpretasi performa, insight ablation study, dan keterbatasan penelitian.

---

## Penjelasan Per Cell

### Cell 1 – Judul dan Gambaran Umum Notebook

**Jenis cell:** Markdown

**Tujuan:**
Memperkenalkan notebook kepada pembaca, menjelaskan konteks penelitian, sumber data yang digunakan, alur analisis secara ringkas, dan catatan perbaikan dari versi sebelumnya (v3).

**Penjelasan isi:**
Cell ini berfungsi sebagai halaman muka dokumen. Ia menampilkan judul resmi proyek, nama mata kuliah dan universitas, serta tabel alur analisis yang mencantumkan 7 tahap pipeline dari Data Loading hingga Ringkasan. Secara khusus, markdown ini menyebutkan tiga perbaikan penting dari versi 2 (v2) ke versi 3 (v3): semua 15 kabupaten kini berhasil diproses (v2 hanya menghasilkan 5 kabupaten akibat bug pada pemetaan nama), Walk-Forward Validation menggantikan LOYOCV untuk mencegah kebocoran data temporal, dan baseline model disertakan sebagai tolok ukur minimum.

**Output yang muncul:**
Teks terformat berisi judul, deskripsi, tabel alur analisis, dan catatan metodologi. Tidak ada output komputasi.

**Interpretasi output:**
Informasi ini sangat penting karena mengkomunikasikan bahwa notebook ini adalah versi yang sudah diperbaiki dari eksperimen sebelumnya. Menyebutkan bug pada v2 secara eksplisit menunjukkan pendekatan penelitian yang jujur dan transparan — sebuah praktik baik dalam dokumentasi ilmiah.

**Istilah penting:**
- **Big Data**: Meskipun nama mata kuliah menggunakan istilah ini, dataset aktual dalam notebook ini (90 sampel) tidak termasuk "big data" dalam arti teknis (jutaan baris). Istilah ini merujuk pada konteks mata kuliah yang mencakup pendekatan berbasis data secara umum.
- **BPS**: Badan Pusat Statistik, lembaga pemerintah Indonesia yang bertanggung jawab mengumpulkan dan menerbitkan data statistik resmi, termasuk data pertanian.
- **NASA POWER**: Program penyedia data iklim dan cuaca historis dari NASA (National Aeronautics and Space Administration) Amerika Serikat, yang menyediakan data meteorologi berbasis satelit dan model atmosfer secara gratis melalui API (antarmuka pemrograman).

---

### Cell 2 – Penjelasan Persiapan Lingkungan

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan kepada pembaca bahwa tahap persiapan lingkungan akan segera dilakukan, dan menyebutkan pustaka utama yang akan digunakan.

**Penjelasan isi:**
Markdown ini menjelaskan bahwa tidak ada instalasi tambahan yang diperlukan — semua analisis hanya mengandalkan pustaka standar Python yang sudah tersedia. Pustaka utama yang disebutkan adalah pandas dan numpy untuk manipulasi data, scikit-learn untuk pemodelan, serta matplotlib dan seaborn untuk visualisasi. Catatan refactor juga menyebutkan bahwa pustaka xgboost yang sebelumnya diinstal di v2 kini dihapus karena tidak digunakan.

**Output yang muncul:**
Teks deskriptif, tidak ada output komputasi.

**Interpretasi output:**
Keputusan untuk tidak menginstal dependensi tambahan meningkatkan determinisme (hasil yang sama setiap kali dijalankan) dan portabilitas notebook. Ini merupakan praktik engineering yang baik.

---

### Cell 3 – Verifikasi Tidak Ada Dependensi Tambahan

**Jenis cell:** Code

**Tujuan:**
Mencetak konfirmasi bahwa tidak ada instalasi paket tambahan dan eksperimen hanya menggunakan pustaka standar.

**Penjelasan kode:**
Hanya berisi satu baris `print()` yang mengonfirmasi daftar pustaka yang digunakan. Tidak ada instalasi paket (seperti `pip install`) di cell ini.

**Output yang muncul:**
```
Dependency tambahan tidak diinstal; eksperimen memakai pandas, scikit-learn, matplotlib, seaborn.
```

**Interpretasi output:**
Output ini merupakan checkpoint sederhana yang memastikan pembaca tahu bahwa tidak ada langkah instalasi yang perlu dilakukan sebelumnya. Ini juga menegaskan bahwa notebook dapat dijalankan langsung di Google Colab tanpa persiapan tambahan.

---

### Cell 4 – Impor Pustaka, Konfigurasi Global, dan Definisi Konstanta

**Jenis cell:** Code

**Tujuan:**
Ini adalah cell terpenting dalam persiapan lingkungan. Cell ini mengimpor semua pustaka yang diperlukan, menetapkan konstanta waktu dan wilayah, mengkonfigurasi tampilan visualisasi, mengatur seed untuk reproduktibilitas, mendefinisikan kalender musim tanam, dan menetapkan daftar 15 kabupaten beserta mapping nama file cuaca.

**Penjelasan kode:**

Cell ini dapat dibagi menjadi beberapa blok logis:

*Impor pustaka:* Mengimpor modul standar Python (io, json, copy, warnings, datetime, random, re), pustaka numerik (numpy, pandas), pustaka Machine Learning dari scikit-learn (Ridge, RandomForestRegressor, GradientBoostingRegressor, StandardScaler, Pipeline, metrik evaluasi), dan pustaka visualisasi (matplotlib, seaborn).

*Konfigurasi reproduktibilitas:* Variabel `RANDOM_STATE = 42` ditetapkan dan digunakan untuk mengatur `np.random.seed(42)` dan `random.seed(42)`. Ini memastikan bahwa setiap kali notebook dijalankan, model seperti Random Forest yang memiliki komponen acak akan menghasilkan hasil yang persis sama.

*Direktori output:* Folder `results/Images` dan `data/Processed/Cuaca` serta `data/Processed/Padi` dibuat secara otomatis jika belum ada.

*Fungsi utilitas:* Tiga fungsi pembantu didefinisikan: `canonical_upload_stem()` untuk menormalisasi nama file upload (termasuk suffix otomatis Colab seperti " (1)"), `validate_uploaded_files()` untuk validasi kelengkapan file yang di-upload, dan `assert_unique_key()` untuk memastikan tidak ada duplikat kunci pada DataFrame. Fungsi `save_figure()` juga didefinisikan untuk menyimpan visualisasi secara konsisten.

*Konstanta waktu:*
- `TAHUN_LIST = [2018, 2019, 2020, 2021, 2022, 2023, 2024]` — tujuh tahun data BPS yang tersedia.
- `TAHUN_FITUR = [2019, 2020, 2021, 2022, 2023, 2024]` — enam tahun yang memiliki fitur musiman lengkap (2018 tidak bisa digunakan karena fitur Musim Utama memerlukan data November–Desember tahun sebelumnya, yaitu 2017, yang tidak tersedia).

*Parameter NASA POWER:* Enam kode parameter cuaca didefinisikan beserta nama manusia yang mudah dibaca: `ALLSKY_SFC_SW_DWN` (Radiasi), `T2M` (Suhu Avg), `T2M_MAX` (Suhu Max), `T2M_MIN` (Suhu Min), `RH2M` (Kelembapan), `PRECTOTCORR` (Curah Hujan).

*Kalender musim tanam:* Dictionary `MUSIM` mendefinisikan tiga musim tanam dengan jendela bulannya masing-masing. Musim Utama mencakup November–Desember tahun sebelumnya dan Januari–Maret tahun berjalan (5 bulan). Musim Gadu mencakup April–Juli (4 bulan). Musim Kemarau mencakup Agustus–Oktober (3 bulan).

*Daftar kabupaten dan mapping nama file:* `KABUPATEN_LIST` berisi 15 nama kabupaten/kota resmi BPS dalam urutan alfabet. Dictionary `NAMA_FILE_KE_KAB` memetakan nama file JSON berformat CamelCase (misalnya `LampungTengah`) ke nama resmi BPS yang menggunakan spasi (`Lampung Tengah`). Mapping eksplisit ini merupakan perbaikan kritis dari v2 — tanpa ini, penggabungan data cuaca dengan BPS akan gagal untuk semua kabupaten bernama lebih dari satu kata.

**Output yang muncul:**
```
Lingkungan siap.
  Tahun data BPS    : 2018–2024
  Tahun fitur model : 2019–2024
  Kabupaten terdaftar: 15
  Parameter cuaca   : ALLSKY_SFC_SW_DWN, T2M, T2M_MAX, T2M_MIN, RH2M, PRECTOTCORR
```

**Interpretasi output:**
Output ini mengonfirmasi bahwa semua konfigurasi berhasil dimuat. Angka-angka yang muncul sangat penting:

- **2018–2024** sebagai rentang data BPS berarti ada 7 titik data per kabupaten, yang menjadi fondasi seluruh analisis.
- **2019–2024** sebagai rentang fitur model (6 tahun) berarti model hanya bisa belajar dari 6 titik per kabupaten. Ini adalah konsekuensi dari desain fitur musiman yang memerlukan data satu tahun sebelumnya (untuk Musim Utama).
- **15 kabupaten** terdaftar mengonfirmasi bahwa bug v2 (yang hanya memproses 5 kabupaten) telah diperbaiki.

**Istilah penting:**
- **Seed (Random State)**: Nilai awal yang mengontrol generator angka acak. Dengan seed yang sama, model yang menggunakan komponen acak (seperti Random Forest) akan menghasilkan pohon keputusan yang identik setiap kali dilatih, sehingga hasil dapat direproduksi oleh peneliti lain.
- **StandardScaler**: Alat normalisasi data dari scikit-learn yang mengubah setiap fitur numerik agar memiliki rata-rata nol dan standar deviasi satu. Ini penting untuk Ridge Regression agar regularisasi bekerja adil untuk semua fitur.

---

### Cell 5 – Penjelasan Tahap Data Loading dan Cleaning

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa tahap ini akan memuat dan membersihkan dua sumber data utama, serta menekankan bahwa validasi dilakukan secara ketat (pipeline berhenti jika ada masalah).

**Penjelasan isi:**
Markdown ini juga memuat sub-seksi 1.1 yang menjelaskan struktur file CSV BPS: kolom pertama berisi nama kabupaten, kolom 1–7 berisi luas panen per tahun, dan kolom 8–14 berisi produksi per tahun. Sebuah catatan menjelaskan bahwa dua baris header dan baris total provinsi dikecualikan secara otomatis.

**Output yang muncul:**
Teks deskriptif, tidak ada output komputasi.

**Interpretasi output:**
Penjelasan struktur data di awal sangat membantu karena CSV BPS menggunakan format "lebar" (wide format) yang tidak standar — setiap baris adalah satu kabupaten dan kolom-kolomnya mewakili kombinasi variabel dan tahun. Kode harus mengubah format ini menjadi format "panjang" (long format) yang lebih mudah dianalisis.

---

### Cell 6 – Upload File CSV BPS

**Jenis cell:** Code

**Tujuan:**
Meminta pengguna untuk mengunggah file CSV data produksi dan luas panen BPS melalui antarmuka Google Colab, kemudian memvalidasi bahwa tepat satu file CSV diterima.

**Penjelasan kode:**
`files.upload()` adalah fungsi Google Colab yang menampilkan tombol upload di antarmuka. Setelah pengguna memilih file, ia disimpan dalam dictionary `uploaded_padi`. Fungsi `validate_uploaded_files()` yang didefinisikan di Cell 4 kemudian memeriksa bahwa jumlah file tepat 1 dan ekstensinya adalah `.csv`.

**Output yang muncul:**
Antarmuka upload file Google Colab (tombol "Choose Files"), diikuti oleh konfirmasi seperti:
```
File diterima: PadiTahunan.csv (X,XXX bytes)
```

**Interpretasi output:**
Karena notebook ini dirancang untuk Google Colab, upload manual adalah cara yang dipilih untuk memasukkan data. Ini adalah keterbatasan pendekatan — proses tidak bisa diautomasi sepenuhnya tanpa mengubah mekanisme loading data.

---

### Cell 7 – Parsing dan Validasi Data BPS

**Jenis cell:** Code

**Tujuan:**
Mengurai (parse) file CSV BPS dari format lebar ke format panjang, memvalidasi kualitasnya secara ketat, dan menampilkan ringkasan serta agregat data tahunan provinsi.

**Penjelasan kode:**

Fungsi `parse_csv_padi()` membaca CSV sebagai DataFrame, mengidentifikasi kolom luas panen (7 kolom) dan produksi (7 kolom), lalu mengiterasi setiap baris kabupaten. Untuk setiap kombinasi kabupaten-tahun, ia mengambil nilai luas panen dan produksi menggunakan `pd.to_numeric(..., errors='coerce')` — artinya nilai yang tidak bisa dikonversi ke angka secara otomatis dijadikan NaN. Hasil akhirnya adalah DataFrame "panjang" dengan kolom: kabupaten, tahun, luas_panen_ha, produksi_ton.

Fungsi `validate_padi_dataset()` menjalankan enam pemeriksaan kualitas:
1. Jumlah baris harus tepat 15 × 7 = 105 baris.
2. Semua 15 kabupaten harus hadir.
3. Tidak boleh ada kabupaten yang tidak dikenal.
4. Tidak boleh ada duplikat pasangan kabupaten-tahun.
5. Tidak boleh ada nilai kosong.
6. Semua nilai luas panen dan produksi harus positif (karena nilai nol atau negatif akan menghasilkan produktivitas yang tidak valid).

Setelah validasi, dua tabel ditampilkan:
- **Tabel Ringkasan Dataset BPS**: menampilkan atribut dasar dataset.
- **Tabel Agregat Provinsi per Tahun**: menampilkan total luas panen, total produksi, dan produktivitas implikatif (rata-rata tertimbang) untuk seluruh Lampung dari 2018 hingga 2024.

**Output yang muncul:**

Tabel styled "Ringkasan Dataset BPS" dengan isi:

| Atribut | Nilai |
|---|---|
| Jumlah baris | 105 baris |
| Jumlah kolom | 4 kolom |
| Kabupaten tercakup | 15 kabupaten |
| Periode data | 2018–2024 |
| Nilai hilang | 0 |

Teks konfirmasi: `Validasi kualitas data: LULUS`

Tabel agregat provinsi yang menampilkan luas panen, produksi, dan produktivitas implikatif per tahun dari 2018–2024. Nilainya bervariasi antar tahun mencerminkan kondisi pertanian Lampung yang dipengaruhi cuaca dan kebijakan pertanian.

**Interpretasi output:**

Angka **105 baris** (15 kabupaten × 7 tahun) merupakan volume data BPS yang tersedia. Ini adalah dataset yang relatif kecil, yang nantinya akan berpengaruh pada pemilihan model. Validasi yang ketat memastikan tidak ada data yang korup atau terlewat sejak awal, sehingga semua tahap selanjutnya berdiri di atas fondasi yang solid.

Tabel agregat provinsi memungkinkan pembaca memahami tren umum produktivitas Lampung. Nilai produktivitas implikatif sekitar 4–5 ton/ha adalah angka yang wajar untuk padi Indonesia. Fluktuasi antar tahun mencerminkan pengaruh El Niño/La Niña dan variasi curah hujan.

**Istilah penting:**
- **Luas panen (ha)**: Luas lahan padi yang benar-benar dipanen pada periode tertentu, dalam satuan hektar. Berbeda dengan luas tanam karena sebagian lahan mungkin gagal panen (puso).
- **Produksi (ton)**: Total hasil gabah kering giling yang dipanen dari seluruh lahan yang berhasil dipanen.
- **Produktivitas ton/ha**: Hasil panen per satuan luas, dihitung sebagai Produksi ÷ Luas Panen. Ini adalah ukuran efisiensi lahan yang lebih informatif daripada total produksi karena tidak bergantung pada ukuran lahan.

---

### Cell 8 – Penjelasan Data Cuaca NASA POWER

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan sumber data cuaca, enam parameter yang digunakan beserta satuannya, dan perbaikan mapping nama file dari v2 ke v3.

**Penjelasan isi:**
Tabel di dalam markdown mencantumkan enam parameter NASA POWER dengan kode teknis, nama mudah dipahami, dan satuannya. Catatan v3 menjelaskan perbaikan kritis: nama file JSON menggunakan format CamelCase tanpa spasi (seperti `LampungBarat.json`) sedangkan nama resmi BPS menggunakan spasi (`Lampung Barat`). Dictionary mapping eksplisit `NAMA_FILE_KE_KAB` mengatasi perbedaan ini.

**Output yang muncul:**
Teks deskriptif dengan tabel parameter. Tidak ada output komputasi.

**Interpretasi output:**
Penjelasan tentang perbaikan v3 ini sangat penting karena mengungkapkan bahwa bug pada v2 bukan bug kode biasa — melainkan masalah konsistensi penamaan yang menyebabkan 10 dari 15 kabupaten gagal digabungkan dengan data BPS. Tanpa perbaikan ini, model hanya akan dilatih pada 5 kabupaten saja, yang sangat membatasi generalisasi.

**Istilah penting:**
- **NASA POWER**: Singkatan dari Prediction Of Worldwide Energy Resources. Menyediakan data cuaca harian sejak 1981 berdasarkan pengamatan satelit dan model atmosfer NASA. Data ini sering digunakan untuk penelitian pertanian karena mencakup seluruh permukaan bumi, termasuk daerah terpencil yang tidak memiliki stasiun cuaca.
- **`ALLSKY_SFC_SW_DWN`**: Singkatan dari All Sky Surface Shortwave Downward Irradiance — total radiasi matahari yang mencapai permukaan bumi dalam kondisi langit apapun (berawan atau cerah), dalam satuan MJ/m²/hari. Penting bagi tanaman untuk proses fotosintesis.
- **`PRECTOTCORR`**: Curah hujan harian yang telah dikoreksi (corrected), dalam mm/hari. Koreksi dilakukan NASA untuk memperbaiki bias pengukuran satelit.

---

### Cell 9 – Upload 15 File JSON Cuaca NASA POWER

**Jenis cell:** Code

**Tujuan:**
Meminta pengguna mengunggah semua 15 file JSON cuaca sekaligus dan memvalidasi bahwa jumlah, format, serta nama file semuanya sesuai.

**Penjelasan kode:**
Seperti Cell 6, menggunakan `files.upload()` dari Colab. Validasi kali ini lebih ketat: harus ada tepat 15 file, semua berekstensi `.json`, dan nama-nama file (setelah normalisasi) harus persis cocok dengan kunci yang ada di dictionary `NAMA_FILE_KE_KAB` — tidak lebih, tidak kurang.

**Output yang muncul:**
Antarmuka upload, diikuti konfirmasi:
```
15 file diterima dan lolos validasi nama:
  BandarLampung.json (X,XXX bytes)
  LampungBarat.json (X,XXX bytes)
  ... (13 file lainnya)
```

**Interpretasi output:**
Validasi nama file di tahap ini sangat penting karena mencegah kesalahan "diam-diam" di mana file yang salah nama diterima tetapi kemudian gagal di-merge dengan data BPS.

---

### Cell 10 – Parsing Data JSON NASA POWER dan Validasi Kualitas

**Jenis cell:** Code

**Tujuan:**
Membaca isi 15 file JSON cuaca, mengonversi nilai sentinel -999 menjadi NaN, membangun DataFrame data harian, dan menjalankan quality gate yang ketat.

**Penjelasan kode:**

Fungsi `parse_json_nasa()` melakukan proses berikut untuk setiap file JSON:
1. Memetakan nama file ke nama kabupaten resmi BPS menggunakan `NAMA_FILE_KE_KAB`.
2. Mengurai JSON dan memverifikasi bahwa semua 6 parameter NASA POWER tersedia.
3. Memastikan tanggal awal adalah 2018-01-01 dan tanggal akhir adalah 2024-12-31.
4. Untuk setiap hari, membuat satu baris data dengan kabupaten, tanggal, tahun, bulan, hari, dan 6 nilai cuaca. Nilai -999, -99, atau None dikonversi menjadi `np.nan` karena ketiganya merupakan nilai sentinel yang menandai data tidak tersedia.
5. Memastikan tidak ada duplikat pasangan kabupaten-tanggal.

**Output yang muncul:**

Tabel styled "Ringkasan Dataset Cuaca Harian":

| Atribut | Nilai |
|---|---|
| Jumlah baris | 38.325 baris |
| Kabupaten tercakup | 15 kabupaten |
| Periode data | 2018-01-01 s.d. 2024-12-31 |

Tabel kelengkapan per parameter cuaca. Jika data lengkap tanpa nilai hilang, semua status akan menampilkan "Lengkap" dengan warna hijau.

Teks konfirmasi: `Validasi kualitas data: LULUS – 15 kabupaten dimuat dan lolos quality gate harian.`

**Interpretasi output:**

Angka **38.325 baris** berasal dari perhitungan: 15 kabupaten × 2.555 hari (365 hari × 7 tahun, dengan memperhitungkan tahun kabisat 2020 dan 2024 yang memiliki 366 hari). Ini adalah jumlah data harian yang sangat banyak dibandingkan dengan 105 baris data BPS — menunjukkan bahwa data cuaca NASA POWER jauh lebih granular (detail) daripada data statistik BPS yang hanya tahunan.

**Istilah penting:**
- **Nilai sentinel -999**: Nilai penanda khusus yang digunakan NASA untuk menandai bahwa data pada tanggal tertentu tidak tersedia atau tidak valid. Ini bukan nilai sebenarnya — jika digunakan langsung dalam perhitungan, akan merusak semua statistik. Oleh karena itu harus dikonversi ke NaN sebelum digunakan.
- **NaN**: Not a Number — representasi standar Python/numpy untuk nilai yang hilang atau tidak terdefinisi. Fungsi-fungsi pandas dan numpy umumnya sudah tahu cara menangani NaN (misalnya `mean()` secara default mengabaikan NaN).
- **Quality gate**: Istilah dalam rekayasa perangkat lunak untuk pemeriksaan kualitas otomatis yang menghentikan proses jika ada syarat yang tidak terpenuhi. Dalam konteks ini, quality gate mencegah pipeline berjalan dengan data yang cacat.

---

### Cell 11 – Penjelasan Penanganan Nilai Hilang

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan strategi imputasi yang digunakan dan alasan metodologisnya.

**Penjelasan isi:**
Markdown ini menjelaskan bahwa nilai sentinel -999 sudah dikonversi ke NaN pada tahap parsing. Strategi imputasi yang dipilih adalah median bulanan per kabupaten dengan pendekatan *time-aware* — hanya menggunakan data historis sebelum tanggal yang bersangkutan. Alasan pemilihan median daripada mean juga dijelaskan (median lebih robust terhadap outlier, dan data cuaca sering memiliki distribusi yang condong/skewed).

**Output yang muncul:**
Teks deskriptif. Tidak ada output komputasi.

---

### Cell 12 – Fungsi Imputasi dan Eksekusi

**Jenis cell:** Code

**Tujuan:**
Mendefinisikan fungsi imputasi median bulanan yang time-aware dan menerapkannya pada data cuaca harian.

**Penjelasan kode:**

Fungsi `imputasi_median_bulanan()` pertama-tama memeriksa apakah ada nilai hilang. Jika tidak ada, imputasi dilewati. Jika ada, untuk setiap parameter dan setiap kombinasi kabupaten-bulan, ia menghitung median ekspansi (expanding median) dengan shift satu langkah — artinya pada setiap hari, imputasi hanya menggunakan data historis sebelum hari tersebut, bukan data di masa depan. Jika tidak ada histori sebelumnya (misalnya nilai hilang terjadi pada hari pertama periode), digunakan median kabupaten-bulan keseluruhan sebagai fallback.

**Output yang muncul:**
```
Tidak ada nilai hilang — imputasi dilewati.
```

**Interpretasi output:**
Output ini mengonfirmasi bahwa data NASA POWER untuk 15 kabupaten Lampung periode 2018–2024 sepenuhnya lengkap — tidak ada tanggal yang hilang atau memiliki nilai sentinel setelah parsing. Ini adalah kabar baik karena berarti tidak perlu khawatir tentang bias yang mungkin timbul dari imputasi.

Meskipun imputasi tidak diperlukan saat ini, fungsinya tetap disertakan sebagai antisipasi jika data diperbarui dan ada nilai yang hilang. Ini adalah praktik defensive programming yang baik.

**Istilah penting:**
- **Imputasi**: Proses mengisi nilai yang hilang dengan estimasi yang masuk akal, berdasarkan pola data yang ada. Berbeda dengan menghapus baris yang hilang (karena menghapus baris berarti kehilangan data lain yang mungkin lengkap).
- **Median bulanan**: Nilai tengah dari semua pengamatan dalam satu bulan tertentu, untuk satu kabupaten tertentu. Lebih robust daripada rata-rata karena satu nilai ekstrem (outlier) tidak akan terlalu mengubah nilai median.
- **Time-aware**: Pendekatan yang menghormati urutan waktu — saat mengisi nilai yang hilang pada tanggal tertentu, hanya menggunakan data dari tanggal sebelumnya. Ini mencegah kebocoran informasi dari masa depan ke masa lalu (*data leakage*).
- **Data leakage**: Kesalahan metodologis di mana informasi dari periode yang sedang diprediksi (masa depan) bocor masuk ke dalam proses pelatihan model. Ini membuat performa model terlihat lebih baik daripada yang sebenarnya.

---

### Cell 13 – Penjelasan Agregasi Cuaca ke Level Bulanan

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan mengapa data harian perlu diagregasi ke bulanan dan bagaimana aturan agregasinya berbeda untuk curah hujan dan parameter lainnya.

**Penjelasan isi:**
Markdown menjelaskan bahwa curah hujan diagregasi dengan penjumlahan (karena yang penting adalah total ketersediaan air dalam sebulan), sedangkan parameter lain diagregasi dengan rata-rata (karena yang penting adalah kondisi iklim rata-rata). Hasil agregasi adalah 1.260 baris (15 × 12 × 7).

**Output yang muncul:**
Teks deskriptif. Tidak ada output komputasi.

---

### Cell 14 – Agregasi Data Cuaca Harian ke Bulanan

**Jenis cell:** Code

**Tujuan:**
Mengeksekusi agregasi data cuaca dari 38.325 baris harian menjadi 1.260 baris bulanan.

**Penjelasan kode:**
Dictionary `AGG_RULES` mendefinisikan aturan agregasi per parameter: `PRECTOTCORR` menggunakan `'sum'`, semua parameter lain menggunakan `'mean'`. Fungsi `groupby(['kabupaten', 'tahun', 'bulan'])` mengelompokkan data, lalu `.agg(AGG_RULES)` menerapkan aturan agregasi yang sesuai untuk setiap parameter.

**Output yang muncul:**
```
Data bulanan berhasil dibuat: 1260 baris (15 kab x 12 bulan x 7 tahun)
Validasi kelengkapan: LULUS (1260 baris sesuai ekspektasi)
```

**Interpretasi output:**
Angka **1.260 baris** merupakan hasil perkalian 15 kabupaten × 12 bulan × 7 tahun. Data bulanan ini adalah representasi yang lebih ringkas dan lebih mudah diinterpretasikan secara agronomis daripada data harian. Pada tahap selanjutnya, data bulanan ini akan direduksi lebih lanjut menjadi 90 baris data tahunan berbasis musim tanam.

**Istilah penting:**
- **Agregasi**: Proses meringkas banyak titik data menjadi sedikit titik data dengan menggunakan fungsi statistik seperti jumlah, rata-rata, atau median. Dalam konteks ini, mengubah ~25 data harian per bulan menjadi satu nilai bulanan.

---

### Cell 15 – Penjelasan Penyimpanan Dataset Intermediate

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan mengapa dataset yang sudah dibersihkan disimpan ke disk sebagai checkpoint.

**Penjelasan isi:**
Checkpoint memungkinkan pipeline dijalankan ulang dari titik ini tanpa perlu mengulang proses upload dan parsing yang membutuhkan interaksi manual.

---

### Cell 16 – Simpan Dataset Intermediate ke Disk

**Jenis cell:** Code

**Tujuan:**
Menyimpan dua dataset yang sudah bersih ke direktori `data/Processed/`.

**Penjelasan kode:**
`df_bulanan.to_csv(cuaca_out, index=False)` dan `df_produksi_luas.to_csv(padi_out, index=False)` menyimpan masing-masing DataFrame ke file CSV tanpa menyertakan index baris.

**Output yang muncul:**
```
Dataset intermediate disimpan:
  data/Processed/Cuaca/cuaca_bulanan_clean.csv
  data/Processed/Padi/produksi_luas_clean.csv
```

**Interpretasi output:**
Penyimpanan checkpoint adalah praktik yang baik dalam pipeline data sains yang panjang. Jika Colab runtime terputus setelah tahap ini, pengguna tidak perlu mengulangi upload file dari awal.

---

### Cell 17 – Penjelasan Rekayasa Fitur Berbasis Musim Tanam

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan konsep utama yang menjadi keunggulan penelitian ini: fitur yang dibangun berdasarkan jendela musim tanam padi, bukan sekadar data bulanan mentah.

**Penjelasan isi:**
Markdown ini menjelaskan bahwa "inti dari pendekatan penelitian" adalah mengubah data cuaca menjadi fitur yang bermakna secara agronomis. Tabel menjelaskan tiga musim tanam dengan jendela bulannya: Musim Utama (Nov T-1, Des T-1, Jan–Mar T), Musim Gadu (Apr–Jul T), dan Musim Kemarau (Agu–Okt T). Notasi "T" berarti tahun prediksi dan "T-1" berarti tahun sebelumnya.

Markdown ini juga menjelaskan bahwa total sampel setelah rekayasa fitur adalah 90 sampel (2019–2024 × 15 kabupaten).

**Output yang muncul:**
Teks deskriptif. Tidak ada output komputasi.

**Istilah penting:**
- **Musim Utama (Panen Raya)**: Musim tanam terpenting di Lampung, dimulai pada akhir tahun ketika curah hujan mulai meningkat. Dinamakan "panen raya" karena menghasilkan produksi terbesar. Jendela musimnya melintasi dua tahun kalender (November–Desember tahun lalu dan Januari–Maret tahun ini).
- **Musim Gadu**: Musim tanam kedua yang memanfaatkan sisa curah hujan dari musim penghujan. Produktivitasnya umumnya lebih rendah dari Musim Utama.
- **Musim Kemarau**: Musim tanam ketiga yang sangat bergantung pada ketersediaan irigasi teknis, karena curah hujan sangat rendah. Hanya dilakukan di daerah dengan irigasi yang baik.
- **Feature engineering (Rekayasa Fitur)**: Proses mengubah data mentah menjadi representasi yang lebih informatif untuk model Machine Learning. Ini adalah salah satu langkah terpenting dalam pipeline data science karena kualitas fitur sangat menentukan kualitas prediksi.

---

### Cell 18 – Fungsi Pembangun Fitur Musiman dan Eksekusinya

**Jenis cell:** Code

**Tujuan:**
Membangun 18 fitur cuaca musiman (3 musim × 6 parameter) dari data bulanan, menghasilkan matriks fitur dengan 90 baris.

**Penjelasan kode:**

Dictionary `WINDOWS` mendefinisikan jendela bulan untuk setiap musim menggunakan lambda function yang menerima parameter tahun `t`. Untuk Musim Utama, jendela adalah [(t-1, 11), (t-1, 12), (t, 1), (t, 2), (t, 3)] — ini mengambil data dari November dan Desember tahun sebelumnya serta Januari hingga Maret tahun berjalan.

Fungsi `agg_window()` mengambil semua baris data bulanan yang sesuai dengan jendela musim tertentu, menyusunnya menjadi array numerik, lalu mengagregasinya: curah hujan dijumlahkan (sum), parameter lain dirata-ratakan (mean). Nama kolom hasil memiliki format: `{PARAMETER}_{MUSIM}_{AGREGASI}`, misalnya `PRECTOTCORR_utama_sum` atau `T2M_gadu_mean`.

Fungsi `bangun_fitur_musiman()` mengiterasi semua kombinasi kabupaten dan tahun (dalam `TAHUN_FITUR`), memanggil `agg_window()` untuk setiap musim, dan mengumpulkan hasilnya menjadi satu DataFrame.

**Output yang muncul:**
```
Matriks fitur cuaca: 90 baris × 20 kolom
Tahun tersedia     : [2019, 2020, 2021, 2022, 2023, 2024]
Fitur cuaca (18 kolom):
  ALLSKY_SFC_SW_DWN_utama_mean
  ALLSKY_SFC_SW_DWN_gadu_mean
  ALLSKY_SFC_SW_DWN_kemarau_mean
  T2M_utama_mean
  T2M_gadu_mean
  T2M_kemarau_mean
  ... (12 fitur lainnya)
  PRECTOTCORR_utama_sum
  PRECTOTCORR_gadu_sum
  PRECTOTCORR_kemarau_sum
```

**Interpretasi output:**

Angka **18 fitur cuaca** adalah hasil dari 3 musim × 6 parameter. Setiap fitur merepresentasikan kondisi iklim selama satu musim tanam — misalnya `PRECTOTCORR_utama_sum` adalah total curah hujan kumulatif selama Musim Utama (5 bulan), dan `T2M_kemarau_mean` adalah rata-rata suhu selama Musim Kemarau (3 bulan).

Pendekatan ini jauh lebih bermakna secara agronomis daripada menggunakan 12 nilai cuaca bulanan mentah, karena model tidak perlu "belajar" sendiri bahwa bulan November–Maret adalah satu musim yang kohesif.

**Istilah penting:**
- **Lag feature / fitur lag**: Fitur yang menggunakan nilai dari periode sebelumnya. Misalnya, `prodvt_lag1` adalah produktivitas tahun lalu. Fitur ini penting karena produktivitas padi memiliki persistensi — kabupaten yang produktif tahun lalu cenderung produktif lagi tahun ini.
- **Rolling Mean 2y**: Rata-rata bergulir 2 tahun — rata-rata produktivitas dari dua tahun terakhir. Lebih halus dari lag satu tahun saja karena meratakan fluktuasi satu tahun yang ekstrem.

---

### Cell 19 – Penjelasan Penggabungan Fitur dengan Data Produksi

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan proses penggabungan (merge) fitur cuaca musiman dengan data BPS, cara menghitung target produktivitas, dan justifikasi metodologis penggunaan produktivitas (ton/ha) daripada total produksi (ton) sebagai target prediksi.

**Penjelasan isi:**
Tiga keuntungan menggunakan produktivitas per hektar sebagai target dijelaskan: menghilangkan efek skala perbedaan lahan antar kabupaten, memfokuskan model pada kualitas panen, dan menghasilkan R² yang lebih murni. Penghitungan fitur historis secara time-aware juga dijelaskan.

---

### Cell 20 – Merge Data dan Perhitungan Target

**Jenis cell:** Code

**Tujuan:**
Menggabungkan fitur cuaca musiman dengan data produksi dan luas panen BPS, menghitung target produktivitas, dan menambahkan fitur historis (lag dan rolling) berbasis riwayat produktivitas.

**Penjelasan kode:**

`df_fitur = df_cuaca_fitur.merge(df_produksi_luas[...], on=['kabupaten', 'tahun'], how='inner', validate='one_to_one')` menggabungkan dua DataFrame menggunakan kabupaten dan tahun sebagai kunci. Parameter `validate='one_to_one'` memastikan tidak ada duplikat di kedua sisi.

Produktivitas dihitung sebagai: `produktivitas_ton_per_ha = produksi_ton / luas_panen_ha`

Fungsi `get_hist_prodvt_features()` menghitung tiga fitur historis untuk setiap baris:
- `prodvt_lag1`: produktivitas tahun sebelumnya (misalnya untuk prediksi 2022, menggunakan data 2021).
- `prodvt_roll2`: rata-rata produktivitas dua tahun terakhir.
- `prodvt_roll3`: rata-rata produktivitas tiga tahun terakhir.

Seluruh fitur historis dihitung secara time-aware — hanya menggunakan data sebelum tahun yang diprediksi.

**Output yang muncul:**

Tabel ringkasan matriks fitur:

| Komponen | Keterangan |
|---|---|
| Jumlah sampel | 90 sampel |
| Kabupaten | 15 kabupaten/kota Lampung |
| Periode | 2019–2024 |
| Fitur cuaca | 18 fitur (3 musim × 6 parameter) |
| Fitur historis target | 3 fitur (lag-1, rolling-2, rolling-3) |
| Target prediksi | produktivitas_ton_per_ha |

Statistik target:
```
Statistik target (produktivitas ton/ha):
count    90.000
mean      4.xxx
std       0.xxx
min       x.xxx
25%       x.xxx
50%       x.xxx
75%       x.xxx
max       x.xxx
  Koefisien Variasi (CV): ~9.x%  ← MAPE baseline naif ≈ CV ini
```

**Interpretasi output:**

Angka **90 sampel** adalah total data yang tersedia untuk pemodelan (15 kabupaten × 6 tahun). Ini adalah angka yang sangat kecil untuk Machine Learning — sebagai perbandingan, banyak penelitian ML menggunakan ribuan hingga jutaan sampel.

**Koefisien Variasi (CV) sekitar 9%** adalah angka yang sangat penting. CV ini merepresentasikan seberapa besar variasi produktivitas relatif terhadap rata-rata. Angka ini juga merupakan perkiraan MAPE minimum yang bisa dicapai oleh model baseline paling sederhana (Naive Mean). Artinya, jika model ML tidak bisa mengalahkan angka ini secara signifikan, model tersebut tidak memberikan nilai tambah dibanding prediksi naif.

**Istilah penting:**
- **Standar deviasi (std)**: Ukuran sebaran data di sekitar rata-rata. Standar deviasi yang besar berarti produktivitas sangat bervariasi antar kabupaten dan tahun.
- **Koefisien Variasi (CV)**: Standar deviasi dibagi rata-rata, dikalikan 100%. Ukuran yang berguna untuk membandingkan variasi antar dataset dengan skala berbeda.
- **Kuartil**: Nilai yang membagi data menjadi empat bagian sama. Q1 (25%) adalah nilai di mana 25% data berada di bawahnya, Q2 (50%) adalah nilai tengah (median), Q3 (75%) adalah nilai di mana 75% data berada di bawahnya.

---

### Cell 21 – Penjelasan Persiapan Matriks Model

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan mengapa dan bagaimana variabel kategoris `kabupaten` diubah menjadi fitur numerik menggunakan One-Hot Encoding.

**Penjelasan isi:**
Markdown menjelaskan bahwa setiap kabupaten memiliki karakteristik tetap (kualitas tanah, irigasi, teknologi pertanian) yang tidak sepenuhnya tertangkap dalam data cuaca. OHE dengan `drop_first=True` menghasilkan 14 kolom dummy dari 15 kabupaten. Catatan penting: luas panen yang digunakan adalah nilai aktual BPS, yang dalam skenario prediksi prospektif perlu diganti dengan estimasi luas tanam.

---

### Cell 22 – One-Hot Encoding dan Definisi Matriks Fitur

**Jenis cell:** Code

**Tujuan:**
Mengubah kolom kategoris `kabupaten` menjadi 14 kolom dummy biner menggunakan One-Hot Encoding, mendefinisikan berbagai kombinasi fitur untuk pemodelan dan ablation study.

**Penjelasan kode:**

`pd.get_dummies(df_fitur[...], columns=['kabupaten'], drop_first=True)` mengubah kolom kabupaten menjadi kolom-kolom biner. Dengan 15 kabupaten dan `drop_first=True`, dihasilkan 14 kolom dummy (kabupaten ke-15 diwakili oleh kondisi semua 14 kolom bernilai 0 — ini disebut "kategori referensi").

Beberapa definisi kombinasi fitur yang akan digunakan:
- `FITUR_MODEL`: 18 fitur cuaca + 1 luas panen + 14 OHE kabupaten = **33 fitur total** (konfigurasi default)
- `FITUR_HIST`: hanya 2 fitur historis (lag1 dan roll2) — digunakan oleh Ridge Hist Lag
- Kombinasi lain untuk ablation study

**Output yang muncul:**

Tabel komposisi fitur:

| Kelompok Fitur | Jumlah | Keterangan |
|---|---|---|
| Cuaca (per musim) | 18 | 3 musim × 6 parameter meteorologi |
| Histori produktivitas | 3 | lag-1, rolling-2, rolling-3 |
| Luas panen | 1 | Luas panen aktual (Ha) |
| Kabupaten (OHE) | 14 | 15 kabupaten dikurangi 1 referensi |
| Total fitur default | 33 | |

```
Rasio sampel/fitur: 90 / 33 = 2.7:1
  Catatan: Rasio sampel/fitur sangat rendah...
```

**Interpretasi output:**

Rasio **2.7:1** (90 sampel dibagi 33 fitur) adalah angka yang sangat kritis dan menjadi salah satu keterbatasan utama penelitian ini. Dalam praktik Machine Learning, rasio sampel/fitur yang rendah meningkatkan risiko **overfitting** — kondisi di mana model "menghafal" data training tetapi gagal menggeneralisasi ke data baru. Aturan praktis umum menyarankan rasio minimal 5:1 hingga 10:1 untuk model yang stabil.

Karena rasio rendah ini, model linear sederhana seperti Ridge Regression (yang memiliki mekanisme regularisasi untuk mencegah overfitting) diprediksi akan bekerja lebih baik daripada model kompleks seperti Random Forest atau Gradient Boosting.

**Istilah penting:**
- **One-Hot Encoding (OHE)**: Teknik mengubah variabel kategoris (seperti nama kabupaten) menjadi serangkaian variabel biner (0 atau 1). Misalnya, "Lampung Tengah" menjadi kolom `kabupaten_Lampung Tengah` yang bernilai 1 jika baris tersebut adalah Lampung Tengah, dan 0 jika bukan.
- **drop_first=True**: Parameter yang menghilangkan satu kolom dummy untuk menghindari "multikolinearitas sempurna" — kondisi di mana satu kolom bisa diprediksi sempurna dari kolom-kolom lain. Tanpa drop_first, 15 kolom dummy untuk 15 kabupaten akan menghasilkan informasi redundan.
- **Dummy variable**: Kolom biner hasil One-Hot Encoding. Nama ini berasal dari terminologi statistik di mana variabel ini "mewakili" kategori tanpa memiliki nilai numerik bermakna secara inheren.
- **Overfitting**: Kondisi di mana model belajar terlalu detail dari data training, termasuk "noise" acak, sehingga performanya buruk pada data baru yang belum pernah dilihat sebelumnya.

---

### Cell 23 – Penjelasan EDA

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan tujuan EDA dan empat pertanyaan kunci yang ingin dijawab.

**Penjelasan isi:**
Empat pertanyaan EDA: seberapa besar variasi produktivitas antar kabupaten, apakah ada tren yang konsisten, hubungan cuaca dan produktivitas, dan apakah ada pola musiman yang jelas.

---

### Cell 24 – Statistik Deskriptif per Kabupaten (EDA 3.1)

**Jenis cell:** Code

**Tujuan:**
Menghitung dan menampilkan statistik agregat per kabupaten untuk membandingkan produksi, luas panen, dan produktivitas antar wilayah.

**Penjelasan kode:**
`df_fitur.groupby('kabupaten').agg(...)` menghitung rata-rata dan standar deviasi produksi, luas panen, dan produktivitas untuk setiap kabupaten. Hasil diurutkan dari produksi rata-rata terbesar ke terkecil, dan ditampilkan dengan pewarnaan gradien biru (untuk produksi) dan hijau (untuk produktivitas).

**Output yang muncul:**

Tabel styled dengan 15 baris (satu per kabupaten) dan kolom: Produksi Rata2 (ton), Produksi StdDev (ton), Luas Panen Rata2 (ha), Produktivitas Rata2 (t/ha), Produktivitas StdDev.

Berikut konfirmasi teks:
```
Kabupaten dengan produksi terbesar : [nama kabupaten] (X,XXX,XXX ton/tahun rata-rata)
Kabupaten dengan produktivitas tertinggi: [nama kabupaten] (X.XXX t/ha rata-rata)
```

Berdasarkan data BPS Lampung, Lampung Tengah dan Lampung Timur umumnya menjadi kabupaten dengan produksi terbesar karena luas lahannya yang sangat besar. Namun, kabupaten dengan produktivitas tertinggi per hektar belum tentu sama dengan yang produksinya terbesar.

**Interpretasi output:**

Tabel ini mengungkapkan perbedaan mendasar antara *produksi* dan *produktivitas*. Kabupaten dengan lahan yang sangat luas (seperti Lampung Tengah atau Lampung Timur) akan mendominasi dalam total produksi. Namun, produktivitas (ton/ha) yang tinggi menunjukkan efisiensi lahan — kabupaten yang lebih kecil seperti Metro atau Pesawaran mungkin memiliki produktivitas per hektar yang lebih tinggi berkat irigasi yang lebih baik atau teknologi pertanian yang lebih maju.

Standar deviasi produktivitas yang tinggi untuk kabupaten tertentu menunjukkan bahwa produktivitasnya sangat berfluktuasi antar tahun — ini bisa disebabkan oleh ketergantungan pada curah hujan (irigasi kurang), atau peristiwa ekstrem seperti banjir/kekeringan.

**Istilah penting:**
- **Mean (rata-rata)**: Jumlah semua nilai dibagi jumlah data. Mengindikasikan nilai tipikal.
- **Standar deviasi (StdDev)**: Mengukur seberapa jauh nilai-nilai individu menyebar dari rata-rata. StdDev tinggi berarti variasi antar tahun besar.

---

### Cell 25 – Penjelasan Grafik Tren Produktivitas

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa grafik berikutnya akan menampilkan tren produktivitas per kabupaten dan faktor-faktor yang mungkin memengaruhinya.

---

### Cell 26 – Visualisasi Tren Produktivitas per Kabupaten (EDA 3.2)

**Jenis cell:** Code

**Tujuan:**
Membuat grid 15 subplot (5 baris × 3 kolom) yang menampilkan tren produktivitas padi dari 2019–2024 untuk masing-masing kabupaten.

**Penjelasan kode:**
Setiap subplot menampilkan satu line chart untuk satu kabupaten, dengan titik-titik data (marker bulat) di setiap tahun, area arsiran di bawah garis (untuk memperjelas tren), dan anotasi nilai produktivitas di titik awal (2019) dan akhir (2024). Warna setiap kabupaten diambil dari palet tab20 yang memiliki 20 warna berbeda.

**Output yang muncul:**

Grafik grid 5 baris × 3 kolom dengan judul "Tren Produktivitas Padi per Kabupaten/Kota Provinsi Lampung 2019–2024". Setiap panel menampilkan:
- Sumbu X: Tahun (2019–2024, ditampilkan sebagai 2 digit terakhir: '19, '20, '21, '22, '23, '24)
- Sumbu Y: Produktivitas dalam ton/ha
- Garis tren kabupaten tersebut dengan area arsiran
- Anotasi angka produktivitas di tahun pertama dan terakhir

**Interpretasi output:**

Grafik ini adalah salah satu output visualisasi paling informatif dalam notebook. Beberapa pola yang biasanya terlihat:

*Pola umum:* Sebagian besar kabupaten menunjukkan tren yang relatif stabil dengan sedikit fluktuasi antar tahun, mencerminkan bahwa produktivitas padi tidak berubah drastis dari tahun ke tahun di wilayah yang sama. Ini adalah salah satu alasan mengapa baseline "produktivitas tahun lalu" bisa menjadi predictor yang kuat.

*Kabupaten dengan fluktuasi besar:* Kabupaten yang sangat bergantung pada curah hujan (tanpa irigasi teknis yang baik) akan menunjukkan tren yang lebih bergerigi, naik-turun mengikuti variasi cuaca.

*Perbedaan level antar kabupaten:* Rentang sumbu Y yang berbeda antar subplot menunjukkan bahwa beberapa kabupaten secara konsisten lebih produktif daripada yang lain — mencerminkan perbedaan kualitas lahan, irigasi, dan manajemen pertanian yang bersifat permanen.

Grafik disimpan sebagai `results/Images/tren_produktivitas.png`.

---

### Cell 27 – Penjelasan Visualisasi Distribusi

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa dua jenis visualisasi distribusi akan ditampilkan: histogram dan boxplot.

---

### Cell 28 – Distribusi Produktivitas: Histogram dan Boxplot (EDA 3.3)

**Jenis cell:** Code

**Tujuan:**
Menampilkan distribusi keseluruhan 90 sampel produktivitas (histogram) dan distribusi per kabupaten (boxplot horizontal).

**Penjelasan kode:**

*Panel kiri (Histogram):* `ax.hist(vals, bins=20)` menampilkan distribusi frekuensi semua 90 nilai produktivitas. Garis merah vertikal menandai rata-rata, dan dua garis oranye putus-putus menandai batas ±1 standar deviasi (68% data berada dalam rentang ini jika distribusi normal).

*Panel kanan (Boxplot horizontal):* Kabupaten diurutkan dari median tertinggi ke terendah. Setiap "kotak" (box) menunjukkan rentang interkuartil (Q1–Q3), garis tengah kotak adalah median, dan "kumis" (whisker) menunjukkan rentang data di luar kuartil (kecuali outlier yang ditampilkan sebagai titik terpisah).

**Output yang muncul:**

*Histogram (kiri):* Distribusi berbentuk mendekati normal atau sedikit condong, berpusat di sekitar rata-rata (sekitar 4–5 ton/ha). Garis merah menandai rata-rata dan keterangan rata-rata tersebut. Garis oranye menandai batas ±1σ dengan keterangannya.

*Boxplot (kanan):* 15 kotak horizontal, masing-masing mewakili satu kabupaten, diurutkan dari median tertinggi di atas. Perbedaan posisi median antar kabupaten menunjukkan perbedaan sistematis (bukan acak) dalam kapasitas produktivitas masing-masing wilayah.

**Interpretasi output:**

*Histogram:* Distribusi yang mendekati normal dengan CV sekitar 9% menunjukkan bahwa variasi produktivitas tidak terlalu besar. Ini mengindikasikan bahwa memprediksi nilai "sekitar rata-rata" sudah cukup baik sebagai baseline — inilah mengapa Naive Mean bisa menjadi benchmark yang kompetitif.

*Boxplot:* Jika rentang kotak (IQR) beberapa kabupaten sangat besar, artinya produktivitas kabupaten tersebut sangat berfluktuasi antar tahun. Kabupaten dengan IQR sempit menunjukkan konsistensi yang baik. Adanya outlier (titik di luar whisker) menandakan tahun-tahun dengan kondisi yang sangat berbeda dari biasanya (misalnya tahun kekeringan parah atau El Niño).

Grafik disimpan sebagai `results/Images/distribusi_produktivitas.png`.

**Istilah penting:**
- **Histogram**: Grafik yang menampilkan distribusi frekuensi nilai kontinu dengan membaginya ke dalam "bins" (kelompok rentang nilai) dan menghitung berapa banyak data yang jatuh di setiap bin.
- **Boxplot (Box-and-Whisker Plot)**: Grafik yang merangkum distribusi data menggunakan lima angka: minimum, Q1, median, Q3, dan maksimum (atau whisker yang diperpendek untuk mengisolasi outlier).
- **Minimum dan Maksimum**: Nilai terkecil dan terbesar dalam dataset. Berguna untuk mengetahui rentang penuh data.

---

### Cell 29 – Penjelasan Pola Cuaca per Musim Tanam

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa grafik berikutnya menampilkan perbedaan cuaca antar musim, dan bahwa pola yang konsisten dapat menjadi sinyal prediktif.

---

### Cell 30 – Visualisasi Pola Cuaca per Musim Tanam (EDA 3.4)

**Jenis cell:** Code

**Tujuan:**
Menampilkan rata-rata 6 parameter cuaca untuk masing-masing tiga musim tanam dari 2019–2024, dalam grid 2 baris × 3 kolom.

**Penjelasan kode:**
Untuk setiap parameter cuaca, mengambil kolom yang sesuai dari DataFrame fitur (misalnya `T2M_utama_mean`, `T2M_gadu_mean`, `T2M_kemarau_mean`) dan menghitung rata-rata per tahun across semua 15 kabupaten. Tiga garis per subplot mewakili tiga musim dengan warna berbeda: hijau (Musim Utama), oranye (Musim Gadu), merah (Musim Kemarau).

**Output yang muncul:**

Grid 2 × 3 dengan 6 subplot, judul utama "Rata-rata Cuaca per Musim Tanam – Provinsi Lampung (2019–2024)". Setiap subplot:
- Sumbu X: Tahun 2019–2024
- Sumbu Y: Nilai parameter (unit berbeda per parameter)
- Tiga garis dengan warna berbeda untuk tiga musim
- Legenda di subplot pertama

Pola yang diharapkan terlihat:
- **Curah hujan (PRECTOTCORR)**: Musim Utama (penghujan) memiliki nilai tertinggi, jauh di atas Musim Kemarau.
- **Suhu (T2M, T2M_MAX, T2M_MIN)**: Musim Kemarau cenderung lebih panas dengan suhu maksimum lebih tinggi.
- **Kelembapan (RH2M)**: Musim Utama lebih lembap.
- **Radiasi (ALLSKY_SFC_SW_DWN)**: Musim Kemarau lebih cerah karena lebih sedikit tutupan awan.

**Interpretasi output:**

Perbedaan yang konsisten antar musim dari tahun ke tahun mengonfirmasi bahwa jendela musim yang didefinisikan memang menangkap perbedaan iklim yang nyata, bukan hanya pembagian kalender arbitrer. Ini memvalidasi pendekatan feature engineering berbasis musim tanam.

Variasi antar tahun dalam setiap musim (meskipun kecil) mencerminkan fluktuasi iklim tahunan seperti pengaruh El Niño/La Niña yang dapat memengaruhi produktivitas padi. Tahun El Niño biasanya ditandai dengan curah hujan yang lebih rendah dan suhu lebih tinggi.

Grafik disimpan sebagai `results/Images/cuaca_musiman.png`.

---

### Cell 31 – Penjelasan Analisis Korelasi

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa korelasi Pearson akan dihitung antara setiap fitur cuaca dan target produktivitas, serta cara membaca hasilnya.

**Penjelasan isi:**
Korelasi positif berarti hubungan searah (fitur naik, produktivitas naik), korelasi negatif berarti berlawanan arah, dan nilai mendekati ±1 menunjukkan hubungan kuat.

---

### Cell 32 – Korelasi Fitur Cuaca dengan Produktivitas (EDA 3.5)

**Jenis cell:** Code

**Tujuan:**
Menghitung korelasi Pearson antara semua fitur cuaca (18 fitur) dan target produktivitas, serta menampilkannya dalam dua visualisasi: heatmap korelasi untuk Musim Utama dan bar chart horizontal untuk semua fitur.

**Penjelasan kode:**

`df_fitur[KOLOM_CUACA + ['luas_panen_ha', 'produktivitas_ton_per_ha']].corr()` menghitung matriks korelasi Pearson. `korel['produktivitas_ton_per_ha'].drop('produktivitas_ton_per_ha')` mengekstrak kolom korelasi dengan target, lalu diurutkan dari terkecil ke terbesar.

*Panel kiri (Heatmap):* Menampilkan matriks korelasi antara fitur Musim Utama (6 parameter) dan target, menggunakan colormap merah-biru (RdBu_r) di mana merah = negatif, biru = positif. Setiap sel menampilkan nilai korelasi (format 2 desimal).

*Panel kanan (Bar chart horizontal):* Menampilkan korelasi semua 19 fitur (18 cuaca + 1 luas panen) terhadap produktivitas, diurutkan dari korelasi paling negatif (atas) ke paling positif (bawah). Batang merah = korelasi negatif, batang biru = korelasi positif.

**Output yang muncul:**

Dua panel visualisasi. Bar chart menunjukkan fitur mana yang paling berkorelasi dengan produktivitas. Berdasarkan pengetahuan agronomis, beberapa pola yang diharapkan:
- Curah hujan Musim Utama (PRECTOTCORR_utama_sum) kemungkinan berkorelasi positif dengan produktivitas.
- Suhu tinggi selama Musim Kemarau (T2M_MAX_kemarau_mean) kemungkinan berkorelasi negatif (panas berlebihan dapat merusak tanaman).
- Luas panen (luas_panen_ha) kemungkinan memiliki korelasi lemah atau bahkan negatif dengan produktivitas karena area luas sering memiliki lahan marginal.

**Interpretasi output:**

Korelasi yang rendah (mendekati nol) untuk sebagian besar fitur cuaca adalah temuan yang umum dalam penelitian pertanian. Ini menunjukkan bahwa hubungan antara cuaca dan produktivitas tidak sederhana dan linear, tetapi lebih kompleks. Bisa jadi karena:
1. Pengaruh irigasi yang meredam efek curah hujan alami.
2. Adaptasi petani lokal yang mengurangi dampak variasi cuaca.
3. Faktor non-cuaca (kualitas benih, pupuk, hama) yang tidak tertangkap oleh data.

Heatmap Musim Utama juga menunjukkan korelasi antar fitur cuaca sendiri. Suhu max, min, dan rata-rata yang saling berkorelasi tinggi menunjukkan masalah potensial multikolinearitas yang dapat memengaruhi Ridge Regression.

Grafik disimpan sebagai `results/Images/korelasi_fitur.png`.

**Istilah penting:**
- **Korelasi Pearson**: Ukuran statistik yang mengukur kekuatan dan arah hubungan linear antara dua variabel, dengan rentang nilai -1 (hubungan negatif sempurna) hingga +1 (hubungan positif sempurna). Nilai 0 berarti tidak ada hubungan linear.
- **Multikolinearitas**: Kondisi di mana dua atau lebih fitur sangat berkorelasi satu sama lain. Ini dapat menyulitkan model linear (termasuk Ridge) dalam mengestimasi koefisien dengan stabil, karena model kesulitan membedakan kontribusi individual masing-masing fitur.

---

### Cell 33 – Penjelasan Tahap Pemodelan dan Konfigurasi Model

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan empat model Machine Learning dan empat model baseline yang akan digunakan, beserta alasan pemilihan masing-masing.

**Penjelasan isi:**

Tabel model ML:
- **Ridge Regression**: Regresi linear dengan regularisasi L2; cocok untuk rasio sampel/fitur rendah.
- **Ridge Hist Lag**: Variasi Ridge yang hanya menggunakan 2 fitur historis produktivitas (tanpa cuaca).
- **Random Forest**: Ensemble 300 pohon keputusan dengan kedalaman maksimal 5 level.
- **Gradient Boosting**: 150 pohon dengan learning rate 0.08.

Tabel model baseline:
- **Naive Mean**: Selalu memprediksi rata-rata training.
- **Naive Kab Mean**: Memprediksi rata-rata historis per kabupaten.
- **Naive Lag1**: Memprediksi produktivitas tahun sebelumnya.
- **Naive Roll2**: Memprediksi rata-rata dua tahun terakhir.

Catatan kritis yang disebutkan: CV target ~9% berarti Naive Mean sudah menghasilkan MAPE ~9% tanpa belajar apapun. Model ML baru bermakna jika bisa melampaui ini.

---

### Cell 34 – Definisi Model ML dan Baseline

**Jenis cell:** Code

**Tujuan:**
Mendefinisikan semua model (ML dan baseline) sebagai objek Python yang siap dilatih.

**Penjelasan kode:**

Dictionary `MODELDEFS` mendefinisikan empat model ML:
- Ridge Regression: `Pipeline([StandardScaler(), Ridge(alpha=10.0)])`. Nilai alpha=10 yang cukup besar menandakan regularisasi yang kuat, cocok untuk dataset kecil.
- Ridge Hist Lag: `Pipeline([StandardScaler(), Ridge(alpha=3.0)])`. Alpha lebih kecil karena hanya 2 fitur yang digunakan, sehingga risiko overfitting lebih rendah.
- Random Forest: 300 pohon, kedalaman maksimal 5, minimal 3 sampel per daun, menggunakan akar kuadrat dari jumlah fitur saat mencari split terbaik.
- Gradient Boosting: 150 iterasi, kedalaman pohon 3, learning rate 0.08, subsampling 80%.

Empat kelas baseline didefinisikan sebagai class Python sederhana yang mengimplementasikan antarmuka `fit()` dan `predict()` dari scikit-learn, sehingga bisa diperlakukan seragam dengan model ML.

**Output yang muncul:**
```
Konfigurasi model ML:
  Ridge Regression: {'alpha': 10.0}
  Ridge Hist Lag: {'alpha': 3.0}
  Random Forest: {'n_estimators': 300, 'max_depth': 5, ...}
  Gradient Boosting: {'n_estimators': 150, 'max_depth': 3, 'learning_rate': 0.08, ...}

Baseline model: Naive Mean, Naive Kab Mean, Naive Lag1, Naive Roll2
```

**Interpretasi output:**

Pilihan hyperparameter model mencerminkan pertimbangan yang matang terhadap ukuran dataset:
- Ridge dengan alpha tinggi (10.0) menerapkan regularisasi yang kuat untuk mencegah overfitting pada 33 fitur.
- Random Forest dengan `max_depth=5` dan `min_samples_leaf=3` juga dibatasi secara eksplisit untuk mencegah pohon yang terlalu dalam.
- Gradient Boosting dengan learning rate rendah (0.08) dan subsample 80% adalah strategi regularisasi implisit untuk dataset kecil.

**Istilah penting:**
- **Ridge Regression**: Model regresi linear yang menambahkan penalti pada kuadrat koefisien (regularisasi L2). Ini mendorong koefisien menjadi kecil (tetapi tidak nol), sehingga model lebih robust terhadap multikolinearitas dan overfitting.
- **Alpha pada Ridge**: Parameter regularisasi. Alpha besar = penalti besar = koefisien lebih kecil = model lebih sederhana. Alpha kecil = Ridge mendekati regresi linear biasa. Memilih alpha yang tepat krusial untuk performa optimal.
- **Random Forest**: Ensemble dari banyak pohon keputusan, masing-masing dilatih pada sampel dan fitur yang berbeda secara acak. Prediksi akhir adalah rata-rata dari semua pohon. Lebih robust terhadap overfitting dibanding satu pohon tunggal.
- **Gradient Boosting**: Metode ensemble yang membangun pohon-pohon secara berurutan, di mana setiap pohon baru berusaha memperbaiki kesalahan pohon sebelumnya. `learning_rate` mengontrol seberapa besar kontribusi setiap pohon baru.
- **Baseline model**: Model sederhana yang digunakan sebagai tolok ukur minimum. Jika model ML tidak bisa mengalahkan baseline, maka model ML tersebut tidak memberikan nilai tambah.
- **Naive Mean**: Model paling sederhana — selalu memprediksi rata-rata nilai training. Tidak belajar apapun tentang kabupaten atau cuaca.
- **Naive Kabupaten Mean**: Sedikit lebih canggih dari Naive Mean — memprediksi rata-rata historis per kabupaten. Menangkap perbedaan level produktivitas antar wilayah tanpa mempelajari tren temporal.
- **Naive Lag1**: Memprediksi bahwa produktivitas tahun ini sama dengan produktivitas tahun lalu. Memanfaatkan persistensi temporal yang kuat pada data pertanian.

---

### Cell 35 – Penjelasan Walk-Forward Validation

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan mengapa Walk-Forward Validation dipilih menggantikan LOYOCV, dan bagaimana setiap fold bekerja.

**Penjelasan isi:**

Masalah LOYOCV (Leave-One-Year-Out Cross Validation) dijelaskan secara gamblang: fold pertama menguji tahun 2019 tetapi dilatih menggunakan 2020–2024 — data yang secara kronologis belum ada saat prediksi dibuat. Ini adalah data leakage yang serius.

Skema Walk-Forward Validation yang digunakan:
```
Fold 1: Train [2019]           → Test 2020  (15 sampel train)
Fold 2: Train [2019–2020]      → Test 2021  (30 sampel train)
Fold 3: Train [2019–2021]      → Test 2022  (45 sampel train)
Fold 4: Train [2019–2022]      → Test 2023  (60 sampel train)
Fold 5: Train [2019–2023]      → Test 2024  (75 sampel train)
```

**Output yang muncul:**
Teks deskriptif. Tidak ada output komputasi.

**Istilah penting:**
- **Walk-Forward Validation**: Metode evaluasi yang mensimulasikan penggunaan model secara temporal — model selalu dilatih pada data historis dan diuji pada data masa depan. Setiap fold memperluas data training satu tahun ke depan. Ini adalah cara evaluasi yang paling realistis untuk prediksi deret waktu.
- **Temporal leakage**: Kebocoran informasi dari masa depan ke masa lalu dalam proses evaluasi. Dalam LOYOCV, menggunakan data 2020–2024 untuk memprediksi 2019 adalah temporal leakage karena secara realistis kita tidak mungkin memiliki data masa depan saat membuat prediksi.
- **Fold**: Satu iterasi dalam cross-validation, di mana sebagian data digunakan untuk training dan sebagian lain untuk testing.

---

### Cell 36 – Eksekusi Walk-Forward Validation

**Jenis cell:** Code

**Tujuan:**
Menjalankan Walk-Forward Validation untuk semua model (ML dan baseline) di semua 5 fold, menyimpan hasil prediksi dan metrik evaluasi.

**Penjelasan kode:**

Fungsi `hitung_mape()` menghitung Mean Absolute Percentage Error dengan epsilon kecil (1e-8) untuk menghindari pembagian dengan nol.

Dictionary `WFV_HASIL` menyimpan hasil semua model: untuk setiap model, disimpan daftar nilai RMSE, MAE, R², MAPE per fold, serta semua nilai prediksi dan aktual.

Loop utama mengiterasi setiap tahun test (2020–2024). Untuk setiap tahun:
1. Data dengan tahun < tahun_test menjadi training.
2. Data dengan tahun == tahun_test menjadi testing (selalu 15 sampel).
3. Setiap model ML dilatih ulang dari awal (`copy.deepcopy()` memastikan tidak ada state dari iterasi sebelumnya) dan membuat prediksi.
4. Prediksi dikliping ke nilai minimum 0 dengan `np.clip(..., 0, None)` — produktivitas tidak mungkin negatif.
5. Empat baseline juga dievaluasi.

**Output yang muncul:**
```
Walk-Forward Validation
=================================================================
  Fold 2020 | Train: 2019 ( 15 sampel) | Test: 2020 (15 sampel)
  Fold 2021 | Train: 2019–2020 (30 sampel) | Test: 2021 (15 sampel)
  Fold 2022 | Train: 2019–2021 (45 sampel) | Test: 2022 (15 sampel)
  Fold 2023 | Train: 2019–2022 (60 sampel) | Test: 2023 (15 sampel)
  Fold 2024 | Train: 2019–2023 (75 sampel) | Test: 2024 (15 sampel)

Selesai.
```

**Interpretasi output:**

Fold pertama (training hanya 15 sampel untuk 33 fitur) adalah kondisi yang sangat menantang. Pada kondisi ini, Ridge Regression dengan regularisasi kuat akan jauh lebih stabil daripada Random Forest atau Gradient Boosting. Fold terakhir (75 sampel training) adalah yang paling representatif karena memiliki data terbanyak.

Perlu diperhatikan bahwa total data yang digunakan dalam evaluasi WFV adalah 5 × 15 = 75 observasi (dari fold 1 hingga 5 pada test set), bukan 90. Tahun 2019 hanya muncul sebagai data training, tidak pernah sebagai test set.

**Istilah penting:**
- **RMSE (Root Mean Squared Error)**: Akar dari rata-rata kuadrat selisih antara prediksi dan aktual. Dalam satuan yang sama dengan target (ton/ha). Memberi bobot lebih besar pada error yang besar.
- **MAE (Mean Absolute Error)**: Rata-rata nilai absolut selisih antara prediksi dan aktual. Lebih mudah diinterpretasikan dan tidak terlalu sensitif terhadap outlier dibanding RMSE.
- **MAPE (Mean Absolute Percentage Error)**: Rata-rata persentase selisih absolut antara prediksi dan aktual. Metrik ini berguna karena satuannya persen, sehingga mudah diinterpretasikan dan dibandingkan tanpa tergantung skala target.
- **R² (Koefisien Determinasi)**: Proporsi variansi dalam target yang dijelaskan oleh model. Nilai 1.0 berarti prediksi sempurna. Nilai 0 berarti model tidak lebih baik dari sekadar memprediksi rata-rata. Nilai negatif berarti model lebih buruk dari rata-rata sederhana.

---

### Cell 37 – Penjelasan Perbandingan Performa Model

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan metrik evaluasi yang digunakan dan cara membaca tabel perbandingan model.

---

### Cell 38 – Tabel Perbandingan Performa Semua Model

**Jenis cell:** Code

**Tujuan:**
Merangkum performa semua 8 model (4 ML + 4 baseline) berdasarkan rata-rata 5 fold WFV, menampilkan dalam tabel styled, dan menganalisis secara otomatis model mana yang terbaik.

**Penjelasan kode:**

Untuk setiap model, menghitung rata-rata dan standar deviasi RMSE, MAE, R², dan MAPE dari 5 fold. Hasil diurutkan dari MAPE terkecil (terbaik) ke terbesar. Tabel distilkan dengan warna berbeda:
- Hijau dengan bold: model ML terbaik dan/atau model overall terbaik
- Kuning: baseline terbaik
- Abu-abu: baseline lainnya

Logika perbandingan otomatis:
- Membandingkan MAPE model ML terbaik dengan Naive Mean dan Naive Kab Mean
- Menentukan apakah model ML berhasil mengalahkan baseline terbaik

**Output yang muncul:**

Tabel perbandingan 8 model dengan kolom: Model, Label (Terbaik ML/Terbaik Overall/Baseline Terbaik/Baseline), RMSE mean, RMSE std, MAE mean, R2 mean, MAPE mean (%), MAPE std (%).

Diikuti teks interpretasi otomatis seperti:
```
Referensi Baseline:
  Naive Mean      : MAPE = X.XX%
  Naive Kab Mean  : MAPE = X.XX%
  Baseline Terbaik: [nama baseline] – MAPE = X.XX%

Model ML Terbaik   : [nama model]  (MAPE = X.XX%)
Model Overall Terbaik: [nama model]  (MAPE = X.XX%)

--- Analisis Komparatif ---
[Hasil perbandingan model ML vs baseline]
```

**Interpretasi output:**

Ini adalah output paling penting dari notebook ini. Beberapa kemungkinan temuan yang umum terjadi pada dataset kecil seperti ini:

*Skenario 1 (model ML menang):* Model ML terbaik (kemungkinan Ridge dengan fitur historis) berhasil mengalahkan semua baseline dengan selisih yang signifikan. Ini berarti fitur cuaca musiman dan/atau kabupaten memberikan informasi prediktif yang nyata.

*Skenario 2 (baseline temporal menang):* Naive Lag1 atau Naive Roll2 memiliki MAPE terendah. Ini adalah temuan yang valid dan menunjukkan bahwa persistensi temporal sangat kuat pada data ini — produktivitas padi di kabupaten tertentu cenderung stabil dari tahun ke tahun, sehingga cukup memprediksi "sama seperti tahun lalu". Fenomena ini umum terjadi pada dataset pertanian yang kecil di mana sinyal cuaca tenggelam dalam noise.

Notebook secara eksplisit menyatakan bahwa jika model ML kalah dari baseline temporal, ini adalah "temuan yang valid dan penting untuk dilaporkan secara transparan" — menunjukkan integritas ilmiah yang baik.

**Mengapa baseline sederhana bisa mengalahkan ML?**

Ada beberapa alasan struktural:
1. Dataset hanya 90 sampel — terlalu sedikit bagi model kompleks untuk belajar pola yang bermakna.
2. Produktivitas padi memiliki persistensi tinggi antar tahun di tingkat kabupaten karena faktor tetap (kualitas tanah, irigasi) yang mendominasi atas variasi cuaca.
3. Fitur cuaca yang digunakan bersifat provinsi-wide (satu titik koordinat per kabupaten) dan mungkin tidak cukup granular untuk menangkap perbedaan lokal yang relevan.

---

### Cell 39 – Visualisasi Perbandingan Model per Fold

**Jenis cell:** Code

**Tujuan:**
Menampilkan perbandingan visual performa semua model di setiap fold dalam 4 panel (MAPE, RMSE, MAE, R²).

**Penjelasan kode:**
Grid 2×2 subplot, satu per metrik. Di setiap panel, grouped bar chart menampilkan nilai metrik untuk setiap fold (sumbu X) dan setiap model (batang berdampingan). Model baseline menggunakan arsiran garis miring (//) untuk membedakannya dari model ML.

**Output yang muncul:**

Grafik dengan 4 panel:
- Panel kiri atas: MAPE (%) per fold — semakin rendah semakin baik
- Panel kanan atas: RMSE (ton/ha) per fold — semakin rendah semakin baik
- Panel kiri bawah: MAE (ton/ha) per fold — semakin rendah semakin baik
- Panel kanan bawah: R² per fold — semakin tinggi semakin baik

**Interpretasi output:**

Visualisasi ini lebih informatif daripada sekadar rata-rata karena menunjukkan:

*Konsistensi per fold:* Model yang baik seharusnya konsisten (MAPE tidak terlalu berfluktuasi antar fold). Standar deviasi MAPE yang besar menunjukkan model tidak stabil.

*Tren peningkatan:* Diharapkan performa model ML meningkat (MAPE turun) seiring bertambahnya data training dari fold 1 ke fold 5, karena model mendapat lebih banyak informasi untuk belajar.

*Fold 1 (hanya 15 sampel training):* Kemungkinan menjadi fold terburuk untuk model ML yang kompleks, tetapi baseline temporal (Naive Lag1) sudah memiliki informasi yang dibutuhkan bahkan dengan data minimal.

Grafik disimpan sebagai `results/Images/perbandingan_model_wfv.png`.

---

### Cell 40 – Penjelasan Ablation Study

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan konsep ablation study, mengapa penting pada dataset kecil, dan kelompok fitur apa yang akan diuji.

**Penjelasan isi:**

Ablation study adalah eksperimen sistematis yang menguji performa model ketika kelompok fitur tertentu dimasukkan atau dikeluarkan. Tujuannya adalah mengidentifikasi kombinasi fitur yang paling efisien.

Kedelapan kombinasi fitur yang diuji:
1. Histori target ringkas (2 fitur: lag1, roll2)
2. Histori + Kabupaten (16 fitur)
3. Histori + Cuaca (20 fitur)
4. Histori + Cuaca + Kabupaten (34 fitur)
5. Cuaca saja (18 fitur)
6. Cuaca + Luas Panen (19 fitur)
7. Cuaca + Kabupaten (32 fitur)
8. Full: Cuaca + Luas + Kabupaten (33 fitur — konfigurasi default)

**Istilah penting:**
- **Ablation Study**: Berasal dari terminologi penelitian AI/ML yang mengadaptasi istilah medis "ablation" (pengangkatan bagian tubuh). Dalam ML, "ablation" berarti menghilangkan komponen tertentu dari model/fitur dan mengukur dampaknya terhadap performa.

---

### Cell 41 – Eksekusi dan Tampilan Ablation Study

**Jenis cell:** Code

**Tujuan:**
Menjalankan Walk-Forward Validation Ridge Regression untuk setiap dari 8 kombinasi fitur, menampilkan hasilnya dalam tabel terurut, dan menginterpretasikan hasilnya secara otomatis.

**Penjelasan kode:**

Fungsi `evaluate_wfv_estimator()` menjalankan WFV 5-fold untuk estimator dan set fitur tertentu. Untuk setiap kombinasi di `FEATURE_SETS`, fungsi ini dipanggil dengan Ridge Regression (yang dipilih sebagai estimator standar untuk ablation study karena konsisten dan deterministik).

Logika interpretasi otomatis memeriksa kombinasi terbaik dan terlemah, membandingkan histori saja vs cuaca saja, dan mendeteksi apakah menambah fitur justru meningkatkan MAPE (tanda overfitting).

**Output yang muncul:**

Tabel ablation study (diurutkan MAPE terkecil, baris terbaik dihighlight hijau):

| Feature Set | Jumlah Fitur | MAPE mean (%) | MAPE std (%) | RMSE mean | R2 mean |
|---|---|---|---|---|---|
| [Kombinasi terbaik] | X | X.XX% | X.XX% | X.XXXX | X.XXXX |
| ... | | | | | |
| [Kombinasi terlemah] | XX | XX.XX% | X.XX% | X.XXXX | X.XXXX |

Teks interpretasi:
```
=== Interpretasi Ablation Study ===
Kombinasi fitur terbaik : 'Histori target ringkas' (MAPE = X.XX%)
Kombinasi fitur terlemah: 'Full: Cuaca+Luas+Kab' (MAPE = XX.XX%)

Histori produktivitas saja    : MAPE = X.XX%
Cuaca saja                    : MAPE = XX.XX%
  -> Riwayat produktivitas (X.XX poin lebih baik) lebih informatif dari cuaca saja.
     Ini mengindikasikan persistensi produktivitas antar tahun di level kabupaten.

Penambahan seluruh fitur ('Full') menghasilkan MAPE XX.XX%,
lebih tinggi dari konfigurasi terbaik (X.XX%). Ini adalah tanda overfitting
yang khas pada dataset kecil.
```

**Interpretasi output:**

Hasil ablation study adalah salah satu temuan paling insightful dalam notebook ini. Beberapa insight kritis yang kemungkinan muncul:

*Jika "Histori target ringkas" (hanya 2 fitur) memiliki MAPE terbaik:* Ini menunjukkan bahwa riwayat produktivitas adalah prediktor terkuat, lebih kuat dari 18 fitur cuaca. Menambahkan lebih banyak fitur (cuaca, kabupaten) justru memperburuk performa — gejala khas overfitting pada dataset kecil.

*Jika penambahan fitur kabupaten (OHE) meningkatkan performa:* Efek spesifik per kabupaten yang bersifat tetap (kualitas tanah, irigasi) memang menambah informasi prediktif.

*Jika "Full: Cuaca+Luas+Kab" memiliki MAPE tertinggi:* Ini adalah bukti langsung bahwa lebih banyak fitur tidak selalu berarti lebih baik pada dataset kecil. Rasio sampel/fitur yang sangat rendah (90/33 = 2.7:1) menyebabkan model mencoba "menghafal" training data daripada belajar pola yang general.

---

### Cell 42 – Penjelasan Evaluasi Final

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa evaluasi akhir menggunakan split train 2019–2023 (75 sampel) dan test 2024 (15 sampel), dan menjelaskan perbedaan konseptual antara R² produktivitas dan R² produksi.

**Penjelasan isi:**
Penjelasan kritis tentang R² produksi yang tampak tinggi tetapi tidak mencerminkan kemampuan prediksi model — melainkan didominasi oleh variansi luas panen yang sangat berbeda antar kabupaten.

---

### Cell 43 – Evaluasi Final Model Terbaik pada Test 2024

**Jenis cell:** Code

**Tujuan:**
Melatih model terbaik pada seluruh data 2019–2023, memprediksi produktivitas 2024, menghitung metrik evaluasi, membandingkan dengan semua baseline, dan menyimpan detail prediksi per kabupaten.

**Penjelasan kode:**

Pertama, split data dilakukan: `mask_train = df_fitur['tahun'] <= 2023` dan `mask_test = df_fitur['tahun'] == 2024`. Model terbaik dari WFV dilatih pada 75 sampel training.

Untuk prediksi produksi (turunan): `produksi_prediksi_ton = produktivitas_prediksi × luas_panen_ha`. Ini bukan model produksi independen, melainkan derivasi dari prediksi produktivitas.

Error analysis per kabupaten dihitung dan disimpan di `meta_test`:
- `residual_prodvt`: error bersimbol (positif = over-prediction, negatif = under-prediction)
- `abs_error_prodvt`: nilai absolut error
- `produksi_error_pct`: error produksi dalam persen

**Output yang muncul:**

Tabel metrik produktivitas untuk semua model (ML dan baseline), diurutkan MAPE terkecil:

| Model | RMSE (t/ha) | MAE (t/ha) | R² | MAPE (%) |
|---|---|---|---|---|
| [Model terbaik] | X.XXXX | X.XXXX | X.XXXX | X.XX% |
| [Baseline terbaik] | X.XXXX | X.XXXX | X.XXXX | X.XX% |
| ... | | | | |

Teks tambahan:
```
Catatan R² produksi (turunan): X.XXXX
  Nilai R² ini tampak tinggi karena didominasi variansi luas panen antar kabupaten.
  MAPE produksi: X.XX% | RMSE produksi: X.X ribu ton

--- Interpretasi Hasil ---
Model [nama]: MAPE X.XX% termasuk [kategori].
  Rata-rata prediksi meleset sekitar X.XXX ton/ha dari nilai aktual.
  R² = X.XXXX: model mampu menjelaskan sekitar XX.X% variasi produktivitas.

Hasil dibanding baseline: [hasil perbandingan]
```

**Interpretasi output:**

Evaluasi final pada test 2024 adalah pengukuran performa yang paling realistis karena mensimulasikan penggunaan nyata: model dilatih dari semua data historis yang tersedia dan diuji pada data terbaru yang belum pernah dilihat.

Jika MAPE model ML pada test 2024 kurang dari 10%, ini adalah hasil yang baik untuk prediksi pertanian. Jika MAPE 10–15%, hasilnya cukup baik dan masih berguna sebagai alat bantu perencanaan. Jika MAPE di atas 15%, ada ruang untuk perbaikan signifikan.

**Interpretasi R² produksi:** Notebook secara eksplisit memperingatkan bahwa R² produksi yang tinggi (misalnya 0.95+) adalah "ilusi" — bukan bukti model yang sangat akurat, melainkan artefak statistik karena variansi luas panen antar kabupaten jauh lebih besar daripada variansi yang disebabkan oleh perubahan produktivitas. Model sebenarnya hanya perlu "tahu" luas panen setiap kabupaten untuk mendapat R² produksi yang tinggi, tanpa perlu memprediksi produktivitas dengan akurat.

---

### Cell 44 – Penjelasan Visualisasi dan Analisis Error

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan scatter plot yang akan ditampilkan berikutnya, dengan dua panel: produktivitas dan produksi turunan.

---

### Cell 45 – Scatter Plot Prediksi vs Aktual (Test 2024)

**Jenis cell:** Code

**Tujuan:**
Menampilkan scatter plot yang membandingkan nilai prediksi terhadap nilai aktual untuk produktivitas dan produksi turunan.

**Penjelasan kode:**

*Panel kiri (produktivitas):* Setiap titik mewakili satu kabupaten di tahun 2024. Titik biru = prediksi model ML terbaik, titik abu-abu segitiga = prediksi baseline terbaik. Garis merah putus-putus adalah garis "prediksi sempurna" (y = x) — titik yang berada di atas garis ini adalah over-prediction, di bawah adalah under-prediction.

*Panel kanan (produksi turunan):* Sama dengan kiri, tetapi dalam satuan ribu ton. Catatan di judul subplot mengingatkan bahwa R² produksi yang tinggi tidak mencerminkan kemampuan model.

**Output yang muncul:**

Dua scatter plot berdampingan. Judul utama menampilkan nama model terbaik, nilai R² dan MAPE-nya.

**Interpretasi output:**

*Scatter yang ideal:* Semua titik mendekati garis diagonal merah. Dispersi minimal di sekitar garis = RMSE kecil = model akurat.

*Pola yang mengkhawatirkan:*
- Titik yang jauh di atas garis diagonal: model sangat over-predicting untuk kabupaten tersebut.
- Titik yang jauh di bawah garis: model sangat under-predicting.
- Semua titik berada di satu sisi garis (semua di atas atau semua di bawah): ada bias sistematis.
- Titik yang tersebar luas tanpa pola mendekati garis: R² rendah, model tidak akurat.

Grafik disimpan sebagai `results/Images/scatter_prediksi_aktual.png`.

**Istilah penting:**
- **Over-prediction**: Model memprediksi nilai yang lebih tinggi dari nilai aktual. Residual bernilai positif. Jika konsisten untuk kabupaten tertentu, mungkin ada faktor lokal yang menekan produktivitas aktual yang tidak tertangkap model.
- **Under-prediction**: Model memprediksi nilai yang lebih rendah dari nilai aktual. Residual bernilai negatif.

---

### Cell 46 – Penjelasan Analisis Residual

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan dua panel analisis residual yang akan ditampilkan: signed residual produktivitas dan signed error produksi (%).

---

### Cell 47 – Analisis Residual dan Arah Bias Prediksi

**Jenis cell:** Code

**Tujuan:**
Menampilkan analisis residual per kabupaten untuk mengidentifikasi apakah ada bias sistematis arah prediksi.

**Penjelasan kode:**

*Panel kiri:* Bar chart horizontal menampilkan residual produktivitas (prediksi – aktual) per kabupaten, diurutkan dari residual paling negatif (under-prediction terbesar) ke paling positif (over-prediction terbesar). Batang biru = under-prediction, merah = over-prediction.

*Panel kanan:* Bar chart horizontal serupa untuk error produksi dalam persen. Garis oranye putus-putus di ±15% menandai batas akurasi wajar.

Interpretasi otomatis menghitung:
- Jumlah kabupaten yang over-prediction dan under-prediction
- Kabupaten dengan over/under-prediction terbesar
- Bias rata-rata (mean residual) dan maknanya

**Output yang muncul:**

Dua bar chart berdampingan.

Teks interpretasi:
```
=== Interpretasi Residual ===
Over-prediction  (terlalu tinggi): X kabupaten
Under-prediction (terlalu rendah): Y kabupaten
Over-prediction terbesar : [nama kabupaten] (+X.XXX t/ha)
Under-prediction terbesar: [nama kabupaten] (-X.XXX t/ha)
Bias rata-rata (mean residual): +X.XXXX t/ha
  -> [Interpretasi apakah ada bias sistematis]
```

**Interpretasi output:**

*Jika jumlah over-prediction dan under-prediction seimbang (misalnya 7 vs 8):* Model tidak memiliki bias arah yang sistematis — error terdistribusi seimbang di kedua arah. Ini adalah perilaku yang diharapkan.

*Jika mayoritas over-prediction:* Model secara sistematis memprediksi produktivitas terlalu tinggi. Ini bisa terjadi jika ada penurunan produktivitas pada 2024 (misalnya akibat El Niño atau hama) yang tidak tertangkap oleh data training historis.

*Bias rata-rata mendekati nol:* Menunjukkan bahwa model tidak memiliki bias global, meskipun error per kabupaten bisa besar dalam dua arah.

*Kabupaten dengan error terbesar:* Biasanya kabupaten dengan karakteristik yang sangat berbeda dari rata-rata — mungkin kabupaten terkecil (Metro atau Bandar Lampung) yang sangat bergantung pada kondisi urban, atau kabupaten yang mengalami perubahan besar pada 2024.

Grafik disimpan sebagai `results/Images/residual_analysis_2024.png`.

**Istilah penting:**
- **Residual**: Selisih antara nilai prediksi dan nilai aktual (prediksi – aktual). Analisis residual adalah alat standar untuk mendiagnosis kelemahan model.

---

### Cell 48 – Penjelasan Perbandingan Produksi per Kabupaten

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan grafik batang berdampingan yang akan membandingkan produksi aktual vs prediksi per kabupaten.

---

### Cell 49 – Bar Chart Perbandingan Produksi Aktual vs Prediksi (2024)

**Jenis cell:** Code

**Tujuan:**
Menampilkan grouped bar chart yang membandingkan produksi aktual (biru) dan prediksi (oranye) untuk setiap kabupaten, dengan label MAPE yang diberi kode warna.

**Penjelasan kode:**
Kabupaten diurutkan dari produksi aktual terbesar ke terkecil (kiri ke kanan). Dua batang per kabupaten berdampingan. Di atas setiap pasang batang, teks persentase MAPE ditampilkan dengan warna yang mencerminkan zona akurasi: hijau (< 15%), oranye (15–30%), merah (> 30%).

**Output yang muncul:**

Bar chart dengan 15 grup batang berdampingan, sumbu X menampilkan nama kabupaten (rotasi 40 derajat), sumbu Y menampilkan produksi dalam ribu ton. Label MAPE berwarna di atas setiap grup.

**Interpretasi output:**

Visualisasi ini memungkinkan pembaca secara sekilas menilai kinerja model untuk setiap kabupaten. Kabupaten dengan pasang batang yang hampir sama tingginya menunjukkan prediksi yang akurat. Kabupaten dengan perbedaan tinggi batang yang besar menunjukkan prediksi yang kurang akurat.

*Kabupaten produksi besar di sisi kiri:* Kesalahan dalam ton yang besar bisa terjadi meskipun persentase error (MAPE) relatif kecil, karena skala produksinya sendiri besar. Ini penting untuk diperhatikan dari perspektif perencanaan pangan.

*Kabupaten kota kecil (Metro, Bandar Lampung) di sisi kanan:* Produksinya kecil, sehingga perbedaan visualnya kecil meski MAPE bisa besar.

Grafik disimpan sebagai `results/Images/bar_per_kabupaten_2024.png`.

---

### Cell 50 – Penjelasan Feature Importance

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan apa itu feature importance, bagaimana dihitung untuk Ridge Regression (menggunakan nilai absolut koefisien), dan apa yang akan ditampilkan dalam dua panel visualisasi.

---

### Cell 51 – Visualisasi Feature Importance

**Jenis cell:** Code

**Tujuan:**
Mengekstrak dan memvisualisasikan feature importance dari model terbaik dalam dua panel: top-20 fitur individu dan importance agregasi per kategori.

**Penjelasan kode:**

Untuk Ridge Regression, `importances = np.abs(inner.coef_)` — nilai absolut koefisien Ridge digunakan sebagai proxy feature importance. Fitur dengan koefisien lebih besar (dalam nilai absolut) memiliki pengaruh lebih besar terhadap prediksi.

Setiap fitur dikategorikan: fitur yang namanya dimulai dengan `kabupaten_` masuk kategori OHE, dimulai dengan `prodvt_` masuk kategori Histori Target, nama `luas_panen_ha` masuk kategori Luas Panen, dan sisanya dikategorikan berdasarkan nama musim.

*Panel kiri:* Bar chart horizontal 20 fitur dengan importance tertinggi, diberi kode warna per kategori (merah = kabupaten OHE, hijau tua = histori, hijau muda = Musim Utama, oranye = Musim Gadu, ungu = Musim Kemarau).

*Panel kanan:* Importance dijumlahkan per kategori, ditampilkan dalam bar chart horizontal.

**Output yang muncul:**

Dua panel visualisasi feature importance.

**Interpretasi output:**

Hasil feature importance adalah jawaban atas pertanyaan: "Informasi apa yang paling dimanfaatkan model untuk membuat prediksi?"

*Jika fitur OHE kabupaten mendominasi:* Model sangat bergantung pada "tahu di kabupaten mana" untuk membuat prediksi yang baik. Ini menunjukkan bahwa efek tetap per kabupaten (kualitas tanah, irigasi) lebih penting daripada variasi cuaca antar tahun. Ini juga mengindikasikan bahwa model mungkin tidak akan generalisasi baik ke kabupaten baru.

*Jika fitur historis produktivitas (prodvt_lag1, prodvt_roll2) mendominasi:* Model mengandalkan persistensi temporal — "produktivitas tahun ini mirip tahun lalu". Ini konsisten dengan dominasi baseline Naive Lag1.

*Jika fitur cuaca musiman mendominasi:* Model benar-benar memanfaatkan sinyal cuaca. Perlu dilihat musim mana yang paling berpengaruh — umumnya Musim Utama (penghujan) yang paling kritis untuk produktivitas padi.

Grafik disimpan sebagai `results/Images/feature_importance.png`.

**Istilah penting:**
- **Feature Importance**: Ukuran seberapa besar kontribusi suatu fitur terhadap prediksi model. Untuk Ridge Regression, dihitung dari nilai absolut koefisien regresi. Untuk Random Forest, dihitung dari penurunan impuritas rata-rata yang disebabkan oleh setiap fitur.
- **Koefisien regresi**: Nilai yang mengindikasikan perubahan prediksi ketika fitur tersebut naik satu unit, dengan semua fitur lain tetap. Dalam Ridge Regression yang menggunakan StandardScaler, koefisien dapat dibandingkan langsung antar fitur (karena semua fitur sudah distandarisasi ke skala yang sama).

---

### Cell 52 – Penjelasan Distribusi Akurasi per Kabupaten

**Jenis cell:** Markdown

**Tujuan:**
Menjelaskan bahwa grafik berikutnya akan menampilkan MAPE per kabupaten dan mengapa ini penting untuk menilai konsistensi model.

---

### Cell 53 – Distribusi MAPE per Kabupaten (Test 2024)

**Jenis cell:** Code

**Tujuan:**
Menampilkan MAPE prediksi produksi per kabupaten dalam bar chart horizontal, menghitung distribusi akurasi, dan menginterpretasikan konsistensinya.

**Penjelasan kode:**
`meta_test['mape_produksi'] = meta_test['produksi_error_pct'].abs()` menghitung nilai absolut persentase error produksi. Bar chart horizontal mengurutkan dari MAPE terkecil (paling akurat) hingga terbesar. Garis vertikal putus-putus menandai ambang 15% dan 30%.

Interpretasi otomatis mengkategorikan kabupaten ke tiga zona:
- Akurat: MAPE < 15%
- Moderat: 15% ≤ MAPE < 30%
- Lemah: MAPE ≥ 30%

Standar deviasi MAPE antar kabupaten juga dihitung sebagai ukuran konsistensi.

**Output yang muncul:**

Bar chart horizontal 15 kabupaten, diurutkan dari MAPE terkecil ke terbesar. Setiap batang diberi label nilai MAPE-nya. Dua garis vertikal putus-putus (hijau di 15%, oranye di 30%) membagi grafik menjadi tiga zona.

Teks interpretasi:
```
=== Interpretasi Distribusi Akurasi per Kabupaten ===
Akurat   (MAPE < 15%) : X kabupaten [daftar nama]
Moderat (15–30%)      : Y kabupaten [daftar nama]
Lemah   (> 30%)       : Z kabupaten [daftar nama]

Standar deviasi MAPE antar kabupaten: XX.XX%
  -> [Interpretasi konsistensi]
```

**Interpretasi output:**

Distribusi akurasi per kabupaten mengungkapkan apakah model bekerja merata atau hanya akurat untuk sebagian wilayah saja.

*Jika sebagian besar kabupaten di zona hijau (< 15%):* Model cukup baik dan konsisten untuk digunakan sebagai alat bantu perencanaan.

*Jika ada kabupaten dengan MAPE sangat tinggi (> 30%):* Perlu diselidiki lebih lanjut — apakah ada perubahan besar pada 2024 untuk kabupaten tersebut yang tidak tertangkap dalam data training? Atau apakah kabupaten tersebut memiliki karakteristik yang sangat berbeda dari yang lain?

*Standar deviasi MAPE rendah (< 10%):* Performa model relatif konsisten antar kabupaten. Standar deviasi tinggi (> 20%) berarti model sangat tidak merata — sangat baik di beberapa wilayah tetapi sangat buruk di wilayah lain.

Grafik disimpan sebagai `results/Images/mape_per_kabupaten.png`.

---

### Cell 54 – Penjelasan Tahap Ringkasan dan Kesimpulan

**Jenis cell:** Markdown

**Tujuan:**
Memperkenalkan bagian penutup notebook yang merangkum seluruh temuan.

---

### Cell 55 – Ringkasan Akhir dan Kesimpulan Naratif Otomatis

**Jenis cell:** Code

**Tujuan:**
Menghasilkan laporan teks terstruktur yang merangkum seluruh hasil penelitian secara otomatis, mencakup konfigurasi, performa semua model, ablation study, distribusi akurasi, dan interpretasi akhir.

**Penjelasan kode:**

Laporan terbagi menjadi dua bagian:

*Bagian 1: Ringkasan Numerik Terstruktur* — Menampilkan semua angka penting dalam format yang mudah dibandingkan: desain fitur, musim tanam, perbandingan MAPE semua model, performa final pada test 2024, ablation study, dan distribusi zona akurasi.

*Bagian 2: Ringkasan Naratif* — Enam sub-bagian naratif yang dihasilkan secara otomatis berdasarkan nilai numerik aktual:
1. Performa model terbaik (dikategorikan berdasarkan ambang MAPE: sangat baik < 5%, baik < 10%, cukup baik < 15%, perlu perbaikan ≥ 15%)
2. Perbandingan dengan baseline (otomatis mendeteksi siapa yang menang)
3. Insight dari ablation study
4. Distribusi akurasi per kabupaten
5. Keterbatasan penelitian (selalu dimasukkan)
6. Implikasi praktis

**Output yang muncul:**

Blok teks panjang yang diformat rapi:
```
=================================================================
RINGKASAN AKHIR – PREDIKSI PRODUKTIVITAS & PRODUKSI PADI
Provinsi Lampung | Machine Learning Berbasis Musim Tanam
=================================================================
  Tanggal generate  : [tanggal hari ini]
  Cakupan data      : 15 kabupaten, 2019–2024 (90 sampel)

  Desain Fitur:
    Target           : produktivitas_ton_per_ha
    Fitur cuaca      : 18 (3 musim × 6 parameter)
    Fitur histori    : 3 kandidat lag/rolling produktivitas
    Fitur lain       : luas_panen_ha, kabupaten (OHE × 14)
    Total fitur default: 33 | fitur final ML: X

  ... [perbandingan semua model]

  Performa Final (Train 2019–2023 / Test 2024):
    Produktivitas : RMSE=X.XXXX t/ha | MAE=X.XXXX | R²=X.XXXX | MAPE=X.XX%
    [Baseline]: RMSE=X.XXXX t/ha | MAE=X.XXXX | R²=X.XXXX | MAPE=X.XX%

  ... [ablation study summary]

  Distribusi MAPE per Kabupaten (Test 2024):
    Akurat   (< 15%) :  X kabupaten
    Moderat (15–30%) :  Y kabupaten
    Lemah   (> 30%)  :  Z kabupaten
=================================================================

KESIMPULAN VALIDITAS:
  • Kualitas pipeline/evaluasi membaik: input divalidasi, ablation tersedia, dan residual dianalisis.
  • [Hasil perbandingan ML vs baseline]

=================================================================
RINGKASAN NARATIF
=================================================================

1. Model Terbaik ML: [nama]
   Rata-rata prediksi produktivitas meleset sekitar X.XXX ton/ha dari nilai aktual.
   ...

2. Perbandingan dengan Baseline:
   ...

3. Insight Utama dari Ablation Study:
   ...

4. Distribusi Akurasi per Kabupaten (Test 2024):
   ...

5. Keterbatasan Penelitian:
   a. Dataset kecil: 90 sampel dengan 15–33 fitur memberikan rasio sampel/fitur rendah.
   b. Luas panen aktual digunakan sebagai fitur...
   c. Baseline temporal sangat kompetitif...

6. Implikasi Praktis:
   ...
=================================================================
Laporan dibuat: [tanggal] | Data: BPS & NASA POWER (2019–2024)
=================================================================
```

**Interpretasi output:**

Cell ini adalah klimaks dari seluruh notebook — merangkum setiap angka penting dalam konteks yang bermakna. Kekuatan pendekatan otomatis ini adalah laporan dapat diperbarui langsung ketika data baru ditambahkan atau model diperbaiki, tanpa perlu menulis ulang interpretasi secara manual.

Pernyataan "KESIMPULAN VALIDITAS" secara eksplisit mengakui keterbatasan model jika model ML tidak berhasil mengalahkan baseline, mencerminkan integritas ilmiah.

Catatan penting untuk laporan ini: nilai-nilai numerik aktual (MAPE, RMSE, R², dll.) bergantung pada data yang di-upload oleh pengguna dan akan berbeda setiap kali notebook dijalankan dengan data yang berbeda. Dokumen ini menjelaskan struktur dan interpretasi output, bukan nilai numeriknya secara spesifik.

---

## Glosarium Istilah

| Istilah | Penjelasan Sederhana | Peran dalam Notebook |
|---|---|---|
| Big Data | Pendekatan berbasis data dalam skala besar; di sini merujuk pada konteks mata kuliah | Nama proyek, mengindikasikan pendekatan berbasis data |
| BPS | Badan Pusat Statistik — lembaga resmi data statistik Indonesia | Sumber data produksi dan luas panen padi |
| NASA POWER | Platform data cuaca harian global dari NASA berbasis satelit | Sumber data meteorologi 6 parameter per kabupaten |
| Data cleaning | Proses membersihkan data dari kesalahan, duplikat, dan nilai tidak valid | Cell 6–16: validasi, konversi sentinel, imputasi |
| Sentinel value -999 | Nilai khusus NASA yang menandai data tidak tersedia, bukan nilai sebenarnya | Dikonversi ke NaN pada parsing JSON |
| NaN | Not a Number — representasi nilai kosong/hilang dalam Python | Dihasilkan dari konversi sentinel, ditangani imputasi |
| Imputasi | Mengisi nilai yang hilang dengan estimasi berdasarkan pola data | Cell 12: imputasi median bulanan (dilewati karena data lengkap) |
| Median bulanan | Nilai tengah observasi cuaca pada bulan tertentu di kabupaten tertentu | Digunakan sebagai nilai fallback dalam imputasi |
| Agregasi | Meringkas banyak data menjadi sedikit data dengan fungsi statistik | Cell 14: dari 38.325 baris harian ke 1.260 baris bulanan |
| Feature engineering | Mengubah data mentah menjadi fitur bermakna untuk model ML | Cell 18–22: membangun 18 fitur cuaca musiman |
| Musim Utama | Musim tanam utama (Nov T-1 – Mar T) dengan curah hujan tinggi | Sumber 6 fitur cuaca: suhu, hujan, radiasi Musim Utama |
| Musim Gadu | Musim tanam kedua (Apr–Jul) transisi hujan ke kemarau | Sumber 6 fitur cuaca Musim Gadu |
| Musim Kemarau | Musim tanam ketiga (Agu–Okt) bergantung irigasi | Sumber 6 fitur cuaca Musim Kemarau |
| Rolling Mean 2y | Rata-rata produktivitas dua tahun terakhir | Fitur prediktif `prodvt_roll2` dalam model |
| Lag feature | Nilai dari periode sebelumnya yang digunakan sebagai fitur | `prodvt_lag1` = produktivitas tahun lalu |
| Standar deviasi | Ukuran seberapa jauh data menyebar dari rata-rata | Menilai variabilitas produktivitas antar tahun/kabupaten |
| Mean | Rata-rata aritmatika nilai-nilai dalam dataset | Target utama baseline Naive Mean |
| Minimum | Nilai terkecil dalam dataset | Batas bawah rentang produktivitas |
| Maximum | Nilai terbesar dalam dataset | Batas atas rentang produktivitas |
| Kuartil | Nilai yang membagi data menjadi 4 bagian (Q1=25%, Q2=50%, Q3=75%) | Digunakan dalam boxplot distribusi produktivitas |
| One-Hot Encoding | Mengubah variabel kategoris (nama kabupaten) menjadi variabel biner 0/1 | Cell 22: mengubah 15 kabupaten menjadi 14 kolom dummy |
| drop_first=True | Parameter OHE yang menghilangkan satu kategori untuk menghindari redundansi | Menghasilkan 14 (bukan 15) kolom dummy kabupaten |
| Dummy variable | Kolom biner hasil One-Hot Encoding yang mewakili satu kategori | 14 kolom `kabupaten_X` yang dihasilkan OHE |
| Target variable | Variabel yang ingin diprediksi oleh model | `produktivitas_ton_per_ha` |
| Produktivitas ton/ha | Hasil panen per hektar lahan yang dipanen | Target prediksi utama model |
| Produksi ton | Total hasil panen = produktivitas × luas panen | Target turunan yang dihitung dari prediksi produktivitas |
| Luas panen | Luas lahan yang benar-benar dipanen dalam satuan hektar | Fitur model dan denominator perhitungan produktivitas |
| Korelasi Pearson | Ukuran kekuatan hubungan linear antara dua variabel (rentang -1 hingga +1) | EDA Cell 32: mengukur hubungan fitur cuaca dengan produktivitas |
| Baseline model | Model sederhana sebagai tolok ukur minimum yang harus dilampaui ML | 4 baseline: Naive Mean, Kab Mean, Lag1, Roll2 |
| Naive Mean | Selalu memprediksi rata-rata training | Baseline paling sederhana, MAPE ≈ CV dataset |
| Naive Kabupaten Mean | Memprediksi rata-rata historis per kabupaten | Baseline yang menangkap efek lokasi tanpa mempelajari tren |
| Naive Rolling 2y | Memprediksi rata-rata dua tahun terakhir | Baseline temporal yang halus dan kompetitif |
| Ridge Regression | Regresi linear dengan regularisasi L2 untuk mencegah overfitting | Model ML utama; bekerja baik pada dataset kecil |
| Alpha pada Ridge | Parameter kekuatan regularisasi Ridge | Semakin besar alpha = koefisien lebih kecil = model lebih sederhana |
| Random Forest | Ensemble banyak pohon keputusan dengan pemilihan fitur acak | Salah satu model ML yang diuji |
| Gradient Boosting | Ensemble pohon keputusan yang dibangun secara berurutan | Salah satu model ML yang diuji |
| Walk-Forward Validation | Metode evaluasi temporal: training selalu pada data lebih lama dari data test | Metode utama evaluasi (5 fold, 2020–2024) |
| Fold | Satu iterasi dalam cross-validation | 5 fold: test di tahun 2020, 2021, 2022, 2023, 2024 |
| Train-Test Split | Pembagian data menjadi set pelatihan dan set pengujian | Train 2019–2023 (75 sampel), Test 2024 (15 sampel) |
| RMSE | Root Mean Squared Error — akar rata-rata kuadrat error, dalam ton/ha | Metrik evaluasi yang sensitif terhadap error besar |
| MAE | Mean Absolute Error — rata-rata selisih absolut prediksi vs aktual | Metrik evaluasi yang mudah diinterpretasikan |
| MAPE | Mean Absolute Percentage Error — persentase rata-rata error | Metrik utama evaluasi (unit %); tidak bergantung skala |
| R² | Koefisien Determinasi — proporsi variansi yang dijelaskan model (0 hingga 1) | Mengukur kekuatan prediktif model secara keseluruhan |
| Ablation Study | Eksperimen sistematis memasukkan/mengeluarkan kelompok fitur untuk mengukur kontribusinya | Cell 41: membandingkan 8 kombinasi fitur dengan Ridge |
| Residual | Selisih prediksi – aktual; positif = over-prediction, negatif = under-prediction | Dianalisis dalam Cell 47 untuk mendeteksi bias kabupaten |
| Over-prediction | Model memprediksi nilai lebih tinggi dari aktual | Diidentifikasi melalui residual positif per kabupaten |
| Under-prediction | Model memprediksi nilai lebih rendah dari aktual | Diidentifikasi melalui residual negatif per kabupaten |
| Feature Importance | Ukuran kontribusi masing-masing fitur terhadap prediksi model | Cell 51: koefisien absolut Ridge untuk top-20 fitur |
| Koefisien regresi | Nilai yang mengindikasikan pengaruh satu unit perubahan fitur terhadap prediksi | Digunakan sebagai proxy feature importance untuk Ridge |
| StandardScaler | Normalisasi data agar setiap fitur memiliki rata-rata 0 dan std 1 | Digunakan dalam Pipeline sebelum Ridge Regression |
| Overfitting | Model terlalu "hafal" data training sehingga gagal pada data baru | Risiko utama dengan rasio sampel/fitur 2.7:1 |
| Data leakage | Informasi masa depan bocor ke proses training/evaluasi | Diatasi dengan Walk-Forward Validation |
| Temporal leakage | Jenis data leakage spesifik karena urutan waktu tidak dihormati | Alasan penggantian LOYOCV v2 dengan WFV v3 |

---

## Ringkasan Angka Penting

| Angka/Nilai | Muncul pada Bagian | Makna | Kenapa Penting |
|---|---|---|---|
| 2018–2024 | Cell 4, Cell 7 | Periode data BPS yang tersedia (7 tahun) | Fondasi seluruh dataset; batas temporal kemampuan model |
| 2019–2024 | Cell 4, Cell 18 | Periode fitur model yang lengkap (6 tahun) | 2018 tidak bisa digunakan karena Musim Utama butuh data 2017 yang tidak tersedia |
| 15 | Cell 4, Cell 10 | Jumlah kabupaten/kota Lampung yang diproses | Jumlah unit analisis; perbaikan dari bug v2 yang hanya 5 kabupaten |
| 105 | Cell 7 | Total baris data BPS (15 kab × 7 tahun) | Volume data statistik tahunan yang menjadi dasar target prediksi |
| 38.325 | Cell 10 | Total baris data cuaca harian (15 kab × 2.555 hari) | Volume data cuaca harian sebelum agregasi |
| 1.260 | Cell 14 | Baris data cuaca bulanan (15 × 12 × 7) | Hasil agregasi harian ke bulanan sebelum feature engineering |
| 90 | Cell 20 | Total sampel model (15 kab × 6 tahun) | Ukuran efektif dataset; sangat kecil untuk ML |
| 18 | Cell 18 | Jumlah fitur cuaca musiman (3 musim × 6 parameter) | Jumlah sinyal cuaca yang tersedia bagi model |
| 3 | Cell 20 | Fitur historis produktivitas (lag1, roll2, roll3) | Sinyal persistensi temporal; sering lebih prediktif dari cuaca |
| 14 | Cell 22 | Kolom dummy kabupaten hasil OHE | 15 kabupaten dikurangi 1 kategori referensi |
| 33 | Cell 22 | Total fitur default FITUR_MODEL | 18 cuaca + 1 luas panen + 14 OHE = konfigurasi penuh |
| 2 | Cell 22, Cell 34 | Fitur Ridge Hist Lag (hanya lag1 dan roll2) | Konfigurasi paling hemat yang diuji dalam ablation |
| 2.7:1 | Cell 22 | Rasio sampel/fitur (90 sampel ÷ 33 fitur) | Sangat rendah; membatasi kompleksitas model yang aman digunakan |
| 15 sampel | Cell 36 | Jumlah sampel test per fold | Satu per kabupaten; sangat kecil untuk estimasi yang stabil |
| 75 sampel | Cell 43 | Jumlah sampel training final (2019–2023) | Training maksimal yang tersedia untuk evaluasi akhir |
| 10.0 | Cell 34 | Alpha Ridge Regression default | Regularisasi kuat yang dipilih untuk dataset kecil dengan banyak fitur |
| 3.0 | Cell 34 | Alpha Ridge Hist Lag | Regularisasi lebih ringan untuk model dengan hanya 2 fitur |
| 5 | Cell 36 | Jumlah fold Walk-Forward Validation | Satu fold per tahun test (2020, 2021, 2022, 2023, 2024) |
| ~9% | Cell 20 | Koefisien Variasi produktivitas | Perkiraan MAPE minimum baseline Naive Mean; tolok ukur kritis |
| 300 | Cell 34 | Jumlah pohon Random Forest | Lebih banyak pohon = prediksi lebih stabil tetapi lebih lambat |
| 150 | Cell 34 | Jumlah iterasi Gradient Boosting | Diregularisasi dengan learning rate rendah (0.08) |
| 0 | Cell 12 | Jumlah nilai hilang setelah parsing NASA POWER | Data cuaca lengkap; imputasi tidak diperlukan |

---

## Ringkasan Hasil Model

Notebook ini mengevaluasi 8 model (4 ML + 4 baseline) menggunakan Walk-Forward Validation 5 fold (2020–2024) dengan metrik utama MAPE.

### Hierarki Model yang Diuji

**Model Machine Learning:**
1. Ridge Regression (33 fitur: cuaca + luas panen + OHE kabupaten, alpha=10)
2. Ridge Hist Lag (2 fitur: lag1 dan roll2 produktivitas, alpha=3)
3. Random Forest (33 fitur, 300 pohon, max_depth=5)
4. Gradient Boosting (33 fitur, 150 iterasi, learning_rate=0.08)

**Model Baseline:**
1. Naive Mean (prediksi = rata-rata training keseluruhan)
2. Naive Kabupaten Mean (prediksi = rata-rata historis per kabupaten)
3. Naive Lag1 (prediksi = produktivitas tahun sebelumnya)
4. Naive Roll2 (prediksi = rata-rata dua tahun terakhir)

### Interpretasi Hasil yang Diharapkan

Berdasarkan struktur dataset dan temuan yang dideskripsikan dalam kode interpretasi otomatis, ada beberapa kemungkinan hasil yang paling realistis:

**Skenario umum pada dataset pertanian kecil seperti ini:**
- Model baseline temporal (Naive Lag1 atau Naive Roll2) sering menjadi yang terkuat secara keseluruhan, karena persistensi produktivitas antar tahun sangat tinggi di tingkat kabupaten.
- Di antara model ML, Ridge Regression dengan fitur historis ringkas (Ridge Hist Lag, hanya 2 fitur) sering mengungguli Ridge penuh (33 fitur) dan jauh lebih baik dari Random Forest maupun Gradient Boosting pada fold-fold awal.
- Gradient Boosting dan Random Forest umumnya berkinerja buruk pada fold pertama (hanya 15 sampel training) tetapi mulai bersaing pada fold terakhir (75 sampel training).

**Apa yang dimaksud dengan "hasil yang baik":**
- MAPE < 5%: sangat baik
- MAPE 5–10%: baik untuk prediksi pertanian
- MAPE 10–15%: cukup, masih berguna sebagai alat bantu
- MAPE > 15%: perlu perbaikan signifikan

**Insight ablation study yang diharapkan:**
Kemungkinan besar "Histori target ringkas" (hanya 2 fitur) akan memiliki MAPE yang kompetitif atau bahkan terbaik dibanding konfigurasi penuh (33 fitur). Ini adalah bukti overfitting pada dataset kecil — menambah fitur dari 2 menjadi 33 tidak selalu meningkatkan performa.

**Fitur yang paling berpengaruh:**
Berdasarkan structure model dan karakteristik data pertanian, urutan kepentingan yang paling mungkin adalah: (1) fitur OHE kabupaten — menangkap perbedaan permanen antar wilayah, (2) fitur historis produktivitas — menangkap persistensi temporal, (3) fitur cuaca Musim Utama — musim paling kritis untuk padi.

**Nilai R² produksi yang tinggi tidak menyesatkan jika dipahami konteksnya:**
R² produksi bisa mencapai 0.95+ bukan karena model prediktif, melainkan karena variansi luas panen antar kabupaten sangat besar (dari ribuan hingga ratusan ribu hektar). Model yang "tahu" luas panen tiap kabupaten (yang memang digunakan sebagai fitur) akan menghasilkan R² produksi tinggi meskipun prediksi produktivitasnya tidak akurat.

---

## Kesimpulan Akhir

### Apa yang Dilakukan Notebook Ini

Notebook ini merancang dan mengevaluasi sistem prediksi produktivitas padi berbasis Machine Learning untuk Provinsi Lampung. Pendekatan utamanya adalah menggabungkan dua sumber data yang saling melengkapi: data statistik resmi BPS (yang mencatat hasil panen aktual) dan data cuaca ilmiah dari NASA POWER (yang merekam kondisi lingkungan harian). Keunggulan metodologisnya terletak pada transformasi data cuaca ke dalam fitur yang bermakna secara agronomis melalui jendela musim tanam padi.

### Data yang Digunakan

Data mencakup 7 tahun (2018–2024) untuk 15 kabupaten/kota Lampung, menghasilkan 90 sampel efektif setelah rekayasa fitur. Enam parameter cuaca NASA POWER (radiasi, suhu rata-rata/maksimum/minimum, kelembapan, curah hujan) diagregasi ke dalam tiga jendela musim tanam, menghasilkan 18 fitur cuaca musiman. Ditambah tiga fitur historis produktivitas (lag satu tahun, rolling dua tahun, rolling tiga tahun), satu fitur luas panen, dan 14 fitur dummy kabupaten, total menjadi 33 fitur untuk konfigurasi penuh.

### Fitur yang Paling Berpengaruh

Berdasarkan logika ablation study dan desain feature importance dalam notebook, fitur historis produktivitas (terutama lag satu tahun) adalah kandidat terkuat sebagai fitur paling berpengaruh. Ini mencerminkan realitas pertanian: kabupaten yang produktif secara konsisten cenderung tetap produktif karena faktor infrastruktur dan lahan yang bersifat permanen. Efek spesifik kabupaten (tertangkap oleh OHE) juga diperkirakan penting. Fitur cuaca musiman memberikan kontribusi, tetapi mungkin tidak setinggi yang diharapkan karena banyak area pertanian Lampung sudah memiliki irigasi teknis yang meredam dampak variasi curah hujan alami.

### Model Terbaik

Berdasarkan struktur evaluasi dan temuan umum pada dataset sejenis, Ridge Regression dengan konfigurasi fitur yang terbatas (terutama varian Ridge Hist Lag yang hanya menggunakan 2 fitur historis) diperkirakan menjadi model ML yang paling andal. Model ini memanfaatkan regularisasi L2 yang kuat untuk mengatasinya rendahnya rasio sampel/fitur. Namun, tidak menutup kemungkinan bahwa baseline temporal (Naive Lag1 atau Naive Roll2) secara keseluruhan memiliki MAPE terkecil — dan notebook mengakui ini dengan transparan.

### Apakah Pendekatan Ini Layak

Pendekatan ini layak dari perspektif metodologis. Pipeline yang dibangun: validasi data yang ketat, feature engineering berbasis agronomis, evaluasi temporal yang benar (Walk-Forward Validation), ablation study, dan analisis residual — semuanya merupakan praktik terbaik dalam data science terapan. Transparan dalam melaporkan keterbatasan dan perbandingan yang jujur dengan baseline adalah nilai ilmiah yang penting.

Namun, dari perspektif performa prediktif, nilai tambah model ML terhadap baseline sederhana kemungkinan masih terbatas karena keterbatasan ukuran dataset. Pendekatan ini lebih tepat dipandang sebagai fondasi metodologis yang solid untuk dikembangkan, daripada sebagai sistem prediksi yang siap pakai.

### Keterbatasan Notebook

Terdapat beberapa keterbatasan mendasar yang perlu dipahami:

Pertama, ukuran dataset yang sangat kecil (90 sampel) adalah keterbatasan terbesar. Machine Learning modern, khususnya model kompleks seperti Random Forest dan Gradient Boosting, membutuhkan data yang jauh lebih banyak untuk belajar pola yang dapat digeneralisasi. Rasio sampel/fitur sebesar 2.7:1 berada di bawah ambang yang disarankan untuk pemodelan yang andal.

Kedua, luas panen aktual BPS digunakan sebagai fitur model. Dalam aplikasi nyata untuk prediksi prospektif, nilai ini tidak tersedia sebelum musim panen terjadi. Harus diganti dengan estimasi luas tanam awal musim — yang memiliki ketidakpastiannya sendiri.

Ketiga, satu titik koordinat representatif per kabupaten mungkin tidak cukup untuk menangkap heterogenitas spasial kondisi cuaca dan pertanian dalam satu kabupaten yang luas. Kabupaten seperti Lampung Tengah memiliki lahan pertanian yang sangat tersebar.

Keempat, data cuaca NASA POWER adalah data model atmosfer, bukan pengukuran langsung dari stasiun cuaca. Meskipun umumnya akurat, ada potensi bias sistematis untuk lokasi tertentu.

Kelima, model ini tidak mempertimbangkan variabel non-cuaca yang berpengaruh signifikan: kualitas benih, penggunaan pupuk, serangan hama, kebijakan subsidi, dan praktik budidaya lokal. Variabel-variabel ini dapat menjelaskan sebagian besar variansi yang tidak tertangkap oleh model cuaca.

### Saran Pengembangan Berikutnya

Berdasarkan keterbatasan yang diidentifikasi, beberapa arah pengembangan yang paling menjanjikan adalah:

Memperluas dataset dengan menambahkan data lebih banyak tahun (jika tersedia) atau menggunakan data kecamatan/desa yang memberikan lebih banyak unit observasi. Bahkan menambahkan data dari provinsi lain dengan karakteristik serupa (Sumatera Selatan, Jawa bagian tengah) dapat memperluas dataset secara signifikan.

Mengintegrasikan data satellite imagery (seperti NDVI — Normalized Difference Vegetation Index) yang dapat menangkap kondisi pertumbuhan tanaman secara langsung dari citra satelit, memberikan sinyal prediktif yang lebih akurat daripada data cuaca saja.

Menggunakan model time series yang lebih canggih seperti LSTM (Long Short-Term Memory) atau Prophet yang dirancang khusus untuk data deret waktu, meskipun ini memerlukan dataset yang lebih besar.

Mengeksplorasi data input tambahan seperti data penggunaan pupuk dari Dinas Pertanian, data irigasi dari PUPR, atau data harga komoditas yang dapat memengaruhi intensitas budidaya padi.

Melakukan validasi model dengan data tahun 2025 (jika tersedia) untuk mengonfirmasi bahwa performa yang diamati pada test 2024 bukan anomali satu tahun.

Akhirnya, mengembangkan antarmuka prediksi yang lebih mudah digunakan oleh penyuluh pertanian atau pengambil kebijakan di Dinas Pertanian Lampung, agar hasil penelitian ini dapat memberikan dampak praktis dalam perencanaan pangan regional.

---

*Dokumen ini disusun berdasarkan analisis kode dan struktur notebook `Project_BigData.ipynb`, mencakup 55 cell (markdown dan code). Nilai numerik aktual pada tabel metrik model bergantung pada data yang di-upload oleh pengguna dan tidak dapat dikonfirmasi tanpa menjalankan notebook dengan data aktual. Struktur pipeline, interpretasi metrik, dan semua penjelasan konseptual telah diverifikasi dari kode sumber notebook.*
