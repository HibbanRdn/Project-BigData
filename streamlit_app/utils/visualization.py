from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go


COLORWAY = [
    "#34d399",
    "#60a5fa",
    "#fbbf24",
    "#f87171",
    "#a78bfa",
    "#22d3ee",
    "#94a3b8",
    "#fb7185",
]

CATEGORY_COLORS = {
    "Machine learning": "#34d399",
    "Baseline temporal": "#fbbf24",
    "Ridge Hist Lag": "#34d399",
    "Naive Lag1": "#fbbf24",
    "Naive Roll2": "#60a5fa",
}


def apply_dark_theme(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe7f3", family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"),
        title=dict(font=dict(color="#f4f7fb", size=17), x=0.01, xanchor="left"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(148,163,184,0.18)",
            borderwidth=0,
            font=dict(color="#cbd5e1", size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(bgcolor="#111c24", bordercolor="#315064", font=dict(color="#f4f7fb")),
        margin=dict(l=18, r=18, t=62, b=26),
        modebar=dict(bgcolor="rgba(0,0,0,0)", color="#94a3b8", activecolor="#34d399"),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#315064",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#dbe7f3"),
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.16)",
        zeroline=False,
        linecolor="#315064",
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#dbe7f3"),
    )
    return fig


def line_chart(df, x, y, color, title, labels, height: int = 390):
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        title=title,
        labels=labels,
        color_discrete_sequence=COLORWAY,
        color_discrete_map=CATEGORY_COLORS,
    )
    fig.update_traces(
        line=dict(width=2.7),
        marker=dict(size=7, line=dict(width=1, color="#0b1118")),
    )
    if color is None:
        fig.update_traces(name="", hovertemplate=f"{labels.get(x, x)}: %{{x}}<br>{labels.get(y, y)}: %{{y:,.3f}}<extra></extra>")
    else:
        fig.update_traces(hovertemplate=f"{labels.get(x, x)}: %{{x}}<br>{labels.get(y, y)}: %{{y:,.3f}}<extra>%{{fullData.name}}</extra>")
    fig.update_layout(legend_title_text="", hovermode="x unified")
    return apply_dark_theme(fig, height=height)


def bar_chart(df, x, y, title, labels, color=None, orientation="v", height: int = 390):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation=orientation,
        title=title,
        labels=labels,
        color_discrete_sequence=COLORWAY,
        color_discrete_map=CATEGORY_COLORS,
    )
    fig.update_traces(
        marker_line_color="rgba(255,255,255,0.08)",
        marker_line_width=1,
        hovertemplate=f"{labels.get(x, x)}: %{{x}}<br>{labels.get(y, y)}: %{{y:,.3f}}<extra></extra>",
    )
    if orientation == "h":
        fig.update_traces(hovertemplate=f"{labels.get(y, y)}: %{{y}}<br>{labels.get(x, x)}: %{{x:,.3f}}<extra></extra>")
    fig.update_layout(legend_title_text="", bargap=0.28)
    return apply_dark_theme(fig, height=height)


def scatter_chart(df, x, y, color, title, labels, trendline=None, height: int = 390):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        trendline=trendline,
        title=title,
        labels=labels,
        color_discrete_sequence=COLORWAY,
        color_discrete_map=CATEGORY_COLORS,
    )
    fig.update_traces(
        marker=dict(size=9, opacity=0.86, line=dict(width=1, color="#0b1118")),
        hovertemplate=f"{labels.get(x, x)}: %{{x:,.3f}}<br>{labels.get(y, y)}: %{{y:,.3f}}<extra>%{{fullData.name}}</extra>",
    )
    fig.update_layout(legend_title_text="")
    return apply_dark_theme(fig, height=height)


def prediction_vs_actual(pred_df, height: int = 430):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=pred_df["prodvt_aktual"],
            y=pred_df["prodvt_prediksi"],
            mode="markers",
            name="Ridge Hist Lag",
            text=pred_df["kabupaten"],
            marker=dict(size=12, color="#34d399", line=dict(width=1, color="#0b1118")),
            hovertemplate="Kabupaten: %{text}<br>Aktual: %{x:.3f} ton/ha<br>Prediksi ML: %{y:.3f} ton/ha<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pred_df["prodvt_aktual"],
            y=pred_df["prodvt_prediksi_baseline"],
            mode="markers",
            name="Baseline terbaik",
            text=pred_df["kabupaten"],
            marker=dict(size=11, color="#fbbf24", symbol="diamond", line=dict(width=1, color="#0b1118")),
            hovertemplate="Kabupaten: %{text}<br>Aktual: %{x:.3f} ton/ha<br>Baseline: %{y:.3f} ton/ha<extra></extra>",
        )
    )
    lo = min(pred_df["prodvt_aktual"].min(), pred_df["prodvt_prediksi"].min(), pred_df["prodvt_prediksi_baseline"].min())
    hi = max(pred_df["prodvt_aktual"].max(), pred_df["prodvt_prediksi"].max(), pred_df["prodvt_prediksi_baseline"].max())
    fig.add_trace(
        go.Scatter(
            x=[lo, hi],
            y=[lo, hi],
            mode="lines",
            name="Prediksi sempurna",
            line=dict(color="#f87171", dash="dash", width=1.6),
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        title="Prediksi vs Aktual Produktivitas 2024",
        xaxis_title="Aktual (ton/ha)",
        yaxis_title="Prediksi (ton/ha)",
        legend_title_text="",
    )
    return apply_dark_theme(fig, height=height)
