"""
app.py — Night Sky Companion

An immersive, offline constellation spotter with open-source AI narration.
Red-light night-vision mode. Pocket mode. No internet required.

NOTE ON STREAMLIT HTML:
Streamlit's markdown parser terminates HTML blocks on blank lines and
treats indented lines as code. Every HTML string in this file therefore
has NO blank lines and uses textwrap.dedent() to strip indentation.
"""

import streamlit as st
import json
import os
import textwrap
from datetime import datetime, timezone
from sky_engine import (
    get_visible_constellations,
    get_moon_phase,
    get_bright_stars,
)
from ai_narrator import narrate_constellation, get_moon_narration


# ============================================================
# HELPERS  (must be defined before use)
# ============================================================
def _compass_arrow(direction):
    return {
        "north": "↑",
        "south": "↓",
        "east": "→",
        "west": "←",
        "northeast": "↗",
        "northwest": "↖",
        "southeast": "↘",
        "southwest": "↙",
    }.get(direction.lower(), "•")


def _dir_from_az(az):
    if 315 <= az or az < 45:
        return "north"
    elif 45 <= az < 135:
        return "east"
    elif 135 <= az < 225:
        return "south"
    else:
        return "west"


def _moon_icon(phase_name):
    name = phase_name.lower()
    if "new" in name:
        return "🌑"
    if "waxing crescent" in name:
        return "🌒"
    if "first quarter" in name:
        return "🌓"
    if "waxing gibbous" in name:
        return "🌔"
    if "full" in name:
        return "🌕"
    if "waning gibbous" in name:
        return "🌖"
    if "last quarter" in name or "third quarter" in name:
        return "🌗"
    if "waning crescent" in name:
        return "🌘"
    return "🌙"


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Night Sky Companion",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLES
# ============================================================
def inject_styles(red_light=False):
    """Inject the full CSS theme."""

    if red_light:
        bg1, bg2, bg3 = "#0a0000", "#1a0000", "#0a0000"
        fg_primary = "#ff5555"
        fg_secondary = "#cc4444"
        accent = "#ff3333"
        card_bg = "rgba(30, 0, 0, 0.6)"
        card_border = "rgba(255, 80, 80, 0.25)"
        glow = "rgba(255, 60, 60, 0.3)"
    else:
        bg1, bg2, bg3 = "#05060f", "#0b0f2a", "#05060f"
        fg_primary = "#e8e8ff"
        fg_secondary = "#9aa0c7"
        accent = "#8b7dff"
        card_bg = "rgba(20, 24, 55, 0.55)"
        card_border = "rgba(139, 125, 255, 0.25)"
        glow = "rgba(139, 125, 255, 0.3)"

    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
