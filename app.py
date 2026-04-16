import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

from crew import research_crew

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #05050f;
    min-height: 100vh;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,57,255,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,200,180,0.08) 0%, transparent 60%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,57,255,0.5); border-radius: 2px; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes gradShift {
    0%, 100% { background-position: 0% 50%; }
    50%       { background-position: 100% 50%; }
}
@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 rgba(99,57,255,0.35); }
    70%  { box-shadow: 0 0 0 12px rgba(99,57,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(99,57,255,0); }
}
@keyframes shimmer {
    0%   { background-position: -600px 0; }
    100% { background-position: 600px 0; }
}

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 52px 24px 44px;
    animation: fadeUp 0.7s ease-out both;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(150,120,255,0.9);
    background: rgba(99,57,255,0.12);
    border: 1px solid rgba(99,57,255,0.28);
    border-radius: 999px;
    padding: 5px 18px;
    margin-bottom: 22px;
}
.hero-eyebrow::before {
    content: '';
    width: 6px; height: 6px;
    background: #6339ff;
    border-radius: 50%;
    box-shadow: 0 0 8px #6339ff;
    animation: pulseRing 2s infinite;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #fff;
    margin: 0 0 16px 0;
}
.hero-title .grad {
    background: linear-gradient(120deg, #a78bfa, #06b6d4, #a78bfa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradShift 4s linear infinite;
}
.hero-desc {
    font-size: 1rem;
    font-weight: 300;
    color: rgba(203,213,225,0.5);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
    letter-spacing: 0.01em;
}

.fancy-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,57,255,0.4), rgba(6,182,212,0.3), transparent);
    margin: 8px 0 28px;
}

.panel {
    background: rgba(12,10,28,0.75);
    border: 1px solid rgba(99,57,255,0.2);
    border-radius: 20px;
    padding: 28px 28px 24px;
    backdrop-filter: blur(20px);
    animation: fadeUp 0.5s ease-out both;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.panel:hover { border-color: rgba(99,57,255,0.42); }
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,57,255,0.55), transparent);
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(150,120,255,0.7);
    margin: 0 0 18px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-label::before {
    content: '';
    width: 3px; height: 3px;
    border-radius: 50%;
    background: rgba(150,120,255,0.7);
}

