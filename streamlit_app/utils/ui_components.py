from __future__ import annotations

from html import escape
from typing import Iterable

import streamlit as st
from streamlit_option_menu import option_menu


NAV_ITEMS = [
    ("Beranda", "house"),
    ("Dashboard Analytical", "bar-chart-line"),
    ("Model dan Evaluasi", "clipboard-data"),
    ("Coba Model", "sliders2"),
    ("Metodologi dan Batasan", "journal-text"),
]


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #070b10;
            --sidebar-bg: #101720;
            --card-bg: #111c24;
            --card-bg-soft: #13222d;
            --card-border: #243746;
            --card-border-strong: #315064;
            --text-main: #f4f7fb;
            --text-muted: #b7c3d1;
            --text-soft: #8fa3b7;
            --accent: #34d399;
            --accent-strong: #10b981;
            --accent-blue: #60a5fa;
            --accent-amber: #fbbf24;
            --danger-soft: #f87171;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 8%, rgba(52, 211, 153, 0.08), transparent 24rem),
                radial-gradient(circle at 82% 4%, rgba(96, 165, 250, 0.07), transparent 28rem),
                var(--app-bg);
            color: var(--text-main);
        }

        .main .block-container {
            padding-top: 2.1rem;
            padding-bottom: 3rem;
            max-width: 1480px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111923 0%, #0d131b 100%);
            border-right: 1px solid var(--card-border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text-main);
        }

        div[data-testid="stSidebarHeader"] {
            padding-top: 1rem;
        }

        .sidebar-brand {
            padding: 0.35rem 0 1.05rem 0;
        }

        .sidebar-kicker {
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .sidebar-title {
            color: var(--text-main);
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }

        .sidebar-subtitle {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .sidebar-separator {
            height: 1px;
            background: linear-gradient(90deg, rgba(52, 211, 153, 0.35), rgba(96, 165, 250, 0.08));
            margin: 0.95rem 0;
        }

        .sidebar-note, .sidebar-footer {
            color: var(--text-muted);
            font-size: 0.82rem;
            line-height: 1.45;
            padding: 0.75rem 0.85rem;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(15, 23, 42, 0.42);
            border-radius: 0.8rem;
        }

        .sidebar-footer {
            margin-top: 0.85rem;
            color: var(--text-soft);
            text-align: center;
        }

        h1, h2, h3 {
            color: var(--text-main);
            letter-spacing: 0;
        }

        p, li {
            color: var(--text-muted);
        }

        div[data-testid="stCaptionContainer"] {
            color: var(--text-muted);
        }

        .app-hero {
            border: 1px solid var(--card-border);
            background:
                linear-gradient(135deg, rgba(17, 28, 36, 0.96), rgba(10, 18, 26, 0.98)),
                linear-gradient(90deg, rgba(52, 211, 153, 0.14), rgba(96, 165, 250, 0.08));
            border-radius: 1.1rem;
            padding: 1.55rem 1.7rem;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.26);
            margin-bottom: 1.1rem;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: #d1fae5;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(52, 211, 153, 0.30);
            border-radius: 999px;
            padding: 0.32rem 0.65rem;
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.85rem;
        }

        .app-hero h1 {
            font-size: clamp(2rem, 4vw, 3.45rem);
            line-height: 1.03;
            margin: 0 0 0.72rem 0;
        }

        .app-hero p {
            max-width: 920px;
            color: var(--text-muted);
            font-size: 1.04rem;
            line-height: 1.6;
            margin: 0;
        }

        .page-heading {
            margin-bottom: 1rem;
        }

        .page-heading .eyebrow {
            color: var(--accent);
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .page-heading h1 {
            margin: 0;
            font-size: 2.25rem;
            line-height: 1.1;
        }

        .page-heading p {
            margin: 0.5rem 0 0 0;
            max-width: 920px;
            color: var(--text-muted);
            font-size: 1rem;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 1rem 0 1.2rem 0;
        }

        .kpi-card {
            min-height: 116px;
            padding: 1rem;
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            background: linear-gradient(180deg, rgba(19, 34, 45, 0.96), rgba(15, 23, 32, 0.98));
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }

        .kpi-label {
            color: var(--text-muted);
            font-size: 0.78rem;
            font-weight: 750;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.42rem;
        }

        .kpi-value {
            color: var(--text-main);
            font-size: 1.72rem;
            line-height: 1.1;
            font-weight: 850;
            margin-bottom: 0.4rem;
            overflow-wrap: anywhere;
        }

        .kpi-caption {
            color: var(--text-soft);
            font-size: 0.82rem;
            line-height: 1.35;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--card-border) !important;
            background: linear-gradient(180deg, rgba(17, 28, 36, 0.94), rgba(11, 18, 25, 0.96)) !important;
            border-radius: 1rem !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }

        .section-title {
            margin-bottom: 0.85rem;
        }

        .section-title h2,
        .section-title h3 {
            font-size: 1.12rem;
            margin: 0;
            color: var(--text-main);
        }

        .section-title p {
            margin: 0.25rem 0 0 0;
            color: var(--text-muted);
            font-size: 0.92rem;
        }

        .callout {
            border-radius: 1rem;
            padding: 1rem 1.05rem;
            border: 1px solid rgba(96, 165, 250, 0.28);
            background: rgba(37, 99, 235, 0.10);
            margin: 0.8rem 0 1rem 0;
        }

        .callout.success {
            border-color: rgba(52, 211, 153, 0.32);
            background: rgba(16, 185, 129, 0.11);
        }

        .callout.warning {
            border-color: rgba(251, 191, 36, 0.36);
            background: rgba(251, 191, 36, 0.10);
        }

        .callout-title {
            color: var(--text-main);
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .callout-body {
            color: var(--text-muted);
            line-height: 1.55;
            font-size: 0.94rem;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }

        .insight-card {
            border: 1px solid var(--card-border);
            background: rgba(15, 23, 42, 0.44);
            border-radius: 0.9rem;
            padding: 0.9rem 0.95rem;
        }

        .insight-card .label {
            color: var(--accent);
            font-weight: 800;
            font-size: 0.78rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }

        .insight-card .body {
            color: var(--text-muted);
            line-height: 1.5;
            font-size: 0.94rem;
        }

        .result-card {
            border: 1px solid rgba(52, 211, 153, 0.34);
            background: linear-gradient(180deg, rgba(16, 185, 129, 0.13), rgba(15, 23, 42, 0.52));
            border-radius: 1rem;
            padding: 1.1rem;
            margin-bottom: 0.9rem;
        }

        .result-label {
            color: #d1fae5;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .result-value {
            color: var(--text-main);
            font-size: 2.15rem;
            font-weight: 850;
            line-height: 1;
        }

        .result-caption {
            color: var(--text-muted);
            margin-top: 0.55rem;
            line-height: 1.45;
        }

        .pipeline {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.75rem;
        }

        .pipeline-step {
            border: 1px solid var(--card-border);
            border-radius: 0.9rem;
            padding: 0.9rem;
            background: rgba(15, 23, 42, 0.42);
        }

        .pipeline-number {
            width: 1.75rem;
            height: 1.75rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            background: rgba(52, 211, 153, 0.14);
            color: #d1fae5;
            border: 1px solid rgba(52, 211, 153, 0.28);
            font-weight: 800;
            margin-bottom: 0.65rem;
        }

        .pipeline-title {
            color: var(--text-main);
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .pipeline-body {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin: 0.45rem 0 0.8rem 0;
        }

        .tag {
            color: #dbeafe;
            border: 1px solid rgba(96, 165, 250, 0.28);
            background: rgba(96, 165, 250, 0.10);
            border-radius: 999px;
            padding: 0.28rem 0.55rem;
            font-size: 0.78rem;
            font-weight: 750;
        }

        div[data-testid="stMetric"] {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            padding: 1rem;
        }

        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricDelta"] {
            color: var(--text-muted) !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--text-main) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            border-bottom: 1px solid var(--card-border);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 0.8rem 0.8rem 0 0;
            background: rgba(15, 23, 42, 0.38);
            color: var(--text-muted);
            padding: 0.7rem 1rem;
        }

        .stTabs [aria-selected="true"] {
            color: var(--text-main) !important;
            background: rgba(52, 211, 153, 0.12) !important;
            border-bottom: 2px solid var(--accent);
        }

        div[data-testid="stAlert"] {
            border-radius: 0.9rem;
            border: 1px solid rgba(96, 165, 250, 0.28);
            background: rgba(15, 23, 42, 0.58);
            color: var(--text-main);
        }

        div[data-testid="stAlert"] * {
            color: var(--text-main);
        }

        label, div[data-testid="stWidgetLabel"] p {
            color: var(--text-main) !important;
            font-weight: 700;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] > div,
        textarea,
        input {
            background-color: rgba(15, 23, 42, 0.72) !important;
            color: var(--text-main) !important;
            border-color: var(--card-border-strong) !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="popover"] span,
        div[data-baseweb="menu"] span {
            color: var(--text-main) !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            background: #111c24 !important;
            border-color: var(--card-border) !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--card-border);
            border-radius: 0.9rem;
            overflow: hidden;
        }

        button[kind="primary"], .stButton > button, div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, var(--accent-strong), #2dd4bf) !important;
            color: #04110d !important;
            border: 0 !important;
            border-radius: 0.85rem !important;
            font-weight: 850 !important;
            min-height: 2.8rem;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            filter: brightness(1.06);
            box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.18);
        }

        @media (max-width: 1200px) {
            .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .pipeline { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        @media (max-width: 720px) {
            .kpi-grid, .pipeline { grid-template-columns: 1fr; }
            .app-hero { padding: 1.1rem; }
            .app-hero h1 { font-size: 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(meta: dict) -> str:
    labels = [label for label, _ in NAV_ITEMS]
    icons = [icon for _, icon in NAV_ITEMS]
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-kicker">Dashboard Akademik</div>
                <div class="sidebar-title">Prediksi Padi Lampung</div>
                <div class="sidebar-subtitle">Produktivitas, produksi, evaluasi temporal, dan simulasi model.</div>
            </div>
            <div class="sidebar-separator"></div>
            """,
            unsafe_allow_html=True,
        )
        selected = option_menu(
            menu_title=None,
            options=labels,
            icons=icons,
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#9fb3c8", "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.94rem",
                    "font-weight": "650",
                    "color": "#cbd5e1",
                    "padding": "0.72rem 0.78rem",
                    "margin": "0.18rem 0",
                    "border-radius": "0.82rem",
                    "--hover-color": "rgba(52, 211, 153, 0.10)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(52, 211, 153, 0.16)",
                    "color": "#ecfdf5",
                    "font-weight": "800",
                    "border-left": "3px solid #34d399",
                },
            },
        )
        st.markdown(
            f"""
            <div class="sidebar-separator"></div>
            <div class="sidebar-note">
                Data deployment dibaca dari artefak lokal. Aplikasi tidak membutuhkan mount Google Drive pribadi.
                <br><br>
                <strong>{escape(str(meta.get("n_kabupaten", 15)))}</strong> kabupaten/kota &bull;
                <strong>{escape(str(meta.get("tahun_min", 2019)))}-{escape(str(meta.get("tahun_max", 2024)))}</strong>
            </div>
            <div class="sidebar-footer">Project Big Data | Prediksi Padi Lampung</div>
            """,
            unsafe_allow_html=True,
        )
    return selected


def hero(title: str, subtitle: str, badge: str = "BIG DATA ANALYTICS &bull; LAMPUNG") -> None:
    st.markdown(
        f"""
        <div class="app-hero">
            <div class="hero-badge">{badge}</div>
            <h1>{escape(title)}</h1>
            <p>{escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="page-heading">
            <div class="eyebrow">{escape(eyebrow)}</div>
            <h1>{escape(title)}</h1>
            <p>{escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_cards(items: Iterable[tuple[str, str, str]]) -> None:
    cards = []
    for label, value, caption in items:
        cards.append(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{escape(label)}</div>
                <div class="kpi-value">{escape(value)}</div>
                <div class="kpi-caption">{escape(caption)}</div>
            </div>
            """
        )
    st.markdown(f"<div class='kpi-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def section_title(title: str, subtitle: str | None = None, level: int = 3) -> None:
    tag = "h2" if level == 2 else "h3"
    subtitle_html = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="section-title">
            <{tag}>{escape(title)}</{tag}>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(title: str, body: str, tone: str = "info") -> None:
    st.markdown(
        f"""
        <div class="callout {escape(tone)}">
            <div class="callout-title">{escape(title)}</div>
            <div class="callout-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_cards(items: Iterable[tuple[str, str]]) -> None:
    cards = []
    for label, body in items:
        cards.append(
            f"""
            <div class="insight-card">
                <div class="label">{escape(label)}</div>
                <div class="body">{body}</div>
            </div>
            """
        )
    st.markdown(f"<div class='insight-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def result_card(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">{escape(label)}</div>
            <div class="result-value">{escape(value)}</div>
            <div class="result-caption">{escape(caption)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tag_row(tags: Iterable[str]) -> None:
    tags_html = "".join(f"<span class='tag'>{escape(tag)}</span>" for tag in tags)
    st.markdown(f"<div class='tag-row'>{tags_html}</div>", unsafe_allow_html=True)


def pipeline(steps: Iterable[tuple[str, str]]) -> None:
    cards = []
    for idx, (title, body) in enumerate(steps, start=1):
        cards.append(
            f"""
            <div class="pipeline-step">
                <div class="pipeline-number">{idx}</div>
                <div class="pipeline-title">{escape(title)}</div>
                <div class="pipeline-body">{escape(body)}</div>
            </div>
            """
        )
    st.markdown(f"<div class='pipeline'>{''.join(cards)}</div>", unsafe_allow_html=True)
