"""About page."""
import streamlit as st
from utils import render_top_navbar

st.set_page_config(page_title="About | AI Resume Critiquer", page_icon="ℹ️", layout="wide", initial_sidebar_state="collapsed")
render_top_navbar()

st.markdown("""
<style>
    .about-hero {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .about-hero h3 { color: #e6edf3; margin-top: 0; }
    .about-hero p { color: #8b949e; line-height: 1.6; }
    @media (max-width: 768px) { .about-hero { padding: 1.5rem 1rem; } }
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ About AI Resume Critiquer")
st.markdown("---")

st.markdown("""
<div class="about-hero">
<h3>Our Mission</h3>
<p>AI Resume Critiquer helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) 
and stand out to recruiters. We use advanced AI to provide professional, actionable feedback.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### What We Offer")
st.markdown("""
- **ATS Compatibility Score** — See how well your resume passes automated screening
- **Skill Gap Analysis** — Identify missing technical and soft skills
- **Resume vs Job Match** — Compare your resume against job descriptions
- **Keyword Optimization** — Improve ATS keyword matching
- **Formatting & Compliance** — Ensure ATS-friendly structure
- **AI-Powered Insights** — Strengths, weaknesses, and improvement suggestions
""")

st.markdown("### How It Works")
st.markdown("""
1. **Upload** your resume (PDF or TXT)
2. **Optional:** Paste the job description for match analysis
3. **Analyze** with one click
4. **Review** professional feedback and act on recommendations
""")

st.markdown("### Built for Job Seekers")
st.markdown("""
Our tool is designed for students, professionals, and career changers who want 
to present their best selves to potential employers. Get feedback in seconds — 
no sign-up required.
""")
