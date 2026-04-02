import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import random
import streamlit.components.v1 as components

# ==============================


# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Gesture2Voice FSK Demo",
    page_icon="🎤",
    layout="wide"
)

# ==============================
# CUSTOM CSS (BLACK + NEON GREEN THEME)
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #000000;
    color: #00FF66;
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #000000 0%, #050805 100%);
    color: #00FF66;
}

.main-title {
    text-align: center;
    color: #00FF66;
    font-size: 42px;
    font-weight: 800;
    text-shadow: 0 0 18px rgba(0, 255, 102, 0.9);
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    color: #7dffb0;
    font-size: 18px;
    margin-bottom: 25px;
}

.glow-box {
    border: 2px solid rgba(0, 255, 102, 0.55);
    border-radius: 18px;
    padding: 20px;
    background: rgba(0, 255, 102, 0.04);
    box-shadow: 0 0 18px rgba(0, 255, 102, 0.22);
    margin-bottom: 20px;
}

.metric-title {
    color: #7dffb0;
    font-size: 18px;
    font-weight: bold;
}

.big-text {
    color: #00FF66;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 0 12px rgba(0, 255, 102, 0.8);
}

.status-ok {
    color: #00FF66;
    font-weight: bold;
    font-size: 18px;
}

.status-wait {
    color: #ffff66;
    font-weight: bold;
    font-size: 18px;
}

.info-chip {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(0, 255, 102, 0.12);
    border: 1px solid rgba(0, 255, 102, 0.35);
    color: #a8ffcc;
    font-size: 14px;
    margin-bottom: 10px;
}

.footer-text {
    text-align: center;
    color: #00FF66;
    font-size: 20px;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(0, 255, 102, 0.6);
    margin-top: 10px;
}

hr {
    border: 1px solid rgba(0, 255, 102, 0.25);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# BROWSER-BASED VOICE OUTPUT (NO pyttsx3)
# ==============================
def play_voice(text):
    safe_text = text.replace('"', '\\"')
    js_code = f"""
    <script>
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance("{safe_text}");
        msg.rate = 1.0;
        msg.pitch = 1.0;
        msg.volume = 1.0;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# ==============================
# SESSION STATE
# ==============================
if "detected_gesture" not in st.session_state:
    st.session_state.detected_gesture = "IDLE"
if "spoken_text" not in st.session_state:
    st.session_state.spoken_text = "Waiting for gesture..."
if "confidence" not in st.session_state:
    st.session_state.confidence = 0
if "system_status" not in st.session_state:
    st.session_state.system_status = "READY"
if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

# ==============================
# TITLE
# ==============================
st.markdown('<div class="main-title">Gesture2Voice FSK Demo</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Gesture → TinyML → FSK Concept → Voice Output (Simulation Mode)</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ==============================
# LAYOUT
# ==============================
col1, col2 = st.columns([1, 1])

# ==============================
# LEFT PANEL - CONTROLS
# ==============================
with col1:
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("## 🎮 Simulate Gesture Input")
    st.write("Press any gesture button to simulate the assistive communication system.")

    gesture_map = {
        "👋 Wave": ("WAVE", "Hi"),
        "🆘 Help": ("HELP", "Help me"),
        "✋ Stop": ("STOP", "Stop please"),
        "💧 Water": ("WATER", "I need water")
    }

    b1, b2 = st.columns(2)
    b3, b4 = st.columns(2)

    clicked = None

    with b1:
        if st.button("👋 Wave", width="stretch"):
            clicked = "👋 Wave"
    with b2:
        if st.button("🆘 Help", width="stretch"):
            clicked = "🆘 Help"
    with b3:
        if st.button("✋ Stop", width="stretch"):
            clicked = "✋ Stop"
    with b4:
        if st.button("💧 Water", width="stretch"):
            clicked = "💧 Water"

    if clicked:
        gesture, text = gesture_map[clicked]
        st.session_state.detected_gesture = gesture
        st.session_state.spoken_text = text
        st.session_state.confidence = random.randint(92, 99)
        st.session_state.system_status = "PROCESSING"
        st.session_state.last_clicked = clicked

        # Simulated processing delay
        time.sleep(0.35)

        # Browser voice output
        play_voice(text)

        st.session_state.system_status = "OUTPUT GENERATED"

    st.markdown('</div>', unsafe_allow_html=True)

    # System Info Box
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("## 🧠 System Status")

    status_color = "status-ok" if st.session_state.system_status != "READY" else "status-wait"
    st.markdown(f'<div class="{status_color}">Current State: {st.session_state.system_status}</div>', unsafe_allow_html=True)
    st.markdown(f"**TinyML Classification:** `{st.session_state.detected_gesture}`")
    st.markdown(f"**Speech Output:** `{st.session_state.spoken_text}`")

    if st.session_state.confidence > 0:
        st.progress(st.session_state.confidence / 100)
    else:
        st.progress(0)

    st.markdown(f"**Confidence:** `{st.session_state.confidence}%`")

    if st.session_state.last_clicked:
        st.markdown(
            f"<div class='info-chip'>Last Triggered Gesture: {st.session_state.last_clicked}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# RIGHT PANEL - LIVE SIGNAL VISUALIZATION
# ==============================
with col2:
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("## 📈 Simulated Gesture Waveform")

    # Generate waveform based on gesture
    t = np.linspace(0, 2, 300)
    gesture = st.session_state.detected_gesture

    if gesture == "WAVE":
        y = 1.2 * np.sin(2 * np.pi * 2 * t) + 0.15 * np.random.randn(len(t))
    elif gesture == "HELP":
        y = 1.5 * np.sign(np.sin(2 * np.pi * 3 * t)) + 0.2 * np.random.randn(len(t))
    elif gesture == "STOP":
        y = 0.9 * np.sin(2 * np.pi * 1 * t) * np.exp(-t / 2) + 0.1 * np.random.randn(len(t))
    elif gesture == "WATER":
        y = 0.7 * np.sin(2 * np.pi * 5 * t) + 0.25 * np.random.randn(len(t))
    else:
        y = 0.08 * np.random.randn(len(t))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=y,
        mode='lines',
        name='Signal',
        line=dict(color='#00FF66', width=3)
    ))

    fig.update_layout(
        title="Real-Time Sensor Signal (Simulated)",
        template="plotly_dark",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="#00FF66"),
        xaxis=dict(
            title="Time (s)",
            gridcolor="rgba(0,255,102,0.18)",
            zerolinecolor="rgba(0,255,102,0.18)"
        ),
        yaxis=dict(
            title="Amplitude",
            gridcolor="rgba(0,255,102,0.18)",
            zerolinecolor="rgba(0,255,102,0.18)"
        ),
        height=430,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, width="stretch", key="main_waveform")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# EXTRA PANELS
# ==============================
st.markdown("---")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("### 🎤 Voice Module")
    st.write("**Engine:** Browser Speech Synthesis")
    st.write("**Status:** Active")
    st.write("**Output Mode:** Real-time speech")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("### 📡 FSK Concept")
    st.write("**Binary 1:** 1200 Hz")
    st.write("**Binary 0:** 2200 Hz")
    st.write("**Purpose:** Robust encoded communication")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    st.markdown("### 🧩 Demo Mode")
    st.write("**Sensor Input:** Simulated")
    st.write("**TinyML:** Simulated classification")
    st.write("**Ready for:** Judge demonstration")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<div class='footer-text'>⚡ Gesture-Based Assistive Communication Using TinyML & FSK ⚡</div>",
    unsafe_allow_html=True
)