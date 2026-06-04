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
            ("Model ML Final", meta["model_ml_terbaik"], "Model machine learning terbaik pada WFV."),
            ("MAPE ML Final", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
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
                        "Interpretasi akademik",
                        "Model ML dipakai sebagai model final demonstrasi, tetapi klaim performa tetap dibandingkan "
                        "secara terbuka terhadap baseline temporal.",
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
        "tetap ditampilkan sebagai pembanding utama karena performanya sangat kompetitif.",
        tone="warning",
    )

    metric_cards(
        [
            ("ML Terbaik WFV", meta["model_ml_terbaik"], "Model ML terbaik berdasarkan rata-rata MAPE WFV."),
            ("Overall Terbaik WFV", meta["model_overall_terbaik_wfv"], "Model terbaik termasuk baseline."),
            ("Baseline Final", meta["baseline_final_terbaik"], "Baseline terbaik pada test 2024."),
            ("MAPE ML Final", fmt_pct(meta["mape_model_final_2024"]), "MAPE Ridge Hist Lag pada test 2024."),
            ("MAPE Baseline Final", fmt_pct(meta["mape_baseline_final_2024"]), "MAPE baseline terbaik pada test 2024."),
        ]
    )

    sorted_eval = eval_df.sort_values("MAPE mean (%)").copy()
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

    with st.container(border=True):
        section_title("MAPE per Fold Walk-Forward Validation", "Pola performa tiap tahun test pada skema temporal.")
        st.plotly_chart(
            line_chart(
                wfv_df,
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

    final_show = final_metrics_df.copy()
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
        "Simulasi prediksi produktivitas memakai model final Ridge Hist Lag dengan fitur historis produktivitas.",
    )

    model = load_model()
    kabupaten_options = sorted(df["kabupaten"].unique())

    col_form, col_result = st.columns([0.92, 1.08], gap="large")
    with col_form:
        with st.container(border=True):
            section_title("Input Model", "Model final membaca prodvt_lag1 dan prodvt_roll2.")
            selected_kab = st.selectbox("Kabupaten/kota referensi", kabupaten_options)
            ref = latest_reference_values(df, selected_kab)

            if ref:
                callout(
                    "Nilai referensi terakhir",
                    f"Referensi <strong>{selected_kab}</strong>: data terakhir {int(ref['tahun'])}, "
                    f"produktivitas aktual <strong>{ref['produktivitas_aktual']:.3f} ton/ha</strong>.",
                    tone="info",
                )

            with st.form("prediction_form"):
                prodvt_lag1 = st.number_input(
                    "Produktivitas tahun sebelumnya - prodvt_lag1 (ton/ha)",
                    min_value=0.0,
                    max_value=12.0,
                    value=round(ref.get("prodvt_lag1", 5.0), 3),
                    step=0.01,
                )
                prodvt_roll2 = st.number_input(
                    "Rata-rata produktivitas dua tahun terakhir - prodvt_roll2 (ton/ha)",
                    min_value=0.0,
                    max_value=12.0,
                    value=round(ref.get("prodvt_roll2", 5.0), 3),
                    step=0.01,
                )
                use_area = st.checkbox("Hitung estimasi produksi dari luas panen", value=True)
                luas_panen = st.number_input(
                    "Luas panen (ha)",
                    min_value=0.0,
                    max_value=250000.0,
                    value=round(ref.get("luas_panen_ha", 0.0), 2),
                    step=100.0,
                    disabled=not use_area,
                )
                submitted = st.form_submit_button("Jalankan Prediksi", type="primary")

    with col_result:
        with st.container(border=True):
            section_title("Hasil Prediksi", "Output dihitung dengan artefak model lokal, bukan rumus dashboard terpisah.")
            tag_row(["Ridge Hist Lag", "prodvt_lag1", "prodvt_roll2", "ton/ha"])

            if submitted:
                errors = validate_prediction_inputs(prodvt_lag1, prodvt_roll2, luas_panen if use_area else None)
                if errors:
                    for error in errors:
                        st.error(error)
                    return

                pred = predict_productivity(model, prodvt_lag1, prodvt_roll2)
                production = estimate_production(pred, luas_panen if use_area else None)
                result_card(
                    "Prediksi produktivitas",
                    f"{pred:.3f} ton/ha",
                    "Nilai ini adalah output model Ridge Hist Lag untuk kombinasi fitur historis yang dimasukkan.",
                )
                metric_items = [
                    ("Input Lag1", f"{prodvt_lag1:.3f} ton/ha", "Produktivitas tahun sebelumnya."),
                    ("Input Roll2", f"{prodvt_roll2:.3f} ton/ha", "Rata-rata dua tahun terakhir."),
                ]
                if production is not None:
                    metric_items.append(("Estimasi Produksi", f"{production:,.0f} ton", "Prediksi produktivitas x luas panen."))
                metric_cards(metric_items)
            else:
                callout(
                    "Belum ada prediksi",
                    "Sesuaikan nilai input di sebelah kiri, lalu tekan <strong>Jalankan Prediksi</strong>. "
                    "Nilai default berasal dari referensi historis kabupaten/kota yang dipilih.",
                    tone="info",
                )

            callout(
                "Catatan akademik",
                "Form ini tidak meminta input cuaca karena model final yang dipilih dari notebook adalah Ridge Hist Lag "
                "dengan fitur historis produktivitas. Prediksi bersifat demonstrasi dan bergantung pada pola historis data.",
                tone="warning",
            )


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
            ("Model Final", meta["model_ml_terbaik"], "Model ML final berbasis fitur historis."),
            ("Fitur Final", ", ".join(meta["fitur_final"]), "Input model prediksi Streamlit."),
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
                ("Modeling", "Membandingkan model ML dengan baseline temporal seperti Naive Lag1 dan Naive Roll2."),
                ("Evaluasi", "Menggunakan Walk-Forward Validation 2020-2024 dan final test tahun 2024."),
                ("Ekspor artefak", "Menyimpan processed data, hasil evaluasi, prediksi 2024, dan model joblib."),
                ("Deployment", "Streamlit membaca artefak lokal tanpa akses Google Drive pribadi."),
            ]
        )

    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        with st.container(border=True):
            section_title("Model Final", "Interpretasi model yang dipakai pada halaman prediksi.")
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
                    ("Form prediksi", "Model final tidak membaca input cuaca langsung pada halaman Coba Model."),
                ]
            )

    callout(
        "Interpretasi akhir",
        "Ridge Hist Lag layak dipakai sebagai model ML final demonstrasi. Namun baseline temporal tetap harus dibahas "
        "karena pada beberapa evaluasi menghasilkan MAPE lebih rendah daripada model ML.",
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
