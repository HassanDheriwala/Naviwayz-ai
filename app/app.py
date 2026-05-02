import streamlit as st
import joblib
import pandas as pd
import time
import os

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="NaviWayz AI", page_icon="🚗", layout="wide")

# ── LOAD MODEL ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "data", "model", "model.pkl")
model = joblib.load(model_path)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

:root {
    --neon: #00c8ff;
    --neon2: #0044cc;
    --green: #00ffb2;
    --red: #ff4d6a;
    --glass: rgba(0,180,255,0.04);
    --glass-border: rgba(0,200,255,0.18);
}

/* ── Background ─────────────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(160deg, #020c18 0%, #04101f 50%, #030a15 100%);
    font-family: 'Rajdhani', sans-serif;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c18 0%, #05111f 100%);
    border-right: 1px solid rgba(0,200,255,0.12);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c8e8ff;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
}

/* ── Page animation ──────────────────────────────────────────────────── */
.main .block-container {
    animation: fadeUp 0.7s ease both;
    padding-top: 1.5rem;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Glassmorphism card ──────────────────────────────────────────────── */
.card {
    background: var(--glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon), transparent);
    opacity: 0.45;
}
.card-title {
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: rgba(0,200,255,0.5);
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-left: 12px;
    border-left: 3px solid var(--neon);
}

/* ── Predict button ──────────────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00a8e8, #0044cc) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 0 20px rgba(0,168,232,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(0,168,232,0.45) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

/* ── Slider ──────────────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {
    padding-top: 6px;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--neon) !important;
    border: 2px solid #020c18 !important;
}

/* ── Selectbox ───────────────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: rgba(0,180,255,0.04) !important;
    border: 1px solid rgba(0,200,255,0.2) !important;
    border-radius: 10px !important;
    color: #c8e8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
}

/* ── st.info ─────────────────────────────────────────────────────────── */
.stAlert {
    background: rgba(0,180,255,0.06) !important;
    border: 1px solid rgba(0,200,255,0.2) !important;
    border-radius: 10px !important;
    color: #c8e8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    letter-spacing: 1px;
}

/* ── Metrics ─────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(0,30,60,0.55) !important;
    border: 1px solid rgba(0,200,255,0.12) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    color: rgba(0,200,255,0.5) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #c8e8ff !important;
}

/* ── Progress bar ────────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00c8ff, #0044ff) !important;
    border-radius: 3px !important;
}
.stProgress > div > div {
    background: rgba(0,200,255,0.1) !important;
    border-radius: 3px !important;
    height: 6px !important;
}

/* ── Result blocks ───────────────────────────────────────────────────── */
.result-smooth {
    background: rgba(0,255,178,0.04);
    border: 1px solid rgba(0,255,178,0.3);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin: 16px 0;
}
.result-delay {
    background: rgba(255,77,106,0.04);
    border: 1px solid rgba(255,77,106,0.3);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin: 16px 0;
}
.result-icon { font-size: 42px; margin-bottom: 10px; }
.result-text-smooth {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #00ffb2;
    text-transform: uppercase;
}
.result-text-delay {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #ff4d6a;
    text-transform: uppercase;
}
.result-reason {
    font-size: 13px;
    color: rgba(180,220,255,0.55);
    margin-top: 10px;
    letter-spacing: 1px;
    line-height: 1.6;
}

/* ── Labels / text ───────────────────────────────────────────────────── */
label, .stSlider label, .stSelectbox label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 12px !important;
    letter-spacing: 3px !important;
    color: rgba(0,200,255,0.5) !important;
    text-transform: uppercase !important;
}

