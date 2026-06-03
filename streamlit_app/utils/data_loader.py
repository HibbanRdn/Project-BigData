from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"
MODEL_DIR = APP_DIR / "models"


@st.cache_data(show_spinner=False)
def load_metadata() -> dict:
    path = DATA_DIR / "metadata.json"
    if not path.exists():
        raise FileNotFoundError(f"Metadata tidak ditemukan: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_processed_data() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "processed_data.csv")


@st.cache_data(show_spinner=False)
def load_weather_monthly() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "weather_monthly.csv")


@st.cache_data(show_spinner=False)
def load_rice_annual() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "rice_annual_clean.csv")


@st.cache_data(show_spinner=False)
def load_evaluation_results() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "evaluation_results.csv")


@st.cache_data(show_spinner=False)
def load_wfv_fold_results() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "wfv_fold_results.csv")


@st.cache_data(show_spinner=False)
def load_ablation_results() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "ablation_results.csv")


@st.cache_data(show_spinner=False)
def load_final_metrics() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "final_2024_metrics.csv")


@st.cache_data(show_spinner=False)
def load_prediction_results() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "prediction_results_2024.csv")


@st.cache_data(show_spinner=False)
def load_feature_importance() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "feature_importance.csv")


@st.cache_resource(show_spinner=False)
def load_model():
    path = MODEL_DIR / "ridge_hist_lag_model.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model tidak ditemukan: {path}")
    return joblib.load(path)


def verify_artifacts() -> list[str]:
    required = [
        DATA_DIR / "metadata.json",
        DATA_DIR / "processed_data.csv",
        DATA_DIR / "weather_monthly.csv",
        DATA_DIR / "rice_annual_clean.csv",
        DATA_DIR / "evaluation_results.csv",
        DATA_DIR / "wfv_fold_results.csv",
        DATA_DIR / "ablation_results.csv",
        DATA_DIR / "final_2024_metrics.csv",
        DATA_DIR / "prediction_results_2024.csv",
        DATA_DIR / "feature_importance.csv",
        MODEL_DIR / "ridge_hist_lag_model.joblib",
    ]
    return [str(path) for path in required if not path.exists()]
