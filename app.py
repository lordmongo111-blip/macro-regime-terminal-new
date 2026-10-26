import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Macro / Regime Terminal", page_icon="⌁", layout="wide")

G10 = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]
MONTHS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at 78% -10%, #14253a 0%, #080d14 48%, #070b11 100%); }
.block-container { max-width: 1800px; padding: 1.15rem 1.65rem 2.5rem; }
[data-testid="stHeader"] { background: rgba(7,11,17,.92); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0b121c 0%,#101925 100%); border-right: 1px solid #1c2b3b; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#a8bfd3; }
[data-testid="stSidebar"] [role="radiogroup"] label { border-radius: 8px; padding: .38rem .5rem; margin: 1px 0; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#192637; }
h1 { letter-spacing:-.035em; font-weight:800; color:#f4f7fb; }
h2,h3 { color:#eaf1f8; letter-spacing:-.02em; }
p, label, .stCaption { color:#9eb2c7; }
[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(20,31,45,.96),rgba(11,18,27,.96)); border:1px solid #1d2d3e; padding:16px 17px; border-radius:13px; box-shadow:0 8px 24px rgba(0,0,0,.12); }
[data-testid="stMetricLabel"] { color:#9db5ca !important; font-size:.82rem; }
[data-testid="stMetricValue"] { color:#f4f7fb; font-weight:750; }
[data-testid="stMetricDelta"] { font-weight:650; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color:#1c2b3b !important; border-radius:13px; }
[data-testid="stAlert"] { border-radius:10px; border:1px solid #29384a; }
.stButton > button, [data-testid="stDownloadButton"] button { background:linear-gradient(105deg,#f20d3a,#c91432); color:white; border:1px solid #ff3454; border-radius:9px; font-weight:700; min-height:2.55rem; transition:all .15s ease; }
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover { background:#ff2448; border-color:#ff526d; color:white; box-shadow:0 0 18px rgba(242,13,58,.2); }
[data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"] > div { background:#111b28; border-color:#2a3b4f; border-radius:8px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #1d2d3e; border-radius:10px; overflow:hidden; }
hr { border-color:#203043; }
a { color:#55b9ff; }
.small-muted { color:#8198ad; font-size:.85rem; }
/* Harmonised Plotly chart styling across all modules */
.js-plotly-plot .plotly .modebar { background:transparent !important; }
@media (max-width: 900px) { .block-container { padding: .8rem .7rem 2rem; } }

/* Reference-inspired terminal accents; analysis logic remains unchanged */
[data-testid="stSidebar"] { background:linear-gradient(180deg,#091521 0%,#07111a 100%); border-right:1px solid #1a2b3a; }
[data-testid="stSidebar"] [role="radiogroup"] label { border-radius:8px; padding:.42rem .55rem; margin:2px 0; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#192637; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background:linear-gradient(100deg,#ff1744,#d90b32); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p { color:#fff !important; font-weight:700; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#0d1b28,#0b1722); border:1px solid #1a2b3a; border-radius:13px; }
[data-testid="stHeader"] { background:rgba(5,13,21,.9); }
.stApp { background:radial-gradient(ellipse at 75% 0%,#102236 0%,#07111b 55%); }
h1,h2,h3 { color:#f4f8fc; }
.stButton > button { background:linear-gradient(100deg,#ff1744,#e90032); border:0; color:#fff; border-radius:9px; font-weight:700; }

/* Reference dashboard refinements */
.block-container { max-width: 1920px; padding: .9rem 1.45rem 2rem; }
[data-testid="stSidebar"] { min-width: 220px; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 { letter-spacing:-.02em; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 3px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  display:flex; align-items:center; min-height:34px; padding:.35rem .55rem;
  border:1px solid transparent; transition:background .15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  box-shadow:0 5px 18px rgba(255,23,68,.16); border-color:rgba(255,75,105,.45);
}
[data-testid="stMetric"] { min-height:105px; display:flex; flex-direction:column; justify-content:center; }
[data-testid="stMetricValue"] { font-size:clamp(1.3rem,2vw,2rem); }
[data-testid="stHorizontalBlock"] { gap: .8rem; }
[data-testid="stDataFrame"] { background:#0a1420; }
[data-testid="stTabs"] button { font-weight:650; }
[data-testid="stPlotlyChart"] { background:linear-gradient(180deg,rgba(10,22,34,.45),rgba(7,15,24,.2)); border:1px solid #182a3b; border-radius:12px; padding:5px; }
.stAlert p { color:#d8e5f1 !important; }
.stButton > button:focus { box-shadow:0 0 0 2px #07111b,0 0 0 4px #ff2447; }
@media (min-width: 1400px) {
  .block-container { padding-left:1.8rem; padding-right:1.8rem; }
}


/* Dashboard design layer merged from richtige design_app.py; analysis modules retained. */
.brand { display:flex; gap:12px; align-items:center; padding:0 0 12px; border-bottom:1px solid #1a2b3a; margin-bottom:14px; }
.brand .logo { width:36px; height:36px; display:flex; align-items:center; justify-content:center; border:3px solid #ff2447; color:#ff2447; border-radius:11px; transform:rotate(45deg); font-weight:900; flex-shrink:0; }
.brand .logo span { transform:rotate(-45deg); }
.brand-title { font-size:20px; font-weight:800; letter-spacing:-.04em; color:#f7fbff; }
.brand-sub { font-size:12px; color:#8ea6bb; margin-top:3px; }
.panel { background:linear-gradient(145deg,rgba(13,27,40,.96),rgba(7,17,27,.96)); border:1px solid #1a2b3a; border-radius:13px; padding:15px 16px; margin-bottom:12px; }
.panel-title { font-weight:750; font-size:15px; margin-bottom:12px; color:#edf5ff; }
.ticker { background:linear-gradient(145deg,#0b1722,#07111b); border:1px solid #1a2b3a; border-radius:9px; padding:8px 9px; min-height:54px; }
.ticker-name { color:#c7d5e3; font-size:10px; font-weight:700; }
.ticker-value { color:#f4f8fc; font-size:12px; font-weight:700; margin-top:5px; }
.positive { color:#00d68f; } .negative { color:#ff2447; } .muted { color:#8ea6bb; }
.small-note { color:#8ea6bb; font-size:11px; line-height:1.5; }

</style>
""", unsafe_allow_html=True)

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def get_fred_series(series_id, api_key, observation_start="2015-01-01"):
    """Fetch FRED observations server-side. Requires a free FRED API key."""
    import requests
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id, "api_key": api_key, "file_type": "json",
        "observation_start": observation_start, "sort_order": "asc"
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    observations = response.json().get("observations", [])
    df = pd.DataFrame(observations)
    if df.empty:
        return pd.DataFrame(columns=["date", "value"])
    df = df[df["value"] != "."].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df[["date", "value"]].dropna()

def load_market_history(symbol, period="10y"):
    """Historical price helper via yfinance; availability/terms depend on symbol/provider."""
    import yfinance as yf
    data = yf.download(symbol, period=period, interval="1d", auto_adjust=True, progress=False)
    if data is None or data.empty:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        close = data["Close"].iloc[:, 0]
    else:
        close = data["Close"]
    out = close.rename("close").to_frame().dropna()
    out.index = pd.to_datetime(out.index)
    out.index.name = "date"
    return out.reset_index()

def seasonality(df):
    if df.empty or "close" not in df:
        return pd.DataFrame()
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values("date")
    d["month"] = d["date"].dt.month
    # Monthly close-to-close returns, grouped by calendar month over available history.
    monthly = d.set_index("date")["close"].resample("ME").last().dropna().pct_change().dropna().to_frame("return")
    monthly["month"] = monthly.index.month
    return monthly.groupby("month")["return"].agg(
        avg_return="mean",
        win_rate=lambda x: (x > 0).mean(),
        observations="count",
        median="median",
        volatility="std"
    ).reset_index()

def cot_api_preview():
    """Official CFTC Socrata API query: latest available records vary by dataset."""
    import requests
    # Public CFTC Legacy Futures Only dataset. Querying schema can change; fail visibly.
    url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"
    params = {"$limit": 5, "$order": "report_date_as_yyyy_mm_dd DESC"}
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return pd.DataFrame(response.json())


# Official CFTC Legacy Futures Only mapping used by the signal engine.
# Mapping must be checked against the selected CFTC dataset and contract metadata.
CFTC_CONTRACT_CODES = {
    "6E": "099741",  # Euro FX
    "6B": "096742",  # British Pound
    "6J": "097741",  # Japanese Yen
    "6A": "232741",  # Australian Dollar
    "6C": "090741",  # Canadian Dollar
    "6S": "092741",  # Swiss Franc
    "6N": "112741",  # New Zealand Dollar
}

def load_cot_history(contract_code, limit=52):
    """Load weekly CFTC Legacy Futures Only net positions for one mapped contract."""
    import requests
    if contract_code not in CFTC_CONTRACT_CODES:
        raise ValueError(f"Kein verifiziertes CFTC-Mapping für {contract_code}")
    url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"
    params = {
        "$where": f"cftc_contract_market_code='{CFTC_CONTRACT_CODES[contract_code]}'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": str(max(26, min(int(limit), 104))),
        "$select": (
            "report_date_as_yyyy_mm_dd,market_and_exchange_names,"
            "cftc_contract_market_code,comm_positions_long_all,comm_positions_short_all,"
            "noncomm_positions_long_all,noncomm_positions_short_all,"
            "nonrept_positions_long_all,nonrept_positions_short_all,open_interest_all"
        ),
    }
    response = requests.get(url, params=params, timeout=20, headers={"Accept": "application/json"})
    response.raise_for_status()
    rows = response.json()
    if not rows:
        raise ValueError(f"CFTC lieferte keine Datensätze für Code {CFTC_CONTRACT_CODES[contract_code]}")
    df = pd.DataFrame(rows)
    required = ["report_date_as_yyyy_mm_dd", "comm_positions_long_all", "comm_positions_short_all",
                "noncomm_positions_long_all", "noncomm_positions_short_all"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError("CFTC-Schema unvollständig: " + ", ".join(missing))
    df["date"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"], errors="coerce", utc=True)
    numeric = ["comm_positions_long_all", "comm_positions_short_all",
               "noncomm_positions_long_all", "noncomm_positions_short_all",
               "nonrept_positions_long_all", "nonrept_positions_short_all", "open_interest_all"]
    for col in numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date"] + required[1:]).sort_values("date").drop_duplicates("date")
    if len(df) < 26:
        raise ValueError(f"Zu wenig COT-Historie ({len(df)}/26 Wochen)")
    df["commercial_net"] = df["comm_positions_long_all"] - df["comm_positions_short_all"]
    df["noncommercial_net"] = df["noncomm_positions_long_all"] - df["noncomm_positions_short_all"]
    if {"nonrept_positions_long_all", "nonrept_positions_short_all"}.issubset(df.columns):
        df["nonreportable_net"] = df["nonrept_positions_long_all"] - df["nonrept_positions_short_all"]
    else:
        df["nonreportable_net"] = np.nan
    df["open_interest"] = pd.to_numeric(df.get("open_interest_all"), errors="coerce")
    age_days = (pd.Timestamp.now(tz="UTC") - df["date"].iloc[-1]).total_seconds() / 86400
    if age_days > 14:
        raise ValueError(f"COT-Bericht veraltet ({age_days:.1f} Tage; Limit 14)")
    df.attrs["market_name"] = str(df.iloc[-1].get("market_and_exchange_names", contract_code))
    df.attrs["age_days"] = age_days
    return df.reset_index(drop=True)

def cot_positioning_score(cot_df, invert=False):
    """Map latest non-commercial net positioning to a bounded 52-week percentile score."""
    if cot_df is None or len(cot_df) < 26 or "noncommercial_net" not in cot_df:
        raise ValueError("COT-Historie reicht für einen Positionsscore nicht aus")
    values = pd.to_numeric(cot_df["noncommercial_net"], errors="coerce").dropna().tail(52)
    if len(values) < 26:
        raise ValueError("Zu wenige gültige Non-commercial COT-Werte")
    latest = float(values.iloc[-1])
    # Percentile rank of latest net position within the available rolling history.
    percentile = float((values <= latest).mean())
    score = int(round(np.clip((percentile - 0.5) * 200, -100, 100)))
    if invert:
        score = -score
    return score, latest, percentile

def seasonality_component_score(prices, invert=False, min_years=5):
    """Score this calendar month's historical mean return; needs >=5 observations."""
    if prices is None or prices.empty or not {"date", "close"}.issubset(prices.columns):
        raise ValueError("Historische Kursdaten für Saisonalität fehlen")
    d = prices.copy()
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d = d.dropna(subset=["date", "close"]).sort_values("date")
    monthly = d.set_index("date")["close"].resample("ME").last().dropna().pct_change().dropna().to_frame("return")
    current_month = pd.Timestamp.now().month
    sample = monthly.loc[monthly.index.month == current_month, "return"].dropna()
    # Count distinct years, not raw rows; only one monthly return per year is valid.
    sample = sample[~sample.index.year.duplicated(keep="last")]
    if len(sample) < min_years:
        years_found = ", ".join(str(y) for y in sample.index.year.tolist()) or "keine"
        raise ValueError(
            f"Zu wenige historische Monatsbeobachtungen ({len(sample)}/{min_years} Jahre; vorhanden: {years_found}). "
            "Für eine belastbare Saisonanalyse werden längere Kursdaten benötigt."
        )
    mean_return = float(sample.mean())
    # Transparent scaling: +/-2% average monthly return maps to +/-100.
    score = int(round(np.clip(mean_return / 0.02 * 100, -100, 100)))
    if invert:
        score = -score
    return score, mean_return, len(sample)


# ---------------- FX signal engine: fail closed on missing/invalid inputs ----------------
FX_PAIRS = {
    "EUR/USD": {"symbol": "EURUSD=X", "base": "EUR", "quote": "USD", "cot": "6E", "cot_invert": False},
    "GBP/USD": {"symbol": "GBPUSD=X", "base": "GBP", "quote": "USD", "cot": "6B", "cot_invert": False},
    "USD/JPY": {"symbol": "JPY=X", "base": "USD", "quote": "JPY", "cot": "6J", "cot_invert": True},
    "AUD/USD": {"symbol": "AUDUSD=X", "base": "AUD", "quote": "USD", "cot": "6A", "cot_invert": False},
    "USD/CAD": {"symbol": "CAD=X", "base": "USD", "quote": "CAD", "cot": "6C", "cot_invert": True},
    "USD/CHF": {"symbol": "CHF=X", "base": "USD", "quote": "CHF", "cot": "6S", "cot_invert": True},
    "NZD/USD": {"symbol": "NZDUSD=X", "base": "NZD", "quote": "USD", "cot": "6N", "cot_invert": False},
    "EUR/GBP": {"symbol": "EURGBP=X", "base": "EUR", "quote": "GBP", "cot": None, "cot_invert": False},
    "EUR/JPY": {"symbol": "EURJPY=X", "base": "EUR", "quote": "JPY", "cot": "6J", "cot_invert": True},
    "GBP/JPY": {"symbol": "GBPJPY=X", "base": "GBP", "quote": "JPY", "cot": "6J", "cot_invert": True},
    "EUR/CHF": {"symbol": "EURCHF=X", "base": "EUR", "quote": "CHF", "cot": "6S", "cot_invert": True},
    "AUD/JPY": {"symbol": "AUDJPY=X", "base": "AUD", "quote": "JPY", "cot": "6J", "cot_invert": True},
    "CAD/JPY": {"symbol": "CADJPY=X", "base": "CAD", "quote": "JPY", "cot": "6J", "cot_invert": True},
}
LONG_SHORT_THRESHOLD = 20
MAX_PRICE_AGE_DAYS = 4
MIN_PRICE_OBSERVATIONS = 220


def validate_price_history(df, max_age_days=MAX_PRICE_AGE_DAYS):
    """Validate real provider-returned daily prices; never create replacement data."""
    if df is None or df.empty or not {"date", "close"}.issubset(df.columns):
        return False, "Kursreihe fehlt", None
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"], utc=True, errors="coerce")
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d = d.dropna(subset=["date", "close"]).sort_values("date")
    if len(d) < MIN_PRICE_OBSERVATIONS:
        return False, f"Zu wenig Historie ({len(d)}/{MIN_PRICE_OBSERVATIONS} Tageswerte)", None
    if (d["close"] <= 0).any() or d["date"].duplicated().any():
        return False, "Ungültige Kurse oder doppelte Zeitstempel", None
    age = (pd.Timestamp.now(tz="UTC") - d["date"].iloc[-1]).total_seconds() / 86400
    if age > max_age_days:
        return False, f"Kursdaten veraltet ({age:.1f} Tage)", None
    return True, f"Validiert · {len(d)} Tageswerte · letzter Kurs {d['date'].iloc[-1].date()}", d


def technical_confirmation(prices):
    """Daily trend/momentum confirmation, returned only for validated prices."""
    if prices is None or len(prices) < 220:
        return None, "Technische Historie unzureichend"
    close = prices["close"].astype(float)
    last = float(close.iloc[-1])
    sma50 = float(close.rolling(50).mean().iloc[-1])
    sma200 = float(close.rolling(200).mean().iloc[-1])
    momentum20 = float(close.pct_change(20).iloc[-1])
    if not np.isfinite([last, sma50, sma200, momentum20]).all():
        return None, "Technische Kennzahlen ungültig"
    if last > sma50 and sma50 > sma200 and momentum20 > 0:
        return 1, f"Bullish bestätigt: Kurs>SMA50>SMA200, 20T-Momentum {momentum20:.2%}"
    if last < sma50 and sma50 < sma200 and momentum20 < 0:
        return -1, f"Bearish bestätigt: Kurs<SMA50<SMA200, 20T-Momentum {momentum20:.2%}"
    return 0, f"Kein eindeutiger Trend: 20T-Momentum {momentum20:.2%}"


def combine_fx_signal(component_scores, component_valid, technical_score):
    """Weighted composite: macro 40%, COT 25%, seasonality 10%, technical 25%.

    Every input is required and must be validated. Technical score is -1/0/+1,
    scaled to -100/0/+100; a neutral technical read cannot confirm a direction.
    """
    required = ("macro", "cot", "seasonality")
    missing = [name for name in required if not component_valid.get(name, False)]
    if missing or technical_score is None:
        blocked = missing + (["Technik"] if technical_score is None else [])
        return {"bias": "NEUTRAL", "score": None,
                "reason": "Signal gesperrt: nicht validiert — " + ", ".join(blocked),
                "signal_quality": "NICHT BEWERTBAR"}
    if any(name not in component_scores for name in required):
        return {"bias": "NEUTRAL", "score": None,
                "reason": "Signal gesperrt: für mindestens eine validierte Komponente fehlt der Score",
                "signal_quality": "NICHT BEWERTBAR"}
    score = int(round(
        0.40 * component_scores["macro"] +
        0.25 * component_scores["cot"] +
        0.10 * component_scores["seasonality"] +
        0.25 * (100 * technical_score)
    ))
    if score >= LONG_SHORT_THRESHOLD:
        if technical_score == 1:
            bias, reason = "LONG", "LONG: gewichteter Score ≥ +20 und Technik bestätigt bullish"
        else:
            bias, reason = "NEUTRAL", "LONG blockiert: Technik bestätigt nicht bullish"
    elif score <= -LONG_SHORT_THRESHOLD:
        if technical_score == -1:
            bias, reason = "SHORT", "SHORT: gewichteter Score ≤ −20 und Technik bestätigt bearish"
        else:
            bias, reason = "NEUTRAL", "SHORT blockiert: Technik bestätigt nicht bearish"
    else:
        bias, reason = "NEUTRAL", "Gewichteter Score innerhalb der Schwelle ±20"
    quality = "MITTEL" if bias != "NEUTRAL" else "NIEDRIG"
    return {"bias": bias, "score": score, "reason": reason, "signal_quality": quality}


# FRED-hosted national/OECD series. For non-US currencies, the short-term
# interest-rate series is a proxy (not necessarily the official policy rate).
# CPI series are price indices; their YoY change is calculated below.
MACRO_CURRENCY_SERIES = {
    "USD": {"rate": "FEDFUNDS", "inflation": "CPIAUCSL", "rate_age": 100, "inflation_age": 100, "label": "US Fed funds"},
    "EUR": {"rate": "ECBDFR", "inflation": "CP0000EZCCM086NEST", "rate_age": 60, "inflation_age": 100, "label": "EZB Einlagezins"},
    "GBP": {"rate": "IRSTCI01GBM156N", "inflation": "GBRCPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "UK Kurzfristzins-Proxy"},
    "JPY": {"rate": "IRSTCI01JPM156N", "inflation": "JPNCPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "Japan Kurzfristzins-Proxy"},
    "CHF": {"rate": "IRSTCI01CHM156N", "inflation": "CHECPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "Schweiz Kurzfristzins-Proxy"},
    "CAD": {"rate": "IRSTCI01CAM156N", "inflation": "CANCPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "Kanada Kurzfristzins-Proxy"},
    "AUD": {"rate": "IRSTCI01AUM156N", "inflation": "AUSCPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "Australien Kurzfristzins-Proxy"},
    "NZD": {"rate": "IRSTCI01NZM156N", "inflation": "NZLCPIALLMINMEI", "rate_age": 100, "inflation_age": 100, "label": "Neuseeland Kurzfristzins-Proxy"},
}

def calculate_relative_macro_score(api_key, base_currency, quote_currency):
    """Compare base and quote macro data. Rates are required; stale CPI is disclosed."""
    if base_currency not in MACRO_CURRENCY_SERIES or quote_currency not in MACRO_CURRENCY_SERIES:
        return None, f"Keine Makro-Zuordnung für {base_currency}/{quote_currency}"
    if base_currency == quote_currency:
        return None, "Basis- und Quotewährung sind identisch"

    loaded = {}
    errors = []
    for currency in (base_currency, quote_currency):
        cfg = MACRO_CURRENCY_SERIES[currency]
        # Rate series are mandatory: without both, no relative macro score is calculated.
        sid = cfg["rate"]
        try:
            df = get_fred_series(sid, api_key)
            if df.empty:
                raise ValueError("keine Beobachtungen")
            df = df.sort_values("date").reset_index(drop=True)
            last_date = pd.Timestamp(df.iloc[-1]["date"])
            age = (pd.Timestamp.now().normalize() - last_date.normalize()).days
            if age < 0 or age > cfg["rate_age"]:
                raise ValueError(f"letzter Wert {last_date.date()} ist {age} Tage alt")
            loaded[(currency, "rate")] = df
        except Exception as exc:
            return None, f"{currency} Zinsreihe {sid} nicht verfügbar/aktuell: {exc}"

        # Inflation is useful but some FRED/OECD CPI index series are discontinued or stale.
        # Do not silently accept stale inflation; transparently fall back to a rate-only score.
        inf_sid = cfg["inflation"]
        try:
            inf = get_fred_series(inf_sid, api_key)
            if inf.empty or len(inf) < 13:
                raise ValueError("zu wenige Beobachtungen")
            inf = inf.sort_values("date").reset_index(drop=True)
            inf_date = pd.Timestamp(inf.iloc[-1]["date"])
            inf_age = (pd.Timestamp.now().normalize() - inf_date.normalize()).days
            if inf_age < 0 or inf_age > cfg["inflation_age"]:
                raise ValueError(f"letzter Wert {inf_date.date()} ist {inf_age} Tage alt")
            loaded[(currency, "inflation")] = inf
        except Exception as exc:
            errors.append(f"{currency}-Inflation ({inf_sid}) nicht aktuell: {exc}")

    base_rate = float(loaded[(base_currency, "rate")].iloc[-1]["value"])
    quote_rate = float(loaded[(quote_currency, "rate")].iloc[-1]["value"])
    rate_diff = base_rate - quote_rate
    rate_component = float(np.clip(rate_diff / 2.0 * 100, -100, 100))

    base_infl = quote_infl = None
    if not errors:
        def yoy(currency):
            df = loaded[(currency, "inflation")]
            last = df.iloc[-1]
            target = pd.Timestamp(last["date"]) - pd.DateOffset(years=1)
            prior = df[df["date"] <= target]
            if prior.empty or float(prior.iloc[-1]["value"]) == 0:
                raise ValueError(f"Kein passender Vorjahreswert für {currency}-Inflation")
            return (float(last["value"]) / float(prior.iloc[-1]["value"]) - 1) * 100
        try:
            base_infl, quote_infl = yoy(base_currency), yoy(quote_currency)
        except Exception as exc:
            errors.append(f"Inflationsvergleich nicht möglich: {exc}")

    base_label = MACRO_CURRENCY_SERIES[base_currency]["label"]
    quote_label = MACRO_CURRENCY_SERIES[quote_currency]["label"]
    if base_infl is not None and quote_infl is not None:
        inflation_diff = base_infl - quote_infl
        inflation_component = float(np.clip(-inflation_diff / 2.0 * 100, -100, 100))
        score = int(round(0.65 * rate_component + 0.35 * inflation_component))
        details = (f"{base_currency} ({base_label}) {base_rate:.2f}% vs. "
                   f"{quote_currency} ({quote_label}) {quote_rate:.2f}% (Zinsdifferenz {rate_diff:+.2f} pp); "
                   f"Inflation YoY {base_currency} {base_infl:.2f}% vs. {quote_currency} {quote_infl:.2f}% "
                   f"(Differenz {inflation_diff:+.2f} pp).")
        mode = "Zinsen + Inflation"
    else:
        score = int(round(rate_component))
        details = (f"TEILWEISE: nur Zinsdifferenz verwendet. {base_currency} ({base_label}) "
                   f"{base_rate:.2f}% vs. {quote_currency} ({quote_label}) {quote_rate:.2f}% "
                   f"(Differenz {rate_diff:+.2f} pp). Inflation wurde wegen fehlender/veralteter Reihe "
                   f"nicht verwendet. " + " | ".join(errors))
        mode = "Nur Zinsdaten"

    return {"score": score, "rate_diff": rate_diff, "base_inflation_yoy": base_infl,
            "quote_inflation_yoy": quote_infl, "details": details, "mode": mode,
            "partial": base_infl is None or quote_infl is None}, None

def calculate_eurusd_macro_score(api_key):
    """Backward-compatible wrapper for the EUR/USD relative macro score."""
    return calculate_relative_macro_score(api_key, "EUR", "USD")

def quality_percent(valid_flags):
    if not valid_flags:
        return 0
    return round(100 * sum(bool(x) for x in valid_flags) / len(valid_flags))

st.markdown('<div class="brand"><div class="logo"><span>◇</span></div><div><div class="brand-title">MACRO / REGIME TERMINAL</div><div class="brand-sub">FX · Makro · COT · Saisonalität · Quant · Regime</div></div></div>', unsafe_allow_html=True)
st.caption("Forex · Makro · COT · Saisonalität · technische Bestätigung")
st.warning("Datenstatus: Ohne konfigurierte Datenquelle werden keine aktuellen Marktmeinungen behauptet. Historische Daten sind nicht automatisch Echtzeitdaten; Anbieter, Verzögerung und Lizenzbedingungen beachten.")

with st.sidebar:
    st.markdown('<div class="brand"><div class="logo"><span>◇</span></div><div><div class="brand-title" style="font-size:16px">MACRO / REGIME</div><div class="brand-sub" style="font-size:10px">FX · Makro · COT · Quant</div></div></div>', unsafe_allow_html=True)
    st.header("Einstellungen")
    page = st.radio("Modul", ["Übersicht", "FX Signal", "ML Lab", "Index ML Lab", "Saisonalität", "COT / Positioning", "NQ & ES", "Index Macro & Seasonality", "Quant & Regression", "Datenquellen"])
    st.divider()
    try:
        saved_fred_key = st.secrets.get("FRED_API_KEY", "")
    except Exception:
        saved_fred_key = ""
    fred_key = st.text_input(
        "FRED API-Key (optional)", value=saved_fred_key, type="password",
        help="Hier eingeben oder sicher in Streamlit Secrets als FRED_API_KEY hinterlegen."
    )
    st.caption(f"Ansicht erstellt: {utc_now()}")
    st.caption("Build: FX Signal Engine v1.2 · FX + COT · Bias nur aus validierten Daten")

# Demo values are intentionally labeled and are not market data.
demo_strength = pd.DataFrame({
    "Währung": G10,
    "Score": [0.8, 0.3, 0.5, -0.9, 0.1, 0.2, -0.4, -0.6]
})
demo_strength["Status"] = "DEMO"

if page == "Übersicht":
    # Reference-style FX ticker strip. It only displays values from the last manual refresh;
    # it never triggers a hidden market-data request on page load.
    ticker_pairs = [("EUR/USD", "EUR/USD"), ("GBP/USD", "GBP/USD"), ("USD/JPY", "USD/JPY"),
                    ("AUD/USD", "AUD/USD"), ("USD/CAD", "USD/CAD"), ("USD/CHF", "USD/CHF"), ("NZD/USD", "NZD/USD")]
    _existing_snap = st.session_state.get("dashboard_snapshot")
    _ticker_df = pd.DataFrame(_existing_snap["prices"]) if _existing_snap else pd.DataFrame()
    _ticker_cols = st.columns(7, gap="small")
    for _col, (_pair_label, _market_label) in zip(_ticker_cols, ticker_pairs):
        _hit = _ticker_df.loc[_ticker_df["Markt"] == _market_label] if not _ticker_df.empty and "Markt" in _ticker_df else pd.DataFrame()
        if not _hit.empty:
            _row = _hit.iloc[0]
            _price = pd.to_numeric(_row.get("Letzter Kurs"), errors="coerce")
            _ret = pd.to_numeric(_row.get("20T-Rendite (%)"), errors="coerce")
            _price_text = "—" if pd.isna(_price) else (f"{_price:.4f}" if _price < 10 else f"{_price:.3f}")
            _ret_text = "—" if pd.isna(_ret) else f"{_ret:+.2f}% / 20T"
            _ret_class = "positive" if pd.notna(_ret) and _ret >= 0 else "negative"
        else:
            _price_text, _ret_text, _ret_class = "—", "Noch nicht geladen", "muted"
        _col.markdown(f'<div class="ticker"><div class="ticker-name">{_pair_label}</div><div class="ticker-value">{_price_text} <span class="{_ret_class}" style="float:right">{_ret_text}</span></div></div>', unsafe_allow_html=True)
    st.write("")
    st.subheader("Zentrales Dashboard")
    st.caption("Ein gemeinsamer Überblick über FX, US-Makro und Cross-Asset-Proxys. Daten werden nur auf Knopfdruck abgerufen; Yahoo Finance ist kein garantierter Echtzeitfeed.")
    st.warning("Regime-Einschätzung ist ein transparenter Proxy aus NQ/ES/VIX und kein validiertes Handelssignal. Fehlende Daten bleiben fehlend.")

    if "dashboard_snapshot" not in st.session_state:
        st.session_state["dashboard_snapshot"] = None

    dcol1, dcol2 = st.columns([1, 3])
    with dcol1:
        refresh_dashboard = st.button("Dashboard aktualisieren", type="primary", use_container_width=True)
    with dcol2:
        st.caption("Abruf: tägliche historische Kurse via yfinance sowie ausgewählte FRED-Reihen. Der FRED-Key wird aus Sidebar/Secrets verwendet.")

    if refresh_dashboard:
        price_rows, price_frames, fred_rows, errors = [], {}, [], []
        dashboard_symbols = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X",
                             "AUD/USD": "AUDUSD=X", "USD/CAD": "CAD=X", "USD/CHF": "CHF=X",
                             "NZD/USD": "NZDUSD=X", "Nasdaq-100 Future": "NQ=F",
                             "S&P 500 Future": "ES=F", "VIX": "^VIX"}
        with st.spinner("Lade Markt- und Makrodaten…"):
            for label, symbol in dashboard_symbols.items():
                try:
                    hist = load_market_history(symbol, "1y")
                    if hist.empty:
                        raise ValueError("keine Kursdaten zurückgegeben")
                    hist = hist.copy()
                    hist["date"] = pd.to_datetime(hist["date"], utc=True, errors="coerce")
                    hist["close"] = pd.to_numeric(hist["close"], errors="coerce")
                    hist = hist.dropna(subset=["date", "close"]).sort_values("date")
                    if hist.empty or float(hist.iloc[-1]["close"]) <= 0:
                        raise ValueError("keine gültigen Schlusskurse")
                    last = hist.iloc[-1]
                    age_days = (pd.Timestamp.now(tz="UTC") - last["date"]).total_seconds() / 86400
                    ret20 = float(hist["close"].pct_change(20).iloc[-1] * 100) if len(hist) > 20 else np.nan
                    price_rows.append({"Markt": label, "Symbol": symbol, "Letzter Kurs": float(last["close"]),
                                       "Letztes Datum (UTC)": last["date"].date().isoformat(),
                                       "Alter (Tage)": round(age_days, 1), "20T-Rendite (%)": ret20,
                                       "Status": "OK" if age_days <= 4 else "VERALTET"})
                    price_frames[label] = hist
                except Exception as exc:
                    errors.append(f"{label} ({symbol}): {exc}")
            fred_map = {"FEDFUNDS": ("Fed Funds Rate", "% p.a."), "DGS10": ("US Treasury 10Y", "% p.a."),
                        "DGS2": ("US Treasury 2Y", "% p.a."), "DTWEXBGS": ("Breiter USD-Index", "Index")}
            if fred_key:
                for sid, (label, unit) in fred_map.items():
                    try:
                        series = get_fred_series(sid, fred_key)
                        if series.empty:
                            raise ValueError("keine Beobachtungen")
                        last = series.iloc[-1]
                        fred_rows.append({"Indikator": label, "FRED-Serie": sid,
                                          "Letzter Wert": float(last["value"]), "Einheit": unit,
                                          "Beobachtungsdatum": pd.Timestamp(last["date"]).date().isoformat(),
                                          "Status": "OK"})
                    except Exception as exc:
                        errors.append(f"FRED {sid}: {exc}")
            else:
                errors.append("FRED: API-Key fehlt; US-Makroindikatoren wurden übersprungen.")
        st.session_state["dashboard_snapshot"] = {"prices": price_rows, "frames": price_frames,
                                                    "fred": fred_rows, "errors": errors,
                                                    "updated": utc_now()}

    snap = st.session_state.get("dashboard_snapshot")
    if snap is None:
        st.info("Klicke auf „Dashboard aktualisieren“, um aktuelle verfügbare Daten abzurufen. Bis dahin werden bewusst keine Marktwerte oder Scores erfunden.")
        st.markdown("#### Enthaltene Bereiche")
        st.write("FX-Spot-Proxys · NQ/ES und VIX · FRED-Zinsen und USD-Index · Datenalter und Fehlerstatus")
    else:
        price_df = pd.DataFrame(snap["prices"])
        fred_df = pd.DataFrame(snap["fred"])
        st.caption(f"Letzter Dashboard-Abruf: {snap['updated']}")
        if not price_df.empty:
            def _row(label):
                found = price_df.loc[price_df["Markt"] == label]
                return found.iloc[0] if not found.empty else None
            nq, es, vix = _row("Nasdaq-100 Future"), _row("S&P 500 Future"), _row("VIX")
            fresh = int((price_df["Status"] == "OK").sum())
            total = len(price_df)
            regime = "UNBESTIMMT"
            regime_note = "NQ/ES/VIX-Daten fehlen oder sind nicht vollständig frisch."
            if nq is not None and es is not None and vix is not None and all(r["Status"] == "OK" for r in (nq, es, vix)):
                if nq["20T-Rendite (%)"] > 0 and es["20T-Rendite (%)"] > 0 and vix["20T-Rendite (%)"] <= 0:
                    regime, regime_note = "RISK-ON (PROXY)", "NQ und ES positiv über 20 Handelstage, VIX nicht gestiegen."
                elif nq["20T-Rendite (%)"] < 0 and es["20T-Rendite (%)"] < 0 and vix["20T-Rendite (%)"] > 0:
                    regime, regime_note = "RISK-OFF (PROXY)", "NQ und ES negativ über 20 Handelstage, VIX gestiegen."
                else:
                    regime, regime_note = "GEMISCHT / NEUTRAL", "Cross-Asset-Bedingungen widersprechen sich oder sind uneindeutig."
            fx_labels = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "NZD/USD"]
            fx = price_df[price_df["Markt"].isin(fx_labels) & (price_df["Status"] == "OK")]
            strongest = weakest = "—"
            if len(fx) >= 2:
                # Directional 20d proxy is pair-based and is NOT a normalized G10 currency-strength model.
                strongest = str(fx.sort_values("20T-Rendite (%)", ascending=False).iloc[0]["Markt"])
                weakest = str(fx.sort_values("20T-Rendite (%)").iloc[0]["Markt"])
            # Reference-style overview: KPI row, three analytical panels, then market table + data quality.
            k1, k2, k3, k4, k5 = st.columns(5, gap="small")
            k1.metric("🛡️ Risk Regime (Proxy)", regime.replace(" (PROXY)", ""), regime_note[:65])
            k2.metric("💱 FX-Paare verfügbar", f"{len(fx)}/7", "Yahoo Finance")
            k3.metric("▤ Frische Marktserien", f"{fresh}/{total}", "Verfügbare Abfragen")
            _us10 = fred_df.loc[fred_df["FRED-Serie"] == "DGS10"] if not fred_df.empty and "FRED-Serie" in fred_df else pd.DataFrame()
            _vix = _row("VIX")
            k4.metric("📈 US 10Y Rendite", (f"{float(_us10.iloc[0]['Letzter Wert']):.2f} %" if not _us10.empty else "—"), "FRED")
            k5.metric("〽️ VIX", (f"{float(_vix['Letzter Kurs']):.2f}" if _vix is not None else "—"), "Yahoo Finance")
            st.caption(regime_note)

            left, middle, right = st.columns([1.05, 1.35, 1.0], gap="medium")
            with left:
                st.markdown("**🌐 G10 Währungsstärke (20 Tage)**")
                if len(fx) >= 2:
                    strength_df = fx[["Markt", "20T-Rendite (%)"]].dropna().sort_values("20T-Rendite (%)")
                    if not strength_df.empty:
                        fig = go.Figure(go.Bar(x=strength_df["20T-Rendite (%)"], y=strength_df["Markt"], orientation="h",
                            marker_color=["#00d49a" if x >= 0 else "#ff2448" for x in strength_df["20T-Rendite (%)"]]))
                        fig.update_layout(height=300, margin=dict(l=0,r=5,t=8,b=8), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#a8bfd3",size=10), xaxis_title="% Veränderung", yaxis_title="", showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else: st.info("Keine ausreichenden FX-Daten.")
                else: st.info("Keine ausreichenden FX-Daten.")
            with middle:
                st.markdown("**♟ Markt-Regime-Indikatoren**")
                fig = go.Figure()
                for label, color in [("Nasdaq-100 Future", "#ff2448"), ("S&P 500 Future", "#55aaff"), ("VIX", "#ffbf47")]:
                    hist = snap["frames"].get(label)
                    if hist is not None and not hist.empty:
                        vals = pd.to_numeric(hist["close"], errors="coerce").dropna()
                        if len(vals) > 1:
                            norm = (vals / vals.iloc[0] - 1) * 100
                            if label == "VIX": norm = -norm
                            fig.add_trace(go.Scatter(x=hist.loc[vals.index, "date"] if "date" in hist else vals.index, y=norm, name=label, mode="lines", line=dict(color=color,width=2)))
                fig.add_hline(y=0, line_color="#526779", line_width=1)
                fig.update_layout(height=300, margin=dict(l=0,r=5,t=8,b=8), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#a8bfd3",size=10), legend=dict(orientation="h",y=1.12), xaxis_title="", yaxis_title="% normalisiert")
                st.plotly_chart(fig, use_container_width=True)
            with right:
                st.markdown("**🏦 US Makro (FRED)**")
                if not fred_df.empty:
                    for _, row in fred_df.iterrows():
                        st.markdown(f"<div style='padding:9px 0;border-bottom:1px solid #203043'><div style='color:#8198ad;font-size:12px'>{row['Indikator']}</div><b style='font-size:18px'>{float(row['Letzter Wert']):.2f}{' %' if '%' in str(row['Einheit']) else ''}</b><div style='color:#8198ad;font-size:11px'>{row['Beobachtungsdatum']}</div></div>", unsafe_allow_html=True)
                else:
                    st.info("Keine FRED-Reihen geladen. API-Key links eingeben.")

            st.write("")
            left, right = st.columns([2.1, 1.0], gap="medium")
            with left:
                st.markdown("**💹 FX- und Cross-Asset-Märkte**")
                st.dataframe(price_df, use_container_width=True, hide_index=True)
            with right:
                st.markdown("**🟢 Datenqualität**")
                _checks = [("FX-Kurse (Yahoo Finance)", len(fx), 7), ("NQ / ES / VIX", sum(_row(x) is not None for x in ["Nasdaq-100 Future", "S&P 500 Future", "VIX"]), 3), ("Makrodaten (FRED)", len(fred_df), 4)]
                for _label, _ok, _total in _checks:
                    _color = "#00d49a" if _ok == _total else ("#ffbf47" if _ok else "#ff2448")
                    st.markdown(f"<div style='padding:10px 0;border-bottom:1px solid #203043'><b>{_label}</b><span style='float:right;color:{_color}'>● {_ok}/{_total}</span></div>", unsafe_allow_html=True)
                st.caption("Historische Daten sind nicht automatisch Echtzeitdaten.")
        else:
            st.error("Keine Kursdaten verfügbar; das Regime bleibt unbestimmt.")
            st.info("Keine FRED-Reihen geladen. FRED_API_KEY in Streamlit Secrets konfigurieren oder links in der Sidebar eingeben.")
        if snap["errors"]:
            with st.expander(f"Datenprobleme ({len(snap['errors'])})", expanded=False):
                for err in snap["errors"]:
                    st.write(f"- {err}")
        st.caption("Hinweis: „Stärkste/Schwächste“ wird hier bewusst nicht als Währungsstärke ausgegeben. Paar-Renditen sind nicht über alle G10-Währungen normalisiert. FX Signal, ML Lab, COT, Saisonalität, NQ & ES und Quant & Regression bleiben eigenständige Module.")

elif page in ("FX Signal", "FX Macro"):
    st.subheader("Forex Bias Engine")
    st.caption("LONG/SHORT erst ab ±20 und nur, wenn Makro, COT, Saisonalität sowie technische Bestätigung validiert sind. Nicht verbundene Faktoren erzwingen NEUTRAL.")
    pair = st.selectbox("Forex-Paar", list(FX_PAIRS.keys()))
    pair_info = FX_PAIRS[pair]
    st.markdown("#### Datenvalidierung & Bias")
    if st.button("Echte Kursdaten laden und validieren", type="primary"):
        try:
            price_df = load_market_history(pair_info["symbol"], "10y")
            price_ok, price_message, validated_prices = validate_price_history(price_df)
            tech_score, tech_message = technical_confirmation(validated_prices) if price_ok else (None, "Technik blockiert: Kursdaten nicht validiert")
            component_valid = {"macro": False, "cot": False, "seasonality": False}
            component_scores = {}
            macro_result, macro_error = (None, "FRED API-Key fehlt")
            if fred_key:
                try:
                    macro_result, macro_error = calculate_relative_macro_score(
                        fred_key, pair_info["base"], pair_info["quote"]
                    )
                    if macro_result is not None:
                        component_valid["macro"] = True
                        component_scores["macro"] = macro_result["score"]
                except Exception as macro_exc:
                    macro_error = str(macro_exc)
            cot_result, cot_error = None, "COT noch nicht geladen"
            season_result, season_error = None, "Saisonalität noch nicht berechnet"
            # COT is loaded from the public CFTC API and accepted only when mapping,
            # history length, schema and report freshness pass validation.
            try:
                cot_df = load_cot_history(pair_info["cot"], limit=52)
                cot_score, cot_net, cot_pct = cot_positioning_score(cot_df, invert=pair_info.get("cot_invert", False))
                cot_result = {"score": cot_score, "net": cot_net, "percentile": cot_pct,
                              "date": cot_df.iloc[-1]["date"].date().isoformat(),
                              "market": cot_df.attrs.get("market_name", pair_info["cot"]),
                              "age_days": cot_df.attrs.get("age_days", None)}
                component_valid["cot"] = True
                component_scores["cot"] = cot_score
            except Exception as cot_exc:
                cot_error = str(cot_exc)
            # Seasonality uses the same actual price history; no synthetic fallback.
            try:
                if price_ok:
                    season_score, mean_return, season_n = seasonality_component_score(
                        validated_prices, invert=pair_info["symbol"] in ("JPY=X", "CAD=X", "CHF=X")
                    )
                    season_result = {"score": season_score, "mean_return": mean_return, "n": season_n}
                    component_valid["seasonality"] = True
                    component_scores["seasonality"] = season_score
                else:
                    season_error = "Kursreihe nicht validiert; Saisonalität blockiert"
            except Exception as season_exc:
                season_error = str(season_exc)
            # Composite score is calculated once in the engine; missing inputs fail closed.
            result = combine_fx_signal(component_scores, component_valid, tech_score)
            flags = [price_ok, component_valid["macro"], component_valid["cot"], component_valid["seasonality"], tech_score is not None]
            q_data = quality_percent(flags)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Bias", result["bias"])
            c2.metric("Gesamtscore", "—" if result["score"] is None else f"{result['score']:+d} / 100")
            c3.metric("Datenqualität", f"{q_data}%")
            c4.metric("Signalqualität", result["signal_quality"])
            st.info(result["reason"])
            # Separate provisional market direction from the fully validated signal.
            # This helps every pair show the available evidence without pretending
            # that missing relative macro data has been validated.
            provisional_parts = []
            provisional_weights = []
            if component_valid.get("cot") and "cot" in component_scores:
                provisional_parts.append(0.45 * component_scores["cot"])
                provisional_weights.append(0.45)
            if component_valid.get("seasonality") and "seasonality" in component_scores:
                provisional_parts.append(0.15 * component_scores["seasonality"])
                provisional_weights.append(0.15)
            if tech_score is not None:
                provisional_parts.append(0.40 * (100 * tech_score))
                provisional_weights.append(0.40)
            st.markdown("#### Vorläufige Richtung (verfügbare Daten, noch kein bestätigtes Handelssignal)")
            if provisional_weights:
                provisional_score = int(round(sum(provisional_parts) / sum(provisional_weights)))
                if provisional_score >= LONG_SHORT_THRESHOLD and tech_score == 1:
                    provisional_bias = "BULLISH / LONG-TENDENZ"
                    st.success(f"{provisional_bias} · Score {provisional_score:+d}/100. COT, Saisonalität und Technik soweit verfügbar; Makrovergleich fehlt ggf. noch.")
                elif provisional_score <= -LONG_SHORT_THRESHOLD and tech_score == -1:
                    provisional_bias = "BEARISH / SHORT-TENDENZ"
                    st.error(f"{provisional_bias} · Score {provisional_score:+d}/100. COT, Saisonalität und Technik soweit verfügbar; Makrovergleich fehlt ggf. noch.")
                else:
                    provisional_bias = "NEUTRAL"
                    st.info(f"{provisional_bias} · Score {provisional_score:+d}/100. Die verfügbaren Faktoren zeigen keine ausreichend bestätigte Richtung.")
                st.caption("Diese vorläufige Richtung ersetzt nicht den finalen Bias. Der finale LONG/SHORT-Status bleibt gesperrt, solange erforderliche Makro-, COT-, Saison- oder Technikdaten fehlen bzw. nicht validiert sind.")
            else:
                st.warning("Vorläufige Richtung nicht bewertbar: Es liegen noch keine validierten COT-, Saison- oder Technikwerte vor.")
            # Explain the direction consistently for every selectable FX pair.
            if result["bias"] == "LONG":
                st.success(f"Einordnung für {pair}: LONG bedeutet, dass die Basiswährung ({pair_info['base']}) gegenüber der Kurswährung ({pair_info['quote']}) bevorzugt wird. Das ist nur ein validiertes Setup, keine Garantie.")
            elif result["bias"] == "SHORT":
                st.error(f"Einordnung für {pair}: SHORT bedeutet, dass die Basiswährung ({pair_info['base']}) gegenüber der Kurswährung ({pair_info['quote']}) schwächer eingeschätzt wird.")
            else:
                st.info(f"Einordnung für {pair}: NEUTRAL — aktuell kein freigegebenes LONG-/SHORT-Signal. Fehlende oder nicht bestätigte Faktoren werden nicht durch Schätzwerte ersetzt.")
            st.caption(
                "Die vorläufige Richtung wird für alle auswählbaren Paare aus den jeweils verfügbaren, "
                "validierten Nicht-Makro-Faktoren berechnet. Der finale Bias wird nur freigegeben, wenn "
                "Makro, COT, Saisonalität und Technik vollständig validiert sind. Für die hinterlegten "
                "Währungen wird der relative Makrovergleich aus Zins- und Inflationsreihen berechnet; "
                "außerhalb USD/EUR dienen teils kurzfristige Zinsreihen als Proxy."
            )
            if result["bias"] == "NEUTRAL":
                missing_names = {
                    "macro": "relativer Makrovergleich fehlt oder ist veraltet",
                    "cot": "COT-Positionierung fehlt oder ist nicht frisch",
                    "seasonality": "Saisonalität ist nicht ausreichend belegt",
                }
                missing_readable = [
                    missing_names.get(name, name)
                    for name in ("macro", "cot", "seasonality")
                    if not component_valid.get(name, False)
                ]
                if tech_score is None:
                    missing_readable.append("technische Daten sind nicht validiert")
                elif tech_score == 0:
                    missing_readable.append("Technik bestätigt weder bullish noch bearish")
                st.info("Warum NEUTRAL? " + (
                    "; ".join(missing_readable) if missing_readable
                    else "Der gewichtete Score erreicht die Schwelle nicht oder Technik bestätigt die Richtung nicht."
                ) + ".")
            st.write("**Technische Prüfung:**", tech_message)
            st.write("**Kursdaten:**", price_message)
            st.markdown(f"#### Relativer Makro-Score ({pair_info['base']} gegenüber {pair_info['quote']})")
            if macro_result is not None:
                st.metric(f"Makro-Score {pair}", f"{macro_result['score']:+d} / 100")
                st.caption(macro_result["details"])
                st.caption("Heuristik: Zinsdifferenz 65%, Inflationsdifferenz 35%. Ein positiver Wert begünstigt die Basiswährung relativ zur Quote-Währung; kein alleiniger Trade-Trigger.")
            else:
                st.warning("Makro-Score nicht verfügbar: " + str(macro_error) + ". Prüfe FRED-Key und Serienverfügbarkeit.")
            quality_rows = [
                {"Komponente": "FX-Kursdaten", "Status": "VALIDIERT" if price_ok else "UNGÜLTIG", "Einordnung": price_message},
                {"Komponente": "Relatives Makro beider Währungen", "Status": "VALIDIERT" if component_valid["macro"] else "FEHLT", "Einordnung": macro_result["details"] if macro_result is not None else str(macro_error)},
                {"Komponente": "COT", "Status": "VALIDIERT" if cot_result is not None else "FEHLT", "Einordnung": (f"{cot_result['market']} · Report {cot_result['date']} · Non-commercial net {cot_result['net']:,.0f} · Score {cot_result['score']:+d} · {cot_result['age_days']:.1f} Tage alt" if cot_result is not None else cot_error)},
                {"Komponente": "Saisonalität", "Status": "VALIDIERT" if season_result is not None else "FEHLT", "Einordnung": (f"Kalendermonat {datetime.now().strftime('%B')} · Ø {season_result['mean_return']:.2%} über {season_result['n']} Jahre · Score {season_result['score']:+d}" if season_result is not None else season_error)},
                {"Komponente": "Technische Bestätigung", "Status": "VALIDIERT" if tech_score is not None else "FEHLT", "Einordnung": tech_message},
            ]
            st.dataframe(pd.DataFrame(quality_rows), use_container_width=True, hide_index=True)
            cota, cotb, cotc = st.columns(3)
            if cot_result is not None:
                cota.metric("COT-Score", f"{cot_result['score']:+d} / 100")
                cotb.metric("Non-commercial net", f"{cot_result['net']:,.0f}")
                cotc.metric("COT-Bericht", cot_result["date"])
                st.caption(f"CFTC Legacy Futures Only · {cot_result['market']} · {cot_result['age_days']:.1f} Tage alt. Non-commercial net ist Futures-Positionierung, kein vollständiges Spot-FX-Orderflow-Maß.")
            else:
                cota.warning("COT nicht validiert: " + cot_error)
            if season_result is not None:
                st.caption(f"Saisonalität: aktueller Kalendermonat Ø {season_result['mean_return']:.2%} aus {season_result['n']} historischen Monatsbeobachtungen; Score {season_result['score']:+d}.")
            else:
                st.caption("Saisonalität nicht freigegeben: " + season_error)
            if price_ok:
                st.line_chart(validated_prices.set_index("date")["close"])
            st.warning("Fail-closed aktiv: Der finale Bias bleibt NEUTRAL, bis Makro, COT und Saisonalität aus echten, korrekt zugeordneten und frischen Daten validiert sind. Der Makro-Score allein ist noch kein Gesamt- oder Handelssignal.")
        except Exception as exc:
            st.error(f"Kursabruf/Validierung fehlgeschlagen: {exc}")
            st.metric("Bias", "NEUTRAL")
            st.metric("Datenqualität", "0% / nicht validiert")
    else:
        st.info("Noch keine aktuelle Kursprüfung durchgeführt. Ohne erfolgreichen Datenabruf bleibt der Bias NEUTRAL.")
    st.divider()
    st.subheader("Makro-Datenlabor (USD, nicht allein signalberechtigt)")
    st.caption("Lädt verfügbare US-Makroserien aus FRED. Das ist noch kein vollständiger G10-Vergleich; andere Länder benötigen eigene Datenzuordnungen.")
    fred_series = {
        "FEDFUNDS": ("US Effective Federal Funds Rate", "% p.a."),
        "CPIAUCSL": ("US CPI Index", "Index"),
        "UNRATE": ("US Arbeitslosenquote", "%"),
        "DGS10": ("US Treasury 10Y", "% p.a."),
        "DGS2": ("US Treasury 2Y", "% p.a."),
        "T10YIE": ("US 10Y Breakeven Inflation", "% p.a."),
        "DTWEXBGS": ("US Dollar Index (breit, nominal)", "Index"),
        "ECBDFR": ("EZB Einlagefazilität (Eurozone)", "% p.a."),
        "CP0000EZCCM086NEST": ("Eurozone HICP (harmonisierter Verbraucherpreisindex)", "Index 2025=100"),
    }
    if not fred_key:
        st.info("Trage links deinen FRED API-Key ein. Danach kannst du die Makroindikatoren laden.")
    selected = st.multiselect("Indikatoren", list(fred_series.keys()), default=["FEDFUNDS", "CPIAUCSL", "UNRATE", "DGS10", "DGS2", "ECBDFR", "CP0000EZCCM086NEST"], format_func=lambda sid: f"{sid} — {fred_series[sid][0]}")
    if st.button("Makroindikatoren laden", type="primary"):
        if not fred_key:
            st.error("Bitte zuerst links einen FRED API-Key eintragen.")
        elif not selected:
            st.warning("Bitte mindestens einen Indikator auswählen.")
        else:
            summary, errors = [], []
            loaded_series = {}
            with st.spinner("Lade FRED-Daten…"):
                for sid in selected:
                    try:
                        series_df = get_fred_series(sid, fred_key)
                        loaded_series[sid] = series_df.copy()
                        if series_df.empty:
                            errors.append(f"{sid}: keine Beobachtungen zurückgegeben.")
                            continue
                        last = series_df.iloc[-1]
                        prev = series_df.iloc[-2] if len(series_df) > 1 else None
                        summary.append({"Serie": sid, "Indikator": fred_series[sid][0], "Letztes Datum": last["date"].date().isoformat(), "Letzter Wert": float(last["value"]), "Einheit": fred_series[sid][1], "Vorwert": float(prev["value"]) if prev is not None else None, "Beobachtungen": len(series_df)})
                    except Exception as exc:
                        errors.append(f"{sid}: {exc}")
            if summary:
                result = pd.DataFrame(summary)
                st.success(f"{len(summary)} von {len(selected)} Serien erfolgreich geladen.")
                st.dataframe(result, use_container_width=True, hide_index=True)
                chosen = st.selectbox("Serie im Verlauf anzeigen", [r["Serie"] for r in summary], format_func=lambda sid: f"{sid} — {fred_series[sid][0]}")
                try:
                    history = get_fred_series(chosen, fred_key)
                    st.line_chart(history.set_index("date")["value"])
                    st.caption(f"Quelle: FRED · Serie {chosen} · letzter verfügbarer Datenpunkt {history.iloc[-1]['date'].date().isoformat()}. Frequenz und Aktualisierung hängen von der Serie ab; keine garantierten Echtzeitdaten.")
                    st.dataframe(history.tail(12), use_container_width=True, hide_index=True)
                except Exception as exc:
                    st.error(f"Verlauf konnte nicht angezeigt werden: {exc}")
            if errors:
                st.warning("Einige Serien konnten nicht geladen werden: " + " | ".join(errors))

            st.info("Die geladenen US-Makroserien dienen derzeit nur der Dateninspektion. Sie erzeugen keinen Forex-Bias, da ein validierter Vergleich mit dem Gegenwährungsraum und Konsistenzchecks fehlen.")
    st.markdown("#### Status der G10-Abdeckung")
    coverage = pd.DataFrame([
        ["USD", "Teilweise verbunden", "US-Makroindikatoren oben über FRED ladbar"],
        ["EUR", "Teilweise verbunden", "EZB-Einlagezins und Eurozonen-HICP via FRED; weitere Reihen fehlen"],
        ["GBP", "Nicht verbunden", "BoE-/ONS-Serien separat integrieren"],
        ["JPY", "Nicht verbunden", "BoJ-/Japan-Statistikserien separat integrieren"],
        ["CHF", "Nicht verbunden", "SNB-/Schweizer Statistikserien separat integrieren"],
        ["CAD", "Nicht verbunden", "BoC-/Statistics Canada-Serien separat integrieren"],
        ["AUD", "Nicht verbunden", "RBA-/ABS-Serien separat integrieren"],
        ["NZD", "Nicht verbunden", "RBNZ-/Stats NZ-Serien separat integrieren"],
    ], columns=["CCY", "Status", "Hinweis"])
    st.dataframe(coverage, use_container_width=True, hide_index=True)

elif page == "ML Lab":
    st.subheader("ML Lab — FX-Richtungsprognose")
    st.caption("Walk-forward-Auswertung je einzelner Währung gegenüber USD bzw. beim USD gegenüber dem breiten Dollarindex. Keine Kursgarantie; Ergebnisse sind nur so belastbar wie Daten und Testdesign.")
    currency_proxies = {
        "EUR — Euro": {"symbol": "EURUSD=X", "invert": False, "reference": "USD"},
        "USD — US-Dollar": {"symbol": "DX-Y.NYB", "invert": False, "reference": "breiter USD-Index (DXY)"},
        "GBP — Britisches Pfund": {"symbol": "GBPUSD=X", "invert": False, "reference": "USD"},
        "JPY — Japanischer Yen": {"symbol": "JPY=X", "invert": True, "reference": "USD (inverse USD/JPY-Reihe)"},
        "CHF — Schweizer Franken": {"symbol": "CHF=X", "invert": True, "reference": "USD (inverse USD/CHF-Reihe)"},
        "CAD — Kanadischer Dollar": {"symbol": "CAD=X", "invert": True, "reference": "USD (inverse USD/CAD-Reihe)"},
        "AUD — Australischer Dollar": {"symbol": "AUDUSD=X", "invert": False, "reference": "USD"},
        "NZD — Neuseeland-Dollar": {"symbol": "NZDUSD=X", "invert": False, "reference": "USD"},
    }
    currency = st.selectbox("Einzelne Währung", list(currency_proxies.keys()), key="ml_currency")
    proxy = currency_proxies[currency]
    horizon = st.selectbox("Prognosehorizont", [10, 30, 60, 90], index=3, format_func=lambda x: f"{x} Handelstage", key="ml_horizon")
    years = st.selectbox("Trainingshistorie", ["5y", "10y", "max"], index=1, key="ml_years")
    st.caption(f"Referenz: {proxy['reference']}. Bei JPY/CHF/CAD wird die inverse USD-Notierung verwendet, damit steigende Werte eine stärkere ausgewählte Währung bedeuten.")

    # Fundamental panel for the selected currency alone (not a currency-pair comparison).
    st.markdown("#### Fundamentaler Währungs-Scanner — jeder Punkt ein Faktor")
    st.caption("Bewertet ausschließlich die oben ausgewählte Einzelwährung. Zins- und Inflationszeitreihen werden mit konservativen Veröffentlichungslags zeitlich an die Kursdaten angelegt und – sofern ausreichend Historie verfügbar ist – direkt als Features im ML-Modell trainiert.")
    fund_ccy = currency.split(" — ")[0]
    cfg = MACRO_CURRENCY_SERIES.get(fund_ccy)
    if not fred_key:
        st.info("Für fundamentale Einzelwährungsdaten bitte links einen FRED API-Key eintragen. Ohne Key werden keine Makro-Bewertungen erfunden.")
    elif not cfg:
        st.warning(f"Keine Makro-Zuordnung für {fund_ccy}.")
    else:
        rows = []
        errors = []
        for label, key, bullish_high in [
            ("Leitzins / Kurzfristzins", "rate", True),
            ("Inflation (CPI/HICP)", "inflation", False),
        ]:
            sid = cfg.get(key)
            if not sid:
                errors.append(f"{label}: keine Serien-ID")
                continue
            try:
                series = get_fred_series(sid, fred_key, observation_start="2015-01-01")
                if series.empty:
                    raise ValueError("keine Beobachtungen")
                latest = series.iloc[-1]
                age = (pd.Timestamp.now().normalize() - pd.Timestamp(latest["date"]).normalize()).days
                max_age = int(cfg.get("rate_age" if key == "rate" else "inflation_age", 120))
                if age > max_age:
                    raise ValueError(f"letzter Wert {latest['date'].date()}, {age} Tage alt")
                vals = pd.to_numeric(series["value"], errors="coerce").dropna()
                if len(vals) < 12:
                    raise ValueError("zu wenige historische Werte")
                median = float(vals.median())
                current = float(latest["value"])
                # Relative-to-own-history classification avoids comparing unrelated national levels.
                delta = current - median
                if abs(delta) < 0.10:
                    bias = "NEUTRAL"
                elif (delta > 0) == bullish_high:
                    bias = "BULLISH"
                else:
                    bias = "BEARISH"
                rows.append({"Faktor": label, "Aktueller Wert": current, "Historischer Median": median,
                             "Abweichung zum Median": delta, "Einordnung": bias, "Datenstand": str(pd.Timestamp(latest["date"]).date()),
                             "Alter (Tage)": age, "Serie": sid})
            except Exception as exc:
                errors.append(f"{label} ({sid}): {exc}")
        if rows:
            fdf = pd.DataFrame(rows)
            colors = {"BULLISH":"#16a34a", "BEARISH":"#dc2626", "NEUTRAL":"#94a3b8"}
            fdf["Punktfarbe"] = fdf["Einordnung"].map(colors)
            fig_f = go.Figure()
            for _, rr in fdf.iterrows():
                fig_f.add_trace(go.Scatter(x=[rr["Abweichung zum Median"]], y=[rr["Faktor"]], mode="markers",
                    marker=dict(size=18, color=rr["Punktfarbe"]), name=rr["Einordnung"],
                    customdata=[[rr["Einordnung"], rr["Aktueller Wert"], rr["Historischer Median"], rr["Datenstand"]]],
                    hovertemplate="%{y}<br>Abweichung: %{x:.3f}<br>Bias: %{customdata[0]}<br>Aktuell: %{customdata[1]:.3f}<br>Median: %{customdata[2]:.3f}<br>Datenstand: %{customdata[3]}<extra></extra>"))
            fig_f.add_vline(x=0, line_dash="dash", line_color="gray")
            fig_f.update_layout(title=f"Fundamentale Faktor-Punkte — {fund_ccy} allein", xaxis_title="Aktueller Wert minus eigener historischer Median", yaxis_title="Fundamentalfaktor", height=300, showlegend=False)
            st.plotly_chart(fig_f, use_container_width=True)
            st.dataframe(fdf[["Faktor", "Einordnung", "Aktueller Wert", "Historischer Median", "Abweichung zum Median", "Datenstand", "Alter (Tage)", "Serie"]], use_container_width=True, hide_index=True)
            bulls = int((fdf["Einordnung"] == "BULLISH").sum())
            bears = int((fdf["Einordnung"] == "BEARISH").sum())
            bias = "BULLISH" if bulls > bears else ("BEARISH" if bears > bulls else "NEUTRAL")
            a, b, c = st.columns(3)
            a.metric(f"Makro-Bias {fund_ccy}", bias)
            b.metric("Bullishe Faktoren", bulls)
            c.metric("Bearishe Faktoren", bears)
        if errors:
            st.warning("Nicht verfügbare/veraltete Einzelwährungsdaten: " + " | ".join(errors))
        st.caption("Interpretation: Ein im eigenen historischen Vergleich hoher Zins wird hier als carry-unterstützend gewertet; überdurchschnittliche Inflation als möglicher Gegenwind. Die Scanner-Punkte sind eine Heuristik. Für das ML-Modell werden stattdessen historische Rohzeitreihen plus Veränderungen mit konservativem Zeitversatz verwendet; die Prognosegüte muss im Holdout geprüft werden.")

    if st.button("Modell trainieren und Backtest ausführen", type="primary", key="run_ml_lab"):
        try:
            with st.spinner("Historische Kurse und Makrozeitreihen laden, Features zeitlich abgleichen und testen…"):
                raw = load_market_history(proxy["symbol"], years)
                if not raw.empty and proxy["invert"]:
                    raw = raw.copy()
                    raw["close"] = 1.0 / pd.to_numeric(raw["close"], errors="coerce")
                if raw.empty or len(raw) < 500:
                    st.error("Zu wenige Kursdaten für einen sinnvollen ML-Test (mindestens 500 Tageswerte erforderlich).")
                else:
                    d = raw.copy()
                    d["date"] = pd.to_datetime(d["date"])
                    d = d.sort_values("date").set_index("date")
                    close = d["close"].astype(float)
                    features = pd.DataFrame(index=d.index)
                    for lag in [1, 2, 5, 10, 20]:
                        features[f"ret_{lag}d"] = close.pct_change(lag)
                    for window in [5, 10, 20, 50, 100, 200]:
                        ma = close.rolling(window).mean()
                        features[f"ma_gap_{window}"] = close / ma - 1
                    features["vol_20d"] = close.pct_change().rolling(20).std()
                    features["mom_60d"] = close.pct_change(60)
                    # Calendar/seasonality features are known at forecast time (no future leakage).
                    month = pd.Series(d.index.month, index=d.index, dtype=float)
                    features["month_sin"] = np.sin(2 * np.pi * month / 12.0)
                    features["month_cos"] = np.cos(2 * np.pi * month / 12.0)
                    # Relative short/long volatility and trend persistence.
                    features["vol_ratio_5_20"] = close.pct_change().rolling(5).std() / close.pct_change().rolling(20).std()
                    features["ret_20_minus_60"] = close.pct_change(20) - close.pct_change(60)

                    # Integrate historical macro data for the selected currency itself.
                    # Observation dates are shifted forward conservatively to reduce release-date look-ahead:
                    # policy-rate proxies +7 calendar days; CPI/HICP index proxies +45 days.
                    # These are safety approximations, not exact release calendars / ALFRED vintages.
                    macro_feature_names = []
                    macro_status = "Makro-Features nicht verfügbar; technisches Modell wird verwendet."
                    macro_cfg = MACRO_CURRENCY_SERIES.get(fund_ccy)
                    if fred_key and macro_cfg:
                        try:
                            rate_hist = get_fred_series(macro_cfg["rate"], fred_key, observation_start="2000-01-01")
                            infl_hist = get_fred_series(macro_cfg["inflation"], fred_key, observation_start="2000-01-01")
                            if len(rate_hist) >= 6 and len(infl_hist) >= 15:
                                rate_hist = rate_hist.sort_values("date").drop_duplicates("date").copy()
                                rate_hist["available_date"] = pd.to_datetime(rate_hist["date"]) + pd.Timedelta(days=7)
                                rate_hist["macro_rate_level"] = pd.to_numeric(rate_hist["value"], errors="coerce")
                                rate_hist["macro_rate_change_3m"] = rate_hist["macro_rate_level"] - rate_hist["macro_rate_level"].shift(3)
                                rate_merge = rate_hist[["available_date", "macro_rate_level", "macro_rate_change_3m"]].dropna(subset=["macro_rate_level"])

                                infl_hist = infl_hist.sort_values("date").drop_duplicates("date").copy()
                                infl_hist["available_date"] = pd.to_datetime(infl_hist["date"]) + pd.Timedelta(days=45)
                                infl_hist["infl_index"] = pd.to_numeric(infl_hist["value"], errors="coerce")
                                # CPI/HICP series are normally monthly; require a full 12-observation comparison.
                                infl_hist["macro_inflation_yoy"] = (infl_hist["infl_index"] / infl_hist["infl_index"].shift(12) - 1.0) * 100.0
                                infl_hist["macro_inflation_change_3m"] = infl_hist["macro_inflation_yoy"] - infl_hist["macro_inflation_yoy"].shift(3)
                                infl_merge = infl_hist[["available_date", "macro_inflation_yoy", "macro_inflation_change_3m"]].dropna(subset=["macro_inflation_yoy"])

                                market_dates = pd.DataFrame({"market_date": pd.to_datetime(features.index)}).sort_values("market_date")
                                aligned = pd.merge_asof(market_dates, rate_merge.sort_values("available_date"),
                                                        left_on="market_date", right_on="available_date", direction="backward")
                                aligned = pd.merge_asof(aligned.sort_values("market_date"), infl_merge.sort_values("available_date"),
                                                        left_on="market_date", right_on="available_date", direction="backward", suffixes=("", "_infl"))
                                aligned.index = features.index
                                candidate_cols = ["macro_rate_level", "macro_rate_change_3m", "macro_inflation_yoy", "macro_inflation_change_3m"]
                                coverage = aligned[candidate_cols].notna().all(axis=1).mean()
                                if coverage >= 0.60:
                                    for col in candidate_cols:
                                        features[col] = aligned[col].to_numpy()
                                    macro_feature_names = candidate_cols
                                    macro_status = f"Makro integriert: {fund_ccy} · 4 Features · {coverage:.0%} gemeinsame Abdeckung. Veröffentlichungslags: Zins +7 Tage, Inflation +45 Tage."
                                else:
                                    macro_status = f"Makro nicht ins Training übernommen: nur {coverage:.0%} gemeinsame Abdeckung (benötigt mindestens 60 %). Technisches Modell als Fallback."
                            else:
                                macro_status = "Makro-Historie zu kurz; technisches Modell als Fallback."
                        except Exception as macro_exc:
                            macro_status = f"Makroabruf fehlgeschlagen ({macro_exc}); technisches Modell als Fallback."
                    elif not fred_key:
                        macro_status = "Kein FRED-Key hinterlegt; technisches Modell als Fallback."
                    st.caption(macro_status)

                    target_return = close.shift(-int(horizon)) / close - 1
                    dataset = features.copy()
                    dataset["target"] = (target_return > 0).astype(int)
                    dataset["future_return"] = target_return
                    dataset = dataset.replace([np.inf, -np.inf], np.nan).dropna()
                    # Drop tail where the future outcome is not yet observable.
                    dataset = dataset.iloc[:-int(horizon)]
                    if len(dataset) < 300:
                        st.error("Nach Feature-Bau bleiben zu wenige Beobachtungen. Bitte längere Historie oder kürzeren Horizont wählen.")
                    else:
                        split = int(len(dataset) * 0.8)
                        X, y = dataset.drop(columns=["target", "future_return"]), dataset["target"]
                        X_train, X_test = X.iloc[:split], X.iloc[split:]
                        y_train, y_test = y.iloc[:split], y.iloc[split:]
                        try:
                            from sklearn.ensemble import RandomForestClassifier
                            from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, log_loss
                            from sklearn.calibration import calibration_curve
                            model = RandomForestClassifier(n_estimators=250, max_depth=5, min_samples_leaf=10,
                                                           class_weight="balanced_subsample", random_state=42, n_jobs=-1)
                            model.fit(X_train, y_train)
                            prob_up = model.predict_proba(X_test)[:, list(model.classes_).index(1)]
                            pred = (prob_up >= 0.5).astype(int)
                            actual = y_test.to_numpy()
                            acc = accuracy_score(actual, pred)
                            bacc = balanced_accuracy_score(actual, pred)
                            baseline = max(float((actual == 1).mean()), float((actual == 0).mean()))
                            brier = brier_score_loss(actual, prob_up)
                            logloss = log_loss(actual, np.clip(prob_up, 1e-6, 1 - 1e-6), labels=[0, 1])
                            # Calibration is measured only on the chronological holdout; bins can be noisy for small samples.
                            frac_positive, mean_predicted = calibration_curve(actual, prob_up, n_bins=8, strategy="quantile")
                            current_prob = float(model.predict_proba(X.iloc[[-1]])[0, list(model.classes_).index(1)])
                            # Transparent directional label for the selected single currency.
                            # This ML estimate is not the validated FX Bias Engine signal.
                            if current_prob >= 0.55:
                                ml_bias = "BULLISH"
                                ml_explanation = (
                                    f"Das Modell schätzt die Wahrscheinlichkeit einer positiven "
                                    f"{horizon}-Tage-Rendite auf {current_prob:.1%}. Das liegt mindestens "
                                    "5 Prozentpunkte über 50 % und spricht im Modell für Aufwärtsdruck."
                                )
                            elif current_prob <= 0.45:
                                ml_bias = "BEARISH"
                                ml_explanation = (
                                    f"Das Modell schätzt die Wahrscheinlichkeit einer positiven "
                                    f"{horizon}-Tage-Rendite auf {current_prob:.1%}. Das liegt mindestens "
                                    "5 Prozentpunkte unter 50 % und spricht im Modell für Abwärtsdruck."
                                )
                            else:
                                ml_bias = "NEUTRAL"
                                ml_explanation = (
                                    f"Mit {current_prob:.1%} liegt die Modellwahrscheinlichkeit nahe an 50 %. "
                                    "Die Richtung ist damit nicht deutlich genug, um bullish oder bearish zu nennen."
                                )
                            st.markdown("#### Aktuelle ML-Einschätzung")
                            b1, b2, b3 = st.columns(3)
                            b1.metric("Richtung", ml_bias)
                            b2.metric("P(Aufwärts)", f"{current_prob:.1%}")
                            b3.metric("Prognosehorizont", f"{horizon} Handelstage")
                            if ml_bias == "BULLISH":
                                st.success(ml_explanation)
                            elif ml_bias == "BEARISH":
                                st.error(ml_explanation)
                            else:
                                st.info(ml_explanation)
                            st.caption(
                                "Die ML-Richtung beschreibt die einzelne ausgewählte Währung gegenüber ihrer "
                                "Referenz. Sie ist kein freigegebenes LONG-/SHORT-Signal des FX Bias Engine."
                            )

                            k1,k2,k3,k4 = st.columns(4)
                            k1.metric("Modell: P(Aufwärts)", f"{current_prob:.1%}")
                            k2.metric("Holdout Accuracy", f"{acc:.1%}")
                            k3.metric("Balanced Accuracy", f"{bacc:.1%}")
                            k4.metric("Mehrheits-Baseline", f"{baseline:.1%}")
                            c1, c2 = st.columns(2)
                            c1.metric("Brier Score ↓", f"{brier:.3f}", help="Niedriger ist besser; 0 wäre perfekt. Bewertet die Wahrscheinlichkeiten, nicht nur die Richtung.")
                            c2.metric("Log Loss ↓", f"{logloss:.3f}", help="Niedriger ist besser; falsche Prognosen mit hoher Sicherheit werden stärker bestraft.")
                            cal_fig = go.Figure()
                            cal_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color="gray"), name="Perfekte Kalibrierung"))
                            cal_fig.add_trace(go.Scatter(x=mean_predicted, y=frac_positive, mode="lines+markers", name="Holdout-Kalibrierung"))
                            cal_fig.update_layout(title="Edge & Calibration — Zuverlässigkeit der Wahrscheinlichkeiten", xaxis_title="Mittlere prognostizierte P(Aufwärts)", yaxis_title="Tatsächlicher Anteil Aufwärts", xaxis=dict(range=[0,1], tickformat=".0%"), yaxis=dict(range=[0,1], tickformat=".0%"), height=360)
                            st.plotly_chart(cal_fig, use_container_width=True)
                            st.caption("Interpretation: Punkte nahe der gestrichelten Diagonale sind besser kalibriert. Die Grafik nutzt ausschließlich den chronologischen Holdout; bei wenigen Fällen je Bin ist sie instabil.")
                            st.caption(f"Testfenster: {X_test.index.min().date()} bis {X_test.index.max().date()} · {len(X_test)} Testfälle · Ziel: Rendite nach {horizon} Handelstagen > 0.")
                            if bacc <= 0.52 or bacc <= (baseline - 0.03):
                                st.warning("Der Test zeigt keinen überzeugenden Richtungs-Vorteil gegenüber einer einfachen Baseline. Die aktuelle Wahrscheinlichkeit nicht als eigenständiges Handelssignal verwenden.")
                            else:
                                st.info("Der Test ist historisch besser als die genutzte Baseline, garantiert aber keine zukünftige Prognosegüte.")
                            importance = pd.DataFrame({"Feature": X.columns, "Wichtigkeit": model.feature_importances_}).sort_values("Wichtigkeit", ascending=False).head(10)
                            st.markdown("#### ML-Faktoren-Scanner — jeder Punkt ein Modellfaktor")
                            st.caption("Jeder Punkt steht für einen tatsächlich verwendeten Kurs-/Trend-/Volatilitäts- oder Saisonfaktor. Die Farbe zeigt, ob das Ersetzen dieses Faktors durch seinen historischen Trainingsmedian die aktuelle Modellwahrscheinlichkeit senkt oder erhöht. Das ist eine Sensitivitätsanalyse, kein kausaler Effekt. Makro, Zinsen, COT und News sind in diesem Modell noch nicht enthalten.")
                            # One-at-a-time sensitivity: compare current probability with the
                            # probability when one feature is set to its training median.
                            current_row = X.iloc[[-1]].copy()
                            current_p = float(model.predict_proba(current_row)[0, list(model.classes_).index(1)])
                            factor_rows = []
                            train_medians = X_train.median(numeric_only=True)
                            for feature_name in X.columns:
                                altered = current_row.copy()
                                altered.loc[:, feature_name] = train_medians.get(feature_name, current_row.iloc[0][feature_name])
                                altered_p = float(model.predict_proba(altered)[0, list(model.classes_).index(1)])
                                delta_pp = (current_p - altered_p) * 100
                                factor_rows.append({
                                    "Faktor": feature_name,
                                    "Wichtigkeit": float(model.feature_importances_[list(X.columns).index(feature_name)]),
                                    "Sensitivität (Prozentpunkte)": delta_pp,
                                    "Einordnung": "BULLISH" if delta_pp >= 1.0 else ("BEARISH" if delta_pp <= -1.0 else "NEUTRAL"),
                                    "Aktueller Wert": float(current_row.iloc[0][feature_name]),
                                })
                            factor_df = pd.DataFrame(factor_rows)
                            factor_df["Einflussgröße"] = factor_df["Sensitivität (Prozentpunkte)"].abs()
                            factor_df = factor_df.sort_values("Wichtigkeit", ascending=False)
                            dot_fig = go.Figure()
                            for _, fr in factor_df.iterrows():
                                color = "#16a34a" if fr["Einordnung"] == "BULLISH" else ("#dc2626" if fr["Einordnung"] == "BEARISH" else "#94a3b8")
                                dot_fig.add_trace(go.Scatter(
                                    x=[fr["Sensitivität (Prozentpunkte)" ]], y=[fr["Faktor"]],
                                    mode="markers", name=fr["Einordnung"],
                                    marker=dict(size=10 + 24 * min(float(fr["Wichtigkeit"]), 1.0), color=color),
                                    customdata=[[fr["Wichtigkeit"], fr["Aktueller Wert"], fr["Einordnung"]]],
                                    hovertemplate="%{y}<br>Sensitivität: %{x:.2f} pp<br>Wichtigkeit: %{customdata[0]:.3f}<br>Aktueller Wert: %{customdata[1]:.4f}<br>%{customdata[2]}<extra></extra>"
                                ))
                            dot_fig.add_vline(x=0, line_dash="dash", line_color="gray")
                            dot_fig.update_layout(title="Faktor-Punkte: Einflussrichtung auf P(Aufwärts)", xaxis_title="Aktuelle P(Aufwärts) minus P(Aufwärts) nach Median-Ersatz (Prozentpunkte)", yaxis_title="Modellfaktor", height=max(400, 34 * len(factor_df)), showlegend=False)
                            st.plotly_chart(dot_fig, use_container_width=True)
                            st.dataframe(factor_df[["Faktor", "Einordnung", "Sensitivität (Prozentpunkte)", "Wichtigkeit", "Aktueller Wert"]], use_container_width=True, hide_index=True)
                            st.markdown("#### Welche Faktoren beeinflussen das Modell?")
                            st.dataframe(importance, use_container_width=True, hide_index=True)
                            st.markdown("#### Letzte historische Testprognosen")
                            hist = pd.DataFrame({"P(Aufwärts)": prob_up, "Tatsächlich aufwärts": actual,
                                                 "Modellrichtung": np.where(pred == 1, "AUFWÄRTS", "ABWÄRTS"),
                                                 "Zielrendite": dataset.loc[X_test.index, "future_return"]})
                            hist["P(Aufwärts)"] = hist["P(Aufwärts)"] * 100
                            st.dataframe(hist.tail(25), use_container_width=True)
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(x=hist.index, y=hist["P(Aufwärts)"], mode="markers", name="P(Aufwärts)"))
                            fig.add_hline(y=50, line_dash="dash", line_color="gray")
                            fig.update_layout(title=f"{currency} — historische Out-of-sample Wahrscheinlichkeiten ({horizon}T)", yaxis_title="P(Aufwärts) %", xaxis_title="Testdatum")
                            st.plotly_chart(fig, use_container_width=True)
                            st.caption("Methodik: chronologischer 80/20-Holdout, Random Forest, technische Preis-/Volatilitäts-/Momentum-Features plus Monats-Saisonalität, keine zufällige Durchmischung. Brier Score, Log Loss und Kalibrierungsdiagramm werden auf dem Holdout berechnet. Der neue Faktoren-Scanner zeigt Sensitivität der aktuell verwendeten technischen und Saison-Features. Wichtig: COT, Makro/Yields und News sind noch NICHT als historische Modellfeatures eingebunden; sie dürfen daher nicht als vom Modell berücksichtigte Faktoren interpretiert werden. Transaktionskosten, Slippage und Overlapping-Horizon-Effekte sind nicht modelliert; dies ist kein handelbarer Netto-Backtest.")
                        except ImportError:
                            st.error("scikit-learn fehlt. Ergänze `scikit-learn` in requirements.txt und deploye die App erneut.")
        except Exception as exc:
            st.error(f"ML Lab fehlgeschlagen: {exc}")

elif page == "Index ML Lab":
    st.subheader("Index ML Lab — probabilistischer Bias")
    st.caption("Chronologischer Holdout-Test für Indexmärkte. Modellfaktoren: Trend, Momentum, Volatilität und Kalendersaisonalität. VIX und US-Renditen werden separat als Kontext angezeigt, nicht als Modellfeatures, sofern ihre Historie nicht zeitlich sauber verfügbar ist.")
    index_universe = {
        "Nasdaq-100 Future (NQ)": "NQ=F",
        "S&P 500 Future (ES)": "ES=F",
        "Dow Jones Future (YM)": "YM=F",
        "Russell 2000 Future (RTY)": "RTY=F",
        "DAX 40": "^GDAXI",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225",
    }
    selected_index = st.selectbox("Index", list(index_universe.keys()), key="index_ml_symbol")
    horizon_idx = st.selectbox("Prognosehorizont", [5, 10, 20, 40, 60], index=2,
                               format_func=lambda x: f"{x} Handelstage", key="index_ml_horizon")
    years_idx = st.selectbox("Historie", ["5y", "10y", "max"], index=1, key="index_ml_years")
    st.markdown("#### Index-Makro-Kontext")
    st.caption("Diese Kontextreihen helfen bei der Interpretation, werden aber nicht als bestätigte fundamentale ML-Features ausgegeben.")
    if st.button("Index-Modell trainieren & testen", type="primary", key="run_index_ml"):
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, log_loss
            from sklearn.impute import SimpleImputer
            with st.spinner("Lade Index- und Kontextdaten; trainiere chronologisch und teste außerhalb der Stichprobe…"):
                symbol_idx = index_universe[selected_index]
                raw_idx = load_market_history(symbol_idx, years_idx)
                if raw_idx.empty or len(raw_idx) < 500:
                    st.error("Zu wenig Kursdaten. Für den ML-Test werden mindestens 500 tägliche Beobachtungen benötigt.")
                else:
                    raw_idx["date"] = pd.to_datetime(raw_idx["date"], errors="coerce")
                    raw_idx["close"] = pd.to_numeric(raw_idx["close"], errors="coerce")
                    raw_idx = raw_idx.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates("date")
                    close_idx = raw_idx.set_index("date")["close"].astype(float)
                    feat = pd.DataFrame(index=close_idx.index)
                    daily = close_idx.pct_change()
                    for lag in [1, 2, 5, 10, 20, 60]:
                        feat[f"return_{lag}d"] = close_idx.pct_change(lag)
                    for window in [5, 10, 20, 50, 100, 200]:
                        feat[f"ma_gap_{window}"] = close_idx / close_idx.rolling(window).mean() - 1
                    for window in [5, 10, 20, 60]:
                        feat[f"volatility_{window}d"] = daily.rolling(window).std()
                    feat["momentum_20_60"] = close_idx.pct_change(20) - close_idx.pct_change(60)
                    feat["vol_ratio_5_20"] = daily.rolling(5).std() / daily.rolling(20).std()
                    month_idx = pd.Series(feat.index.month, index=feat.index, dtype=float)
                    feat["month_sin"] = np.sin(2*np.pi*month_idx/12)
                    feat["month_cos"] = np.cos(2*np.pi*month_idx/12)
                    future_return = close_idx.shift(-horizon_idx) / close_idx - 1
                    dataset_idx = feat.copy()
                    dataset_idx["future_return"] = future_return
                    dataset_idx["target"] = (future_return > 0).astype(int)
                    dataset_idx = dataset_idx.replace([np.inf, -np.inf], np.nan).dropna()
                    if len(dataset_idx) < 350:
                        st.error("Nach Feature-Bereinigung bleiben zu wenige Beobachtungen für einen stabilen Test.")
                    else:
                        X_idx = dataset_idx.drop(columns=["future_return", "target"])
                        y_idx = dataset_idx["target"].astype(int)
                        split_idx = int(len(dataset_idx) * 0.8)
                        X_train_idx, X_test_idx = X_idx.iloc[:split_idx], X_idx.iloc[split_idx:]
                        y_train_idx, y_test_idx = y_idx.iloc[:split_idx], y_idx.iloc[split_idx:]
                        # Fit imputer on training data only; never use future holdout statistics.
                        imp_idx = SimpleImputer(strategy="median")
                        X_train_imp = imp_idx.fit_transform(X_train_idx)
                        X_test_imp = imp_idx.transform(X_test_idx)
                        model_idx = RandomForestClassifier(n_estimators=400, max_depth=5,
                            min_samples_leaf=10, class_weight="balanced_subsample",
                            random_state=42, n_jobs=-1)
                        model_idx.fit(X_train_imp, y_train_idx)
                        pred_prob_idx = model_idx.predict_proba(X_test_imp)[:, list(model_idx.classes_).index(1)]
                        pred_idx = (pred_prob_idx >= 0.5).astype(int)
                        acc_idx = accuracy_score(y_test_idx, pred_idx)
                        bacc_idx = balanced_accuracy_score(y_test_idx, pred_idx)
                        baseline_idx = max(float(y_test_idx.mean()), float(1-y_test_idx.mean()))
                        brier_idx = brier_score_loss(y_test_idx, pred_prob_idx)
                        logloss_idx = log_loss(y_test_idx, np.clip(pred_prob_idx, 1e-6, 1-1e-6), labels=[0,1])
                        current_feat_idx = feat.replace([np.inf, -np.inf], np.nan).dropna().iloc[[-1]]
                        current_prob_idx = float(model_idx.predict_proba(imp_idx.transform(current_feat_idx[X_idx.columns]))[0, list(model_idx.classes_).index(1)])
                        if current_prob_idx >= 0.55:
                            bias_idx = "BULLISH"
                        elif current_prob_idx <= 0.45:
                            bias_idx = "BEARISH"
                        else:
                            bias_idx = "NEUTRAL"
                        st.markdown("#### Aktuelle ML-Einschätzung")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Modell-Bias", bias_idx)
                        m2.metric("P(positive Rendite)", f"{current_prob_idx:.1%}")
                        m3.metric("Horizont", f"{horizon_idx} Handelstage")
                        if bias_idx == "BULLISH":
                            st.success("Die geschätzte Aufwärtswahrscheinlichkeit liegt mindestens 5 Prozentpunkte über 50 %. Das ist ein Modell-Bias, keine Trade-Garantie.")
                        elif bias_idx == "BEARISH":
                            st.error("Die geschätzte Aufwärtswahrscheinlichkeit liegt mindestens 5 Prozentpunkte unter 50 %. Das ist ein Modell-Bias, keine Trade-Garantie.")
                        else:
                            st.info("Die Modellwahrscheinlichkeit liegt nahe 50 %; kein klarer Richtungs-Bias.")
                        st.markdown("#### Out-of-sample Qualität")
                        q1, q2, q3, q4, q5 = st.columns(5)
                        q1.metric("Accuracy", f"{acc_idx:.1%}")
                        q2.metric("Balanced accuracy", f"{bacc_idx:.1%}")
                        q3.metric("Mehrheits-Baseline", f"{baseline_idx:.1%}")
                        q4.metric("Brier ↓", f"{brier_idx:.3f}")
                        q5.metric("Log Loss ↓", f"{logloss_idx:.3f}")
                        st.caption(f"Chronologischer 80/20-Holdout: {X_test_idx.index.min().date()} bis {X_test_idx.index.max().date()} · {len(X_test_idx)} Testfälle. Überlappende Prognosehorizonte und Transaktionskosten sind nicht bereinigt.")
                        if bacc_idx <= 0.52 or bacc_idx <= baseline_idx - 0.03:
                            st.warning("Kein überzeugender Richtungs-Vorteil gegenüber der Baseline im Holdout. Modellwahrscheinlichkeit vorsichtig interpretieren.")
                        importance_idx = pd.DataFrame({"Faktor": X_idx.columns, "Wichtigkeit": model_idx.feature_importances_}).sort_values("Wichtigkeit", ascending=False)
                        st.markdown("#### Wichtigste ML-Faktoren")
                        st.dataframe(importance_idx.head(15), use_container_width=True, hide_index=True)
                        fig_idx = go.Figure()
                        fig_idx.add_trace(go.Scatter(x=X_test_idx.index, y=pred_prob_idx*100, mode="lines", name="P(Aufwärts)"))
                        fig_idx.add_hline(y=50, line_dash="dash", line_color="gray")
                        fig_idx.update_layout(title=f"{selected_index} — Holdout-Prognosen", xaxis_title="Datum", yaxis_title="P(Aufwärts) %", yaxis=dict(range=[0,100]), height=350)
                        st.plotly_chart(fig_idx, use_container_width=True)
                        hist_idx = pd.DataFrame({"P(Aufwärts) %": pred_prob_idx*100,
                            "Modellrichtung": np.where(pred_idx == 1, "AUFWÄRTS", "ABWÄRTS"),
                            "Tatsächlich": np.where(y_test_idx.to_numpy() == 1, "AUFWÄRTS", "ABWÄRTS"),
                            "Zielrendite %": dataset_idx.loc[X_test_idx.index, "future_return"].to_numpy()*100}, index=X_test_idx.index)
                        st.dataframe(hist_idx.tail(30), use_container_width=True)
                        # Separate context panel: fresh historical proxies only, not fed to classifier.
                        context_rows_idx = []
                        for context_name, context_symbol in [("VIX", "^VIX"), ("US 10Y yield proxy", "^TNX"), ("USD index proxy", "DX-Y.NYB")]:
                            try:
                                context_df = load_market_history(context_symbol, "1y")
                                if not context_df.empty:
                                    last_ctx = context_df.iloc[-1]
                                    age_ctx = (pd.Timestamp.now().normalize() - pd.Timestamp(last_ctx["date"]).normalize()).days
                                    context_rows_idx.append({"Kontext": context_name, "Symbol": context_symbol,
                                        "Letzter Wert": float(last_ctx["close"]), "Datenstand": str(pd.Timestamp(last_ctx["date"]).date()),
                                        "Alter (Tage)": age_ctx, "Status": "OK" if age_ctx <= 4 else "VERALTET"})
                            except Exception as context_exc:
                                context_rows_idx.append({"Kontext": context_name, "Symbol": context_symbol, "Status": f"FEHLER: {context_exc}"})
                        st.markdown("#### Makro-/Risk-Kontext (separat, kein ML-Feature)")
                        if context_rows_idx:
                            st.dataframe(pd.DataFrame(context_rows_idx), use_container_width=True, hide_index=True)
                        else:
                            st.info("VIX-/Rendite-/USD-Kontextdaten nicht verfügbar.")
                        st.caption("Methodik: Random Forest, chronologischer 80/20-Holdout, technische Preis-/Volatilitäts-/Momentum-Features plus Kalender-Saisonalität. Fundamentaldaten, COT, Marktbreite, Earnings und News sind nicht im Modell enthalten. Daten kommen aus yfinance und können verzögert oder unvollständig sein; kein Netto-Backtest und keine Anlageberatung.")
        except ImportError:
            st.error("scikit-learn fehlt. Ergänze `scikit-learn` in requirements.txt und deploye die App erneut.")
        except Exception as exc:
            st.error(f"Index ML Lab fehlgeschlagen: {exc}")

elif page == "Saisonalität":
    st.subheader("Seasonality Terminal")
    st.caption("Saisonaler Jahresverlauf aus historischen Kursen: jedes Kalenderjahr wird auf 100 am Jahresanfang normiert. Kennzahlen beziehen sich auf das ausgewählte Kalenderfenster und vergleichen dieselben Daten im jeweiligen historischen Jahr.")
    symbols = {name: info["symbol"] for name, info in FX_PAIRS.items()}
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        label = st.selectbox("Instrument / Proxy", list(symbols), key="seasonality_symbol")
    with c2:
        years = st.selectbox("Historie", ["5y", "10y", "max"], index=1, key="seasonality_years")
    with c3:
        horizon = st.selectbox("Haltedauer", [5, 10, 20, 30, 60], index=3, format_func=lambda x: f"{x} Handelstage", key="seasonality_horizon")
    with c4:
        cost_bps = st.number_input("Kosten (bps Round-trip)", min_value=0.0, max_value=100.0, value=2.0, step=0.5, key="seasonality_costs")

    month_names = {i + 1: MONTHS[i] for i in range(12)}
    c5, c6, c7, c8 = st.columns([1, 1, 1, 1])
    with c5:
        start_month = st.selectbox("Saisonfenster Startmonat", list(range(1, 13)), index=4, format_func=lambda x: month_names[x], key="season_start_month")
    with c6:
        start_day = st.number_input("Starttag", min_value=1, max_value=28, value=20, key="season_start_day")
    with c7:
        end_month = st.selectbox("Saisonfenster Endmonat", list(range(1, 13)), index=7, format_func=lambda x: month_names[x], key="season_end_month")
    with c8:
        end_day = st.number_input("Endtag", min_value=1, max_value=31, value=16, key="season_end_day")

    if st.button("Historische Daten laden / aktualisieren", type="primary", key="run_seasonality_plus"):
        with st.spinner("Lade echte historische Kurse und berechne saisonalen Jahresverlauf…"):
            try:
                prices = load_market_history(symbols[label], years)
                if prices is None or prices.empty:
                    st.error("Die Datenquelle hat keine historischen Kurse geliefert.")
                else:
                    d = prices.copy()
                    # Robust gegen unterschiedliche Datenformate: Datum kann als Spalte oder Index kommen.
                    if "date" not in d.columns:
                        if "Date" in d.columns:
                            d = d.rename(columns={"Date": "date"})
                        elif "Datetime" in d.columns:
                            d = d.rename(columns={"Datetime": "date"})
                        elif isinstance(d.index, pd.DatetimeIndex) or d.index.name in ("date", "Date", "Datetime"):
                            d = d.reset_index()
                            if "index" in d.columns and "date" not in d.columns:
                                d = d.rename(columns={"index": "date"})
                            elif "Date" in d.columns:
                                d = d.rename(columns={"Date": "date"})
                    if "close" not in d.columns:
                        for candidate in ("Close", "Adj Close", "adjclose", "price", "Price"):
                            if candidate in d.columns:
                                d = d.rename(columns={candidate: "close"})
                                break
                    if not {"date", "close"}.issubset(d.columns):
                        st.error(f"Historische Daten haben unerwartete Spalten: {list(d.columns)[:12]}")
                    else:
                        d["date"] = pd.to_datetime(d["date"], errors="coerce", utc=True).dt.tz_convert(None)
                        d["close"] = pd.to_numeric(d["close"], errors="coerce")
                        d = d.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates("date")
                        d = d[d["close"] > 0].set_index("date")
                        close = d["close"].astype(float).resample("B").last().dropna()
                        if len(close) < 100:
                            st.error(f"Zu wenige gültige Kursbeobachtungen: {len(close)}.")
                        else:
                            # Build one normalized price path per calendar year, then average by month/day.
                            # This creates a meaningful seasonal path; it does not plot the full-history price series.
                            yearly_paths = []
                            for year, group in close.groupby(close.index.year):
                                group = group.sort_index()
                                if len(group) < 40:
                                    continue
                                normalized = group / group.iloc[0] * 100.0
                                path = pd.DataFrame({"date": group.index, "index100": normalized.values})
                                path["month_day"] = path["date"].dt.strftime("%m-%d")
                                path["year"] = year
                                yearly_paths.append(path)
                            if not yearly_paths:
                                st.error("Es konnten keine vollständigen Jahresverläufe aus den Kursdaten erstellt werden.")
                            else:
                                paths = pd.concat(yearly_paths, ignore_index=True)
                                seasonal = paths.groupby("month_day", sort=True)["index100"].agg(["mean", "count"]).reset_index()
                                seasonal["date"] = pd.to_datetime("2000-" + seasonal["month_day"], errors="coerce")
                                seasonal = seasonal.dropna(subset=["date"]).sort_values("date")
                                seasonal["date_label"] = seasonal["date"].dt.strftime("%b %d")
                                start_key = f"{int(start_month):02d}-{int(start_day):02d}"
                                end_key = f"{int(end_month):02d}-{int(end_day):02d}"
                                if start_key <= end_key:
                                    in_window = (paths["month_day"] >= start_key) & (paths["month_day"] <= end_key)
                                else:
                                    in_window = (paths["month_day"] >= start_key) | (paths["month_day"] <= end_key)
                                selected_paths = paths[in_window].copy()
                                # For each historical year, use the first and last available close in the chosen calendar window.
                                outcomes = []
                                for yr, group in selected_paths.groupby("year"):
                                    group = group.sort_values("date")
                                    if len(group) >= 2:
                                        gross = float(group["index100"].iloc[-1] / group["index100"].iloc[0] - 1.0)
                                        net = gross - float(cost_bps) / 10000.0
                                        outcomes.append({"Jahr": int(yr), "Startdatum": group["date"].iloc[0],
                                                         "Enddatum": group["date"].iloc[-1], "Netto-Rendite": net,
                                                         "Kursindex Start": float(group["index100"].iloc[0]),
                                                         "Kursindex Ende": float(group["index100"].iloc[-1])})
                                result = pd.DataFrame(outcomes)
                                if result.empty:
                                    st.warning("Für dieses Saisonfenster gibt es nicht genügend historische Daten.")
                                else:
                                    result["Gewinn"] = result["Netto-Rendite"] > 0
                                    win_rate = float(result["Gewinn"].mean())
                                    avg_ret = float(result["Netto-Rendite"].mean())
                                    median_ret = float(result["Netto-Rendite"].median())
                                    avg_abs_move = float(result["Netto-Rendite"].abs().mean())
                                    avg_win = result.loc[result["Netto-Rendite"] > 0, "Netto-Rendite"].mean()
                                    avg_loss = result.loc[result["Netto-Rendite"] <= 0, "Netto-Rendite"].mean()
                                    gp = result.loc[result["Netto-Rendite"] > 0, "Netto-Rendite"].sum()
                                    gl = -result.loc[result["Netto-Rendite"] <= 0, "Netto-Rendite"].sum()
                                    pf = gp / gl if gl > 0 else np.nan
                                    n = len(result)
                                    annualized = ((1 + avg_ret) ** (252 / max(1, int(horizon))) - 1) if avg_ret > -1 else np.nan

                                    st.caption(f"Quelle: load_market_history · Symbol {symbols[label]} · {d.index.min().date()} bis {d.index.max().date()} · {len(d):,} valide Kurse · {n} auswertbare Kalenderjahre.")
                                    # Smooth daily noise so the chart communicates the seasonal pattern rather than each year's day-to-day FX noise.
                                    seasonal["mean_smooth"] = seasonal["mean"].rolling(window=9, center=True, min_periods=1).mean()
                                    fig = go.Figure()
                                    date_keys = seasonal["date"].dt.strftime("%m-%d")
                                    selected_season = (date_keys >= start_key) & (date_keys <= end_key) if start_key <= end_key else ((date_keys >= start_key) | (date_keys <= end_key))
                                    # Thin raw line remains visible for context; bold rolling average is the primary seasonal curve.
                                    fig.add_trace(go.Scatter(x=seasonal["date"], y=seasonal["mean"], mode="lines", name="Tagesmittel (ungeglättet)", line=dict(color="rgba(75,181,204,0.28)", width=1), customdata=seasonal[["count"]], hovertemplate="%{x|%d. %b}<br>Index: %{y:.2f}<br>Jahresbeobachtungen: %{customdata[0]}<extra></extra>"))
                                    fig.add_trace(go.Scatter(x=seasonal["date"], y=seasonal["mean_smooth"], mode="lines", name="Saisonaler Durchschnitt (9-Tage-Glättung)", line=dict(color="#42c5df", width=3.2, shape="spline", smoothing=0.55), hovertemplate="%{x|%d. %b}<br>Geglätteter Index: %{y:.2f}<extra></extra>"))
                                    if selected_season.any():
                                        x0 = pd.to_datetime("2000-" + start_key, errors="coerce")
                                        x1 = pd.to_datetime(("2000-" if start_key <= end_key else "2001-") + end_key, errors="coerce")
                                        if pd.notna(x0) and pd.notna(x1):
                                            fig.add_vrect(x0=x0, x1=x1, fillcolor="#42c5df", opacity=0.13, line_width=0, layer="below")
                                            fig.add_vline(x=x0, line_width=1.5, line_color="#b8f3ff", line_dash="dot")
                                            fig.add_vline(x=x1, line_width=1.5, line_color="#b8f3ff", line_dash="dot")
                                    fig.update_layout(title=dict(text="ANNUAL SEASONALITY · Durchschnittlicher Kursverlauf", x=0.015, xanchor="left", font=dict(size=16)),
                                        xaxis_title="Kalenderjahr", yaxis_title="Index (Jahresstart = 100)", hovermode="x unified", height=470,
                                        margin=dict(l=35, r=20, t=58, b=35), plot_bgcolor="#0b1118", paper_bgcolor="#0b1118",
                                        font=dict(color="#cbd5e1", size=11), legend=dict(orientation="h", y=1.02, x=0.01),
                                        hoverlabel=dict(bgcolor="#111b26", bordercolor="#42c5df", font_color="#f1f5f9"))
                                    fig.update_xaxes(tickformat="%b", dtick="M1", showgrid=True, gridcolor="rgba(148,163,184,0.13)", zeroline=False, tickfont=dict(color="#9ca3af"))
                                    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.13)", zeroline=False, tickfont=dict(color="#9ca3af"), fixedrange=False)
                                    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True, "modeBarButtonsToAdd": ["select2d", "lasso2d"]})
                                    st.caption("Die feine Linie zeigt den täglichen Mittelwert; die kräftige Linie glättet kurzfristiges Rauschen über 9 Kalendertage. Das hervorgehobene Fenster entspricht den Saison-Start-/Enddaten.")
                                    st.markdown("#### Ergebnis für den ausgewählten Saisonbereich")
                                    m1, m2, m3, m4 = st.columns(4)
                                    m1.metric("Annualisierte Rendite*", "—" if pd.isna(annualized) else f"{annualized:.2%}")
                                    m2.metric("Gewinnrate", f"{win_rate:.1%}")
                                    m3.metric("Ø Rendite je Fenster", f"{avg_ret:.2%}")
                                    m4.metric("Beobachtungen", f"{n}")
                                    m1, m2, m3, m4 = st.columns(4)
                                    m1.metric("Medianrendite", f"{median_ret:.2%}")
                                    m2.metric("Ø absolute Bewegung", f"{avg_abs_move:.2%}")
                                    m3.metric("Ø Gewinn / Verlust", f"{'—' if pd.isna(avg_win) else f'{avg_win:.2%}'} / {'—' if pd.isna(avg_loss) else f'{avg_loss:.2%}'}")
                                    m4.metric("Profit Factor", "—" if pd.isna(pf) else f"{pf:.2f}")
                                    st.caption(f"Fenster: {month_names[int(start_month)]} {int(start_day)} – {month_names[int(end_month)]} {int(end_day)} · Kosten: {cost_bps:.1f} bps Round-trip. *Annualisierte Rendite ist eine rechnerische Extrapolation, keine Prognose.")
                                    left, right = st.columns([1.2, 1])
                                    with left:
                                        yr_fig = px.bar(result, x="Jahr", y="Netto-Rendite", color="Netto-Rendite", color_continuous_scale=["#e05260", "#263f52", "#4bb5cc"], title="Saisonfenster — Rendite je Jahr")
                                        yr_fig.update_layout(height=330, coloraxis_showscale=False, margin=dict(l=10, r=10, t=45, b=10), yaxis_tickformat=".1%")
                                        st.plotly_chart(yr_fig, use_container_width=True)
                                    with right:
                                        hist_fig = px.histogram(result, x="Netto-Rendite", nbins=20, title="Pattern Returns", color_discrete_sequence=["#4bb5cc"])
                                        hist_fig.add_vline(x=0, line_dash="dash", line_color="#e05260")
                                        hist_fig.update_layout(height=330, margin=dict(l=10, r=10, t=45, b=10), xaxis_tickformat=".1%")
                                        st.plotly_chart(hist_fig, use_container_width=True)
                                    st.markdown("#### Beste saisonale Zeitfenster — historische Rangliste")
                                    st.caption("Scan über Kalender-Starttage und mehrere Haltedauern. Die Rangliste basiert auf historischen Forward-Renditen nach Kosten; kleine Stichproben und überlappende Zeitfenster können die Ergebnisse verzerren.")
                                    scan_horizons = [5, 10, 20, 30, 60]
                                    scan_rows = []
                                    scan_close = close.dropna().sort_index()
                                    scan_dates = pd.DataFrame({"date": scan_close.index, "close": scan_close.values})
                                    scan_dates["month_day"] = scan_dates["date"].dt.strftime("%m-%d")
                                    for scan_h in scan_horizons:
                                        forward = scan_dates["close"].shift(-scan_h) / scan_dates["close"] - 1.0 - float(cost_bps) / 10000.0
                                        scan_frame = scan_dates[["date", "month_day"]].copy()
                                        scan_frame["forward_net"] = forward
                                        scan_frame = scan_frame.dropna(subset=["forward_net"])
                                        grouped = scan_frame.groupby("month_day")["forward_net"].agg(["mean", "median", "count", lambda x: float((x > 0).mean())])
                                        grouped.columns = ["avg_return", "median_return", "n", "win_rate"]
                                        # Avoid ranking tiny samples; require at least 5 yearly observations where available.
                                        grouped = grouped[grouped["n"] >= min(5, max(2, int(scan_frame["date"].dt.year.nunique() * 0.5)))]
                                        if grouped.empty:
                                            grouped = scan_frame.groupby("month_day")["forward_net"].agg(avg_return="mean", median_return="median", n="count", win_rate=lambda x: float((x > 0).mean()))
                                        for month_day, row in grouped.sort_values("avg_return", ascending=False).head(10).iterrows():
                                            scan_rows.append({"Haltedauer (Handelstage)": scan_h, "Startfenster": pd.to_datetime("2000-" + month_day).strftime("%d. %b"), "Ø Rendite": row["avg_return"], "Medianrendite": row["median_return"], "Gewinnrate": row["win_rate"], "Beobachtungen": int(row["n"])})
                                    scan_result = pd.DataFrame(scan_rows)
                                    if not scan_result.empty:
                                        scan_display = scan_result.copy()
                                        scan_display["Ø Rendite"] = scan_display["Ø Rendite"].map(lambda x: f"{x:.2%}")
                                        scan_display["Medianrendite"] = scan_display["Medianrendite"].map(lambda x: f"{x:.2%}")
                                        scan_display["Gewinnrate"] = scan_display["Gewinnrate"].map(lambda x: f"{x:.1%}")
                                        st.dataframe(scan_display, use_container_width=True, hide_index=True)
                                        st.download_button("Saisonaler Scanner als CSV herunterladen", data=scan_result.to_csv(index=False).encode("utf-8"), file_name="seasonality_best_windows.csv", mime="text/csv", key="download_seasonality_scan")
                                    st.markdown("#### Renditevergleich nach Haltedauer")
                                    comparison_rows = []
                                    for compare_h in scan_horizons:
                                        compare_forward = scan_close.shift(-compare_h) / scan_close - 1.0 - float(cost_bps) / 10000.0
                                        compare_frame = pd.DataFrame({"date": scan_close.index, "forward_net": compare_forward.values}).dropna()
                                        compare_frame["month_day"] = compare_frame["date"].dt.strftime("%m-%d")
                                        if start_key <= end_key:
                                            chosen = (compare_frame["month_day"] >= start_key) & (compare_frame["month_day"] <= end_key)
                                        else:
                                            chosen = (compare_frame["month_day"] >= start_key) | (compare_frame["month_day"] <= end_key)
                                        vals = compare_frame.loc[chosen, "forward_net"]
                                        if len(vals):
                                            comparison_rows.append({"Haltedauer (Handelstage)": compare_h, "Ø Rendite": float(vals.mean()), "Medianrendite": float(vals.median()), "Gewinnrate": float((vals > 0).mean()), "Beobachtungen": int(len(vals))})
                                    if comparison_rows:
                                        comparison = pd.DataFrame(comparison_rows)
                                        comp_fig = go.Figure()
                                        comp_fig.add_trace(go.Bar(x=comparison["Haltedauer (Handelstage)"].astype(str), y=comparison["Ø Rendite"], name="Ø Rendite", marker_color="#4bb5cc"))
                                        comp_fig.add_trace(go.Scatter(x=comparison["Haltedauer (Handelstage)"].astype(str), y=comparison["Gewinnrate"], name="Gewinnrate", yaxis="y2", mode="lines+markers", line=dict(color="#f0b45a", width=2.5)))
                                        comp_fig.update_layout(title="Ausgewähltes Saisonfenster — Rendite und Gewinnrate nach Haltedauer", xaxis_title="Haltedauer (Handelstage)", yaxis=dict(title="Ø Netto-Rendite", tickformat=".1%"), yaxis2=dict(title="Gewinnrate", overlaying="y", side="right", tickformat=".0%", range=[0, 1]), height=350, margin=dict(l=10, r=10, t=45, b=10), legend=dict(orientation="h", y=1.12))
                                        st.plotly_chart(comp_fig, use_container_width=True)
                                        comparison_display = comparison.copy()
                                        comparison_display["Ø Rendite"] = comparison_display["Ø Rendite"].map(lambda x: f"{x:.2%}")
                                        comparison_display["Medianrendite"] = comparison_display["Medianrendite"].map(lambda x: f"{x:.2%}")
                                        comparison_display["Gewinnrate"] = comparison_display["Gewinnrate"].map(lambda x: f"{x:.1%}")
                                        st.dataframe(comparison_display, use_container_width=True, hide_index=True)
                                    st.markdown("#### Historische Einzelergebnisse")
                                    st.dataframe(result.sort_values("Jahr", ascending=False).style.format({"Netto-Rendite":"{:.2%}", "Kursindex Start":"{:.2f}", "Kursindex Ende":"{:.2f}"}), use_container_width=True, hide_index=True)
                                    st.download_button("Saison-Ergebnisse als CSV herunterladen", data=result.to_csv(index=False).encode("utf-8"), file_name="seasonality_results.csv", mime="text/csv")
                                    st.caption("Methodik: jedes Jahr wird auf 100 am ersten verfügbaren Handelstag normiert. Die Saisonalitätslinie ist der Durchschnitt dieser normierten Jahresverläufe. Rendite und Gewinnrate werden über die einzelnen historischen Jahresfenster berechnet, nicht über alle überlappenden Tagesstarts.")
            except Exception as e:
                st.error(f"Seasonality-Berechnung fehlgeschlagen: {e}")
    else:
        st.info("Wähle Instrument, Historie, Saisonfenster und Kostenannahme und lade dann die echten historischen Kursdaten. Es werden nur echte historische Kurse verwendet; fehlende Werte werden nicht durch Demo-Daten ersetzt.")

elif page == "COT / Positioning":
    st.subheader("COT / Positioning")
    st.caption("CFTC-Daten sind Futures-Positionierung, nicht der gesamte globale Spot-FX-Markt. Contract code mapping muss je Datensatz geprüft werden.")
    cot_contract = st.selectbox("CFTC-Futures-Kontrakt", list(CFTC_CONTRACT_CODES), format_func=lambda c: {
        "6E": "Euro FX (6E)", "6B": "British Pound (6B)", "6J": "Japanese Yen (6J)",
        "6A": "Australian Dollar (6A)", "6C": "Canadian Dollar (6C)",
        "6S": "Swiss Franc (6S)", "6N": "New Zealand Dollar (6N)"
    }.get(c, c))
    if st.button("CFTC-Historie laden", type="primary"):
        try:
            cot = load_cot_history(cot_contract, limit=52)
            st.success(f"{len(cot)} wöchentliche Datensätze · letzter Bericht {cot.iloc[-1]['date'].date()} · {cot.attrs.get('age_days', 0):.1f} Tage alt.")
            st.caption("Quelle: CFTC Public Reporting API · Legacy Futures Only. Net = Long minus Short. Non-reportable ist keine direkt ausgewiesene Retail-Kategorie.")
            c1, c2, c3 = st.columns(3)
            c1.metric("Commercial net", f"{cot.iloc[-1]['commercial_net']:,.0f}")
            c2.metric("Non-commercial net", f"{cot.iloc[-1]['noncommercial_net']:,.0f}")
            c3.metric("Non-reportable net", "—" if pd.isna(cot.iloc[-1]['nonreportable_net']) else f"{cot.iloc[-1]['nonreportable_net']:,.0f}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=cot["date"], y=cot["commercial_net"], mode="lines", name="Commercial net"))
            fig.add_trace(go.Scatter(x=cot["date"], y=cot["noncommercial_net"], mode="lines", name="Non-commercial net"))
            fig.add_trace(go.Scatter(x=cot["date"], y=cot["nonreportable_net"], mode="lines", name="Non-reportable net"))
            fig.update_layout(title=f"{cot.attrs.get('market_name', cot_contract)} — Netto-Positionen", yaxis_title="Kontrakte", legend_title="Gruppe")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(cot[["date", "commercial_net", "noncommercial_net", "nonreportable_net", "open_interest"]].tail(20).sort_values("date", ascending=False), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"CFTC-Daten nicht verfügbar/validiert: {e}")
    st.markdown("#### Kontrakte für FX-Recherche")
    st.dataframe(pd.DataFrame([
        ["EUR", "Euro FX", "6E"], ["GBP", "British Pound", "6B"], ["JPY", "Japanese Yen", "6J"],
        ["CAD", "Canadian Dollar", "6C"], ["AUD", "Australian Dollar", "6A"],
        ["CHF", "Swiss Franc", "6S"], ["NZD", "New Zealand Dollar", "6N"], ["USD", "Kein einzelner direkter G10-COT-Proxy", "—"]
    ], columns=["Währung", "CFTC-Futures-Kontrakt", "Ticker/Code"]), use_container_width=True, hide_index=True)
    st.warning("Der CFTC-Endpunkt und seine Felder können sich ändern. Vor produktiver Nutzung Reporttyp (Legacy/Disaggregated/TFF), Datenfelder, Berichtswoche und Kontrakt-ID validieren.")

elif page == "NQ & ES":
    st.subheader("NQ & ES Macro Lens")
    symbols = {"NQ=F": "Nasdaq-100 Futures (Datenanbieter-Symbol)", "ES=F": "S&P 500 Futures (Datenanbieter-Symbol)"}
    symbol = st.selectbox("Historisches Symbol", list(symbols), format_func=lambda x: symbols[x])
    period = st.selectbox("Zeitraum", ["3mo", "1y", "5y"], index=1)
    if st.button("Historie laden"):
        try:
            df = load_market_history(symbol, period)
            if df.empty:
                st.error("Keine historischen Preise erhalten.")
            else:
                st.caption(f"Historischer Preis-Proxy · Abruf {utc_now()} · keine Zusicherung von Echtzeit oder Börsenlizenz.")
                st.line_chart(df.set_index("date")["close"])
                df["return_pct"] = df["close"].pct_change()*100
                st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Marktdaten konnten nicht geladen werden: {e}")
    st.markdown("#### Makro-Checkliste")
    st.write("- US-Realrenditen / Treasury yields")
    st.write("- Fed-Erwartungen und Inflationsüberraschungen")
    st.write("- Marktbreite, Volatilität und Kreditspreads")
    st.write("- Earnings breadth / Revisionen")
    st.info("NQ-/ES-Futures-Symbole über kostenlose Wrapper können verzögert, unvollständig oder anders gerollt sein. Für Trading-Anwendungen Broker- oder lizenzierte Börsendaten nutzen.")

elif page == "Quant & Regression":
    st.subheader("Quant & Regression")
    st.caption("OLS auf historischen Kursrenditen aus der vorhandenen Yahoo Finance/yfinance-Datenquelle. Keine synthetischen Demo-Werte.")
    fx_pairs = {
        "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X", "USD/CAD": "CAD=X", "USD/CHF": "CHF=X",
        "NZD/USD": "NZDUSD=X", "EUR/GBP": "EURGBP=X", "EUR/JPY": "EURJPY=X",
    }
    benchmarks = {
        "US-Dollar-Index (DXY)": "DX-Y.NYB", "S&P 500": "^GSPC",
        "Nasdaq 100": "^NDX", "Gold": "GC=F", "US 10Y Treasury Yield": "^TNX",
        "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X", "USD/CAD": "CAD=X", "USD/CHF": "CHF=X",
        "NZD/USD": "NZDUSD=X",
    }
    with st.form("quant_regression_form"):
        c1, c2 = st.columns(2)
        pair_label = c1.selectbox("FX-Paar (abhängige Variable)", list(fx_pairs), index=0)
        bench_label = c2.selectbox("Benchmark (erklärende Variable)", list(benchmarks), index=0)
        c3, c4 = st.columns(2)
        period_label = c3.selectbox("Historischer Zeitraum", ["1 Jahr", "2 Jahre", "5 Jahre", "10 Jahre"], index=1)
        freq_label = c4.selectbox("Renditefrequenz", ["Täglich", "Wöchentlich"], index=0)
        submitted = st.form_submit_button("Historische Regression berechnen", type="primary")
    if submitted:
        pair_symbol, bench_symbol = fx_pairs[pair_label], benchmarks[bench_label]
        period_map = {"1 Jahr": "1y", "2 Jahre": "2y", "5 Jahre": "5y", "10 Jahre": "10y"}
        period = period_map[period_label]
        try:
            if pair_symbol == bench_symbol:
                raise ValueError("FX-Paar und Benchmark müssen unterschiedlich sein.")
            pair_prices = load_market_history(pair_symbol, period)
            bench_prices = load_market_history(bench_symbol, period)
            if pair_prices.empty:
                raise ValueError(f"Keine historischen Daten für {pair_label} ({pair_symbol}).")
            if bench_prices.empty:
                raise ValueError(f"Keine historischen Daten für {bench_label} ({bench_symbol}).")
            pair_prices["date"] = pd.to_datetime(pair_prices["date"]).dt.tz_localize(None)
            bench_prices["date"] = pd.to_datetime(bench_prices["date"]).dt.tz_localize(None)
            if freq_label == "Wöchentlich":
                pair_prices = pair_prices.set_index("date")["close"].resample("W-FRI").last().dropna().rename("pair_close").reset_index()
                bench_prices = bench_prices.set_index("date")["close"].resample("W-FRI").last().dropna().rename("bench_close").reset_index()
            pair_prices["pair_return_pct"] = pair_prices["close"].pct_change() * 100
            bench_prices["bench_return_pct"] = bench_prices["close"].pct_change() * 100
            merged = pd.merge(
                pair_prices[["date", "pair_return_pct"]],
                bench_prices[["date", "bench_return_pct"]], on="date", how="inner"
            ).replace([np.inf, -np.inf], np.nan).dropna().sort_values("date")
            if len(merged) < 10:
                raise ValueError(f"Nur {len(merged)} gemeinsame Renditebeobachtungen; mindestens 10 werden benötigt.")
            x = merged["bench_return_pct"].to_numpy(dtype=float)
            y = merged["pair_return_pct"].to_numpy(dtype=float)
            if np.std(x) == 0 or np.std(y) == 0:
                raise ValueError("Regression nicht möglich: mindestens eine Renditereihe hat keine Varianz.")
            beta, alpha = np.polyfit(x, y, 1)
            predicted = alpha + beta * x
            ss_res = float(np.sum((y - predicted) ** 2))
            ss_tot = float(np.sum((y - np.mean(y)) ** 2))
            r2 = 1 - ss_res / ss_tot if ss_tot else np.nan
            corr = float(np.corrcoef(x, y)[0, 1])
            merged["OLS_fit_pct"] = predicted
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Beta", f"{beta:.4f}")
            c2.metric("R²", f"{r2:.4f}")
            c3.metric("Korrelation", f"{corr:.4f}")
            c4.metric("Beobachtungen", f"{len(merged):,}")
            st.caption(f"{pair_label} gegen {bench_label} · {period_label} · {freq_label.lower()} · Quelle: Yahoo Finance via yfinance · Abruf {utc_now()}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=merged["bench_return_pct"], y=merged["pair_return_pct"], mode="markers", name="Historische Renditen", marker={"opacity": 0.6}))
            line_df = merged.sort_values("bench_return_pct")
            fig.add_trace(go.Scatter(x=line_df["bench_return_pct"], y=alpha + beta * line_df["bench_return_pct"], mode="lines", name="OLS-Regressionslinie"))
            fig.update_layout(xaxis_title=f"{bench_label} Rendite (%)", yaxis_title=f"{pair_label} Rendite (%)", legend_title="Serie", hovermode="closest")
            st.plotly_chart(fig, use_container_width=True)
            display = merged.rename(columns={"date": "Datum", "pair_return_pct": f"{pair_label} Rendite (%)", "bench_return_pct": f"{bench_label} Rendite (%)", "OLS_fit_pct": "OLS-Schätzwert (%)"})
            st.dataframe(display.sort_values("Datum", ascending=False), use_container_width=True, hide_index=True)
            st.download_button("CSV exportieren", data=display.to_csv(index=False).encode("utf-8-sig"), file_name="quant_regression_historical_returns.csv", mime="text/csv")
            st.info("Interpretation: Beta beschreibt die lineare Sensitivität der FX-Paar-Rendite gegenüber der Benchmark-Rendite. R² ist der erklärte Anteil der Stichprobenvarianz; es beweist keine Kausalität und garantiert keine Prognosegüte.")
        except Exception as e:
            st.error(f"Historische Regression fehlgeschlagen: {e}")
            st.caption("Es werden keine synthetischen Werte als Ersatz angezeigt. Prüfe die Datenverbindung, Symbolverfügbarkeit und installierte yfinance-Version.")
    st.markdown("#### Risk regime inputs")
    st.write("Noch nicht bewertet: Aktienbreite, Realrenditen, Kreditspreads, Dollartrend und Volatilität. Keine Risk-on/off-Klassifikation ohne verifizierte Inputs.")


elif page == "Index Macro & Seasonality":
    st.subheader("Cash Indices — Macro Regime & Seasonality")
    st.caption("Analyse für die acht Alpha Capital Group Cash-Index-Symbole. Historische Preise werden über verfügbare Yahoo Finance-Proxies geladen; diese sind nicht zwingend identisch mit dem Broker-CFD und nicht als Echtzeit-/Ausführungskurse zu verstehen.")
    index_specs = {
        "EUSTX50": {"name": "EURO STOXX 50", "proxy": "^STOXX50E", "region": "Eurozone", "drivers": "EZB-Leitzinsen und Kommunikation; Eurozone HICP/Inflation; PMI/Industrie und Wachstum; EUR-Wechselkurs; Banken- und Unternehmensgewinne.", "rates": "EZB", "fx": "EUR"},
        "GER30": {"name": "Germany 40 / DAX", "proxy": "^GDAXI", "region": "Deutschland", "drivers": "EZB-Zinspfad; deutscher Ifo/PMI und Industrieaufträge; Exportnachfrage, Energiepreise und EUR; globale Industriekonjunktur und DAX-Gewinne.", "rates": "EZB", "fx": "EUR"},
        "HK50": {"name": "Hang Seng Index", "proxy": "^HSI", "region": "Hongkong / China", "drivers": "China-PMI und Kreditimpulse; PBoC-Liquidität; Immobiliensektor und regulatorische Maßnahmen; CNH/CNY; US-China-Handels- und Technologierisiken.", "rates": "PBoC / Fed / HKMA", "fx": "HKD/CNH"},
        "JPN225": {"name": "Nikkei 225", "proxy": "^N225", "region": "Japan", "drivers": "BoJ-Politik und JGB-Renditen; USD/JPY und Yen-Stärke; Löhne/Inflation; Exportdaten; globale Chip- und Industrienachfrage.", "rates": "BoJ", "fx": "JPY"},
        "NAS100": {"name": "Nasdaq-100", "proxy": "^NDX", "region": "USA — Growth / Tech", "drivers": "US Treasury-Renditen, besonders 2Y/10Y; Fed und Inflation; Mega-Cap-Gewinne und Guidance; Halbleiter-/AI-Investitionen; Bewertungs- und Liquiditätsbedingungen.", "rates": "Fed", "fx": "USD"},
        "UK100": {"name": "FTSE 100", "proxy": "^FTSE", "region": "Vereinigtes Königreich", "drivers": "BoE und UK-Inflation/Löhne; GBP-Wechselkurs; Energie-, Bergbau- und Rohstoffpreise; globaler Umsatzanteil der FTSE-Konzerne; UK-Wachstum.", "rates": "BoE", "fx": "GBP"},
        "US30": {"name": "Dow Jones Industrial Average", "proxy": "^DJI", "region": "USA — Large Cap / Industrials", "drivers": "Fed und US-Renditen; Arbeitsmarkt und ISM; Industrie-/Finanzwerte und Unternehmensgewinne; Kreditbedingungen; defensiver vs. zyklischer Sektor-Mix.", "rates": "Fed", "fx": "USD"},
        "US500": {"name": "S&P 500", "proxy": "^GSPC", "region": "USA — Broad Market", "drivers": "Fed, Inflation und reale Renditen; Arbeitsmarkt und Wachstum; Gewinnrevisionen und Margen; Kreditspreads/Liquidität; Marktbreite und Bewertungsniveau.", "rates": "Fed", "fx": "USD"},
    }
    selected_index = st.selectbox("Alpha Capital Group Symbol", list(index_specs), format_func=lambda s: f"{s} — {index_specs[s]['name']}")
    spec = index_specs[selected_index]
    c1, c2, c3 = st.columns(3)
    c1.metric("Markt", selected_index)
    c2.metric("Makroregion", spec["region"])
    c3.metric("Zentralbank-Fokus", spec["rates"])
    st.markdown("#### Fundamental-Checkliste")
    st.write(spec["drivers"])
    st.info("Das ist ein transparenter Research-Rahmen, kein automatisch gemessener Fundamental-Score. Es werden keine unbekannten Makrodaten oder Konsensüberraschungen erfunden. Für einen quantitativen Live-Makro-Score müssen frische, länderspezifische Serien geladen und auf Veröffentlichungszeitpunkt/Revision geprüft werden.")
    st.markdown("#### Historische Kurs- und Saisonanalyse")
    history_period = st.selectbox("Historienlänge", ["5y", "10y", "max"], index=1, key="index_history_period")
    if st.button("Index-Historie laden und Saisonmuster berechnen", type="primary", key="load_index_history"):
        try:
            prices = load_market_history(spec["proxy"], history_period)
            if prices.empty or len(prices) < 260:
                st.error(f"Zu wenig Kursdaten für {selected_index} über Proxy {spec['proxy']}. Saison- und Regime-Auswertung bleibt gesperrt.")
            else:
                prices = prices.copy()
                prices["date"] = pd.to_datetime(prices["date"], errors="coerce")
                prices["close"] = pd.to_numeric(prices["close"], errors="coerce")
                prices = prices.dropna(subset=["date", "close"]).sort_values("date")
                close = prices.set_index("date")["close"]
                last = float(close.iloc[-1])
                ret20 = float(close.pct_change(20).iloc[-1])
                ret60 = float(close.pct_change(60).iloc[-1])
                sma50 = float(close.rolling(50).mean().iloc[-1])
                sma200 = float(close.rolling(200).mean().iloc[-1])
                regime = "NEUTRAL / GEMISCHT"
                if np.isfinite([last, ret20, ret60, sma50, sma200]).all():
                    if last > sma50 > sma200 and ret20 > 0 and ret60 > 0:
                        regime = "TREND AUFWÄRTS (technischer Proxy)"
                    elif last < sma50 < sma200 and ret20 < 0 and ret60 < 0:
                        regime = "TREND ABWÄRTS (technischer Proxy)"
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Letzter Proxy-Schlusskurs", f"{last:,.2f}")
                k2.metric("20 Handelstage", f"{ret20:+.2%}")
                k3.metric("60 Handelstage", f"{ret60:+.2%}")
                k4.metric("Technischer Regime-Proxy", regime)
                st.caption(f"Proxy: {spec['proxy']} · Beobachtungen: {len(prices):,} · Letztes Datum: {prices['date'].iloc[-1].date()} · Datenanbieter: Yahoo Finance/yfinance")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=prices["date"], y=prices["close"], mode="lines", name="Schlusskurs"))
                fig.add_trace(go.Scatter(x=prices["date"], y=close.rolling(50).mean().values, mode="lines", name="SMA 50"))
                fig.add_trace(go.Scatter(x=prices["date"], y=close.rolling(200).mean().values, mode="lines", name="SMA 200"))
                fig.update_layout(title=f"{selected_index} — Kurs & Trend (Proxy)", xaxis_title="Datum", yaxis_title="Indexpunkte", hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
                # Calendar-month seasonality: average return and empirical win rate by month.
                monthly_close = close.resample("ME").last().dropna()
                monthly_returns = monthly_close.pct_change().dropna()
                season_df = pd.DataFrame({"return": monthly_returns})
                season_df["month"] = season_df.index.month
                seasonal = season_df.groupby("month")["return"].agg(
                    avg_return="mean",
                    median_return="median",
                    win_rate=lambda x: float((x > 0).mean()),
                    observations="count"
                ).reindex(range(1, 13))
                seasonal.index = [MONTHS[m-1] for m in seasonal.index]
                fig_season = go.Figure()
                fig_season.add_trace(go.Bar(x=seasonal.index, y=seasonal["avg_return"] * 100, name="Ø Monatsrendite (%)"))
                fig_season.add_trace(go.Scatter(x=seasonal.index, y=seasonal["win_rate"] * 100, mode="lines+markers", name="Historische Gewinnquote (%)", yaxis="y2"))
                fig_season.update_layout(title=f"{selected_index} — Kalender-Monats-Saisonalität", xaxis_title="Kalendermonat", yaxis_title="Ø Monatsrendite (%)", yaxis2=dict(title="Gewinnquote (%)", overlaying="y", side="right", range=[0, 100]), hovermode="x unified")
                st.plotly_chart(fig_season, use_container_width=True)
                season_display = seasonal.copy()
                season_display["avg_return"] = (season_display["avg_return"] * 100).round(2)
                season_display["median_return"] = (season_display["median_return"] * 100).round(2)
                season_display["win_rate"] = (season_display["win_rate"] * 100).round(1)
                season_display = season_display.rename(columns={"avg_return": "Ø Rendite %", "median_return": "Median %", "win_rate": "Positive Monate %", "observations": "Anzahl Monate"})
                st.dataframe(season_display, use_container_width=True)
                # Calendar-year performance and drawdown, derived only from loaded historical prices.
                annual = close.resample("YE").last().pct_change().dropna() * 100
                if not annual.empty:
                    annual_df = annual.rename("Jahresrendite %").to_frame()
                    annual_df.index = annual_df.index.year
                    st.markdown("#### Kalenderjahresrenditen")
                    st.bar_chart(annual_df)
                if len(monthly_returns) < 60:
                    st.warning("Weniger als 5 Jahre monatlicher Renditen: Saisonmuster sind statistisch schwach und können stark vom Zeitraum abhängen.")
                st.download_button("Saison-Daten als CSV exportieren", data=seasonal.reset_index(names="Monat").to_csv(index=False).encode("utf-8-sig"), file_name=f"{selected_index.lower()}_seasonality.csv", mime="text/csv")
        except Exception as exc:
            st.error(f"Historienabruf/Analyse fehlgeschlagen: {exc}")
            st.caption("Prüfe Internetzugriff, yfinance-Verfügbarkeit und die Symbolabdeckung des Datenanbieters.")
    else:
        st.info("Klicke auf „Index-Historie laden…“, um die Historie abzurufen. Ohne erfolgreichen Abruf wird kein saisonales Ergebnis behauptet.")
    st.markdown("#### Wie das in den Gesamt-Workflow passt")
    st.write("- Saisonality: historische Kalender-Monatsrenditen, Median und Gewinnquote.")
    st.write("- Regime: SMA50/SMA200 plus 20-/60-Tage-Momentum — ausdrücklich ein technischer Proxy, kein Fundamental-Makroregime.")
    st.write("- Fundamentals: die oben genannten länderspezifischen Treiber sind Research-Kontext. Für eine automatische Richtungsbewertung braucht es echte, frische Daten und klare Gewichtung.")
    st.write("- COT: nur dann verwenden, wenn ein passender, korrekt zugeordneter Futures-Kontrakt und ein validierter CFTC-Datensatz vorhanden sind; nicht einfach den Cash-Index-Ticker als COT-Kontrakt behandeln.")
    st.write("- Paper Trading: bestehendes manuelles Journal bleibt separat und kann für diese Symbole über das Markt-/Notizfeld dokumentiert werden.")

else:
    st.subheader("Datenquellen & Aktualität")
    st.markdown("#### Quellenregister")
    sources = pd.DataFrame([
        ["Makro/Zinsen", "FRED API", "API-Key nötig; Frequenz je Serie; kein Konsenssurprise ohne Zusatzanbieter"],
        ["Zentralbankpfade", "Fed, EZB, BoE, BoJ, SNB, BoC, RBA, RBNZ", "Offizielle Veröffentlichungen; Parsing/Mapping erforderlich"],
        ["COT", "CFTC Public Reporting · Legacy Futures Only", "Wöchentlich; Kontraktcode/Schema und Aktualität werden zur Laufzeit geprüft"],
        ["Historische Preise", "yfinance Wrapper / Yahoo Finance", "Nicht garantiert offiziell, vollständig, lizenziert oder echtzeitfähig"],
        ["FX-Kurse", "FX-Datenanbieter / Broker", "Aktualität, Historie und Lizenzbedingungen validieren"],
        ["Konsensdaten", "Separater Makro-Kalender-Anbieter", "Meist separat/lizenziert"]
    ], columns=["Bereich", "Quelle", "Hinweis"])
    st.dataframe(sources, use_container_width=True, hide_index=True)
    st.markdown("#### Freshness-Regeln für Produktion")
    st.write("- Jede Beobachtung braucht Quelle, Zeitstempel, Einheit und Frequenz.")
    st.write("- Fehlende/veraltete Daten dürfen nicht stillschweigend durch Nullen ersetzt werden.")
    st.write("- Jedes Signal muss auf die tatsächlich verwendeten Datenpunkte zurückführbar sein.")
    st.write("- API-Schlüssel in Streamlit Secrets oder Server-Umgebung speichern, niemals in öffentliche Frontend-Dateien.")
    st.markdown("#### FRED API-Key konfigurieren")
    st.code('[secrets.toml]\nFRED_API_KEY = "dein_api_key"', language="toml")
    st.caption("Die Beispielabfrage akzeptiert den Schlüssel im Sidebar-Feld. Für dauerhaftes Hosting besser st.secrets verwenden und das Secret nicht ins GitHub-Repository hochladen.")

st.divider()
st.caption("Macro / Regime Terminal — FX + COT Signal Engine. NEUTRAL bei unzureichenden oder nicht validierten Daten. COT ist wöchentlich, kein Spot-FX-Orderflow. Keine Anlageberatung.")
