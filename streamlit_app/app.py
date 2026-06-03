from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Prediksi Padi Lampung",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.data_loader import (
    load_ablation_results,
    load_evaluation_results,
    load_feature_importance,
    load_final_metrics,
    load_metadata,
    load_model,
    load_prediction_results,
    load_processed_data,
    load_rice_annual,
    load_weather_monthly,
    load_wfv_fold_results,
    verify_artifacts,
)
from utils.preprocessing import (
    estimate_production,
    latest_reference_values,
    predict_productivity,
    validate_prediction_inputs,
)
from utils.visualization import bar_chart, line_chart, prediction_vs_actual, scatter_chart


st.markdown(
    """
    <style>
    .main .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    .metric-card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 14px 16px;
        background: #ffffff;
    }
    .small-note {color: #4b5563; font-size: 0.92rem;}
    .method-box {
        border-left: 4px solid #2563eb;
        background: #f8fafc;
        padding: 12px 16px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def fmt_num(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


@st.cache_data(show_spinner=False)
def load_all_data():
    missing = verify_artifacts()
    if missing:
        raise FileNotFoundError("Artefak deployment belum lengkap:\n" + "\n".join(missing))
    return {
        "metadata": load_metadata(),
        "processed": load_processed_data(),
        "weather": load_weather_monthly(),
        "rice": load_rice_annual(),
        "eval": load_evaluation_results(),
        "wfv": load_wfv_fold_results(),
        "ablation": load_ablation_results(),
        "final_metrics": load_final_metrics(),
        "predictions": load_prediction_results(),
        "importance": load_feature_importance(),
    }


try:
    data = load_all_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

meta = data["metadata"]
df = data["processed"]
weather = data["weather"]
rice = data["rice"]
eval_df = data["eval"]
wfv_df = data["wfv"]
ablation_df = data["ablation"]
final_metrics_df = data["final_metrics"]
pred_df = data["predictions"]
importance_df = data["importance"]


st.sidebar.title("Prediksi Padi Lampung")
page = st.sidebar.radio(
    "Navigasi",
    [
        "Beranda",
        "Dashboard Analytical",
        "Model dan Evaluasi",
        "Coba Model",
        "Metodologi dan Batasan",
    ],
)
st.sidebar.caption("Data deployment dibaca dari artefak lokal, bukan Google Drive pribadi.")


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value, help=help_text)


def page_home():
    st.title("Prediksi Produktivitas dan Produksi Padi Provinsi Lampung")
    st.caption("Machine Learning berbasis musim tanam, fitur historis produktivitas, dan evaluasi temporal 2019-2024.")

    metric_row(
        [
            ("Kabupaten/kota", f"{meta['n_kabupaten']}", "Jumlah wilayah Lampung yang dianalisis."),
            ("Periode fitur", f"{meta['tahun_min']}-{meta['tahun_max']}", "Periode sampel model setelah feature engineering."),
            ("Sampel model", f"{meta['n_samples']}", "15 kabupaten/kota x 6 tahun."),
            ("Model ML final", meta["model_ml_terbaik"], "Model machine learning terbaik berdasarkan WFV."),
            ("MAPE final ML", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
        ]
    )

    st.markdown(
        """
        <div class="method-box">
        Project ini memprediksi produktivitas padi dalam satuan ton/ha. Estimasi produksi dihitung sebagai turunan
        dari prediksi produktivitas dikalikan luas panen. Sumber data utama adalah BPS untuk produksi dan luas panen,
        serta NASA POWER untuk cuaca harian yang diagregasi menjadi fitur musim tanam.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.1, 0.9])
    with left:
        prod_by_year = (
            df.groupby("tahun", as_index=False)
            .agg(
                produktivitas_ton_per_ha=("produktivitas_ton_per_ha", "mean"),
                produksi_ton=("produksi_ton", "sum"),
                luas_panen_ha=("luas_panen_ha", "sum"),
            )
        )
        st.plotly_chart(
            line_chart(
                prod_by_year,
                "tahun",
                "produktivitas_ton_per_ha",
                None,
                "Rata-rata Produktivitas Padi Lampung",
                {"tahun": "Tahun", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)"},
            ),
            width="stretch",
        )
    with right:
        st.subheader("Ringkasan Hasil")
        st.write(
            f"Model ML terbaik adalah **{meta['model_ml_terbaik']}** dengan MAPE final "
            f"**{fmt_pct(meta['mape_model_final_2024'])}** pada test 2024."
        )
        st.write(
            f"Baseline final terbaik adalah **{meta['baseline_final_terbaik']}** dengan MAPE "
            f"**{fmt_pct(meta['mape_baseline_final_2024'])}**. Ini berarti baseline temporal masih menjadi pembanding kuat."
        )
        st.write(
            f"Pada WFV, model overall terbaik adalah **{meta['model_overall_terbaik_wfv']}**."
        )


