# Deployment Streamlit - Prediksi Padi Lampung

## 1. Tujuan Aplikasi

Aplikasi ini dibuat sebagai media demonstrasi project Big Data untuk analisis dan prediksi produktivitas serta produksi padi di 15 kabupaten/kota Provinsi Lampung. Dashboard menampilkan EDA, evaluasi model, ablation study, hasil prediksi final 2024, serta halaman coba model berbasis model final `Ridge Hist Lag`.

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
│   └── metadata.json
├── models/
│   └── ridge_hist_lag_model.joblib
└── utils/
    ├── data_loader.py
    ├── preprocessing.py
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

4. Jalankan seluruh notebook sampai cell akhir `Ekspor Artefak untuk Streamlit`.
5. Cell ekspor akan membuat atau memperbarui file di `streamlit_app/data` dan `streamlit_app/models`.

Catatan: aplikasi deployment tidak membaca Google Drive secara langsung. Google Drive hanya dipakai notebook untuk membangun artefak.

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
- `streamlit_app/models/ridge_hist_lag_model.joblib`

Jika salah satu file hilang, aplikasi akan menampilkan error artefak belum lengkap.

## 7. Fitur Dashboard

Halaman yang tersedia:

- **Beranda**: ringkasan project, metric cards, model final, dan posisi baseline.
- **Dashboard Analytical**: filter kabupaten/kota dan tahun, tren produktivitas, produksi, luas panen, perbandingan wilayah, dan eksplorasi cuaca.
- **Model dan Evaluasi**: tabel WFV, grafik MAPE, fold-level metrics, evaluasi final 2024, ablation study, dan feature importance.
- **Coba Model**: input `prodvt_lag1`, `prodvt_roll2`, dan luas panen opsional untuk estimasi produksi.
- **Metodologi dan Batasan**: sumber data, pipeline, fitur musim tanam, model final, baseline, dan keterbatasan.

## 8. Fitur Coba Model

Model final `Ridge Hist Lag` hanya memakai dua fitur:

- `prodvt_lag1`: produktivitas tahun sebelumnya dalam ton/ha.
- `prodvt_roll2`: rata-rata produktivitas dua tahun terakhir dalam ton/ha.

Form tidak meminta input cuaca karena model final aktual tidak memakai fitur cuaca. Jika luas panen diisi, aplikasi menghitung:

```text
estimasi produksi = prediksi produktivitas x luas panen
```

## 9. Keterbatasan dan Interpretasi

Hasil harus dibaca secara hati-hati:

- `Ridge Hist Lag` adalah model machine learning terbaik berdasarkan notebook terbaru.
- Pada WFV, baseline overall terbaik adalah `Naive Roll2`.
- Pada test 2024, baseline `Naive Lag1` masih sedikit lebih baik daripada `Ridge Hist Lag`.
- Dataset efektif hanya 90 sampel, sehingga baseline temporal sangat kompetitif.
- Aplikasi ini adalah demonstrasi akademik, bukan sistem operasional prediksi pangan.