.agent-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(99,57,255,0.1);
}
.agent-row:last-child { border-bottom: none; padding-bottom: 0; }
.agent-avatar {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem;
    flex-shrink: 0;
    border: 1px solid rgba(99,57,255,0.25);
}
.agent-avatar.blue   { background: rgba(6,182,212,0.12);  border-color: rgba(6,182,212,0.3); }
.agent-avatar.purple { background: rgba(99,57,255,0.12);  border-color: rgba(99,57,255,0.3); }
.agent-avatar.teal   { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.3); }
.agent-body { flex: 1; min-width: 0; }
.agent-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 3px;
}
.agent-desc {
    font-size: 0.73rem;
    color: rgba(148,163,184,0.65);
    margin: 0;
    line-height: 1.4;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    border-radius: 999px;
    padding: 8px 18px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    width: 100%;
    justify-content: center;
}
.status-pill .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.s-idle { background: rgba(99,57,255,0.1);  border: 1px solid rgba(99,57,255,0.28);  color: #a78bfa; }
.s-idle .dot { background: #a78bfa; }
.s-ok   { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.35); color: #6ee7b7; }
.s-ok   .dot { background: #10b981; box-shadow: 0 0 8px #10b981; animation: pulseRing 2s infinite; }
.s-err  { background: rgba(244,63,94,0.1);  border: 1px solid rgba(244,63,94,0.35);  color: #fda4af; }
.s-err  .dot { background: #f43f5e; }

.key-badge {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 500;
    margin-bottom: 8px;
}
.key-badge.ok  { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); color: #6ee7b7; }
.key-badge.err { background: rgba(244,63,94,0.08);  border: 1px solid rgba(244,63,94,0.2);  color: #fda4af; }
.key-badge .kd { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.key-badge.ok  .kd { background: #10b981; }
.key-badge.err .kd { background: #f43f5e; }

/* Step items — self-contained, no wrapping panel div needed */
.step-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 13px 18px;
    border-radius: 12px;
    background: rgba(99,57,255,0.07);
    border: 1px solid rgba(99,57,255,0.18);
    margin-bottom: 10px;
    animation: fadeUp 0.35s ease-out both;
    position: relative;
    overflow: hidden;
}
.step-item::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99,57,255,0.08), transparent);
    animation: shimmer 1.8s ease-in-out infinite;
}
.step-num {
    width: 28px; height: 28px;
    border-radius: 8px;
    background: rgba(99,57,255,0.2);
    border: 1px solid rgba(99,57,255,0.4);
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: #a78bfa;
    flex-shrink: 0;
}
.step-text { flex: 1; }
.step-agent {
    font-size: 0.82rem;
    font-weight: 600;
    color: #c4b5fd;
    margin: 0 0 2px;
}
.step-desc {
    font-size: 0.75rem;
    color: rgba(148,163,184,0.65);
    margin: 0;
}

div[data-baseweb="tab-list"] {
    background: rgba(12,10,28,0.8) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(99,57,255,0.2) !important;
    padding: 5px !important;
    gap: 3px !important;
    backdrop-filter: blur(12px) !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: rgba(148,163,184,0.7) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
    padding: 9px 20px !important;
}
button[data-baseweb="tab"]:hover {
    background: rgba(99,57,255,0.1) !important;
    color: #a78bfa !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,57,255,0.3), rgba(6,182,212,0.15)) !important;
    color: #c4b5fd !important;
    font-weight: 700 !important;
}
div[data-baseweb="tab-panel"] {
    border: 1px solid rgba(99,57,255,0.15) !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    background: rgba(8,7,20,0.7) !important;
    padding: 28px !important;
    backdrop-filter: blur(12px) !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background: rgba(12,10,28,0.9) !important;
    border: 1px solid rgba(99,57,255,0.3) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="textarea"] textarea:focus {
    border-color: rgba(99,57,255,0.75) !important;
    box-shadow: 0 0 0 3px rgba(99,57,255,0.14), 0 0 20px rgba(99,57,255,0.1) !important;
    outline: none !important;
}
div[data-baseweb="input"] input::placeholder { color: rgba(148,163,184,0.35) !important; }
label[data-testid="stWidgetLabel"] p {
    color: rgba(203,213,225,0.7) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6339ff 0%, #0891b2 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.72rem 2.2rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 24px rgba(99,57,255,0.45), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    width: 100% !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="stButton"] > button[kind="primary"]::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.06) 100%);
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 36px rgba(99,57,255,0.6), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active  { transform: translateY(0) !important; }
div[data-testid="stButton"] > button[kind="primary"]:disabled {
    opacity: 0.35 !important;
    transform: none !important;
    cursor: not-allowed !important;
}

div[data-testid="stDownloadButton"] > button {
    background: rgba(99,57,255,0.1) !important;
    border: 1px solid rgba(99,57,255,0.35) !important;
    border-radius: 10px !important;
    color: #a78bfa !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(99,57,255,0.22) !important;
    border-color: rgba(99,57,255,0.65) !important;
    color: #c4b5fd !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stProgressBar"] > div {
    background: rgba(99,57,255,0.12) !important;
    border-radius: 999px !important;
    height: 5px !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #6339ff, #06b6d4, #a78bfa) !important;
    background-size: 200% 100% !important;
    border-radius: 999px !important;
    animation: gradShift 1.8s linear infinite !important;
    transition: width 0.08s linear !important;
}

section[data-testid="stSidebar"] {
    background: rgba(6,5,16,0.97) !important;
    border-right: 1px solid rgba(99,57,255,0.18) !important;
    backdrop-filter: blur(24px) !important;
}
section[data-testid="stSidebar"] > div { padding: 2rem 1.4rem !important; }

.sb-section {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(150,120,255,0.6);
    margin: 22px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sb-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(99,57,255,0.18);
}

div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border-left: none !important;
    background: rgba(244,63,94,0.08) !important;
    border: 1px solid rgba(244,63,94,0.25) !important;
}

div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #c4b5fd !important;
    letter-spacing: -0.02em !important;
}
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    color: rgba(203,213,225,0.8) !important;
    line-height: 1.8 !important;
    font-size: 0.93rem !important;
}
div[data-testid="stMarkdownContainer"] code {
    background: rgba(99,57,255,0.14) !important;
    color: #a78bfa !important;
    border-radius: 5px !important;
    padding: 2px 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8em !important;
}
div[data-testid="stMarkdownContainer"] pre {
    background: rgba(8,7,20,0.9) !important;
    border: 1px solid rgba(99,57,255,0.2) !important;
    border-radius: 12px !important;
    padding: 18px !important;
}
div[data-testid="stMarkdownContainer"] pre code { background: transparent !important; padding: 0 !important; }
div[data-testid="stMarkdownContainer"] hr { border-color: rgba(99,57,255,0.2) !important; }
div[data-testid="stMarkdownContainer"] blockquote {
    border-left: 3px solid rgba(99,57,255,0.6) !important;
    padding-left: 18px !important;
    color: rgba(167,139,250,0.7) !important;
}

.how-step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 14px;
}
.how-num {
    width: 22px; height: 22px;
    border-radius: 6px;
    background: rgba(99,57,255,0.18);
    border: 1px solid rgba(99,57,255,0.35);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    color: #a78bfa;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.how-text { font-size: 0.78rem; color: rgba(148,163,184,0.7); line-height: 1.5; }

.footer {
    text-align: center;
    padding: 32px 0 10px;
    font-size: 0.75rem;
    color: rgba(100,116,139,0.45);
    letter-spacing: 0.06em;
}
.footer .hl { color: rgba(150,120,255,0.5); }

.result-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}
.result-heading .rh-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(150,120,255,0.7);
}
.result-heading .rh-badge {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.68rem;
    font-weight: 700;
    color: #6ee7b7;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

div[data-testid="column"] { padding: 0 8px; }

h2 {
    font-size: 26px !important;
    font-weight: 600;
    margin-bottom: 10px;
}

h3 {
    font-size: 20px !important;
    margin-top: 15px;
}
</style>
"""


def check_api_keys():
    required_vars = ['SERPER_API_KEY', 'OPENAI_API_KEY']
    return [var for var in required_vars if not os.getenv(var)]


def render_sidebar(missing_vars: list[str]):
    with st.sidebar:
        st.markdown(
            "<div style='display:flex;align-items:center;gap:10px;margin-bottom:28px;'>"
            "<div style='width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#6339ff,#06b6d4);"
            "display:flex;align-items:center;justify-content:center;font-size:1.1rem;'>🔬</div>"
            "<div>"
            "<div style='font-family:Syne,sans-serif;font-size:0.88rem;font-weight:700;color:#e2e8f0;'>Research AI</div>"
            "<div style='font-size:0.68rem;color:rgba(148,163,184,0.5);letter-spacing:0.08em;text-transform:uppercase;'>Multi-Agent System</div>"
            "</div></div>",
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sb-section'>API Status</div>", unsafe_allow_html=True)

        api_key_labels = {
            'SERPER_API_KEY': 'SERPER',
            'OPENAI_API_KEY': 'GROQ',
        }

        for var, display_label in api_key_labels.items():
            try:
                is_set = st.secrets[var] is not None
            except Exception:
                is_set = os.getenv(var) is not None
            cls = "ok" if is_set else "err"
            label = "Configured" if is_set else "Missing"
            st.markdown(
                f"<div class='key-badge {cls}'>"
                f"<div class='kd'></div>"
                f"<span style='flex:1;'>{display_label}</span>"
                f"<span style='font-family:JetBrains Mono,monospace;font-size:0.68rem;'>{label}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        if missing_vars:
            st.markdown(
                "<div style='margin-top:10px;padding:12px 14px;border-radius:10px;"
                "background:rgba(244,63,94,0.07);border:1px solid rgba(244,63,94,0.2);'>"
                "<p style='font-size:0.72rem;color:rgba(253,164,175,0.8);margin:0 0 8px;font-weight:600;'>"
                "Add to your <code>.env</code> file:</p>",
                unsafe_allow_html=True,
            )
            for var in missing_vars:
                st.code(f"{var}=your_key_here", language="bash")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sb-section'>Active Agents</div>", unsafe_allow_html=True)

        agents = [
            ("blue",   "🔍", "Research Specialist", "Queries the web and collects sources"),
            ("purple", "📊", "Data Analyst",        "Synthesises and structures findings"),
            ("teal",   "✍️",  "Content Writer",      "Composes the polished final report"),
        ]
        html = ""
        for color, icon, name, desc in agents:
            html += (
                f"<div class='agent-row'>"
                f"<div class='agent-avatar {color}'>{icon}</div>"
                f"<div class='agent-body'>"
                f"<p class='agent-name'>{name}</p>"
                f"<p class='agent-desc'>{desc}</p>"
                f"</div></div>"
            )
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("<div class='sb-section'>How to Use</div>", unsafe_allow_html=True)

        steps = [
            "Make sure both API keys are configured in your <code>.env</code> file.",
            "Type any research topic into the input field.",
            "Hit <strong>Launch Research Agents</strong> and watch the pipeline run.",
            "Download the generated Markdown reports when complete.",
        ]
        for i, s in enumerate(steps, 1):
            st.markdown(
                f"<div class='how-step'>"
                f"<div class='how-num'>{i:02d}</div>"
                f"<div class='how-text'>{s}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div class='sb-section'>About</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.76rem;color:rgba(148,163,184,0.55);line-height:1.65;margin:0;'>"
            "A three-agent CrewAI pipeline that researches any topic using live web search "
            "(Serper) and Groq-powered LLMs — then delivers structured Markdown reports."
            "</p>",
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    defaults = {
        'research_completed': False,
        'research_result': None,
        'research_error': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    missing_vars = check_api_keys()
    render_sidebar(missing_vars)

    # ── Hero ─────────────────────────────────────────────────────
    st.markdown(
        "<div class='hero-wrap'>"
        "<div class='hero-eyebrow'>⚡ &nbsp; Multi-Agent Research Pipeline</div>"
        "<h1 class='hero-title'>AI Research <span class='grad'>Assistant</span></h1>"
        "<p class='hero-desc'>Three specialised agents search, analyse, and synthesise the web into polished research reports — fully automated.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ── Main Layout ──────────────────────────────────────────────
    col_left, col_right = st.columns([3, 1], gap="large")

    with col_left:
        # Input panel
        st.markdown(
            "<div class='panel'><p class='panel-label'>Research Topic</p>",
            unsafe_allow_html=True,
        )
        topic = st.text_input(
            label="research_topic",
            placeholder="e.g., Quantum computing breakthroughs in 2025",
            help="Enter any topic you want the AI agents to research",
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

        btn_disabled = bool(missing_vars)
        if st.button(" Launch Research Agents", type="primary", disabled=btn_disabled):
            if not topic.strip():
                st.markdown(
                    "<div class='status-pill s-err' style='margin-top:12px;border-radius:12px;'>"
                    "<span class='dot'></span>Please enter a research topic to continue."
                    "</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.session_state.research_completed = False
                st.session_state.research_result = None
                st.session_state.research_error = None

                st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

                # ── Agent Activity label ──────────────────────────
                st.markdown(
                    "<p class='panel-label' style='margin-top:4px;'>Agent Activity</p>",
                    unsafe_allow_html=True,
                )

                # Step + progress placeholders — NO wrapping div
                step_placeholder = st.empty()
                prog_placeholder = st.empty()

                steps = [
                    ("🔍", "Research Specialist", "Searching the web for relevant sources…"),
                    ("📊", "Data Analyst",        "Synthesising and analysing data…"),
                    ("✍️",  "Content Writer",      "Composing the final report…"),
                ]

                progress_bar = prog_placeholder.progress(0)
                for idx, (icon, agent, desc) in enumerate(steps):
                    step_placeholder.markdown(
                        f"<div class='step-item'>"
                        f"<div class='step-num'>{idx + 1:02d}</div>"
                        f"<div class='step-text'>"
                        f"<p class='step-agent'>{icon} &nbsp; {agent}</p>"
                        f"<p class='step-desc'>{desc}</p>"
                        f"</div></div>",
                        unsafe_allow_html=True,
                    )
                    start = idx * 33
                    end = min(start + 33, 99)
                    for v in range(start, end + 1):
                        progress_bar.progress(v)
                        time.sleep(0.015)

                # ── Run Crew ──────────────────────────────────────
                try:
                    result = research_crew.kickoff({"topic": topic})
                    st.session_state.research_result = result
                    st.session_state.research_completed = True
                    st.session_state.research_error = None
                    progress_bar.progress(100)
                except Exception as e:
                    st.session_state.research_error = str(e)
                    st.session_state.research_completed = True

                # Clear progress UI immediately after completion
                step_placeholder.empty()
                prog_placeholder.empty()

    with col_right:
        # Status panel — uses only st.markdown + Streamlit widgets, no raw unclosed divs
        st.markdown("<div class='panel'><p class='panel-label'>Status</p>", unsafe_allow_html=True)

        if st.session_state.research_completed:
            if st.session_state.research_error:
                st.markdown(
                    "<div class='status-pill s-err'>"
                    "<span class='dot'></span>Research Failed"
                    "</div>"
                    f"<p style='font-size:0.73rem;color:rgba(253,164,175,0.6);margin:10px 0 0;line-height:1.5;'>"
                    f"{st.session_state.research_error}</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='status-pill s-ok'>"
                    "<span class='dot'></span>Research Complete"
                    "</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div class='status-pill s-idle'>"
                "<span class='dot'></span>Awaiting Topic"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Results Section ──────────────────────────────────────────
    if st.session_state.research_completed and not st.session_state.research_error:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='result-heading'>"
            "<span class='rh-label'>Research Results</span>"
            "<span class='rh-badge'>✓ &nbsp; Completed</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        output_files = {
            "research_findings.md": "🔍 Findings",
            "analysis_report.md":   "📊 Analysis",
            "final_report.md":      "📝 Final Report",
        }

        tabs = st.tabs(list(output_files.values()))

        for i, (filename, title) in enumerate(output_files.items()):
            with tabs[i]:
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    st.markdown(content)
                    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                    st.download_button(
                        label=f"📥  Download {title}",
                        data=content,
                        file_name=filename,
                        mime="text/markdown",
                    )
                else:
                    st.markdown(
                        f"<div class='status-pill s-idle' style='border-radius:12px;'>"
                        f"<span class='dot'></span>{filename} will appear here after research completes."
                        f"</div>",
                        unsafe_allow_html=True,
                    )

    # ── Footer ───────────────────────────────────────────────────
    st.markdown(
        "<div class='footer'>"
        "Built with <span class='hl'>CrewAI</span> · "
        "<span class='hl'>Streamlit</span> · "
        "<span class='hl'>Groq</span> · "
        "<span class='hl'>Serper</span>"
        "</div>",
        unsafe_allow_html=True,
    )




if __name__ == "__main__":
    main()