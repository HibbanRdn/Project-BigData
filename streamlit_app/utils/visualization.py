from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go


COLORWAY = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#4b5563"]


def line_chart(df, x, y, color, title, labels):
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title, labels=labels, color_discrete_sequence=COLORWAY)
    fig.update_layout(legend_title_text="", hovermode="x unified", margin=dict(l=10, r=10, t=60, b=10))
    return fig


def bar_chart(df, x, y, title, labels, color=None, orientation="v"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation=orientation,
        title=title,
        labels=labels,
        color_discrete_sequence=COLORWAY,
    )
    fig.update_layout(legend_title_text="", margin=dict(l=10, r=10, t=60, b=10))
    return fig


def scatter_chart(df, x, y, color, title, labels, trendline=None):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        trendline=trendline,
        title=title,
        labels=labels,
        color_discrete_sequence=COLORWAY,
    )
    fig.update_layout(legend_title_text="", margin=dict(l=10, r=10, t=60, b=10))
    return fig


def prediction_vs_actual(pred_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pred_df["prodvt_aktual"],
            y=pred_df["prodvt_prediksi"],
            mode="markers",
            name="Ridge Hist Lag",
            text=pred_df["kabupaten"],
            marker=dict(size=11, color="#2563eb"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pred_df["prodvt_aktual"],
            y=pred_df["prodvt_prediksi_baseline"],
            mode="markers",
            name="Baseline terbaik",
            text=pred_df["kabupaten"],
            marker=dict(size=10, color="#f59e0b", symbol="diamond"),
        )
    )
    lo = min(pred_df["prodvt_aktual"].min(), pred_df["prodvt_prediksi"].min(), pred_df["prodvt_prediksi_baseline"].min())
    hi = max(pred_df["prodvt_aktual"].max(), pred_df["prodvt_prediksi"].max(), pred_df["prodvt_prediksi_baseline"].max())
    fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="Prediksi sempurna", line=dict(color="#dc2626", dash="dash")))
    fig.update_layout(
        title="Prediksi vs Aktual Produktivitas 2024",
        xaxis_title="Aktual (ton/ha)",
        yaxis_title="Prediksi (ton/ha)",
        legend_title_text="",
        margin=dict(l=10, r=10, t=60, b=10),
    )
    return fig
