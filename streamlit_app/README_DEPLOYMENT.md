# Deployment Streamlit - Prediksi Padi Lampung

## 1. Tujuan Aplikasi

Aplikasi ini dibuat sebagai media demonstrasi project Big Data untuk analisis dan prediksi produktivitas serta produksi padi di 15 kabupaten/kota Provinsi Lampung. Dashboard menampilkan EDA, evaluasi model, ablation study, hasil prediksi final 2024, serta dua mode prediksi interaktif:

- `Ridge Cuaca + Histori Ringkas` untuk simulasi kondisi cuaca musiman.
- `Ridge Hist Lag` sebagai pembanding berbasis histori produktivitas.

## 2. Struktur Folder

```text
streamlit_app/
├── app.py
├── requirements.txt
├── README_DEPLOYMENT.md
├── assets/
├── data/
│   ├── processed_data.csv
│   ├── weather_monthly.csv
│   ├── rice_annual_clean.csv
│   ├── evaluation_results.csv
│   ├── wfv_fold_results.csv
│   ├── ablation_results.csv
│   ├── final_2024_metrics.csv
│   ├── prediction_results_2024.csv
│   ├── feature_importance.csv
│   ├── weather_model_metadata.json
│   ├── weather_model_metrics.csv
│   ├── weather_model_wfv_folds.csv
│   ├── weather_reference_values.csv
│   └── metadata.json
├── models/
│   ├── ridge_hist_lag_model.joblib
│   └── weather_interactive_model.joblib
├── scripts/
│   └── build_weather_model.py
└── utils/
    ├── data_loader.py
    ├── preprocessing.py
    ├── ui_components.py
    └── visualization.py
```

## 3. Cara Menghasilkan Artefak dari Notebook

Notebook revisi berada di:

```text
notebook/Project_BigData_Drive_Streamlit.ipynb
```

Langkah di Google Colab:

1. Upload atau buka notebook tersebut di Google Colab.
2. Jalankan cell mount Google Drive:

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. Pastikan struktur dataset tersedia di:

   ```text
   /content/drive/MyDrive/Dataset-BigData/
   ├── Padi/PadiTahunan.csv
   └── Cuaca/*.json
   ```

4. Jalankan seluruh notebook sampai bagian `Model Deployment Interaktif Berbasis Cuaca`.
5. Jalankan cell ekspor artefak model utama dan model simulasi cuaca.
6. Cell ekspor akan membuat atau memperbarui file di `streamlit_app/data` dan `streamlit_app/models`.

Catatan: aplikasi deployment tidak membaca Google Drive secara langsung. Google Drive hanya dipakai notebook untuk membangun artefak.

Model simulasi cuaca juga dapat dibangun ulang secara lokal dari `processed_data.csv` tanpa mengakses dataset mentah:

```bash
cd "/Users/muhamadhibbanramadhan/Documents/Big Data/streamlit_app"
python scripts/build_weather_model.py
```

## 4. Cara Menjalankan Lokal

Dari folder aplikasi:

```bash
cd "/Users/muhamadhibbanramadhan/Documents/Big Data/streamlit_app"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Jika dependencies sudah terpasang secara global, cukup:

```bash
cd "/Users/muhamadhibbanramadhan/Documents/Big Data/streamlit_app"
streamlit run app.py
```

## 5. Cara Deploy ke Streamlit Community Cloud

1. Push repository ke GitHub.
2. Pastikan folder `streamlit_app` ikut terunggah lengkap dengan:
   - `app.py`
   - `requirements.txt`
   - folder `data/`
   - folder `models/`
   - folder `utils/`
3. Di Streamlit Community Cloud, pilih repository dan set main file path:

   ```text
   streamlit_app/app.py
   ```

4. Streamlit akan memasang dependencies dari `streamlit_app/requirements.txt`.

Tidak perlu credential Google Drive, token, atau mount akun pribadi.

## 6. File yang Wajib Ada Saat Deployment

Minimal file berikut harus tersedia:

- `streamlit_app/data/processed_data.csv`
- `streamlit_app/data/weather_monthly.csv`
- `streamlit_app/data/evaluation_results.csv`
- `streamlit_app/data/wfv_fold_results.csv`
- `streamlit_app/data/ablation_results.csv`
- `streamlit_app/data/final_2024_metrics.csv`
- `streamlit_app/data/prediction_results_2024.csv`
- `streamlit_app/data/metadata.json`
- `streamlit_app/data/weather_model_metadata.json`
- `streamlit_app/data/weather_model_metrics.csv`
- `streamlit_app/data/weather_model_wfv_folds.csv`
- `streamlit_app/data/weather_reference_values.csv`
- `streamlit_app/models/ridge_hist_lag_model.joblib`
- `streamlit_app/models/weather_interactive_model.joblib`

Jika salah satu file hilang, aplikasi akan menampilkan error artefak belum lengkap.

## 7. Fitur Dashboard

Halaman yang tersedia:

- **Beranda**: ringkasan project, metric cards, model final, dan posisi baseline.
- **Dashboard Analytical**: filter kabupaten/kota dan tahun, tren produktivitas, produksi, luas panen, perbandingan wilayah, dan eksplorasi cuaca.
- **Model dan Evaluasi**: tabel WFV, grafik MAPE, fold-level metrics, evaluasi final 2024, ablation study, dan feature importance.
- **Coba Model**: simulasi cuaca musiman sebagai mode utama dan model historis sebagai pembanding.
- **Metodologi dan Batasan**: sumber data, pipeline, fitur musim tanam, model final, baseline, dan keterbatasan.

## 8. Fitur Coba Model

### Simulasi Berbasis Cuaca

Model `Ridge Cuaca + Histori Ringkas` benar-benar memakai sebelas fitur:

- Total curah hujan, suhu rata-rata, dan kelembapan rata-rata untuk musim utama.
- Total curah hujan, suhu rata-rata, dan kelembapan rata-rata untuk musim gadu.
- Total curah hujan, suhu rata-rata, dan kelembapan rata-rata untuk musim kemarau.
- `prodvt_lag1` dan `prodvt_roll2`.

Model menggunakan pipeline `StandardScaler` dan `Ridge(alpha=30.0)`. Evaluasi aktualnya adalah MAPE WFV `8.18%` dan MAPE final 2024 `6.56%`. Model ini disediakan untuk simulasi interaktif, bukan diklaim sebagai model dengan performa terbaik.

### Model Historis / Pembanding

Model `Ridge Hist Lag` hanya memakai dua fitur:

- `prodvt_lag1`: produktivitas tahun sebelumnya dalam ton/ha.
- `prodvt_roll2`: rata-rata produktivitas dua tahun terakhir dalam ton/ha.

Jika luas panen diisi pada salah satu mode, aplikasi menghitung:

```text
estimasi produksi = prediksi produktivitas x luas panen
```

## 9. Keterbatasan dan Interpretasi

Hasil harus dibaca secara hati-hati:

- `Ridge Hist Lag` adalah model machine learning terbaik berdasarkan notebook terbaru.
- `Ridge Cuaca + Histori Ringkas` adalah model simulasi interaktif dengan performa lebih rendah daripada model historis terbaik.
- Pada WFV, baseline overall terbaik adalah `Naive Roll2`.
- Pada test 2024, baseline `Naive Lag1` masih sedikit lebih baik daripada `Ridge Hist Lag`.
- Dataset efektif hanya 90 sampel, sehingga baseline temporal sangat kompetitif.
- Aplikasi ini adalah demonstrasi akademik, bukan sistem operasional prediksi pangan.
