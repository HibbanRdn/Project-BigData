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
    load_weather_model,
    load_weather_model_metadata,
    load_weather_model_metrics,
    load_weather_model_wfv_folds,
    load_weather_reference_values,
    load_wfv_fold_results,
    verify_artifacts,
)
from utils.preprocessing import (
    estimate_production,
    latest_reference_values,
    predict_productivity,
    predict_weather_productivity,
    validate_prediction_inputs,
    validate_weather_prediction_inputs,
    weather_reference_values,
)
from utils.ui_components import (
    apply_theme,
    callout,
    hero,
    insight_cards,
    metric_cards,
    page_heading,
    pipeline,
    render_sidebar,
    result_card,
    section_title,
    tag_row,
)
from utils.visualization import bar_chart, line_chart, prediction_vs_actual, scatter_chart


CHART_CONFIG = {"displayModeBar": False, "responsive": True}

apply_theme()


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def fmt_num(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def model_category(model_name: str) -> str:
    if model_name == weather_model_meta.get("model_name"):
        return "Model simulasi cuaca"
    return "Baseline temporal" if model_name.startswith("Naive") else "Machine learning"


@st.cache_data(show_spinner=False)
def load_all_data():
    missing = verify_artifacts()
    if missing:
        raise FileNotFoundError("Artefak deployment belum lengkap:\n" + "\n".join(missing))
    return {
        "metadata": load_metadata(),
        "processed": load_processed_data(),
        "weather": load_weather_monthly(),
        "weather_model_metadata": load_weather_model_metadata(),
        "weather_model_metrics": load_weather_model_metrics(),
        "weather_model_wfv": load_weather_model_wfv_folds(),
        "weather_references": load_weather_reference_values(),
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
weather_model_meta = data["weather_model_metadata"]
weather_model_metrics = data["weather_model_metrics"]
weather_model_wfv = data["weather_model_wfv"]
weather_references = data["weather_references"]
rice = data["rice"]
eval_df = data["eval"]
wfv_df = data["wfv"]
ablation_df = data["ablation"]
final_metrics_df = data["final_metrics"]
pred_df = data["predictions"]
importance_df = data["importance"]
weather_wfv_summary = weather_model_metrics.loc[weather_model_metrics["Evaluasi"] == "WFV 2020-2024"].iloc[0]
weather_final_summary = weather_model_metrics.loc[weather_model_metrics["Evaluasi"] == "Final test 2024"].iloc[0]

page = render_sidebar(meta)


def page_home():
    hero(
        "Prediksi Produktivitas dan Produksi Padi Provinsi Lampung",
        "Analisis temporal produktivitas padi berdasarkan data BPS dan cuaca NASA POWER periode 2019-2024.",
    )

    metric_cards(
        [
            ("Kabupaten/Kota", f"{meta['n_kabupaten']}", "Cakupan wilayah Lampung yang dianalisis."),
            ("Periode Analisis", f"{meta['tahun_min']}-{meta['tahun_max']}", "Sampel tahunan hasil feature engineering."),
            ("Sampel Tahunan", f"{meta['n_samples']}", "15 wilayah dikalikan 6 tahun observasi."),
        ]
    )

    metric_cards(
        [
            ("Model Performa Terbaik", meta["model_ml_terbaik"], "Model ML berbasis histori terbaik pada WFV."),
            ("MAPE Histori Final", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
            ("Model Simulasi Interaktif", weather_model_meta["model_name"], "Model deployment yang benar-benar membaca cuaca."),
            ("MAPE Simulasi Final", fmt_pct(weather_final_summary["MAPE (%)"]), "MAPE model simulasi cuaca pada test 2024."),
        ]
    )

    callout(
        "Konteks analisis",
        "Project ini memprediksi produktivitas padi dalam satuan <strong>ton/ha</strong>. Estimasi produksi dihitung "
        "sebagai turunan dari prediksi produktivitas dikalikan luas panen. Data padi bersumber dari BPS, sedangkan "
        "cuaca harian NASA POWER diagregasi menjadi fitur musim tanam.",
        tone="success",
    )

    prod_by_year = (
        df.groupby("tahun", as_index=False)
        .agg(
            produktivitas_ton_per_ha=("produktivitas_ton_per_ha", "mean"),
            produksi_ton=("produksi_ton", "sum"),
            luas_panen_ha=("luas_panen_ha", "sum"),
        )
        .sort_values("tahun")
    )
    first_year = prod_by_year.iloc[0]
    last_year = prod_by_year.iloc[-1]
    delta_prod = last_year["produktivitas_ton_per_ha"] - first_year["produktivitas_ton_per_ha"]

    left, right = st.columns([1.18, 0.82], gap="large")
    with left:
        with st.container(border=True):
            section_title(
                "Rata-rata Produktivitas Padi Lampung",
                "Tren agregat seluruh kabupaten/kota pada data model.",
            )
            st.plotly_chart(
                line_chart(
                    prod_by_year,
                    "tahun",
                    "produktivitas_ton_per_ha",
                    None,
                    "Rata-rata Produktivitas Padi Lampung",
                    {"tahun": "Tahun", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)"},
                    height=420,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )
            callout(
                "Catatan tren",
                f"Rata-rata produktivitas bergerak dari <strong>{first_year['produktivitas_ton_per_ha']:.2f} ton/ha</strong> "
                f"pada {int(first_year['tahun'])} menjadi <strong>{last_year['produktivitas_ton_per_ha']:.2f} ton/ha</strong> "
                f"pada {int(last_year['tahun'])}. Perubahan bersihnya sekitar <strong>{delta_prod:+.2f} ton/ha</strong>.",
            )
    with right:
        with st.container(border=True):
            section_title(
                "Ringkasan Hasil",
                "Angka utama dipertahankan sesuai artefak evaluasi terakhir.",
            )
            insight_cards(
                [
                    (
                        "Model ML terbaik",
                        f"<strong>{meta['model_ml_terbaik']}</strong> mencatat MAPE final 2024 "
                        f"<strong>{fmt_pct(meta['mape_model_final_2024'])}</strong>.",
                    ),
                    (
                        "Baseline final terbaik",
                        f"<strong>{meta['baseline_final_terbaik']}</strong> mencatat MAPE "
                        f"<strong>{fmt_pct(meta['mape_baseline_final_2024'])}</strong> pada test 2024.",
                    ),
                    (
                        "Walk-forward validation",
                        f"Metode overall terbaik pada WFV adalah <strong>{meta['model_overall_terbaik_wfv']}</strong>, "
                        "sehingga baseline temporal tetap menjadi pembanding penting.",
                    ),
                    (
                        "Model simulasi cuaca",
                        f"<strong>{weather_model_meta['model_name']}</strong> memakai 9 fitur cuaca musiman dan 2 fitur "
                        f"histori, dengan MAPE WFV <strong>{fmt_pct(weather_wfv_summary['MAPE (%)'])}</strong>.",
                    ),
                    (
                        "Perbedaan tujuan",
                        "Ridge Hist Lag dipertahankan sebagai model ML dengan performa terbaik. Model simulasi cuaca "
                        "disediakan agar pengguna dapat menguji perubahan kondisi musim secara nyata.",
                    ),
                ]
            )


def page_dashboard():
    page_heading(
        "Exploratory data analysis",
        "Dashboard Analytical",
        "Eksplorasi produktivitas, produksi, luas panen, dan fitur cuaca musiman pada data Lampung.",
    )

    kabupaten_options = sorted(df["kabupaten"].unique())
    min_year, max_year = int(df["tahun"].min()), int(df["tahun"].max())

    with st.container(border=True):
        section_title("Filter Analisis", "Gunakan filter ini untuk menyesuaikan wilayah dan periode grafik.")
        col_filter_1, col_filter_2 = st.columns([1.45, 0.55], gap="large")
        with col_filter_1:
            selected_kab = st.multiselect(
                "Kabupaten/kota",
                kabupaten_options,
                default=kabupaten_options[:5],
                help="Pilih satu atau beberapa wilayah Lampung.",
            )
        with col_filter_2:
            year_range = st.slider(
                "Rentang tahun",
                min_year,
                max_year,
                (min_year, max_year),
                step=1,
                help="Filter tahun sampel model.",
            )

    if not selected_kab:
        st.warning("Pilih minimal satu kabupaten/kota agar visualisasi dapat ditampilkan.")
        return

    filtered = df[df["kabupaten"].isin(selected_kab) & df["tahun"].between(year_range[0], year_range[1])]
    best_area = (
        filtered.groupby("kabupaten")["produktivitas_ton_per_ha"].mean().sort_values(ascending=False).index[0]
        if not filtered.empty
        else "-"
    )

    metric_cards(
        [
            ("Sampel Terpilih", f"{len(filtered)}", "Jumlah baris kabupaten-tahun setelah filter."),
            ("Rata-rata Produktivitas", f"{filtered['produktivitas_ton_per_ha'].mean():.2f} ton/ha", "Mean produktivitas filter aktif."),
            ("Total Produksi", f"{filtered['produksi_ton'].sum()/1000:,.1f} ribu ton", "Akumulasi produksi pada filter aktif."),
            ("Total Luas Panen", f"{filtered['luas_panen_ha'].sum()/1000:,.1f} ribu ha", "Akumulasi luas panen pada filter aktif."),
            ("Wilayah Tertinggi", best_area, "Rata-rata produktivitas tertinggi pada filter aktif."),
        ]
    )

    tab1, tab2, tab3 = st.tabs(["Tren Padi", "Perbandingan Wilayah", "Cuaca dan Musim Tanam"])
    with tab1:
        with st.container(border=True):
            section_title("Tren Produktivitas per Kabupaten", "Satuan produktivitas: ton/ha.")
            st.plotly_chart(
                line_chart(
                    filtered,
                    "tahun",
                    "produktivitas_ton_per_ha",
                    "kabupaten",
                    "Tren Produktivitas per Kabupaten",
                    {"tahun": "Tahun", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)", "kabupaten": "Kabupaten"},
                    height=430,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )
        col1, col2 = st.columns(2, gap="large")
        with col1:
            with st.container(border=True):
                section_title("Tren Produksi", "Satuan produksi: ton.")
                st.plotly_chart(
                    line_chart(
                        filtered,
                        "tahun",
                        "produksi_ton",
                        "kabupaten",
                        "Tren Produksi per Kabupaten",
                        {"tahun": "Tahun", "produksi_ton": "Produksi (ton)", "kabupaten": "Kabupaten"},
                        height=360,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )
        with col2:
            with st.container(border=True):
                section_title("Tren Luas Panen", "Satuan luas panen: ha.")
                st.plotly_chart(
                    line_chart(
                        filtered,
                        "tahun",
                        "luas_panen_ha",
                        "kabupaten",
                        "Tren Luas Panen per Kabupaten",
                        {"tahun": "Tahun", "luas_panen_ha": "Luas panen (ha)", "kabupaten": "Kabupaten"},
                        height=360,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
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
        left, right = st.columns([1.2, 0.8], gap="large")
        with left:
            with st.container(border=True):
                section_title("Rata-rata Produktivitas antar Kabupaten", "Perbandingan wilayah pada filter aktif.")
                st.plotly_chart(
                    bar_chart(
                        summary,
                        "kabupaten",
                        "produktivitas_ton_per_ha",
                        "Rata-rata Produktivitas antar Kabupaten",
                        {"kabupaten": "Kabupaten", "produktivitas_ton_per_ha": "Produktivitas (ton/ha)"},
                        height=430,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )
        with right:
            with st.container(border=True):
                section_title("Ringkasan Wilayah", "Tabel diurutkan dari produktivitas tertinggi.")
                st.dataframe(
                    summary.style.format(
                        {
                            "produktivitas_ton_per_ha": "{:.3f}",
                            "produksi_ton": "{:,.0f}",
                            "luas_panen_ha": "{:,.0f}",
                        }
                    ),
                    width="stretch",
                    hide_index=True,
                )

    with tab3:
        weather_filtered = weather[
            weather["kabupaten"].isin(selected_kab) & weather["tahun"].between(year_range[0] - 1, year_range[1])
        ]
        weather_labels = {
            "PRECTOTCORR": "Curah hujan (mm/bulan)",
            "T2M": "Suhu rata-rata (C)",
            "T2M_MAX": "Suhu maksimum (C)",
            "T2M_MIN": "Suhu minimum (C)",
            "RH2M": "Kelembapan (%)",
            "ALLSKY_SFC_SW_DWN": "Radiasi matahari (MJ/m2/hari)",
        }
        with st.container(border=True):
            section_title("Parameter Cuaca", "Pilih variabel bulanan dan fitur musim tanam yang ingin dibandingkan.")
            col_weather_1, col_weather_2 = st.columns(2, gap="large")
            with col_weather_1:
                weather_param = st.selectbox(
                    "Variabel cuaca bulanan",
                    list(weather_labels.keys()),
                    format_func=weather_labels.get,
                )
            with col_weather_2:
                seasonal_cols = [c for c in df.columns if any(token in c for token in ["_utama_", "_gadu_", "_kemarau_"])]
                selected_feature = st.selectbox(
                    "Fitur cuaca musiman",
                    seasonal_cols,
                    index=seasonal_cols.index("PRECTOTCORR_utama_sum"),
                )

        weather_month = (
            weather_filtered.groupby(["tahun", "bulan"], as_index=False)[weather_param]
            .mean()
            .sort_values(["tahun", "bulan"])
        )
        weather_month["periode"] = weather_month["tahun"].astype(str) + "-" + weather_month["bulan"].astype(str).str.zfill(2)
        corr_value = filtered[[selected_feature, "produktivitas_ton_per_ha"]].corr(numeric_only=True).iloc[0, 1]

        col_weather_chart, col_weather_scatter = st.columns(2, gap="large")
        with col_weather_chart:
            with st.container(border=True):
                section_title("Rata-rata Cuaca Bulanan", weather_labels[weather_param])
                st.plotly_chart(
                    line_chart(
                        weather_month,
                        "periode",
                        weather_param,
                        None,
                        "Rata-rata Cuaca Bulanan pada Filter Aktif",
                        {"periode": "Periode", weather_param: "Nilai"},
                        height=390,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )
        with col_weather_scatter:
            with st.container(border=True):
                section_title("Hubungan Cuaca dan Produktivitas", f"Korelasi Pearson pada filter aktif: {corr_value:.3f}.")
                st.plotly_chart(
                    scatter_chart(
                        filtered,
                        selected_feature,
                        "produktivitas_ton_per_ha",
                        "kabupaten",
                        "Hubungan Fitur Cuaca Musiman dan Produktivitas",
                        {
                            selected_feature: selected_feature,
                            "produktivitas_ton_per_ha": "Produktivitas (ton/ha)",
                            "kabupaten": "Kabupaten",
                        },
                        height=390,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )


def page_model():
    page_heading(
        "Model evaluation",
        "Model dan Evaluasi",
        "Perbandingan model machine learning, baseline temporal, WFV, ablation study, dan final test 2024.",
    )

    callout(
        "Prinsip interpretasi",
        "Aplikasi menampilkan <strong>Ridge Hist Lag</strong> sebagai model machine learning final, tetapi baseline temporal "
        "tetap ditampilkan sebagai pembanding utama karena performanya sangat kompetitif. "
        "<strong>Ridge Cuaca + Histori Ringkas</strong> ditampilkan terpisah sebagai model simulasi interaktif.",
        tone="warning",
    )

    metric_cards(
        [
            ("ML Terbaik WFV", meta["model_ml_terbaik"], "Model ML terbaik berdasarkan rata-rata MAPE WFV."),
            ("Overall Terbaik WFV", meta["model_overall_terbaik_wfv"], "Model terbaik termasuk baseline."),
            ("Model Simulasi Cuaca", weather_model_meta["model_name"], "Model yang dipakai pada simulasi kondisi cuaca."),
            ("MAPE ML Final", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
            ("MAPE Simulasi Final", fmt_pct(weather_final_summary["MAPE (%)"]), "MAPE model simulasi cuaca pada test 2024."),
        ]
    )

    weather_eval_row = pd.DataFrame(
        [
            {
                "Model": weather_model_meta["model_name"],
                "RMSE mean": weather_wfv_summary["RMSE (t/ha)"],
                "RMSE std": float("nan"),
                "MAE mean": weather_wfv_summary["MAE (t/ha)"],
                "R2 mean": weather_wfv_summary["R2"],
                "MAPE mean (%)": weather_wfv_summary["MAPE (%)"],
                "MAPE std (%)": weather_wfv_summary["MAPE std (%)"],
            }
        ]
    )
    sorted_eval = pd.concat([eval_df, weather_eval_row], ignore_index=True).sort_values("MAPE mean (%)").copy()
    sorted_eval["Kategori"] = sorted_eval["Model"].map(model_category)

    col1, col2 = st.columns([1.08, 0.92], gap="large")
    with col1:
        with st.container(border=True):
            section_title("Walk-Forward Validation", "Rata-rata MAPE 2020-2024, semakin kecil semakin baik.")
            st.plotly_chart(
                bar_chart(
                    sorted_eval,
                    "Model",
                    "MAPE mean (%)",
                    "Rata-rata MAPE WFV 2020-2024",
                    {"Model": "Model", "MAPE mean (%)": "MAPE (%)", "Kategori": "Kategori"},
                    color="Kategori",
                    height=430,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )
    with col2:
        with st.container(border=True):
            section_title("Tabel Evaluasi WFV", "Model diberi kategori agar baseline dan ML mudah dibedakan.")
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

    weather_wfv_plot = weather_model_wfv[["tahun_test", "MAPE (%)"]].rename(columns={"MAPE (%)": "MAPE"})
    weather_wfv_plot["Model"] = weather_model_meta["model_name"]
    all_wfv_plot = pd.concat([wfv_df, weather_wfv_plot], ignore_index=True)

    with st.container(border=True):
        section_title("MAPE per Fold Walk-Forward Validation", "Pola performa tiap tahun test pada skema temporal.")
        st.plotly_chart(
            line_chart(
                all_wfv_plot,
                "tahun_test",
                "MAPE",
                "Model",
                "MAPE per Fold Walk-Forward Validation",
                {"tahun_test": "Tahun test", "MAPE": "MAPE (%)", "Model": "Model"},
                height=430,
            ),
            width="stretch",
            config=CHART_CONFIG,
        )

    weather_final_row = pd.DataFrame(
        [
            {
                "Model": weather_model_meta["model_name"],
                "RMSE (t/ha)": weather_final_summary["RMSE (t/ha)"],
                "MAE (t/ha)": weather_final_summary["MAE (t/ha)"],
                "R²": weather_final_summary["R2"],
                "MAPE (%)": weather_final_summary["MAPE (%)"],
            }
        ]
    )
    final_show = pd.concat([final_metrics_df, weather_final_row], ignore_index=True).sort_values("MAPE (%)")
    final_show["Kategori"] = final_show["Model"].map(model_category)
    col3, col4 = st.columns([0.95, 1.05], gap="large")
    with col3:
        with st.container(border=True):
            section_title("Evaluasi Final Tahun 2024", "Test terakhir yang menjadi ringkasan performa final.")
            st.dataframe(
                final_show.style.format(
                    {"RMSE (t/ha)": "{:.4f}", "MAE (t/ha)": "{:.4f}", "R2": "{:.4f}", "R²": "{:.4f}", "MAPE (%)": "{:.2f}"}
                ),
                width="stretch",
                hide_index=True,
            )
            callout(
                "Pembacaan hasil",
                "Pada test 2024, <strong>Ridge Hist Lag</strong> adalah model ML final. Namun <strong>Naive Lag1</strong> "
                "memiliki MAPE lebih rendah, sehingga baseline temporal tetap menjadi pembanding yang kuat.",
                tone="warning",
            )
    with col4:
        with st.container(border=True):
            section_title("Prediksi vs Aktual 2024", "Titik semakin dekat ke garis putus-putus berarti semakin akurat.")
            st.plotly_chart(prediction_vs_actual(pred_df), width="stretch", config=CHART_CONFIG)

    col5, col6 = st.columns([1.05, 0.95], gap="large")
    with col5:
        with st.container(border=True):
            section_title("Ablation Study", "Kontribusi kelompok fitur terhadap MAPE WFV.")
            st.plotly_chart(
                bar_chart(
                    ablation_df.sort_values("MAPE mean (%)"),
                    "Feature Set",
                    "MAPE mean (%)",
                    "Kontribusi Kelompok Fitur terhadap MAPE",
                    {"Feature Set": "Feature Set", "MAPE mean (%)": "MAPE (%)"},
                    height=430,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )
    with col6:
        with st.container(border=True):
            section_title("Tabel Ablation", "Semakin rendah MAPE, semakin baik.")
            st.dataframe(
                ablation_df.style.format({"MAPE mean (%)": "{:.2f}", "MAPE std (%)": "{:.2f}", "RMSE mean": "{:.4f}", "R2 mean": "{:.4f}"}),
                width="stretch",
                hide_index=True,
            )

    with st.container(border=True):
        section_title("Feature Importance Model Final", "Koefisien absolut Ridge Hist Lag pada dua fitur historis.")
        st.plotly_chart(
            bar_chart(
                importance_df.sort_values("importance", ascending=True),
                "importance",
                "feature",
                "Koefisien Absolut Ridge Hist Lag",
                {"importance": "Importance", "feature": "Fitur"},
                orientation="h",
                height=320,
            ),
            width="stretch",
            config=CHART_CONFIG,
        )


def page_predict():
    page_heading(
        "Interactive prediction",
        "Coba Model",
        "Simulasikan produktivitas dari kondisi cuaca musiman, atau bandingkan dengan model historis Ridge Hist Lag.",
    )

    historical_model = load_model()
    weather_artifact = load_weather_model()
    kabupaten_options = sorted(df["kabupaten"].unique())
    weather_tab, historical_tab = st.tabs(["Simulasi Berbasis Cuaca", "Model Historis / Pembanding"])

    with weather_tab:
        metric_cards(
            [
                ("Model Simulasi", weather_model_meta["model_name"], "Model deployment yang benar-benar membaca input cuaca."),
                ("Komposisi Fitur", "9 cuaca + 2 histori", "Tiga parameter cuaca pada tiga musim tanam."),
                ("MAPE WFV", fmt_pct(weather_wfv_summary["MAPE (%)"]), "Walk-forward validation 2020-2024."),
                ("MAPE Final 2024", fmt_pct(weather_final_summary["MAPE (%)"]), "Performa final model simulasi cuaca."),
            ]
        )
        callout(
            "Cara membaca mode ini",
            "Kabupaten/kota hanya digunakan untuk mengisi nilai referensi terbaru. Prediksi benar-benar dihitung dari "
            "<strong>curah hujan, suhu rata-rata, kelembapan tiga musim, prodvt_lag1, dan prodvt_roll2</strong>. "
            "Luas panen hanya dipakai untuk menghitung estimasi produksi setelah produktivitas diprediksi.",
            tone="success",
        )

        weather_form_col, weather_result_col = st.columns([1.15, 0.85], gap="large")
        with weather_form_col:
            with st.container(border=True):
                section_title("Input Kondisi Cuaca", "Nilai default berasal dari observasi terbaru wilayah referensi.")
                selected_weather_kab = st.selectbox(
                    "Kabupaten/kota referensi",
                    kabupaten_options,
                    key="weather_reference_kabupaten",
                )
                weather_ref = weather_reference_values(
                    weather_references,
                    selected_weather_kab,
                    weather_artifact["features"],
                )
                callout(
                    "Referensi aktif",
                    f"<strong>{selected_weather_kab}</strong>, data {weather_ref['tahun']}. Produktivitas aktual referensi "
                    f"<strong>{weather_ref['produktivitas_aktual']:.3f} ton/ha</strong>.",
                )

                feature_metadata = {item["feature"]: item for item in weather_artifact["feature_metadata"]}
                weather_values = {}
                with st.form("weather_prediction_form"):
                    for group in ["Musim Utama", "Musim Gadu", "Musim Kemarau"]:
                        st.markdown(f"#### {group}")
                        group_features = [
                            item["feature"]
                            for item in weather_artifact["feature_metadata"]
                            if item["group"] == group
                        ]
                        input_columns = st.columns(3, gap="small")
                        for input_col, feature in zip(input_columns, group_features):
                            item = feature_metadata[feature]
                            observed_range = item["observed_max"] - item["observed_min"]
                            margin = max(observed_range * 0.35, item["step"])
                            min_value = max(0.0, item["observed_min"] - margin)
                            max_value = item["observed_max"] + margin
                            weather_values[feature] = input_col.number_input(
                                f"{item['label']} ({item['unit']})",
                                min_value=float(min_value),
                                max_value=float(max_value),
                                value=float(weather_ref[feature]),
                                step=float(item["step"]),
                                format="%.2f",
                                key=f"weather_{feature}",
                                help=f"Rentang historis: {item['observed_min']:.2f}-{item['observed_max']:.2f} {item['unit']}.",
                            )

                    st.markdown("#### Histori Produktivitas")
                    hist_col_1, hist_col_2 = st.columns(2, gap="small")
                    weather_values["prodvt_lag1"] = hist_col_1.number_input(
                        "Produktivitas tahun sebelumnya (ton/ha)",
                        min_value=0.0,
                        max_value=12.0,
                        value=float(weather_ref["prodvt_lag1"]),
                        step=0.01,
                        format="%.3f",
                        key="weather_prodvt_lag1",
                    )
                    weather_values["prodvt_roll2"] = hist_col_2.number_input(
                        "Rata-rata produktivitas dua tahun (ton/ha)",
                        min_value=0.0,
                        max_value=12.0,
                        value=float(weather_ref["prodvt_roll2"]),
                        step=0.01,
                        format="%.3f",
                        key="weather_prodvt_roll2",
                    )

                    weather_use_area = st.checkbox(
                        "Hitung estimasi produksi dari luas panen",
                        value=True,
                        key="weather_use_area",
                    )
                    weather_area = st.number_input(
                        "Luas panen opsional (ha)",
                        min_value=0.0,
                        max_value=250000.0,
                        value=float(weather_ref["luas_panen_ha"]),
                        step=100.0,
                        disabled=not weather_use_area,
                        key="weather_area",
                        help="Tidak memengaruhi prediksi produktivitas; hanya digunakan untuk estimasi produksi.",
                    )
                    weather_submitted = st.form_submit_button("Jalankan Simulasi Cuaca", type="primary")

        with weather_result_col:
            with st.container(border=True):
                section_title("Hasil Simulasi Cuaca", "Inference memakai artefak weather_interactive_model.joblib.")
                tag_row(["Ridge", "3 musim tanam", "9 fitur cuaca", "2 fitur histori"])
                if weather_submitted:
                    weather_errors = validate_weather_prediction_inputs(
                        weather_values,
                        weather_artifact["feature_metadata"],
                    )
                    weather_errors.extend(
                        validate_prediction_inputs(
                            weather_values["prodvt_lag1"],
                            weather_values["prodvt_roll2"],
                            weather_area if weather_use_area else None,
                        )
                    )
                    if weather_errors:
                        for error in dict.fromkeys(weather_errors):
                            st.error(error)
                    else:
                        weather_prediction = predict_weather_productivity(weather_artifact, weather_values)
                        weather_production = estimate_production(
                            weather_prediction,
                            weather_area if weather_use_area else None,
                        )
                        result_card(
                            "Prediksi produktivitas berbasis cuaca",
                            f"{weather_prediction:.3f} ton/ha",
                            "Perubahan input cuaca dan histori pada form digunakan langsung sebagai feature vector model.",
                        )
                        weather_result_metrics = [
                            ("Model", weather_model_meta["model_name"], "Model simulasi cuaca deployment."),
                            ("MAPE WFV", fmt_pct(weather_wfv_summary["MAPE (%)"]), "Performa evaluasi temporal model."),
                        ]
                        if weather_production is not None:
                            weather_result_metrics.append(
                                ("Estimasi Produksi", f"{weather_production:,.0f} ton", "Prediksi produktivitas x luas panen.")
                            )
                        metric_cards(weather_result_metrics)
                else:
                    callout(
                        "Belum ada simulasi",
                        "Ubah satu atau beberapa kondisi musim di sebelah kiri, lalu tekan "
                        "<strong>Jalankan Simulasi Cuaca</strong>.",
                    )
                callout(
                    "Posisi metodologis",
                    f"Model simulasi cuaca memiliki MAPE WFV <strong>{fmt_pct(weather_wfv_summary['MAPE (%)'])}</strong>, "
                    f"lebih tinggi daripada Ridge Hist Lag. Model ini disediakan untuk eksplorasi kondisi cuaca, bukan "
                    "diklaim sebagai model dengan performa terbaik.",
                    tone="warning",
                )

    with historical_tab:
        callout(
            "Mode pembanding historis",
            "Ridge Hist Lag hanya menggunakan <strong>prodvt_lag1</strong> dan <strong>prodvt_roll2</strong>. "
            "Mode ini dipertahankan karena merupakan model ML dengan performa terbaik pada evaluasi utama.",
        )
        hist_form_col, hist_result_col = st.columns([0.92, 1.08], gap="large")
        with hist_form_col:
            with st.container(border=True):
                section_title("Input Model Historis", "Tidak menggunakan kondisi cuaca.")
                selected_hist_kab = st.selectbox(
                    "Kabupaten/kota referensi",
                    kabupaten_options,
                    key="historical_reference_kabupaten",
                )
                hist_ref = latest_reference_values(df, selected_hist_kab)
                with st.form("historical_prediction_form"):
                    hist_lag1 = st.number_input(
                        "Produktivitas tahun sebelumnya (ton/ha)",
                        min_value=0.0,
                        max_value=12.0,
                        value=round(hist_ref.get("prodvt_lag1", 5.0), 3),
                        step=0.01,
                        key="historical_lag1",
                    )
                    hist_roll2 = st.number_input(
                        "Rata-rata produktivitas dua tahun (ton/ha)",
                        min_value=0.0,
                        max_value=12.0,
                        value=round(hist_ref.get("prodvt_roll2", 5.0), 3),
                        step=0.01,
                        key="historical_roll2",
                    )
                    hist_use_area = st.checkbox("Hitung estimasi produksi", value=True, key="historical_use_area")
                    hist_area = st.number_input(
                        "Luas panen opsional (ha)",
                        min_value=0.0,
                        max_value=250000.0,
                        value=round(hist_ref.get("luas_panen_ha", 0.0), 2),
                        step=100.0,
                        disabled=not hist_use_area,
                        key="historical_area",
                    )
                    hist_submitted = st.form_submit_button("Jalankan Model Historis", type="primary")

        with hist_result_col:
            with st.container(border=True):
                section_title("Hasil Model Historis", "Output Ridge Hist Lag sebagai benchmark ML berbasis histori.")
                tag_row(["Ridge Hist Lag", "prodvt_lag1", "prodvt_roll2", "ton/ha"])
                if hist_submitted:
                    hist_errors = validate_prediction_inputs(hist_lag1, hist_roll2, hist_area if hist_use_area else None)
                    if hist_errors:
                        for error in hist_errors:
                            st.error(error)
                    else:
                        hist_prediction = predict_productivity(historical_model, hist_lag1, hist_roll2)
                        hist_production = estimate_production(hist_prediction, hist_area if hist_use_area else None)
                        result_card(
                            "Prediksi produktivitas historis",
                            f"{hist_prediction:.3f} ton/ha",
                            "Output Ridge Hist Lag berdasarkan pola produktivitas tahun sebelumnya.",
                        )
                        hist_metrics = [
                            ("MAPE Final 2024", fmt_pct(meta["mape_model_final_2024"]), "Performa final Ridge Hist Lag."),
                            ("MAPE WFV", fmt_pct(eval_df.loc[eval_df["Model"] == "Ridge Hist Lag", "MAPE mean (%)"].iloc[0]), "Evaluasi temporal."),
                        ]
                        if hist_production is not None:
                            hist_metrics.append(("Estimasi Produksi", f"{hist_production:,.0f} ton", "Prediksi x luas panen."))
                        metric_cards(hist_metrics)
                else:
                    callout("Belum ada prediksi", "Masukkan fitur histori lalu tekan <strong>Jalankan Model Historis</strong>.")


def page_methodology():
    page_heading(
        "Methodology",
        "Metodologi dan Batasan",
        "Ringkasan alur penelitian, sumber data, model final, validasi temporal, dan batasan interpretasi.",
    )

    metric_cards(
        [
            ("Sumber Padi", "BPS", "Produksi, luas panen, dan produktivitas kabupaten/kota."),
            ("Sumber Cuaca", "NASA POWER", "Data harian yang diagregasi menjadi fitur musim tanam."),
            ("Validasi", "WFV", "Walk-forward validation untuk menjaga urutan temporal."),
            ("Model Performa Terbaik", meta["model_ml_terbaik"], "Model ML terbaik berbasis fitur historis."),
            ("Model Simulasi", weather_model_meta["model_name"], "Model interaktif yang membaca kondisi cuaca."),
        ]
    )

    with st.container(border=True):
        section_title("Pipeline Analisis", "Alur dibuat ringkas agar mudah dipresentasikan.")
        pipeline(
            [
                ("Validasi data", "Memastikan struktur data padi dan cuaca tersedia untuk 15 kabupaten/kota."),
                ("Cleaning", "Parsing data BPS, parsing JSON NASA POWER, dan konversi sentinel -999 menjadi missing value."),
                ("Agregasi cuaca", "Cuaca harian digabung menjadi bulanan dan fitur musim tanam utama, gadu, kemarau."),
                ("Feature engineering", "Menghitung produktivitas serta fitur lag1, rolling 2 tahun, dan rolling 3 tahun."),
                ("Modeling", "Membandingkan ML, baseline temporal, dan model simulasi cuaca yang terpisah."),
                ("Evaluasi", "Menggunakan Walk-Forward Validation 2020-2024 dan final test tahun 2024."),
                ("Ekspor artefak", "Menyimpan processed data, hasil evaluasi, prediksi 2024, dan model joblib."),
                ("Deployment", "Streamlit membaca artefak lokal tanpa akses Google Drive pribadi."),
            ]
        )

    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        with st.container(border=True):
            section_title("Peran Model", "Model terbaik dan model simulasi memiliki tujuan yang berbeda.")
            insight_cards(
                [
                    (
                        "Model ML",
                        f"<strong>{meta['model_ml_terbaik']}</strong> menggunakan fitur "
                        f"<strong>{', '.join(meta['fitur_final'])}</strong>.",
                    ),
                    (
                        "MAPE final",
                        f"MAPE model ML pada test 2024 adalah <strong>{fmt_pct(meta['mape_model_final_2024'])}</strong>.",
                    ),
                    (
                        "Model simulasi cuaca",
                        f"<strong>{weather_model_meta['model_name']}</strong> memakai 9 fitur cuaca musiman dan 2 histori. "
                        f"MAPE WFV-nya <strong>{fmt_pct(weather_wfv_summary['MAPE (%)'])}</strong>.",
                    ),
                    (
                        "Baseline",
                        f"Baseline final terbaik adalah <strong>{meta['baseline_final_terbaik']}</strong> dengan MAPE "
                        f"<strong>{fmt_pct(meta['mape_baseline_final_2024'])}</strong>.",
                    ),
                ]
            )
    with col_right:
        with st.container(border=True):
            section_title("Batasan Penelitian", "Hal penting sebelum hasil dipakai di luar konteks akademik.")
            insight_cards(
                [
                    ("Ukuran data", "Dataset efektif hanya 90 sampel sehingga model kompleks mudah overfit."),
                    ("Luas panen", "Prediksi prospektif membutuhkan estimasi luas panen jika produksi ingin dihitung."),
                    ("Representasi cuaca", "Satu titik cuaca representatif per kabupaten belum menangkap variasi spasial detail."),
                    ("Simulasi cuaca", "Input cuaca adalah skenario agregat per musim, bukan prakiraan cuaca harian operasional."),
                ]
            )

    callout(
        "Interpretasi akhir",
        "Ridge Hist Lag tetap menjadi model ML dengan performa terbaik. Ridge Cuaca + Histori Ringkas disediakan sebagai "
        "model simulasi interaktif, sedangkan baseline temporal tetap harus dibahas karena menghasilkan MAPE yang kompetitif.",
        tone="warning",
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
