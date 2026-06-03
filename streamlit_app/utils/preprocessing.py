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
