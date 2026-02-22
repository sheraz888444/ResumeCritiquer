"""AI Resume Critiquer - Home / Landing Page."""
import streamlit as st
from utils import render_top_navbar, get_theme

st.set_page_config(
    page_title="AI Resume Critiquer | Land Your Dream Job",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Resume-related background images (Unsplash)
CAROUSEL_IMAGES = [
    "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=1200&q=80",  # resume
    "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1200&q=80",  # office
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80",  # business
    "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&q=80",  # team
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&q=80",  # collaboration
]

# Dark theme & professional styling (responsive)
st.markdown("""
<style>
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 1.5rem;
        background: linear-gradient(135deg, rgba(22,27,34,0.98) 0%, rgba(13,17,23,0.95) 100%);
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .hero h1 {
        font-size: 2.25rem;
        background: linear-gradient(90deg, #58a6ff, #79c0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInUp 1s ease-out;
    }
    .hero p { font-size: 1.1rem; color: #8b949e; animation: fadeInUp 1s ease-out 0.2s both; }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .feature-card {
        background: #161b22;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin: 0.75rem 0;
        animation: slideIn 0.6s ease-out both;
    }
    .feature-card:nth-child(1) { animation-delay: 0.1s; }
    .feature-card:nth-child(2) { animation-delay: 0.2s; }
    .feature-card:nth-child(3) { animation-delay: 0.3s; }
    .feature-card:nth-child(4) { animation-delay: 0.4s; }
    
    .carousel-container {
        width: 100%;
        height: 320px;
        overflow: hidden;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .carousel-track { display: flex; width: 500%; animation: slide 20s infinite; }
    .carousel-slide {
        width: 20%; height: 320px; flex-shrink: 0;
        background-size: cover; background-position: center;
    }
    @keyframes slide {
        0%, 18% { transform: translateX(0); }
        20%, 38% { transform: translateX(-20%); }
        40%, 58% { transform: translateX(-40%); }
        60%, 78% { transform: translateX(-60%); }
        80%, 98% { transform: translateX(-80%); }
        100% { transform: translateX(0); }
    }
    
    @media (max-width: 768px) {
        .hero { padding: 2rem 1rem; }
        .hero h1 { font-size: 1.75rem; }
        .hero p { font-size: 1rem; }
        .carousel-container, .carousel-slide { height: 220px; }
    }
    @media (max-width: 768px) {
        .feature-card { padding: 1rem; }
    }
    @media (max-width: 480px) {
        .carousel-container, .carousel-slide { height: 180px; }
    }
    /* Stack columns on mobile */
    @media (max-width: 640px) {
        [data-testid="stHorizontalBlock"] [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Image carousel HTML
carousel_html = f"""
<div class="carousel-container">
    <div class="carousel-track">
        {"".join(f'<div class="carousel-slide" style="background-image:url({img})"></div>' for img in CAROUSEL_IMAGES)}
    </div>
</div>
"""

render_top_navbar()

# Main content - Landing page
st.markdown(carousel_html, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>AI-Powered Resume Analysis</h1>
    <p>Get professional ATS-focused feedback. Optimize your resume for recruiters and land your dream job.</p>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Start Free Analysis", type="primary", use_container_width=True):
    st.switch_page("pages/1_Analyze.py")

st.markdown("### Why Choose Our AI Resume Critiquer?")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 ATS Compatibility Score</h4>
        <p>Know if your resume passes applicant tracking systems.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🧩 Skill Gap Analysis</h4>
        <p>Identify missing skills and keywords for your target role.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>⭐ Job Match Score</h4>
        <p>Compare your resume against job descriptions for better fit.</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Actionable Tips</h4>
        <p>Get specific improvement suggestions from AI.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer (homepage only)
st.markdown("---")
tq = get_theme()
qs = f"?theme={tq}" if tq else ""
footer_html = f"""
<style>
    .app-footer {{
        margin-top: 3rem;
        padding: 2rem 1rem;
        text-align: center;
        border-top: 1px solid #30363d;
        background: rgba(22, 27, 34, 0.5);
        border-radius: 0 0 12px 12px;
    }}
    body:has(.theme-light) .app-footer {{
        border-top-color: #dee2e6;
        background: #f8f9fa;
    }}
    .app-footer a {{ color: #58a6ff; text-decoration: none; margin: 0 0.75rem; }}
    .app-footer a:hover {{ text-decoration: underline; }}
    body:has(.theme-light) .app-footer a {{ color: #0d6efd; }}
    .app-footer p {{ margin: 0.5rem 0; color: #8b949e; font-size: 0.9rem; }}
    body:has(.theme-light) .app-footer p {{ color: #6c757d; }}
</style>
<footer class="app-footer">
    <p><a href="/{qs}">Home</a> · <a href="/Analyze{qs}">Analyze</a> · <a href="/About{qs}">About</a> · <a href="/Contact{qs}">Contact</a> · <a href="/Privacy_Policy{qs}">Privacy</a></p>
    <p>© 2025 AI Resume Critiquer. Built to help you land your dream job.</p>
</footer>
"""
st.markdown(footer_html, unsafe_allow_html=True)
