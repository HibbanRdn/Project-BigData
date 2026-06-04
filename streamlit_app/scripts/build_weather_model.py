from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"
MODEL_DIR = APP_DIR / "models"

TARGET = "produktivitas_ton_per_ha"
MODEL_NAME = "Ridge Cuaca + Histori Ringkas"
MODEL_ROLE = "Model simulasi interaktif berbasis cuaca"
RIDGE_ALPHA = 30.0

SEASONS = ["utama", "gadu", "kemarau"]
WEATHER_FEATURES = [
    feature
    for season in SEASONS
    for feature in [
        f"PRECTOTCORR_{season}_sum",
        f"T2M_{season}_mean",
        f"RH2M_{season}_mean",
    ]
]
HISTORY_FEATURES = ["prodvt_lag1", "prodvt_roll2"]
MODEL_FEATURES = WEATHER_FEATURES + HISTORY_FEATURES

FEATURE_LABELS = {
    "PRECTOTCORR": ("Curah hujan", "mm/musim", 10.0),
    "T2M": ("Suhu rata-rata", "C", 0.1),
    "RH2M": ("Kelembapan rata-rata", "%", 0.5),
}
SEASON_LABELS = {
    "utama": "Musim Utama",
    "gadu": "Musim Gadu",
    "kemarau": "Musim Kemarau",
}


def mape(y_true, y_pred) -> float:
    denominator = np.clip(np.abs(np.asarray(y_true, dtype=float)), 1e-8, None)
    return float(np.mean(np.abs((np.asarray(y_true) - np.asarray(y_pred)) / denominator)) * 100)


def new_model() -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=RIDGE_ALPHA)),
        ]
    )


def metric_row(y_true, y_pred, evaluasi: str) -> dict:
    return {
        "Evaluasi": evaluasi,
        "Model": MODEL_NAME,
        "Peran": MODEL_ROLE,
        "Jumlah Fitur": len(MODEL_FEATURES),
        "RMSE (t/ha)": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAE (t/ha)": float(mean_absolute_error(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
        "MAPE (%)": mape(y_true, y_pred),
    }


def build_feature_metadata(df: pd.DataFrame) -> list[dict]:
    metadata = []
    for feature in MODEL_FEATURES:
        values = df[feature].astype(float)
        if feature.startswith("prodvt_"):
            label = "Produktivitas tahun sebelumnya" if feature == "prodvt_lag1" else "Rata-rata produktivitas dua tahun"
            group = "Histori Produktivitas"
            unit = "ton/ha"
            step = 0.01
        else:
            parameter, season, _ = feature.split("_", maxsplit=2)
            label, unit, step = FEATURE_LABELS[parameter]
            group = SEASON_LABELS[season]
        metadata.append(
            {
                "feature": feature,
                "label": label,
                "group": group,
                "unit": unit,
                "step": step,
                "observed_min": float(values.min()),
                "observed_max": float(values.max()),
                "observed_median": float(values.median()),
            }
        )
    return metadata


def main() -> None:
    df = pd.read_csv(DATA_DIR / "processed_data.csv")
    missing = [column for column in MODEL_FEATURES + [TARGET, "tahun", "kabupaten"] if column not in df.columns]
    if missing:
        raise ValueError(f"Kolom model cuaca tidak tersedia: {missing}")

    wfv_rows = []
    for year in range(2020, 2025):
        train_mask = df["tahun"] < year
        test_mask = df["tahun"] == year
        model = new_model()
        model.fit(df.loc[train_mask, MODEL_FEATURES], df.loc[train_mask, TARGET])
        prediction = np.clip(model.predict(df.loc[test_mask, MODEL_FEATURES]), 0, None)
        row = metric_row(df.loc[test_mask, TARGET], prediction, f"WFV fold {year}")
        row["tahun_test"] = year
        wfv_rows.append(row)

    wfv_folds = pd.DataFrame(wfv_rows)
    wfv_summary = {
        "Evaluasi": "WFV 2020-2024",
        "Model": MODEL_NAME,
        "Peran": MODEL_ROLE,
        "Jumlah Fitur": len(MODEL_FEATURES),
        "RMSE (t/ha)": float(wfv_folds["RMSE (t/ha)"].mean()),
        "MAE (t/ha)": float(wfv_folds["MAE (t/ha)"].mean()),
        "R2": float(wfv_folds["R2"].mean()),
        "MAPE (%)": float(wfv_folds["MAPE (%)"].mean()),
        "MAPE std (%)": float(wfv_folds["MAPE (%)"].std(ddof=0)),
    }

    train_mask = df["tahun"] < 2024
    test_mask = df["tahun"] == 2024
    final_model = new_model()
    final_model.fit(df.loc[train_mask, MODEL_FEATURES], df.loc[train_mask, TARGET])
    final_prediction = np.clip(final_model.predict(df.loc[test_mask, MODEL_FEATURES]), 0, None)
    final_metrics = metric_row(df.loc[test_mask, TARGET], final_prediction, "Final test 2024")
    final_metrics["MAPE std (%)"] = np.nan

    deployment_model = new_model()
    deployment_model.fit(df[MODEL_FEATURES], df[TARGET])

    feature_metadata = build_feature_metadata(df)
    artifact = {
        "model": deployment_model,
        "model_name": MODEL_NAME,
        "model_role": MODEL_ROLE,
        "features": MODEL_FEATURES,
        "weather_features": WEATHER_FEATURES,
        "history_features": HISTORY_FEATURES,
        "target": TARGET,
        "ridge_alpha": RIDGE_ALPHA,
        "feature_metadata": feature_metadata,
        "evaluation": {
            "wfv_mape": wfv_summary["MAPE (%)"],
            "wfv_rmse": wfv_summary["RMSE (t/ha)"],
            "wfv_mae": wfv_summary["MAE (t/ha)"],
            "wfv_r2": wfv_summary["R2"],
            "final_2024_mape": final_metrics["MAPE (%)"],
            "final_2024_rmse": final_metrics["RMSE (t/ha)"],
            "final_2024_mae": final_metrics["MAE (t/ha)"],
            "final_2024_r2": final_metrics["R2"],
        },
    }

    reference_columns = ["kabupaten", "tahun", "luas_panen_ha", TARGET] + MODEL_FEATURES
    references = (
        df.sort_values(["kabupaten", "tahun"])
        .groupby("kabupaten", as_index=False)
        .tail(1)[reference_columns]
        .sort_values("kabupaten")
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_DIR / "weather_interactive_model.joblib")
    pd.DataFrame([wfv_summary, final_metrics]).to_csv(DATA_DIR / "weather_model_metrics.csv", index=False)
    wfv_folds.to_csv(DATA_DIR / "weather_model_wfv_folds.csv", index=False)
    references.to_csv(DATA_DIR / "weather_reference_values.csv", index=False)
    (DATA_DIR / "weather_model_metadata.json").write_text(
        json.dumps(
            {
                "model_name": MODEL_NAME,
                "model_role": MODEL_ROLE,
                "features": MODEL_FEATURES,
                "weather_features": WEATHER_FEATURES,
                "history_features": HISTORY_FEATURES,
                "target": TARGET,
                "ridge_alpha": RIDGE_ALPHA,
                "feature_metadata": feature_metadata,
                "evaluation": artifact["evaluation"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Model: {MODEL_NAME}")
    print(f"Fitur: {len(MODEL_FEATURES)}")
    print(f"WFV MAPE: {wfv_summary['MAPE (%)']:.4f}%")
    print(f"Final 2024 MAPE: {final_metrics['MAPE (%)']:.4f}%")


if __name__ == "__main__":
    main()
