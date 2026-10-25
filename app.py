import os
from datetime import datetime, timezone

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="Macro / Regime Terminal", page_icon="◇", layout="wide")

# --- Theme ---
BG, PANEL, BORDER = "#07111b", "#0b1722", "#1a2b3a"
TEXT, MUTED = "#edf4fb", "#8ea6bb"
RED, GREEN, BLUE, YELLOW, CYAN = "#ff2447", "#00d68f", "#3292ff", "#ffbf3f", "#44c8ff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {{ color-scheme: dark; }}
html, body, [class*="css"] {{ font-family: Inter, sans-serif; }}
.stApp {{ background:radial-gradient(ellipse at 75% 0%,#102236 0%,{BG} 52%); color:{TEXT}; }}
[data-testid="stHeader"] {{ background:rgba(5,13,21,.88); }}
[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#091521,#07111a); border-right:1px solid {BORDER}; }}
h1,h2,h3,h4,p,label {{ color:{TEXT}; }}
h1 {{ letter-spacing:-.04em; font-weight:800; }}
[data-testid="stMetric"] {{ background:linear-gradient(145deg,#0d1b28,{PANEL}); border:1px solid {BORDER}; border-radius:13px; padding:16px; min-height:115px; }}
[data-testid="stMetricLabel"] {{ color:{MUTED}; }}
[data-testid="stMetricValue"] {{ color:{TEXT}; font-weight:750; }}
div[data-testid="stButton"]>button {{ background:linear-gradient(100deg,#ff1744,#e90032); color:white; border:0; border-radius:9px; font-weight:700; min-height:42px; }}
div[data-testid="stButton"]>button:hover {{ background:#ff3658; color:white; }}
div[data-testid="stTextInput"] input {{ background:#0b1925; color:{TEXT}; border:1px solid {BORDER}; }}
[data-testid="stDataFrame"] {{ border:1px solid {BORDER}; border-radius:10px; }}
hr {{ border-color:{BORDER}; }}
.brand {{ display:flex; gap:12px; align-items:center; padding:0 0 12px; border-bottom:1px solid {BORDER}; margin-bottom:14px; }}
.logo {{ width:36px; height:36px; display:flex; align-items:center; justify-content:center; border:3px solid {RED}; color:{RED}; border-radius:11px; transform:rotate(45deg); font-weight:900; }}
.logo span {{ transform:rotate(-45deg); }}
.brand-title {{ font-size:20px; font-weight:800; letter-spacing:-.04em; color:#f7fbff; }}
.brand-sub {{ font-size:12px; color:{MUTED}; margin-top:3px; }}
.panel {{ background:linear-gradient(145deg,rgba(13,27,40,.96),rgba(7,17,27,.96)); border:1px solid {BORDER}; border-radius:13px; padding:15px 16px; margin-bottom:12px; }}
.panel-title {{ font-weight:750; font-size:15px; margin-bottom:12px; color:#edf5ff; }}
.ticker {{ background:linear-gradient(145deg,#0b1722,#07111b); border:1px solid {BORDER}; border-radius:9px; padding:8px 9px; min-height:54px; }}
.ticker-name {{ color:#c7d5e3; font-size:10px; font-weight:700; }}
.ticker-value {{ color:#f4f8fc; font-size:12px; font-weight:700; margin-top:5px; }}
.positive {{ color:{GREEN}; }} .negative {{ color:{RED}; }} .muted {{ color:{MUTED}; }}
.small-note {{ color:{MUTED}; font-size:11px; line-height:1.5; }}
</style>
""", unsafe_allow_html=True)

FX = {
    "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X", "USD/CAD": "CAD=X", "USD/CHF": "CHF=X", "NZD/USD": "NZDUSD=X"
}
FRED_SERIES = {
    "Fed Funds Rate": "DFF", "US 2Y Yield": "DGS2",
    "US 10Y Yield": "DGS10", "US Dollar Index": "DTWEXBGS"
}
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
try:
    FRED_API_KEY = FRED_API_KEY or st.secrets.get("FRED_API_KEY", "")
except Exception:
    pass

@st.cache_data(ttl=300, show_spinner=False)
def history(ticker, period="1y", interval="1d"):
    try:
        df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
        if df is None or df.empty or "Close" not in df:
            return pd.DataFrame()
        return df[["Close"]].dropna()
    except Exception:
        return pd.DataFrame()

def latest_change(ticker):
    df = history(ticker, "5d", "1d")
    if df.empty:
        return None, None
    val = float(df.Close.iloc[-1])
    chg = (val / float(df.Close.iloc[-2]) - 1) * 100 if len(df) > 1 and df.Close.iloc[-2] else None
    return val, chg

@st.cache_data(ttl=1800, show_spinner=False)
def fred_observation(series, api_key):
    if not api_key:
        return None, None
    try:
        r = requests.get("https://api.stlouisfed.org/fred/series/observations",
            params={"series_id": series, "api_key": api_key, "file_type": "json",
                    "sort_order": "desc", "limit": 20}, timeout=10)
        r.raise_for_status()
        for item in r.json().get("observations", []):
            if item.get("value") not in (None, "."):
                return float(item["value"]), item.get("date")
    except Exception:
        pass
    return None, None

def chart_style(fig, height=280):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a9bfd2", size=10), margin=dict(l=8,r=8,t=12,b=8),
        legend=dict(orientation="h", y=1.12, x=0, font=dict(size=10)),
        xaxis=dict(gridcolor="#182a39", zerolinecolor="#26394a"),
        yaxis=dict(gridcolor="#182a39", zerolinecolor="#26394a"))
    return fig

with st.sidebar:
    st.markdown('<div class="brand"><div class="logo"><span>◇</span></div><div><div class="brand-title">MACRO / REGIME</div><div class="brand-sub">FX · Makro · COT · Saisonalität · Quant</div></div></div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["Übersicht", "FX Signal", "ML Lab", "Saisonalität",
        "COT / Positioning", "NQ & ES", "Quant & Regression", "Datenquellen"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("EINSTELLUNGEN")
    key_input = st.text_input("FRED API-Key (optional)", value=FRED_API_KEY, type="password")
    if st.button("⟳  Daten aktualisieren", use_container_width=True):
        history.clear()
        fred_observation.clear()
        st.rerun()
    st.markdown("**Letzter Abruf:**")
    st.caption(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))

api_key = key_input if "key_input" in locals() else FRED_API_KEY
st.markdown('<div class="brand"><div class="logo"><span>◇</span></div><div><div class="brand-title">MACRO / REGIME TERMINAL</div><div class="brand-sub">FX · Makro · COT · Saisonalität · Quant · Regime</div></div></div>', unsafe_allow_html=True)

tick_cols = st.columns(7, gap="small")
fx_data = {}
for col, (pair, ticker) in zip(tick_cols, FX.items()):
    val, change = latest_change(ticker)
    fx_data[pair] = (val, change)
    value_text = "—" if val is None else (f"{val:.4f}" if val < 10 else f"{val:.3f}")
    change_text = "Keine Daten" if change is None else f"{change:+.2f}%"
    css = "positive" if (change or 0) >= 0 else "negative"
    col.markdown(f'<div class="ticker"><div class="ticker-name">{pair}</div><div class="ticker-value">{value_text} <span class="{css}" style="float:right">{change_text}</span></div></div>', unsafe_allow_html=True)

st.write("")
left, right = st.columns([3.1, 1.2])
with left:
    st.title("Zentrales Dashboard" if page == "Übersicht" else page)
    st.caption("Ein gemeinsamer Überblick über FX, Makro und Cross-Asset-Proxies.")
with right:
    st.markdown(f'<div class="panel"><div class="small-note">{datetime.now().strftime("%A, %d. %B %Y")}</div><div style="font-size:22px;font-weight:800">{datetime.now(timezone.utc).strftime("%H:%M UTC")}</div><div class="small-note"><span style="color:{GREEN}">● Datenabfrage</span> · Yahoo Finance / FRED</div></div>', unsafe_allow_html=True)

nq, nq_ch = latest_change("NQ=F")
es, es_ch = latest_change("ES=F")
vix, vix_ch = latest_change("^VIX")
fred = {name: fred_observation(series, api_key) for name, series in FRED_SERIES.items()}
us10, us10_date = fred["US 10Y Yield"]
fed, fed_date = fred["Fed Funds Rate"]
us2, us2_date = fred["US 2Y Yield"]
dxy, dxy_date = fred["US Dollar Index"]

risk_off = ((nq_ch is not None and nq_ch < 0) and (es_ch is not None and es_ch < 0)) or (vix_ch is not None and vix_ch > 0)
regime = "RISK-OFF" if risk_off else ("RISK-ON" if nq_ch is not None and es_ch is not None else "NICHT VERFÜGBAR")

def metric_value(v, fmt="{:.2f}", suffix=""):
    return "—" if v is None else fmt.format(v) + suffix

mcols = st.columns(5, gap="small")
mcols[0].metric("🛡️ Risk Regime (Proxy)", regime, "NQ/ES Tagesbewegung und VIX")
mcols[1].metric("💱 FX-Paare verfügbar", f'{sum(v is not None for v, _ in fx_data.values())} / 7', "Yahoo Finance")
mcols[2].metric("▤ Frische Marktserien", f'{sum(v is not None for v, _ in [ (nq,nq_ch),(es,es_ch),(vix,vix_ch),(us10,us10_date),(fed,fed_date),(us2,us2_date),(dxy,dxy_date)])} / 7', "Verfügbare Abfragen")
mcols[3].metric("📈 US 10Y Rendite", metric_value(us10, "{:.2f}", " %"), f"FRED {us10_date or 'nicht verfügbar'}")
mcols[4].metric("〽️ VIX", metric_value(vix, "{:.2f}"), f"{vix_ch:+.2f}% 1D" if vix_ch is not None else "Yahoo Finance")

if page == "Übersicht":
    a, b, c = st.columns([1.05, 1.35, 1.0], gap="small")
    with a:
        st.markdown('<div class="panel-title">🌐 G10 Währungsstärke (20 Tage)</div>', unsafe_allow_html=True)
        strengths = []
        for pair, ticker in FX.items():
            h = history(ticker, "1mo", "1d")
            if len(h) >= 2:
                strength = (float(h.Close.iloc[-1]) / float(h.Close.iloc[0]) - 1) * 100
                base = pair.split("/")[0]
                strengths.append((base, strength))
        if strengths:
            df = pd.DataFrame(strengths, columns=["Währung", "Stärke %"]).sort_values("Stärke %")
            fig = go.Figure(go.Bar(x=df["Stärke %"], y=df["Währung"], orientation="h",
                marker_color=[GREEN if x >= 0 else RED for x in df["Stärke %"]]))
            fig.update_layout(yaxis=dict(title="", gridcolor="#182a39"), xaxis=dict(title="% Veränderung", gridcolor="#182a39"))
            st.plotly_chart(chart_style(fig, 300), use_container_width=True)
        else:
            st.info("Aktuell keine FX-Historie verfügbar.")
    with b:
        st.markdown('<div class="panel-title">♟ Markt-Regime-Indikatoren</div>', unsafe_allow_html=True)
        series = []
        for label, ticker, color in [("NQ (norm.)","NQ=F",RED),("ES (norm.)","ES=F",BLUE),("VIX (invertiert)","^VIX",YELLOW)]:
            h = history(ticker, "1y", "1d")
            if not h.empty:
                s = h.Close
                norm = (s / s.iloc[0] - 1) * 100
                if "VIX" in label: norm = -norm
                series.append((label, norm, color))
        fig = go.Figure()
        for label, values, color in series:
            fig.add_trace(go.Scatter(x=values.index, y=values, name=label, mode="lines", line=dict(color=color, width=2)))
        fig.add_hline(y=0, line_color="#526779", line_width=1)
        st.plotly_chart(chart_style(fig, 300), use_container_width=True)
    with c:
        st.markdown('<div class="panel-title">🏦 US Makro (FRED)</div>', unsafe_allow_html=True)
        for name, value, date in [("Fed Funds Rate",fed,fed_date),("US 2Y Rendite",us2,us2_date),("US 10Y Rendite",us10,us10_date),("US Dollar Index",dxy,dxy_date)]:
            st.markdown(f'<div style="padding:11px 2px;border-bottom:1px solid {BORDER}"><div style="color:{MUTED};font-size:12px">{name}</div><b style="font-size:19px">{metric_value(value,"{:.2f}"," %") if value is not None and name != "US Dollar Index" else metric_value(value,"{:.2f}")}</b><div class="small-note">{date or "Key / Daten nicht verfügbar"}</div></div>', unsafe_allow_html=True)
        if not api_key:
            st.caption("FRED API-Key in der Sidebar eingeben oder in Streamlit Secrets speichern.")

    st.write("")
    left, right = st.columns([2.1, 1.0], gap="small")
    with left:
        st.markdown('<div class="panel-title">💹 FX- und Cross-Asset-Märkte</div>', unsafe_allow_html=True)
        rows = []
        for pair, ticker in FX.items():
            value, change = fx_data[pair]
            h = history(ticker, "1y", "1d")
            change_200 = ((float(h.Close.iloc[-1]) / float(h.Close.iloc[-min(200,len(h))]) - 1) * 100) if len(h) > 1 else None
            rows.append({"Markt":pair,"Symbol":ticker,"Letzter Kurs":round(value,5) if value is not None else None,
                "Δ 1D (%)":round(change,2) if change is not None else None,
                "Δ ~200D (%)":round(change_200,2) if change_200 is not None else None,
                "Letztes Datum (UTC)":str(h.index[-1].date()) if not h.empty else "—",
                "Status":"OK" if value is not None else "Keine Daten"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    with right:
        st.markdown('<div class="panel-title">🟢 Datenqualität</div>', unsafe_allow_html=True)
        checks = [
            ("FX-Kurse (yfinance)", sum(v is not None for v,_ in fx_data.values()), 7),
            ("NQ / ES / VIX", sum(v is not None for v in [nq,es,vix]), 3),
            ("Makrodaten (FRED)", sum(v is not None for v,_ in fred.values()), 4),
        ]
        for label, ok, total in checks:
            color = GREEN if ok == total else YELLOW if ok else RED
            st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid {BORDER}"><b>{label}</b><span style="float:right;color:{color}">● {ok}/{total}</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="small-note">Datenanbieter können Verzögerungen oder Ausfälle haben. Historische Daten sind nicht automatisch Echtzeitdaten.</p>', unsafe_allow_html=True)

elif page == "FX Signal":
    st.subheader("FX Signal")
    chosen = st.selectbox("Währungspaar", list(FX.keys()))
    ticker = FX[chosen]
    h = history(ticker, "1y", "1d")
    if h.empty:
        st.warning("Für dieses Paar sind aktuell keine Kursdaten verfügbar.")
    else:
        st.line_chart(h.Close, use_container_width=True)
        st.metric("Letzter Kurs", f'{h.Close.iloc[-1]:.5f}', f'{(h.Close.iloc[-1]/h.Close.iloc[-2]-1)*100:+.2f}%' if len(h)>1 else None)
        st.caption("Das Signal ist eine Marktübersicht, keine Anlageberatung.")

elif page == "ML Lab":
    st.subheader("ML Lab — einfache Modell-Demo")
    chosen = st.selectbox("Markt", list(FX.keys()))
    h = history(FX[chosen], "2y", "1d")
    if len(h) > 30:
        h["Return"] = h.Close.pct_change()
        h["Volatilität 20T"] = h["Return"].rolling(20).std() * (252 ** 0.5) * 100
        st.line_chart(h[["Volatilität 20T"]].dropna(), use_container_width=True)
        st.caption("Deskriptive Volatilität, kein trainiertes Prognosemodell.")
    else:
        st.info("Zu wenige historische Daten für diese Ansicht.")

elif page == "Saisonalität":
    st.subheader("Saisonalität")
    chosen = st.selectbox("FX-Paar", list(FX.keys()))
    h = history(FX[chosen], "5y", "1d")
    if not h.empty:
        h["Monat"] = h.index.month
        h["Return"] = h.Close.pct_change()
        monthly = h.groupby("Monat")["Return"].mean().reindex(range(1,13)) * 100
        fig = go.Figure(go.Bar(x=["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"], y=monthly.values,
            marker_color=[GREEN if x >= 0 else RED for x in monthly.fillna(0)]))
        st.plotly_chart(chart_style(fig, 320), use_container_width=True)
    else:
        st.info("Keine historischen Daten verfügbar.")

elif page == "COT / Positioning":
    st.subheader("COT / Positioning")
    st.info("COT-Daten sind in dieser Version noch nicht angebunden. Keine Positionierungswerte werden erfunden.")
    st.markdown("Für die Integration kann eine CFTC-Datenquelle ergänzt werden.")

elif page == "NQ & ES":
    st.subheader("Nasdaq- und S&P-Futures")
    cols = st.columns(2)
    for col, label, ticker in [(cols[0],"Nasdaq Futures","NQ=F"),(cols[1],"S&P 500 Futures","ES=F")]:
        h = history(ticker, "1y", "1d")
        with col:
            st.markdown(f"**{label}**")
            if not h.empty: st.line_chart(h.Close, use_container_width=True)
            else: st.warning("Keine Daten verfügbar.")

elif page == "Quant & Regression":
    st.subheader("Quant & Regression")
    left_ticker = st.selectbox("X-Variable", list(FX.keys()), index=0)
    right_ticker = st.selectbox("Y-Variable", list(FX.keys()), index=1)
    x = history(FX[left_ticker], "1y", "1d")
    y = history(FX[right_ticker], "1y", "1d")
    if not x.empty and not y.empty:
        joined = pd.concat([x.Close.pct_change().rename("X"), y.Close.pct_change().rename("Y")], axis=1).dropna()
        if len(joined) > 10:
            corr = joined.X.corr(joined.Y)
            slope = joined.X.cov(joined.Y) / joined.X.var() if joined.X.var() else float("nan")
            c1,c2 = st.columns(2)
            c1.metric("Korrelation", f"{corr:.3f}")
            c2.metric("Regression-Slope", f"{slope:.3f}")
            fig = go.Figure(go.Scatter(x=joined.X, y=joined.Y, mode="markers", marker=dict(color=CYAN, size=5)))
            st.plotly_chart(chart_style(fig, 320), use_container_width=True)
        else: st.info("Nicht genug gemeinsame Daten.")
    else: st.info("Daten für die Regression sind nicht verfügbar.")

elif page == "Datenquellen":
    st.subheader("Datenquellen und Status")
    st.write("FX und Futures: Yahoo Finance / yfinance. Makro: Federal Reserve Economic Data (FRED).")
    st.write("FRED API-Key:", "hinterlegt" if api_key else "nicht hinterlegt")
    st.dataframe(pd.DataFrame([
        {"Quelle":"Yahoo Finance","Verwendung":"FX, NQ, ES, VIX","Status":"Verfügbar" if any(v is not None for v,_ in fx_data.values()) else "Keine Daten"},
        {"Quelle":"FRED","Verwendung":"DFF, DGS2, DGS10, Dollar Index","Status":"Key vorhanden" if api_key else "API-Key fehlt"},
        {"Quelle":"CFTC COT","Verwendung":"Positionierung","Status":"Noch nicht integriert"},
    ]), use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown('<div class="small-note">Macro / Regime Terminal · Informations- und Analysewerkzeug, keine Anlageberatung. Datenverfügbarkeit und Verzögerungen hängen von den jeweiligen Anbietern ab.</div>', unsafe_allow_html=True)
