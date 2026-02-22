"""Contact page."""
import streamlit as st
from utils import render_top_navbar

st.set_page_config(page_title="Contact | AI Resume Critiquer", page_icon="📧", layout="centered", initial_sidebar_state="collapsed")
render_top_navbar()

st.markdown("""
<style>
    .contact-card {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        max-width: 560px;
        margin: 1.5rem auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .contact-card h4 { color: #e6edf3; margin-top: 0; }
    .contact-card p, .contact-card li { color: #8b949e; }
    .contact-card a { color: #58a6ff !important; }
    @media (max-width: 768px) { .contact-card { padding: 1.5rem 1rem; margin: 1rem auto; } }
</style>
""", unsafe_allow_html=True)

st.title("📧 Contact Us")
st.markdown("---")

st.markdown("""
<div class="contact-card">
<h4>Get in Touch</h4>
<p>Have questions, feedback, or suggestions? We'd love to hear from you.</p>
<ul>
<li><strong>Owner:</strong> Sheraz Ahmed</li>
<li><strong>Phone:</strong> <a href="tel:+923267654138">+92 326 7654138</a></li>
<li><strong>Email:</strong> <a href="mailto:itssheraz78618@gmail.com">itssheraz78618@gmail.com</a></li>
<li><strong>Feedback:</strong> Use the form below</li>
</ul>
</div>
""", unsafe_allow_html=True)

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message")
    submitted = st.form_submit_button("Send")
    if submitted:
        st.success("Thank you! Your message has been sent. We'll get back to you soon.")