def page_dashboard():
    st.title("Dashboard Analytical")
    st.caption("Eksplorasi produktivitas, produksi, luas panen, dan fitur cuaca musiman.")

    kabupaten_options = sorted(df["kabupaten"].unique())
    selected_kab = st.sidebar.multiselect("Filter kabupaten/kota", kabupaten_options, default=kabupaten_options[:5])
    min_year, max_year = int(df["tahun"].min()), int(df["tahun"].max())
    year_range = st.sidebar.slider("Rentang tahun", min_year, max_year, (min_year, max_year), step=1)
    if not selected_kab:
        st.warning("Pilih minimal satu kabupaten/kota.")
        return

    filtered = df[df["kabupaten"].isin(selected_kab) & df["tahun"].between(year_range[0], year_range[1])]

    metric_row(
        [
            ("Sampel terpilih", f"{len(filtered)}", "Jumlah baris kabupaten-tahun setelah filter."),
            ("Rata-rata produktivitas", f"{filtered['produktivitas_ton_per_ha'].mean():.2f} ton/ha", "Mean produktivitas filter aktif."),
            ("Total produksi", f"{filtered['produksi_ton'].sum()/1000:,.1f} ribu ton", "Akumulasi produksi pada filter aktif."),
            ("Total luas panen", f"{filtered['luas_panen_ha'].sum()/1000:,.1f} ribu ha", "Akumulasi luas panen pada filter aktif."),
        ]
    )

    tab1, tab2, tab3 = st.tabs(["Tren Padi", "Perbandingan Wilayah", "Cuaca dan Musim Tanam"])
    with tab1:
        st.plotly_chart(
            line_chart(
                filtered,
                "tahun",
                "produktivitas_ton_per_ha",
                "kabupaten",
                "Tren Produktivitas per Kabupaten",
                {"tahun": "Tahun", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)", "kabupaten": "Kabupaten"},
            ),
            width="stretch",
        )
        col1, col2 = st.columns(2)
        col1.plotly_chart(
            line_chart(
                filtered,
                "tahun",
                "produksi_ton",
                "kabupaten",
                "Tren Produksi per Kabupaten",
                {"tahun": "Tahun", "produksi_ton": "Produksi (ton)", "kabupaten": "Kabupaten"},
            ),
            width="stretch",
        )
        col2.plotly_chart(
            line_chart(
                filtered,
                "tahun",
                "luas_panen_ha",
                "kabupaten",
                "Tren Luas Panen per Kabupaten",
                {"tahun": "Tahun", "luas_panen_ha": "Luas panen (ha)", "kabupaten": "Kabupaten"},
            ),
            width="stretch",
        )

    with tab2:
        summary = (
            filtered.groupby("kabupaten", as_index=False)
            .agg(
                produktivitas_ton_per_ha=("produktivitas_ton_per_ha", "mean"),
                produksi_ton=("produksi_ton", "mean"),
                luas_panen_ha=("luas_panen_ha", "mean"),
            )
            .sort_values("produktivitas_ton_per_ha", ascending=False)
        )
        st.plotly_chart(
            bar_chart(
                summary,
                "kabupaten",
                "produktivitas_ton_per_ha",
                "Rata-rata Produktivitas antar Kabupaten",
                {"kabupaten": "Kabupaten", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)"},
            ),
            width="stretch",
        )
        st.dataframe(summary, width="stretch", hide_index=True)

    with tab3:
        weather_filtered = weather[
            weather["kabupaten"].isin(selected_kab) & weather["tahun"].between(year_range[0] - 1, year_range[1])
        ]
        weather_param = st.selectbox(
            "Variabel cuaca bulanan",
            ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M", "ALLSKY_SFC_SW_DWN"],
            format_func={
                "PRECTOTCORR": "Curah hujan (mm/bulan)",
                "T2M": "Suhu rata-rata (C)",
                "T2M_MAX": "Suhu maksimum (C)",
                "T2M_MIN": "Suhu minimum (C)",
                "RH2M": "Kelembapan (%)",
                "ALLSKY_SFC_SW_DWN": "Radiasi matahari (MJ/m2/hari)",
            }.get,
        )
        weather_month = (
            weather_filtered.groupby(["tahun", "bulan"], as_index=False)[weather_param]
            .mean()
            .sort_values(["tahun", "bulan"])
        )
        weather_month["periode"] = weather_month["tahun"].astype(str) + "-" + weather_month["bulan"].astype(str).str.zfill(2)
        st.plotly_chart(
            line_chart(
                weather_month,
                "periode",
                weather_param,
                None,
                "Rata-rata Cuaca Bulanan pada Filter Aktif",
                {"periode": "Periode", weather_param: "Nilai"},
            ),
            width="stretch",
        )
        seasonal_cols = [c for c in df.columns if any(token in c for token in ["_utama_", "_gadu_", "_kemarau_"])]
        selected_feature = st.selectbox("Fitur cuaca musiman", seasonal_cols, index=seasonal_cols.index("PRECTOTCORR_utama_sum"))
        st.plotly_chart(
            scatter_chart(
                filtered,
                selected_feature,
                "produktivitas_ton_per_ha",
                "kabupaten",
                "Hubungan Fitur Cuaca Musiman dan Produktivitas",
                {selected_feature: selected_feature, "produktivitas_ton_per_ha": "Produktivitas (ton/ha)", "kabupaten": "Kabupaten"},
            ),
            width="stretch",
        )


