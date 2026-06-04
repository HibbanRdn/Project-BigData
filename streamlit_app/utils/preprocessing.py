from __future__ import annotations

import numpy as np
import pandas as pd


def validate_prediction_inputs(prodvt_lag1: float, prodvt_roll2: float, luas_panen_ha: float | None) -> list[str]:
    errors: list[str] = []

    if prodvt_lag1 is None or np.isnan(prodvt_lag1):
        errors.append("Produktivitas tahun sebelumnya wajib diisi.")
    elif prodvt_lag1 <= 0:
        errors.append("Produktivitas tahun sebelumnya harus lebih dari 0 ton/ha.")
    elif prodvt_lag1 > 12:
        errors.append("Produktivitas tahun sebelumnya terlihat tidak realistis untuk satuan ton/ha.")

    if prodvt_roll2 is None or np.isnan(prodvt_roll2):
        errors.append("Rata-rata produktivitas dua tahun terakhir wajib diisi.")
    elif prodvt_roll2 <= 0:
        errors.append("Rata-rata produktivitas dua tahun terakhir harus lebih dari 0 ton/ha.")
    elif prodvt_roll2 > 12:
        errors.append("Rata-rata produktivitas dua tahun terakhir terlihat tidak realistis untuk satuan ton/ha.")

    if luas_panen_ha is not None:
        if np.isnan(luas_panen_ha):
            errors.append("Luas panen harus berupa angka.")
        elif luas_panen_ha < 0:
            errors.append("Luas panen tidak boleh negatif.")
        elif luas_panen_ha > 250_000:
            errors.append("Luas panen terlihat terlalu besar untuk level kabupaten.")

    return errors


def predict_productivity(model, prodvt_lag1: float, prodvt_roll2: float) -> float:
    features = pd.DataFrame(
        [{"prodvt_lag1": float(prodvt_lag1), "prodvt_roll2": float(prodvt_roll2)}],
        columns=["prodvt_lag1", "prodvt_roll2"],
    )
    pred = float(model.predict(features.values)[0])
    return max(pred, 0.0)


def validate_weather_prediction_inputs(values: dict[str, float], feature_metadata: list[dict]) -> list[str]:
    errors: list[str] = []
    metadata_by_feature = {item["feature"]: item for item in feature_metadata}
    for feature, value in values.items():
        metadata = metadata_by_feature.get(feature, {})
        label = metadata.get("label", feature)
        group = metadata.get("group", "")
        unit = metadata.get("unit", "")
        if value is None or not np.isfinite(float(value)):
            errors.append(f"{label} {group} wajib berupa angka yang valid.")
            continue
        observed_min = metadata.get("observed_min")
        observed_max = metadata.get("observed_max")
        if observed_min is not None and observed_max is not None:
            margin = max((observed_max - observed_min) * 0.35, 0.1)
            if value < observed_min - margin or value > observed_max + margin:
                errors.append(
                    f"{label} {group} ({value:.2f} {unit}) berada jauh di luar rentang data historis "
                    f"{observed_min:.2f}-{observed_max:.2f} {unit}."
                )
    return errors


def predict_weather_productivity(artifact: dict, values: dict[str, float]) -> float:
    features = artifact["features"]
    missing = [feature for feature in features if feature not in values]
    if missing:
        raise ValueError(f"Input model simulasi cuaca belum lengkap: {missing}")
    frame = pd.DataFrame([{feature: float(values[feature]) for feature in features}], columns=features)
    prediction = float(artifact["model"].predict(frame)[0])
    return max(prediction, 0.0)


def estimate_production(productivity_ton_per_ha: float, luas_panen_ha: float | None) -> float | None:
    if luas_panen_ha is None or luas_panen_ha <= 0:
        return None
    return productivity_ton_per_ha * luas_panen_ha


def latest_reference_values(df: pd.DataFrame, kabupaten: str) -> dict:
    subset = df[df["kabupaten"] == kabupaten].sort_values("tahun")
    if subset.empty:
        return {}
    row = subset.iloc[-1]
    return {
        "tahun": int(row["tahun"]),
        "prodvt_lag1": float(row["prodvt_lag1"]),
        "prodvt_roll2": float(row["prodvt_roll2"]),
        "luas_panen_ha": float(row["luas_panen_ha"]),
        "produktivitas_aktual": float(row["produktivitas_ton_per_ha"]),
    }


def weather_reference_values(reference_df: pd.DataFrame, kabupaten: str, features: list[str]) -> dict:
    subset = reference_df[reference_df["kabupaten"] == kabupaten]
    if subset.empty:
        return {}
    row = subset.iloc[0]
    result = {
        "tahun": int(row["tahun"]),
        "luas_panen_ha": float(row["luas_panen_ha"]),
        "produktivitas_aktual": float(row["produktivitas_ton_per_ha"]),
    }
    result.update({feature: float(row[feature]) for feature in features})
    return result
