# Refactor Notes – Prediksi Padi Lampung v3-2

Dokumen ini mencatat perubahan teknis yang diterapkan pada notebook `notebook/Prediksi_Padi_Lampung_v3-2.ipynb` setelah review metodologi, data pipeline, dan machine-learning pipeline.

## Priority Analysis Before Refactor

### High Priority

1. **Validitas input data upload manual**
   - Workflow `files.upload()` tetap dipertahankan untuk Google Colab.
   - Risiko awal: notebook dapat berjalan dengan jumlah file salah, ekstensi salah, atau nama JSON tidak cocok dengan mapping kabupaten.

2. **Quality gate dataset**
   - Risiko awal: parsing BPS/NASA dapat menghasilkan data tidak lengkap tanpa menghentikan pipeline.
   - Dampak: hasil model dapat terlihat valid padahal kabupaten/tahun/tanggal tidak lengkap.

3. **Evaluasi metodologis terhadap baseline**
   - Risiko awal: model ML dapat dipilih sebagai “terbaik” di antara model ML walaupun tidak melampaui baseline historis kabupaten.
   - Dampak: kesimpulan penelitian terlalu kuat dibanding evidence.

4. **Ablation study**
   - Risiko awal: tidak jelas apakah cuaca, luas panen, atau OHE kabupaten yang benar-benar memberi kontribusi.
   - Dampak: interpretasi feature importance dapat misleading.

5. **Residual analysis**
   - Risiko awal: evaluasi terlalu bergantung pada MAPE/R² agregat.
   - Dampak: bias over-prediction/under-prediction per kabupaten tidak terlihat.

### Medium Priority

1. **Reproducibility runtime**
   - Menghapus instalasi dependency yang tidak dipakai.
   - Menetapkan `RANDOM_STATE` global.

2. **Output management**
   - Risiko awal: visualisasi disimpan ke working directory, bukan folder hasil yang konsisten.
   - Solusi: helper `save_figure()` ke `results/Images`.

3. **Time-aware missing handling**
   - Risiko awal: median bulanan seluruh periode dapat memakai informasi masa depan jika missing muncul.
   - Solusi: imputasi historis kabupaten-bulan dengan fallback yang dilaporkan.

## Change Documentation

### Problem

Notebook menerima upload manual tanpa validasi ketat.

### Why It Matters

Satu file cuaca yang hilang atau salah nama dapat mengurangi jumlah kabupaten dan mengubah distribusi data, tetapi error tersebut sulit terlihat bila pipeline tetap berjalan.

### Fix Applied

Ditambahkan `validate_uploaded_files()`, `canonical_upload_stem()`, validasi jumlah file, ekstensi, dan stem file JSON terhadap mapping kabupaten.

### Expected Impact

Kesalahan input terdeteksi lebih awal dan eksperimen lebih defensible tanpa menghapus workflow upload manual Colab.

---

### Problem

Dataset BPS dan NASA POWER belum memiliki quality gate formal setelah parsing.

### Why It Matters

Model regresi tahunan sangat sensitif terhadap missing key kabupaten-tahun dan duplicate key. Error kecil dapat mengubah 90 sampel final secara signifikan.

### Fix Applied

Ditambahkan validasi schema BPS, jumlah baris expected, key uniqueness, nilai positif luas/produksi, konsistensi parameter NASA, rentang tanggal harian, dan jumlah baris harian expected.

### Expected Impact

Pipeline berhenti lebih cepat bila data tidak sesuai asumsi metodologis.

---

### Problem

Imputasi median bulanan berpotensi memakai informasi masa depan jika pada data update muncul missing value.

### Why It Matters

Untuk eksperimen temporal, preprocessing yang melihat seluruh periode dapat menciptakan leakage walaupun model split sudah walk-forward.

### Fix Applied

Imputasi diubah menjadi median historis kabupaten-bulan berdasarkan urutan tanggal; fallback median kabupaten-bulan hanya dipakai jika tidak ada histori sebelumnya dan dilaporkan.

### Expected Impact

Preprocessing lebih selaras dengan desain temporal dan lebih aman untuk update data masa depan.

---

### Problem

Kontribusi kelompok fitur belum diuji secara eksplisit.

### Why It Matters

Dengan dataset kecil dan baseline kabupaten kuat, feature importance saja tidak cukup untuk menyatakan bahwa fitur cuaca memberi nilai prediktif.

### Fix Applied

Ditambahkan ablation study Ridge Regression untuk empat feature set: cuaca saja, cuaca + luas panen, cuaca + kabupaten, dan full feature set.

### Expected Impact

Kesimpulan model dapat membedakan kontribusi fitur dan tidak hanya bergantung pada performa full model.

---

### Problem

Evaluasi final belum menampilkan arah bias prediksi.

### Why It Matters

MAPE tinggi/rendah tidak menunjukkan apakah model sistematis overestimate atau underestimate pada kabupaten tertentu.

### Fix Applied

Ditambahkan residual produktivitas, signed percentage error produksi, dan visualisasi `residual_analysis_2024.png`.

### Expected Impact

Error analysis lebih informatif untuk diagnosis model dan diskusi akademik.