:root {{
    --bg1: {bg1};
    --bg2: {bg2};
    --bg3: {bg3};
    --fg-primary: {fg_primary};
    --fg-secondary: {fg_secondary};
    --accent: {accent};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --glow: {glow};
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
.stApp {{
    background: radial-gradient(ellipse at 20% 0%, var(--bg2) 0%, transparent 50%), radial-gradient(ellipse at 80% 100%, var(--bg2) 0%, transparent 50%), linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 50%, var(--bg3) 100%);
    background-attachment: fixed;
    color: var(--fg-primary);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}}
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: radial-gradient(1px 1px at 12% 18%, rgba(255,255,255,0.75), transparent), radial-gradient(1px 1px at 32% 62%, rgba(255,255,255,0.55), transparent), radial-gradient(1.5px 1.5px at 47% 23%, rgba(255,255,255,0.85), transparent), radial-gradient(1px 1px at 62% 78%, rgba(255,255,255,0.5), transparent), radial-gradient(1px 1px at 78% 12%, rgba(255,255,255,0.65), transparent), radial-gradient(1.5px 1.5px at 88% 55%, rgba(255,255,255,0.7), transparent), radial-gradient(1px 1px at 8% 88%, rgba(255,255,255,0.6), transparent), radial-gradient(1px 1px at 55% 42%, rgba(255,255,255,0.4), transparent), radial-gradient(1px 1px at 92% 82%, rgba(255,255,255,0.55), transparent), radial-gradient(1px 1px at 22% 44%, rgba(255,255,255,0.5), transparent);
    background-size: 100% 100%;
    opacity: 0.9;
    animation: twinkle 6s ease-in-out infinite alternate;
    z-index: 0;
}}
@keyframes twinkle {{
    0%   {{ opacity: 0.7; }}
    100% {{ opacity: 1.0; }}
}}
.main, .block-container, section.main > div {{
    position: relative;
    z-index: 1;
}}
.block-container {{
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}}
h1, h2, h3 {{
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    color: var(--fg-primary) !important;
}}
h1 {{
    font-size: 3.5rem !important;
    line-height: 1.05 !important;
    margin-bottom: 0.3rem !important;
    background: linear-gradient(135deg, var(--fg-primary) 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
h2 {{
    font-size: 2rem !important;
    margin-top: 1.6rem !important;
    margin-bottom: 0.6rem !important;
}}
h3 {{ font-size: 1.4rem !important; }}
p, span, div, label {{
    color: var(--fg-primary);
    font-family: 'Inter', sans-serif;
}}
.hero-subtitle {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    font-style: italic;
    color: var(--fg-secondary);
    letter-spacing: 0.03em;
    margin-bottom: 2rem;
    line-height: 1.6;
}}
.section-label {{
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: var(--fg-secondary);
    font-weight: 600;
    margin: 2.5rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
.section-label::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--card-border), transparent);
}}
.sky-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.75rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}}
.sky-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.5;
}}
.sky-card:hover {{
    transform: translateY(-3px);
    border-color: var(--accent);
    box-shadow: 0 20px 40px -10px var(--glow);
}}
.constellation-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}}
.constellation-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--fg-primary);
    line-height: 1.1;
}}
.constellation-abbr {{
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--fg-secondary);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-left: 0.5rem;
}}
.compass {{
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--card-border);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    color: var(--fg-secondary);
    font-weight: 500;
}}
.compass-arrow {{ font-size: 1.1rem; }}
.alt-gauge {{ margin: 0.9rem 0 1rem 0; }}
.alt-labels {{
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: var(--fg-secondary);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}}
.alt-bar {{
    position: relative;
    height: 8px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
}}
.alt-fill {{
    position: absolute;
    inset: 0 auto 0 0;
    background: linear-gradient(90deg, var(--accent), #ffb347);
    border-radius: 999px;
    box-shadow: 0 0 12px var(--glow);
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}}
.alt-value {{
    text-align: right;
    font-size: 0.85rem;
    color: var(--fg-primary);
    font-weight: 600;
    margin-top: 0.35rem;
    font-family: 'Inter', sans-serif;
}}
.info-block {{
    background: rgba(255,255,255,0.03);
    border-left: 3px solid var(--accent);
    padding: 0.85rem 1.1rem;
    border-radius: 0 10px 10px 0;
    margin: 0.75rem 0;
}}
.info-label {{
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 700;
    margin-bottom: 0.4rem;
}}
.info-text {{
    color: var(--fg-primary);
    font-size: 0.95rem;
    line-height: 1.65;
}}
.narration-block {{
    background: linear-gradient(135deg, rgba(139,125,255,0.08), rgba(139,125,255,0.02));
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.9rem;
}}
.narration-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-style: italic;
    line-height: 1.55;
    color: var(--fg-primary);
}}
.moon-card {{
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    display: flex;
    align-items: center;
    gap: 1.75rem;
    backdrop-filter: blur(20px);
}}
.moon-icon {{
    font-size: 3.5rem;
    filter: drop-shadow(0 0 12px rgba(255,255,220,0.5));
}}
.moon-info h3 {{
    margin: 0 0 0.4rem 0 !important;
    font-size: 1.6rem !important;
}}
.moon-note {{
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    color: var(--fg-secondary);
    font-size: 1.05rem;
    line-height: 1.5;
    margin-top: 0.5rem;
}}
.moon-pct {{
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 600;
}}
.stats-strip {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}
.stat-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    backdrop-filter: blur(20px);
}}
.stat-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--fg-primary);
    line-height: 1;
}}
.stat-label {{
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--fg-secondary);
    margin-top: 0.35rem;
}}
.pocket-banner {{
    background: linear-gradient(135deg, var(--bg2), var(--bg1));
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 2rem;
    position: relative;
    overflow: hidden;
}}
.pocket-banner::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 50%, var(--glow), transparent 70%);
    opacity: 0.4;
    pointer-events: none;
}}
.pocket-banner h2 {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem !important;
    margin: 0 0 0.5rem 0 !important;
    position: relative;
}}
.pocket-banner p {{
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.2rem;
    color: var(--fg-secondary);
    margin: 0;
    position: relative;
}}
.journal-entry {{
    position: relative;
    padding-left: 2rem;
    padding-bottom: 1.5rem;
    border-left: 2px solid var(--card-border);
    margin-left: 0.5rem;
}}
.journal-entry::before {{
    content: "";
    position: absolute;
    left: -7px;
    top: 0.4rem;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 12px var(--glow);
}}
.journal-time {{
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--fg-secondary);
    font-weight: 600;
}}
.journal-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--fg-primary);
    margin: 0.2rem 0;
}}
.journal-meta {{
    font-size: 0.85rem;
    color: var(--fg-secondary);
}}
.stButton > button {{
    background: linear-gradient(135deg, var(--accent), #b8a4ff);
    color: #0a0a1a !important;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 1.5rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.85rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 24px -6px var(--glow);
    width: 100%;
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 14px 32px -6px var(--glow);
    filter: brightness(1.1);
}}
.stButton > button:active {{ transform: translateY(0); }}
.stButton > button[kind="secondary"] {{
    background: transparent;
    color: var(--fg-primary) !important;
    border: 1px solid var(--card-border);
    box-shadow: none;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.5rem;
    border-bottom: 1px solid var(--card-border);
    background: transparent;
    padding-bottom: 0;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border: none;
    color: var(--fg-secondary);
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.85rem 1.25rem;
    letter-spacing: 0.05em;
}}
.stTabs [aria-selected="true"] {{
    color: var(--fg-primary) !important;
    background: transparent !important;
    border-bottom: 2px solid var(--accent) !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: transparent; }}
.stTextInput input, .stNumberInput input {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--fg-primary) !important;
    border-radius: 10px !important;
    padding: 0.6rem 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--glow) !important;
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--bg2), var(--bg1));
    border-right: 1px solid var(--card-border);
}}
section[data-testid="stSidebar"] * {{ color: var(--fg-primary); }}
section[data-testid="stSidebar"] h2 {{
    font-size: 1.6rem !important;
    margin-top: 0.5rem !important;
}}
.stCheckbox label, .stToggle label {{
    color: var(--fg-primary) !important;
    font-size: 0.9rem !important;
}}
.streamlit-expanderHeader {{
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    color: var(--fg-primary) !important;
    font-weight: 500 !important;
}}
.stSpinner > div {{ border-top-color: var(--accent) !important; }}
.stAlert {{
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--fg-primary) !important;
    border-radius: 12px !important;
}}
.caption, .stCaption, small {{ color: var(--fg-secondary) !important; }}
hr {{
    border-color: var(--card-border) !important;
    opacity: 0.5;
}}
.stSpinner > div > div {{ color: var(--fg-secondary) !important; }}
@media (max-width: 768px) {{
    h1 {{ font-size: 2.4rem !important; }}
    .stats-strip {{ grid-template-columns: 1fr; }}
    .moon-card {{ flex-direction: column; text-align: center; }}
    .constellation-header {{ flex-direction: column; align-items: flex-start; }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "journal" not in st.session_state:
    st.session_state.journal = []
if "red_light" not in st.session_state:
    st.session_state.red_light = False
if "pocket_mode" not in st.session_state:
    st.session_state.pocket_mode = False
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🌙 Settings")
    st.markdown(
        "<p style='font-size:0.85rem;color:#9aa0c7;margin-top:-0.5rem;'>"
        "Configure your observation point and viewing mode."
        "</p>",
        unsafe_allow_html=True,
    )

    latitude = st.number_input(
        "Latitude",
        value=28.6139,
        format="%.4f",
        help="Decimal degrees. Positive = North.",
    )
    longitude = st.number_input(
        "Longitude",
        value=77.2090,
        format="%.4f",
        help="Decimal degrees. Positive = East.",
    )

    st.markdown("---")

    st.session_state.red_light = st.toggle(
        "🔴 Red-Light Night Vision",
        value=st.session_state.red_light,
        help="Preserves your dark adaptation when stargazing.",
    )

    st.session_state.pocket_mode = st.toggle(
        "📴 Pocket Mode",
        value=st.session_state.pocket_mode,
        help="Narrates results aloud so you never look at the screen.",
    )

    st.markdown("---")

    st.markdown(
        "<p style='font-size:0.78rem;color:#9aa0c7;line-height:1.5;'>"
        "🌌 <strong>Fully offline.</strong> Skyfield computes positions locally. "
        "Gemma narrates via Ollama on your machine. No data leaves your device."
        "</p>",
        unsafe_allow_html=True,
    )


# ============================================================
# APPLY THEME
# ============================================================
inject_styles(red_light=st.session_state.red_light)


# ============================================================
# HERO HEADER
# ============================================================
st.markdown("<h1>Night Sky Companion</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='hero-subtitle'>An offline stargazing companion. "
    "Point, look up, and let the universe introduce itself.</p>",
    unsafe_allow_html=True,
)


# ============================================================
# TABS
# ============================================================
tab_sky, tab_journal, tab_about = st.tabs(["🔭 Tonight's Sky", "📔 Journal", "ℹ️ About"])


# ============================================================
# TAB 1: Tonight's Sky
# ============================================================
with tab_sky:

    col_scan, col_meta = st.columns([2, 1])

    with col_scan:
        scan_clicked = st.button("🔭  Scan the Sky", use_container_width=True)

    with col_meta:
        st.markdown(
            f"<div style='text-align:right;font-size:0.8rem;color:#9aa0c7;padding-top:0.9rem;'>"
            f"📍 {latitude:.2f}°, {longitude:.2f}°"
            f"</div>",
            unsafe_allow_html=True,
        )

    # --- Handle scan ---
    if scan_clicked:
        with st.spinner("Consulting the sky…"):
            now = datetime.now(timezone.utc)
            constellations = get_visible_constellations(latitude, longitude, now)
            moon = get_moon_phase(now)
            bright_stars = get_bright_stars(latitude, longitude, now)

            narrations = []
            for c in constellations[:5]:
                n = narrate_constellation(c["abbreviation"], c["altitude_max"], c["azimuth"])
                narrations.append({**n, "altitude_max": c["altitude_max"]})

        st.session_state.scan_results = {
            "time": now,
            "constellations": constellations,
            "moon": moon,
            "bright_stars": bright_stars,
            "narrations": narrations,
        }

        for n in narrations:
            st.session_state.journal.append({
                "time": now.strftime("%Y-%m-%d %H:%M UTC"),
                "constellation": n["name"],
                "abbreviation": n["abbreviation"],
                "altitude": round(n["altitude_max"], 1),
                "direction": n["direction"],
            })

    # --- Render results ---
    if st.session_state.scan_results:
        data = st.session_state.scan_results
        moon = data["moon"]

        # ---- Stats strip ----
        stats_html = textwrap.dedent(f"""\
        <div class="stats-strip">
        <div class="stat-card">
        <div class="stat-value">{len(data['constellations'])}</div>
        <div class="stat-label">Constellations Up</div>
        </div>
        <div class="stat-card">
        <div class="stat-value">{len(data['bright_stars'])}</div>
        <div class="stat-label">Bright Stars</div>
        </div>
        <div class="stat-card">
        <div class="stat-value">{moon['illumination_pct']:.0f}<span style="font-size:1.2rem;">%</span></div>
        <div class="stat-label">Moon Illumination</div>
        </div>
        </div>
        """)
        st.markdown(stats_html, unsafe_allow_html=True)

        # ---- Moon card ----
        moon_note = get_moon_narration(moon)
        moon_icon = _moon_icon(moon["name"])
        moon_html = textwrap.dedent(f"""\
        <div class="moon-card">
        <div class="moon-icon">{moon_icon}</div>
        <div class="moon-info" style="flex:1;">
        <div class="moon-pct">Tonight's Moon</div>
        <h3>{moon['name']}</h3>
        <div class="moon-note">{moon_note}</div>
        </div>
        </div>
        """)
        st.markdown(moon_html, unsafe_allow_html=True)

        # ---- Constellations ----
        st.markdown(
            "<div class='section-label'>✨ Most Prominent Constellations</div>",
            unsafe_allow_html=True,
        )

        for i, n in enumerate(data["narrations"]):
            alt_pct = min(100, max(0, n["altitude_max"]))
            arrow = _compass_arrow(n["direction"])
            compass_txt = n["direction"].capitalize()

            card_html = textwrap.dedent(f"""\
            <div class="sky-card">
            <div class="constellation-header">
            <div>
            <span class="constellation-name">{n['name']}</span>
            <span class="constellation-abbr">{n['abbreviation']}</span>
            </div>
            <div class="compass">
            <span class="compass-arrow">{arrow}</span>
            <span>{compass_txt}</span>
            </div>
            </div>
            <div class="alt-gauge">
            <div class="alt-labels">
            <span>Horizon</span>
            <span>Zenith</span>
            </div>
            <div class="alt-bar">
            <div class="alt-fill" style="width:{alt_pct:.1f}%;"></div>
            </div>
            <div class="alt-value">{n['altitude_max']:.0f}° above horizon</div>
            </div>
            <div class="info-block">
            <div class="info-label">Mythology</div>
            <div class="info-text">{n['myth']}</div>
            </div>
            <div class="info-block">
            <div class="info-label">Look Here</div>
            <div class="info-text">{n['look_here']}</div>
            </div>
            <div class="narration-block">
            <div class="info-label">🎙️ Your Guide Says</div>
            <div class="narration-text">"{n['narration']}"</div>
            </div>
            </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)

        # ---- Bright stars ----
        st.markdown(
            "<div class='section-label'>⭐ Brightest Stars Above the Horizon</div>",
            unsafe_allow_html=True,
        )

        for s in data["bright_stars"][:6]:
            arrow = _compass_arrow(_dir_from_az(s["azimuth"]))
            star_html = textwrap.dedent(f"""\
            <div class="sky-card" style="padding:1rem 1.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:600;">
            {s['constellation']}
            </div>
            <div style="display:flex;gap:1.5rem;align-items:center;font-size:0.9rem;color:#9aa0c7;">
            <span>mag {s['magnitude']:.1f}</span>
            <span>{s['altitude']}° up</span>
            <span>{arrow} {_dir_from_az(s['azimuth']).capitalize()}</span>
            </div>
            </div>
            </div>
            """)
            st.markdown(star_html, unsafe_allow_html=True)

        # ---- Pocket mode banner ----
        if st.session_state.pocket_mode:
            pocket_html = textwrap.dedent("""\
            <div class="pocket-banner">
            <h2>📴 Pocket Mode</h2>
            <p>Results are narrated. Put your phone in your pocket and look up.<br>
            The sky will still be there when you come back.</p>
            </div>
            """)
            st.markdown(pocket_html, unsafe_allow_html=True)

    else:
        # Empty state
        empty_html = textwrap.dedent("""\
        <div class="sky-card" style="text-align:center;padding:3rem 2rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">🌌</div>
        <h2 style="margin:0 0 0.5rem 0 !important;">The sky awaits</h2>
        <p style="color:#9aa0c7;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;margin:0;">
        Enter your location in the sidebar, then press <strong>Scan the Sky</strong> to see what's overhead.
        </p>
        </div>
        """)
        st.markdown(empty_html, unsafe_allow_html=True)


# ============================================================
# TAB 2: Journal
# ============================================================
with tab_journal:
    st.markdown(
        "<div class='section-label'>📔 Your Sky Journal</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.journal:
        for entry in reversed(st.session_state.journal):
            arrow = _compass_arrow(entry["direction"])
            entry_html = textwrap.dedent(f"""\
            <div class="journal-entry">
            <div class="journal-time">{entry['time']}</div>
            <div class="journal-name">{entry['constellation']} <span style="font-size:0.9rem;color:#9aa0c7;">({entry['abbreviation']})</span></div>
            <div class="journal-meta">{arrow} {entry['direction'].capitalize()} · {entry['altitude']}° above horizon</div>
            </div>
            """)
            st.markdown(entry_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️  Clear Journal", type="secondary"):
            st.session_state.journal = []
            st.rerun()
    else:
        empty_journal = textwrap.dedent("""\
        <div class="sky-card" style="text-align:center;padding:3rem 2rem;">
        <div style="font-size:2.5rem;margin-bottom:1rem;">📖</div>
        <p style="color:#9aa0c7;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;margin:0;">
        No sightings yet. Scan the sky to begin your observing log.
        </p>
        </div>
        """)
        st.markdown(empty_journal, unsafe_allow_html=True)


# ============================================================
# TAB 3: About
# ============================================================
with tab_about:
    st.markdown(
        "<div class='section-label'>ℹ️ About Night Sky Companion</div>",
        unsafe_allow_html=True,
    )

    about1 = textwrap.dedent("""\
    <div class="sky-card">
    <h3 style="margin-top:0 !important;">How it works</h3>
    <p>Each scan performs five steps, entirely on your device:</p>
    <ol style="line-height:1.8;">
    <li><strong>Skyfield</strong> computes the position of every bright star for your latitude, longitude, and the current time.</li>
    <li><strong>The constellation map</strong> identifies which constellation each star belongs to.</li>
    <li><strong>Altitude and azimuth</strong> tell you how high up and which direction to look.</li>
    <li><strong>Ollama + Gemma 2B</strong> narrates the mythology and "look here" direction in a warm, natural voice.</li>
    <li>The UI applies <strong>red-light mode</strong> to preserve your night vision.</li>
    </ol>
    </div>
    """)
    st.markdown(about1, unsafe_allow_html=True)

    about2 = textwrap.dedent("""\
    <div class="sky-card">
    <h3 style="margin-top:0 !important;">Why open source matters</h3>
    <ul style="line-height:1.8;">
    <li><strong>Offline capability.</strong> Closed cloud APIs don't work at a dark-sky site with no signal. Skyfield's ephemeris is bundled; Gemma runs locally via Ollama.</li>
    <li><strong>Privacy.</strong> Your GPS coordinates and observing times never leave your device.</li>
    <li><strong>Zero cost.</strong> No API keys, no subscriptions, no usage limits.</li>
    <li><strong>Modifiability.</strong> Swap the model, add constellations, change the narration style — all possible with open code.</li>
    </ul>
    </div>
    """)
    st.markdown(about2, unsafe_allow_html=True)

    about3 = textwrap.dedent("""\
    <div class="sky-card">
    <h3 style="margin-top:0 !important;">Tech stack</h3>
    <table style="width:100%;border-collapse:collapse;">
    <tr style="border-bottom:1px solid rgba(139,125,255,0.2);">
    <td style="padding:0.7rem 0;color:#9aa0c7;">Astronomy</td>
    <td style="padding:0.7rem 0;">Skyfield (MIT)</td>
    </tr>
    <tr style="border-bottom:1px solid rgba(139,125,255,0.2);">
    <td style="padding:0.7rem 0;color:#9aa0c7;">Star catalog</td>
    <td style="padding:0.7rem 0;">Hipparcos (public domain)</td>
    </tr>
    <tr style="border-bottom:1px solid rgba(139,125,255,0.2);">
    <td style="padding:0.7rem 0;color:#9aa0c7;">AI narration</td>
    <td style="padding:0.7rem 0;">Ollama + Gemma 2B (Apache 2.0)</td>
    </tr>
    <tr>
    <td style="padding:0.7rem 0;color:#9aa0c7;">UI</td>
    <td style="padding:0.7rem 0;">Streamlit (Apache 2.0)</td>
    </tr>
    </table>
    </div>
    """)
    st.markdown(about3, unsafe_allow_html=True)