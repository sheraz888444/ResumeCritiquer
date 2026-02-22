"""Shared utilities for Resume Critiquer."""
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_theme():
    """Theme from session_state, synced with query_params so it persists across all pages."""
    # Sync from URL so theme persists when navigating between pages
    q = st.query_params.get("theme")
    if q in ("light", "dark"):
        st.session_state.theme = q
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    return st.session_state.theme


def toggle_theme():
    st.session_state.theme = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"


def _rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


def _theme_query():
    """Current theme for URL query (so links preserve theme)."""
    return get_theme()


def render_top_navbar():
    """Navbar with integrated dark/light toggle. Theme from query_params so it works on all pages."""
    theme = get_theme()
    tq = _theme_query()
    qs = f"?theme={tq}" if tq else ""

    # Hidden theme marker (must be first so body:has() works)
    theme_class = "theme-light" if theme == "light" else "theme-dark"
    st.markdown(
        f'<div class="{theme_class}" id="theme-marker" style="display:none" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <style>
        /* ===== NO HORIZONTAL SCROLL (mobile/tablet) ===== */
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }
        /* ===== REMOVE SIDEBAR ===== */
        [data-testid="stSidebar"], header[data-testid="stHeader"], section[data-testid="stSidebar"],
        [data-testid="stAppViewContainer"] > section:first-child {
            display: none !important; width: 0 !important; min-width: 0 !important;
        }
        section.main { margin-left: 0 !important; }
        [data-testid="stAppViewContainer"] { width: 100% !important; max-width: 100% !important; }

        /* ===== FULL WIDTH + NAVBAR AT TOP ===== */
        .block-container {
            max-width: 100% !important;
            padding: 0 2rem 3rem 2rem !important;
            margin-top: 0 !important;
        }
        @media (min-width: 1400px) { .block-container { padding-left: 3rem !important; padding-right: 3rem !important; } }
        @media (max-width: 1024px) { .block-container { padding: 0 1.25rem 2rem 1.25rem !important; } }
        @media (max-width: 768px) { .block-container { padding: 0 1rem 1.5rem 1rem !important; } }
        @media (max-width: 480px) { .block-container { padding: 0 0.75rem 1rem 0.75rem !important; } }

        /* ===== DARK THEME ===== */
        body:not(:has(.theme-light)) .stApp, body:has(.theme-dark) .stApp {
            background: #0d1117 !important; min-height: 100vh;
        }
        body:not(:has(.theme-light)) .block-container, body:has(.theme-dark) .block-container {
            background: #161b22 !important; color: #e6edf3 !important; border: 1px solid #30363d !important;
            border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
        }
        body:not(:has(.theme-light)) p, body:not(:has(.theme-light)) li, body:not(:has(.theme-light)) span,
        body:has(.theme-dark) p, body:has(.theme-dark) li, body:has(.theme-dark) span { color: #c9d1d9 !important; }
        body:not(:has(.theme-light)) h1, body:not(:has(.theme-light)) h2, body:not(:has(.theme-light)) h3,
        body:has(.theme-dark) h1, body:has(.theme-dark) h2, body:has(.theme-dark) h3 { color: #e6edf3 !important; }
        body:not(:has(.theme-light)) label, body:has(.theme-dark) label { color: #c9d1d9 !important; }
        body:not(:has(.theme-light)) .stMarkdown, body:has(.theme-dark) .stMarkdown { color: #c9d1d9 !important; }
        body:not(:has(.theme-light)) small, body:not(:has(.theme-light)) [data-testid="stCaptionContainer"],
        body:has(.theme-dark) small, body:has(.theme-dark) [data-testid="stCaptionContainer"] { color: #8b949e !important; }

        /* ===== LIGHT THEME (white, all text visible) ===== */
        body:has(.theme-light) .stApp {
            background: #f5f5f5 !important; min-height: 100vh;
        }
        body:has(.theme-light) .block-container {
            background: #ffffff !important; color: #212529 !important;
            border: 1px solid #e0e0e0 !important; box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
        }
        body:has(.theme-light) p, body:has(.theme-light) li, body:has(.theme-light) span { color: #212529 !important; }
        body:has(.theme-light) h1, body:has(.theme-light) h2, body:has(.theme-light) h3 { color: #1a1a1a !important; }
        body:has(.theme-light) label { color: #212529 !important; }
        body:has(.theme-light) .stMarkdown { color: #212529 !important; }
        body:has(.theme-light) small, body:has(.theme-light) [data-testid="stCaptionContainer"] { color: #495057 !important; }
        body:has(.theme-light) [data-testid="stExpander"] label { color: #212529 !important; }
        body:has(.theme-light) .stAlert { color: #212529 !important; }
        body:has(.theme-light) .stSuccess, body:has(.theme-light) .stError, body:has(.theme-light) .stWarning { color: #1a1a1a !important; }
        body:has(.theme-light) div[data-testid="stMetricValue"], body:has(.theme-light) div[data-testid="stMetricLabel"] { color: #212529 !important; }

        /* Light mode: inputs, file uploader, buttons, form - light backgrounds */
        body:has(.theme-light) input, body:has(.theme-light) textarea {
            background-color: #ffffff !important; color: #212529 !important;
            border: 1px solid #ced4da !important;
        }
        body:has(.theme-light) [data-testid="stFileUploader"],
        body:has(.theme-light) [data-testid="stFileUploader"] section,
        body:has(.theme-light) [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"],
        body:has(.theme-light) [data-testid="stFileUploader"] > div {
            background-color: #f8f9fa !important; border: 1px solid #dee2e6 !important; color: #212529 !important;
        }
        body:has(.theme-light) [data-testid="stFileUploader"] label,
        body:has(.theme-light) [data-testid="stFileUploader"] p { color: #212529 !important; }
        body:has(.theme-light) .stButton > button {
            background-color: #0d6efd !important; color: #ffffff !important; border: 1px solid #0d6efd !important;
        }
        body:has(.theme-light) .stButton > button:hover {
            background-color: #0b5ed7 !important; border-color: #0a58ca !important; color: #fff !important;
        }
        body:has(.theme-light) [data-testid="stForm"] {
            background: #f8f9fa !important; border: 1px solid #dee2e6 !important; border-radius: 8px !important;
        }
        body:has(.theme-light) [data-testid="stForm"] input,
        body:has(.theme-light) [data-testid="stForm"] textarea {
            background: #ffffff !important; color: #212529 !important;
        }

        /* Navbar row - fixed at very top, sticky on scroll */
        .stApp [data-testid="stHorizontalBlock"]:first-of-type {
            margin: -1rem -1rem 0 -1rem !important; padding: 0.6rem 1.5rem !important;
            background: #212529 !important; border-bottom: 2px solid #58a6ff !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            position: sticky !important; top: 0 !important; z-index: 999 !important;
        }
        body:has(.theme-light) .stApp [data-testid="stHorizontalBlock"]:first-of-type {
            background: #fff !important; border-bottom-color: #0d6efd !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        }
        .stApp [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:last-child {
            display: flex; align-items: center; justify-content: flex-end;
        }
        .nav-brand { font-size: 1.2rem; font-weight: 700; color: #e6edf3 !important; text-decoration: none; }
        body:has(.theme-light) .nav-brand { color: #212529 !important; }
        .nav-links { display: flex; align-items: center; gap: 0.25rem; flex-wrap: wrap; }
        .nav-link { color: #adb5bd !important; font-weight: 500; text-decoration: none; padding: 0.4rem 0.65rem; border-radius: 6px; }
        .nav-link:hover { color: #58a6ff !important; background: rgba(255,255,255,0.08); }
        body:has(.theme-light) .nav-link { color: #495057 !important; }
        body:has(.theme-light) .nav-link:hover { color: #0d6efd !important; background: #f0f0f0; }
        .stApp [data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
            margin: 0 !important; padding: 0.4rem 0.75rem !important; font-size: 0.85rem !important;
            border-radius: 6px !important; background: #40464d !important; color: #e6edf3 !important; border: 1px solid #484f58 !important;
        }
        body:has(.theme-light) .stApp [data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
            background: #e9ecef !important; color: #212529 !important; border-color: #dee2e6 !important;
        }
        /* ===== RESPONSIVE: NAVBAR (tablet & mobile) ===== */
        @media (max-width: 1024px) {
            .stApp [data-testid="stHorizontalBlock"]:first-of-type { padding: 0.5rem 1rem !important; }
            .nav-brand { font-size: 1.1rem !important; }
            .nav-link { padding: 0.5rem 0.5rem !important; font-size: 0.9rem !important; }
        }
        @media (max-width: 768px) {
            .stApp [data-testid="stHorizontalBlock"]:first-of-type {
                flex-wrap: wrap !important; padding: 0.5rem 0.75rem !important;
            }
            .stApp [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] {
                min-width: 100% !important; max-width: 100% !important; flex: 0 0 100% !important;
            }
            .stApp [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child {
                order: 1;
            }
            .stApp [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:last-child {
                order: 2; justify-content: center !important; padding-top: 0.25rem !important;
            }
            .nav-brand { font-size: 1rem !important; text-align: center; display: block; }
            .nav-links { justify-content: center !important; gap: 0.35rem !important; }
            .nav-link { padding: 0.5rem 0.6rem !important; font-size: 0.85rem !important; min-height: 44px; display: inline-flex; align-items: center; }
        }
        @media (max-width: 480px) {
            .stApp [data-testid="stHorizontalBlock"]:first-of-type { padding: 0.4rem 0.5rem !important; }
            .nav-brand { font-size: 0.95rem !important; }
            .nav-link { padding: 0.45rem 0.5rem !important; font-size: 0.8rem !important; }
            .stApp [data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
                padding: 0.5rem 0.75rem !important; min-height: 44px !important;
            }
        }
        /* ===== RESPONSIVE: STACK COLUMNS (except navbar) on tablet/mobile ===== */
        @media (max-width: 900px) {
            .stApp [data-testid="stHorizontalBlock"]:not(:first-of-type) [data-testid="column"] {
                min-width: 100% !important; flex: 1 1 100% !important;
            }
        }
        @media (max-width: 768px) {
            .stApp h1 { font-size: 1.5rem !important; }
            .stApp h2 { font-size: 1.25rem !important; }
            .stApp h3 { font-size: 1.1rem !important; }
        }
        @media (max-width: 480px) {
            .stApp h1 { font-size: 1.35rem !important; }
            .stApp h2 { font-size: 1.15rem !important; }
        }
        /* Touch-friendly: buttons and inputs on mobile (16px font avoids iOS zoom) */
        @media (max-width: 768px) {
            .stButton > button { min-height: 44px !important; padding: 0.5rem 1rem !important; }
            input[type="text"], input[type="email"], input[type="number"] { font-size: 16px !important; }
            textarea { font-size: 16px !important; min-height: 100px !important; }
        }
        @media (max-width: 480px) {
            .stButton > button { width: 100% !important; min-height: 48px !important; }
        }
    </style>
    """, unsafe_allow_html=True)

    col_nav, col_btn = st.columns([9, 1])
    with col_nav:
        st.markdown(f"""
        <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:1rem;">
            <a href="/{qs}" class="nav-brand">📃 AI Resume Critiquer</a>
            <div class="nav-links">
                <a href="/{qs}" class="nav-link">🏠 Home</a>
                <a href="/Analyze{qs}" class="nav-link">📊 Analyze</a>
                <a href="/About{qs}" class="nav-link">ℹ️ About</a>
                <a href="/Contact{qs}" class="nav-link">📧 Contact</a>
                <a href="/Privacy_Policy{qs}" class="nav-link">🔒 Privacy</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        if theme == "dark":
            if st.button("☀️ Light", key="theme_toggle", help="Switch to light mode"):
                toggle_theme()
                st.query_params["theme"] = "light"
                _rerun()
        else:
            if st.button("🌙 Dark", key="theme_toggle", help="Switch to dark mode"):
                toggle_theme()
                st.query_params["theme"] = "dark"
                _rerun()

    # Theme-aware cards
    st.markdown("""
    <style>
        body:not(:has(.theme-light)) .hero, body:has(.theme-dark) .hero {
            background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important; border: 1px solid #30363d; color: #e6edf3;
        }
        body:has(.theme-light) .hero {
            background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%) !important; border: 1px solid #dee2e6; color: #212529;
        }
        body:has(.theme-light) .hero h1 { color: #0d6efd !important; }
        body:has(.theme-light) .hero p { color: #495057 !important; }
        body:not(:has(.theme-light)) .feature-card, body:has(.theme-dark) .feature-card {
            background: #21262d !important; border: 1px solid #30363d; color: #e6edf3;
        }
        body:has(.theme-light) .feature-card {
            background: #f8f9fa !important; border: 1px solid #dee2e6; color: #212529;
        }
        body:has(.theme-light) .feature-card h4, body:has(.theme-light) .feature-card p { color: #212529 !important; }
        body:not(:has(.theme-light)) .contact-card, body:has(.theme-dark) .contact-card,
        body:not(:has(.theme-light)) .about-hero, body:has(.theme-dark) .about-hero {
            background: #21262d !important; border: 1px solid #30363d; color: #e6edf3;
        }
        body:has(.theme-light) .contact-card, body:has(.theme-light) .about-hero {
            background: #f8f9fa !important; border: 1px solid #dee2e6; color: #212529;
        }
        body:has(.theme-light) .contact-card a { color: #0d6efd !important; }
        body:has(.theme-light) .contact-card h4, body:has(.theme-light) .about-hero h3 { color: #212529 !important; }
        body:has(.theme-light) .carousel-container { border: 1px solid #dee2e6; }
        body:has(.theme-light) .ats-score-card {
            background: linear-gradient(135deg, #e7f1ff 0%, #cfe2ff 100%) !important; border-color: #9ec5fe !important; color: #212529 !important;
        }
        body:has(.theme-light) .section-card {
            background: #f8f9fa !important; border-left-color: #0d6efd !important; color: #212529 !important;
        }
        body:has(.theme-light) .ats-score-number { color: #0d6efd !important; }

        /* Professional loading spinner */
        .stSpinner > div { border-top-color: #58a6ff !important; }
        body:has(.theme-light) .stSpinner > div { border-top-color: #0d6efd !important; }
    </style>
    """, unsafe_allow_html=True)


import io
import json
import re
import PyPDF2
from openai import OpenAI


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        return None, None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1"), api_key


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


def parse_ai_json(text: str) -> dict | None:
    text = text.strip()
    if "```json" in text:
        text = re.search(r"```json\s*([\s\S]*?)\s*```", text)
        text = text.group(1) if text else text
    elif "```" in text:
        text = re.search(r"```\s*([\s\S]*?)\s*```", text)
        text = text.group(1) if text else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