def page_model():
    st.title("Model dan Evaluasi")
    st.caption("Perbandingan model ML, baseline temporal, WFV, ablation study, dan evaluasi final 2024.")

    metric_row(
        [
            ("ML terbaik WFV", meta["model_ml_terbaik"], "Model ML terbaik berdasarkan rata-rata MAPE WFV."),
            ("Overall terbaik WFV", meta["model_overall_terbaik_wfv"], "Model terbaik termasuk baseline."),
            ("Baseline final terbaik", meta["baseline_final_terbaik"], "Baseline terbaik pada test 2024."),
            ("MAPE ML final", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
            ("MAPE baseline final", fmt_pct(meta["mape_baseline_final_2024"]), "MAPE baseline terbaik pada test 2024."),
        ]
    )

    st.subheader("Walk-Forward Validation")
    col1, col2 = st.columns([1.05, 0.95])
    with col1:
        sorted_eval = eval_df.sort_values("MAPE mean (%)")
        st.plotly_chart(
            bar_chart(
                sorted_eval,
                "Model",
                "MAPE mean (%)",
                "Rata-rata MAPE WFV 2020-2024",
                {"Model": "Model", "MAPE mean (%)": "MAPE (%)"},
                color="Model",
            ),
            width="stretch",
        )
    with col2:
        st.dataframe(
            sorted_eval.style.format(
                {
                    "RMSE mean": "{:.4f}",
                    "RMSE std": "{:.4f}",
                    "MAE mean": "{:.4f}",
                    "R2 mean": "{:.4f}",
                    "MAPE mean (%)": "{:.2f}",
                    "MAPE std (%)": "{:.2f}",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    st.plotly_chart(
        line_chart(
            wfv_df,
            "tahun_test",
            "MAPE",
            "Model",
            "MAPE per Fold Walk-Forward Validation",
            {"tahun_test": "Tahun test", "MAPE": "MAPE (%)", "Model": "Model"},
        ),
        width="stretch",
    )

    st.subheader("Evaluasi Final Tahun 2024")
    col3, col4 = st.columns([1, 1])
    with col3:
        st.dataframe(
            final_metrics_df.style.format(
                {"RMSE (t/ha)": "{:.4f}", "MAE (t/ha)": "{:.4f}", "R2": "{:.4f}", "R²": "{:.4f}", "MAPE (%)": "{:.2f}"}
            ),
            width="stretch",
            hide_index=True,
        )
        st.info(
            "Pada test 2024, Ridge Hist Lag adalah model ML final, tetapi Naive Lag1 masih memiliki MAPE lebih rendah. "
            "Karena itu aplikasi menampilkan baseline sebagai pembanding utama, bukan sekadar catatan tambahan."
        )
    with col4:
        st.plotly_chart(prediction_vs_actual(pred_df), width="stretch")

    st.subheader("Ablation Study")
    col5, col6 = st.columns([1.05, 0.95])
    with col5:
        st.plotly_chart(
            bar_chart(
                ablation_df.sort_values("MAPE mean (%)"),
                "Feature Set",
                "MAPE mean (%)",
                "Kontribusi Kelompok Fitur terhadap MAPE",
                {"Feature Set": "Feature Set", "MAPE mean (%)": "MAPE (%)"},
            ),
            width="stretch",
        )
    with col6:
        st.dataframe(ablation_df, width="stretch", hide_index=True)

    st.subheader("Feature Importance Model Final")
    st.plotly_chart(
        bar_chart(
            importance_df.sort_values("importance", ascending=True),
            "importance",
            "feature",
            "Koefisien Absolut Ridge Hist Lag",
            {"importance": "Importance", "feature": "Fitur"},
            orientation="h",
        ),
        width="stretch",
    )


def page_predict():
    st.title("Coba Model Prediksi")
    st.caption("Model final menggunakan dua fitur historis: prodvt_lag1 dan prodvt_roll2.")

    model = load_model()
    kabupaten_options = sorted(df["kabupaten"].unique())
    selected_kab = st.selectbox("Kabupaten/kota referensi", kabupaten_options)
    ref = latest_reference_values(df, selected_kab)

    st.write(
        "Pilihan kabupaten digunakan untuk mengisi nilai referensi historis terakhir. "
        "Model final Ridge Hist Lag sendiri hanya membaca dua fitur produktivitas historis."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        prodvt_lag1 = st.number_input(
            "Produktivitas tahun sebelumnya (ton/ha)",
            min_value=0.0,
            max_value=12.0,
            value=round(ref.get("prodvt_lag1", 5.0), 3),
            step=0.01,
        )
    with col2:
        prodvt_roll2 = st.number_input(
            "Rata-rata produktivitas dua tahun terakhir (ton/ha)",
            min_value=0.0,
            max_value=12.0,
            value=round(ref.get("prodvt_roll2", 5.0), 3),
            step=0.01,
        )
    with col3:
        use_area = st.checkbox("Hitung estimasi produksi", value=True)
        luas_panen = st.number_input(
            "Luas panen (ha)",
            min_value=0.0,
            max_value=250000.0,
            value=round(ref.get("luas_panen_ha", 0.0), 2),
            step=100.0,
            disabled=not use_area,
        )

    if ref:
        st.caption(
            f"Referensi {selected_kab}: data terakhir {ref['tahun']}, "
            f"produktivitas aktual {ref['produktivitas_aktual']:.3f} ton/ha."
        )

    errors = validate_prediction_inputs(prodvt_lag1, prodvt_roll2, luas_panen if use_area else None)
    if errors:
        for error in errors:
            st.warning(error)
        return

    pred = predict_productivity(model, prodvt_lag1, prodvt_roll2)
    production = estimate_production(pred, luas_panen if use_area else None)

    metric_items = [
        ("Prediksi produktivitas", f"{pred:.3f} ton/ha", "Output model Ridge Hist Lag."),
        ("Input lag1", f"{prodvt_lag1:.3f} ton/ha", "Produktivitas tahun sebelumnya."),
        ("Input roll2", f"{prodvt_roll2:.3f} ton/ha", "Rata-rata dua tahun terakhir."),
    ]
    if production is not None:
        metric_items.append(("Estimasi produksi", f"{production:,.0f} ton", "Produktivitas prediksi x luas panen."))
    metric_row(metric_items)

    st.info(
        "Prediksi ini bersifat demonstrasi akademik. Model tidak membaca input cuaca pada form ini karena model final "
        "yang dipilih dari notebook adalah Ridge Hist Lag dengan fitur historis produktivitas."
    )


def page_methodology():
    st.title("Metodologi dan Batasan")

    st.subheader("Sumber Data")
    st.write(
        "Data produksi dan luas panen berasal dari BPS Provinsi Lampung. Data cuaca harian berasal dari NASA POWER "
        "untuk enam parameter meteorologi: radiasi matahari, suhu rata-rata, suhu maksimum, suhu minimum, kelembapan, "
        "dan curah hujan."
    )

    st.subheader("Pipeline Analisis")
    st.markdown(
        """
        1. Validasi struktur data padi dan cuaca.
        2. Parsing data BPS dari format lebar menjadi format kabupaten-tahun.
        3. Parsing JSON NASA POWER dan konversi sentinel seperti -999 menjadi nilai hilang.
        4. Agregasi cuaca harian menjadi bulanan.
        5. Rekayasa fitur musim tanam: utama, gadu, dan kemarau.
        6. Penggabungan dengan produksi dan luas panen, lalu perhitungan target produktivitas.
        7. Penambahan fitur historis produktivitas: lag1, rolling 2 tahun, rolling 3 tahun.
        8. Evaluasi model menggunakan Walk-Forward Validation 2020-2024.
        """
    )

    st.subheader("Model Final")
    st.write(
        f"Model ML final adalah **{meta['model_ml_terbaik']}** dengan fitur {', '.join(meta['fitur_final'])}. "
        f"MAPE final model pada test 2024 adalah **{fmt_pct(meta['mape_model_final_2024'])}**."
    )
    st.write(
        f"Baseline final terbaik adalah **{meta['baseline_final_terbaik']}** dengan MAPE "
        f"**{fmt_pct(meta['mape_baseline_final_2024'])}**. Ini perlu ditampilkan karena baseline temporal masih sangat kompetitif."
    )

    st.subheader("Batasan")
    st.markdown(
        """
        - Dataset efektif hanya 90 sampel, sehingga model kompleks mudah overfit.
        - Luas panen aktual tersedia di data historis, tetapi dalam prediksi prospektif harus diganti estimasi luas tanam/panen.
        - Satu titik cuaca representatif per kabupaten belum menangkap heterogenitas spasial seluruh wilayah.
        - Model final menggunakan fitur historis, bukan input cuaca langsung pada form prediksi.
        - Aplikasi deployment memakai artefak lokal dan tidak mengakses Google Drive pribadi.
        """
    )


if page == "Beranda":
    page_home()
elif page == "Dashboard Analytical":
    page_dashboard()
elif page == "Model dan Evaluasi":
    page_model()
elif page == "Coba Model":
    page_predict()
else:
    page_methodology()