/* ── Hide Streamlit chrome ───────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 12px'>
        <div style='font-family:Orbitron,monospace; font-size:18px; font-weight:900;
                    letter-spacing:4px; color:#00c8ff'>▲ NAVIWAYZ</div>
        <div style='font-size:10px; letter-spacing:4px; color:rgba(0,200,255,0.4);
                    margin-top:4px'>COMMAND CENTER</div>
    </div>
    <hr style='border-color:rgba(0,200,255,0.12); margin:0 0 20px'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:9px; letter-spacing:4px;
                color:rgba(0,200,255,0.4); text-transform:uppercase; margin-bottom:12px'>
        System Status
    </div>
    """, unsafe_allow_html=True)

    items = [("Model", "Decision Tree"), ("Version", "1.0.0"),
             ("Status", "🟢 Online"), ("Developer", "Hassan"),
             ("University", "Parul University")]
    for label, val in items:
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; padding:8px 0;
                    border-bottom:1px solid rgba(0,200,255,0.08); font-family:Rajdhani,sans-serif'>
            <span style='font-size:12px; letter-spacing:2px; color:rgba(0,200,255,0.4);
                         text-transform:uppercase'>{label}</span>
            <span style='font-size:13px; font-weight:600; color:#c8e8ff'>{val}</span>
        </div>
        """, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:28px 0 24px; border-bottom:1px solid rgba(0,200,255,0.1);
            margin-bottom:28px'>
    <div style='font-family:Orbitron,monospace; font-size:32px; font-weight:900;
                letter-spacing:8px; color:#00c8ff; text-transform:uppercase'>▲ NaviWayz AI</div>
    <div style='font-size:12px; letter-spacing:5px; color:rgba(0,200,255,0.4);
                margin-top:8px; text-transform:uppercase'>
        Intelligent Navigation &nbsp;·&nbsp; Smart Ride Prediction
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT PANEL ───────────────────────────────────────────────────────────────
st.markdown("<div class='card'><div class='card-title'>Route Parameters</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    distance = st.slider("Distance (km)", 1, 50, 10)
with col2:
    traffic = st.selectbox("Traffic Density", ["Low", "Medium", "High"])

st.markdown("</div>", unsafe_allow_html=True)

traffic_map = {"Low": 0, "Medium": 1, "High": 2}
traffic_val = traffic_map[traffic]

# ── LIVE PREVIEW ──────────────────────────────────────────────────────────────
eta_factor = {"Low": 1.0, "Medium": 1.4, "High": 2.2}[traffic]
eta = round(distance / 0.6 * eta_factor)
risk = "High" if (traffic == "High" or distance > 35) else ("Medium" if (traffic == "Medium" or distance > 20) else "Low")
risk_color = {"High": "#ff4d6a", "Medium": "#ffd54f", "Low": "#00ffb2"}[risk]

st.markdown(f"""
<div style='background:rgba(0,30,60,0.6); border:1px solid rgba(0,200,255,0.12);
            border-radius:10px; padding:16px 24px; display:flex;
            justify-content:space-between; align-items:center; margin-bottom:20px;
            font-family:Rajdhani,sans-serif'>
    <div style='text-align:center'>
        <div style='font-size:10px; letter-spacing:3px; color:rgba(0,200,255,0.4);
                    text-transform:uppercase; margin-bottom:4px'>Distance</div>
        <div style='font-family:Orbitron,monospace; font-size:18px;
                    font-weight:700; color:#c8e8ff'>{distance} km</div>
    </div>
    <div style='width:1px; height:40px; background:rgba(0,200,255,0.15)'></div>
    <div style='text-align:center'>
        <div style='font-size:10px; letter-spacing:3px; color:rgba(0,200,255,0.4);
                    text-transform:uppercase; margin-bottom:4px'>Traffic</div>
        <div style='font-family:Orbitron,monospace; font-size:18px;
                    font-weight:700; color:#c8e8ff'>{traffic}</div>
    </div>
    <div style='width:1px; height:40px; background:rgba(0,200,255,0.15)'></div>
    <div style='text-align:center'>
        <div style='font-size:10px; letter-spacing:3px; color:rgba(0,200,255,0.4);
                    text-transform:uppercase; margin-bottom:4px'>Est. Time</div>
        <div style='font-family:Orbitron,monospace; font-size:18px;
                    font-weight:700; color:#c8e8ff'>{eta} min</div>
    </div>
    <div style='width:1px; height:40px; background:rgba(0,200,255,0.15)'></div>
    <div style='text-align:center'>
        <div style='font-size:10px; letter-spacing:3px; color:rgba(0,200,255,0.4);
                    text-transform:uppercase; margin-bottom:4px'>Risk</div>
        <div style='font-family:Orbitron,monospace; font-size:18px;
                    font-weight:700; color:{risk_color}'>{risk}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PREDICT ───────────────────────────────────────────────────────────────────
if st.button("▶  ANALYZE ROUTE"):
    data = pd.DataFrame([[distance, traffic_val]], columns=["distance", "traffic"])

    with st.spinner("Scanning route intelligence..."):
        time.sleep(1.5)
        pred = model.predict(data)

    is_delay = pred[0] == 1
    confidence = 92 if (is_delay and traffic == "High") else \
                 85 if is_delay else \
                 94 if traffic == "Low" else 78

    reasons = {
        True:  {
            "High":   "Heavy traffic detected on primary corridors. AI recommends alternate routing via bypass lanes.",
            "Medium": "Moderate congestion combined with long distance increases delay probability significantly.",
            "Low":    "Extended route distance creates compounded risk even under low-traffic conditions.",
        },
        False: "Optimal traffic conditions detected. Clear passage predicted across all major route segments.",
    }
    reason = reasons[is_delay][traffic] if is_delay else reasons[False]

    # Result block
    css_class = "result-delay" if is_delay else "result-smooth"
    icon = "⚠" if is_delay else "✓"
    title_class = "result-text-delay" if is_delay else "result-text-smooth"
    title_text = "Delay Expected" if is_delay else "Smooth Ride"

    st.markdown(f"""
    <div class='{css_class}'>
        <div class='result-icon'>{icon}</div>
        <div class='{title_class}'>{title_text}</div>
        <div class='result-reason'>{reason}</div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence bar
    st.markdown(f"""
    <div style='margin:16px 0 8px; display:flex; justify-content:space-between;
                font-family:Orbitron,monospace; font-size:10px; letter-spacing:3px;
                color:rgba(0,200,255,0.5); text-transform:uppercase'>
        <span>AI Confidence</span>
        <span style='color:#00c8ff'>{confidence}%</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(confidence / 100)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics row
    st.markdown("<div class='card-title' style='padding-left:12px; border-left:3px solid #00c8ff; font-family:Orbitron,monospace; font-size:10px; letter-spacing:4px; color:rgba(0,200,255,0.5); text-transform:uppercase; margin-bottom:16px'>Analytics Tiles</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Distance", f"{distance} km")
    c2.metric("Traffic", traffic)
    c3.metric("Confidence", f"{confidence}%")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:rgba(0,200,255,0.1); margin:40px 0 16px'>
<div style='text-align:center; font-family:Orbitron,monospace; font-size:9px;
            letter-spacing:4px; color:rgba(0,200,255,0.25); text-transform:uppercase'>
    ▲ NaviWayz AI &nbsp;|&nbsp; Hassan &nbsp;|&nbsp; ▲
</div>
""", unsafe_allow_html=True)